from sqlalchemy.orm import Session
from app.models.customeruser import CustomerUser
from app.models.customer_preferences import CustomerPreferences
from app.schemas.customeruserSchema import CustomerUserSchema
from app.utils import hash_password, generate_random_password
from app.core.logging import get_logger
from sqlalchemy import func
from app.core.cache import Cache
from sqlalchemy import select, or_
from math import ceil
from typing import List, Optional
logger = get_logger(__name__)
cache = Cache()

class EmailAlreadyExistsError(Exception):
    pass

class LoginAlreadyExistsError(Exception):
    pass

class CommanErrorException(Exception):
    pass

def customeruser_add(db: Session, user: CustomerUserSchema, change_user_id: int):
    # Check required fields
    required_fields = ["first_name", "last_name", "login", "email", "valid_id"]
    for field in required_fields:
        if not getattr(user, field, None):
            logger.error(f"Need {field}!")
            return None

    # Check if email address is valid
    if not is_valid_email(user.email):
        logger.error(f"Email address ({user.email}) not valid!")
        return None

    # Check if email is already used
    if email_exists(db, user.email):
        logger.error(f"Email address ({user.email}) is already used by another user.")
        raise EmailAlreadyExistsError(f"Email address ({user.email}) is already used.")

    # Check if user with this login already exists
    existing_user = UserLoginExistsCheck(db, user.login)
    if existing_user:
        logger.error(f"A user with the username '{user.login}' already exists.")
        raise LoginAlreadyExistsError(f"A user with the username '{user.login}' already exists.")

    # Generate password if not provided
    if not user.password:
        user.password = generate_random_password()

    # Create new user with the additional fields
    new_user = CustomerUser(
        title=user.title,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        login=user.login,
        pw=hash_password(user.password),
        valid_id=user.valid_id,
        customer_id=user.customer_id,  # Added customer_id
        phone=user.phone,  # Added phone
        fax=user.fax,  # Added fax
        mobile=user.mobile,  # Added mobile
        street=user.street,  # Added street
        zip=user.zip,  # Added zip
        city=user.city,  # Added city
        country=user.country,  # Added country
        comments=user.comments,  # Added comments
        create_by=change_user_id,
        change_by=change_user_id,
        create_time=func.now(),
        change_time=func.now()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    user_id = new_user.id
    # Set user preferences

    user_data = {
        'id': new_user.id,
        'title': new_user.title,
        'first_name': new_user.first_name,
        'last_name': new_user.last_name,
        'login': new_user.login,
        'valid_id': new_user.valid_id,
        'create_by': new_user.create_by,
        'change_by': new_user.change_by,
        'create_time': new_user.create_time.isoformat(),
        'change_time': new_user.change_time.isoformat(),
        'email': new_user.email,
        'mobile': new_user.mobile,
        'customer_id': new_user.customer_id,  # Added customer_id to user_data
        'phone': new_user.phone,  # Added phone to user_data
        'fax': new_user.fax,  # Added fax to user_data
        'street': new_user.street,  # Added street to user_data
        'zip': new_user.zip,  # Added zip to user_data
        'city': new_user.city,  # Added city to user_data
        'country': new_user.country,  # Added country to user_data
        'comments': new_user.comments  # Added comments to user_data
    }

    # Cache user data
    cache.set(f"customeruser:{user.login}", user_data, expire=3600)  # Store user object in cache
    return user_data


def is_valid_email(email: str) -> bool:
    # Implement email validation logic
    return True  # Assuming email validation is correct

def email_exists(db: Session, email: str) -> bool:
    # Check if the email exists in the UserPreference table
    email_exists = db.query(CustomerUser.email).filter(
        CustomerUser.email == email.encode('utf-8')
    ).first()
    
    # If a matching email is found, return True
    if email_exists:
        return True
    
    # If no matching email is found, return False
    return False

def get_customeruser_data(db: Session, identifier):
    cache_key = f"customeruser:{identifier}"
    cached_user = cache.get(cache_key)
    print(f"cached_user {cached_user}")

    if cached_user:
        return cached_user

    # Fetch user data from the database
    user_data = None
    if isinstance(identifier, int):
        user_data = db.query(CustomerUser).filter(CustomerUser.id == identifier).first()
    elif isinstance(identifier, str):
        user_data = db.query(CustomerUser).filter(CustomerUser.login == identifier).first()
    
    if user_data:
        # Fetch user preferences
        preferences = get_all_preferences(db, user_data.login)

        # Prepare response data with additional fields
        response_data = {
            'id': user_data.id,
            'login': user_data.login,
            'title': user_data.title,
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'email': user_data.email,
            'valid_id': user_data.valid_id,
            'customer_id': user_data.customer_id,  # Added customer_id
            'phone': user_data.phone,              # Added phone
            'fax': user_data.fax,                  # Added fax
            'mobile': user_data.mobile,            # Added mobile
            'street': user_data.street,            # Added street
            'zip': user_data.zip,                  # Added zip
            'city': user_data.city,                # Added city
            'country': user_data.country,          # Added country
            'comments': user_data.comments,        # Added comments
            'create_by': user_data.create_by,
            'change_by': user_data.change_by,
            'create_time': user_data.create_time.isoformat(),
            'change_time': user_data.change_time.isoformat(),
            'preferences': preferences,
        }
        print(f"response_data {response_data}")
        
        # Store in cache if found
        cache.set(cache_key, response_data, expire=3600)  # Cache for 1 hour

        return response_data

    return None


def set_preferences(db: Session, user_id: int, key: str, value: str):
    # Delete old data
    db.query(CustomerPreferences).filter(CustomerPreferences.user_id == user_id, CustomerPreferences.preferences_key == key).delete()

    # Insert new data
    new_preference = CustomerPreferences(
        user_id=user_id,
        preferences_key=key,
        preferences_value=value.encode('utf-8') if value else None  # Convert string to bytes
    )
    db.add(new_preference)
    db.commit()

def get_preferences(db: Session, user_id: str = None, key: str = None) -> List[str]:
    # Create a select query to retrieve preferences based on user_id and/or key
    if user_id and key:
        stmt = select(CustomerPreferences.preferences_value).where(
            CustomerPreferences.user_id == user_id,
            CustomerPreferences.preferences_key == key
        )
    elif user_id:
        stmt = select(CustomerPreferences.preferences_value).where(
            CustomerPreferences.user_id == user_id
        )
    elif key:
        stmt = select(CustomerPreferences.preferences_value).where(
            CustomerPreferences.preferences_key == key
        )        
    else:
        return []  # Return an empty list if neither user_id nor key is provided

    
    # Execute the query and fetch all results
    result = db.execute(stmt).scalars().all()  # Fetch all matching records

    # Decode each result (as they're stored as bytes) and return as a list of strings
    return [r.decode('utf-8') for r in result] if result else []


def get_all_preferences(db: Session, user_id: str) -> dict:
    cache_key = f"customerpreferences:{user_id}"
    cached_preferences = cache.get(cache_key)
    logger.info(f"Fetching preferences for user {user_id} from cache: {cached_preferences}")

    if cached_preferences:
        return cached_preferences

    try:
        # Create a select query to retrieve all preferences based on user_id
        stmt = select(CustomerPreferences.preferences_key, CustomerPreferences.preferences_value).where(
            CustomerPreferences.user_id == user_id
        )

        # Execute the query and fetch all results
        result = db.execute(stmt).all()

        if not result:
            logger.info(f"No preferences found for user {user_id}.")
            return {}

        # Convert the result into a dictionary
        preferences = {
            row[0]: row[1] if isinstance(row[1], str) else row[1].decode('utf-8') if row[1] else None
            for row in result
        }
        
        # Cache the preferences
        cache.set(cache_key, preferences, expire=3600)
        logger.info(f"Caching preferences for user {user_id}: {preferences}")
        
        return preferences

    except Exception as e:
        logger.error(f"Error fetching preferences for user {user_id}: {str(e)}")
        return {}



def get_customeruser_hash_pwd(db: Session, login: str) -> str:
    existing_user_password = db.query(CustomerUser.pw).filter(CustomerUser.login == login).first()
    
    if existing_user_password:
        return existing_user_password[0]  # Return the first element of the tuple
    return None

def UserLoginExistsCheck(db: Session, user_login: str, user_id: int = None) -> bool:
    query = select(CustomerUser.id).where(CustomerUser.login == user_login)
    result = db.execute(query).fetchall()

    # If a user login is found
    for row in result:
        existing_user_id = row[0]
        if not user_id or user_id != existing_user_id:
            return True  # User login exists, and user_id doesn't match

    return False  # User login does not exist or matches the current user

from math import ceil

def get_customeruser_list(db: Session, page_no: int = 1, count_per_page: int = 10):
    try:
        # Validate input
        if page_no < 1 or count_per_page < 1:
            logger.error("Page number and count per page must be greater than zero.")
            raise CommanErrorException("Page number and count per page must be greater than zero.")

        # Calculate the offset (how many records to skip)
        offset_value = (page_no - 1) * count_per_page

        # Get the total number of users
        total_users = db.query(CustomerUser).count()

        # Calculate the total number of pages
        total_pages = ceil(total_users / count_per_page)

        # Select the users for the given page
        stmt = select(CustomerUser).offset(offset_value).limit(count_per_page)
        result = db.execute(stmt).scalars().all()

        # Prepare the user data in a list
        user_list = []
        for user in result:
            user_data = {
                'id': user.id,
                'login': user.login,
                'title': user.title,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,                  # Added email
                'valid_id': user.valid_id,
                'customer_id': user.customer_id,      # Added customer_id
                'phone': user.phone,                  # Added phone
                'fax': user.fax,                      # Added fax
                'mobile': user.mobile,                # Added mobile
                'street': user.street,                # Added street
                'zip': user.zip,                      # Added zip
                'city': user.city,                    # Added city
                'country': user.country,              # Added country
                'comments': user.comments,            # Added comments
                'create_by': user.create_by,
                'change_by': user.change_by,
                'create_time': user.create_time.isoformat(),
                'change_time': user.change_time.isoformat(),
            }
            user_list.append(user_data)

        # Pagination response
        return {
            'total_users': total_users,
            'total_pages': total_pages,
            'current_page': page_no,
            'users': user_list
        }
    except Exception as e:
        logger.exception("Failed to retrieve user list.")
        raise CommanErrorException("Failed to retrieve user list.")


def get_customeruser_search(db: Session, 
                    Search: Optional[str] = None, 
                    UserLogin: Optional[str] = None) -> List[dict]:
    """
    Searches for users based on Search (for name or login), UserLogin (exact login), 
    or PostMasterSearch (preference key search). At least one search parameter is required.

    :param db: SQLAlchemy session to interact with the database.
    :param Search: A string to search in first name, last name, or login.
    :param UserLogin: A string to perform an exact login match.
    :param PostMasterSearch: A preference key to search related to users.
    :return: A list of user dictionaries or preferences.
    :raises HTTPException: If no search parameters are provided or an error occurs.
    """
    try:
        # Ensure at least one search parameter is provided
        if not Search and not UserLogin:
            logger.error("No search parameters provided")
            raise CommanErrorException("At least one search parameter must be provided.")

        # Initialize the query
        query = db.query(CustomerUser)

        # Apply filters based on provided parameters
        if Search:
            search_term = f"%{Search}%"  # Wildcard search
            query = query.filter(
                or_(
                    CustomerUser.first_name.ilike(search_term),  # Case-insensitive search
                    CustomerUser.last_name.ilike(search_term),
                    CustomerUser.login.ilike(search_term)
                )
            )
            logger.info(f"Searching users by name or login using: {Search}")

        if UserLogin:
            user_login_term = f"%{UserLogin}%"
            query = query.filter(CustomerUser.login.ilike(user_login_term))  # Case-insensitive for login
            logger.info(f"Searching users by exact login using: {UserLogin}")

        # Execute the query and fetch results
        users = query.all()

        # If no users are found, return an empty list
        if not users:
            logger.info("No users found for the given search parameters")
            return []

        # Prepare the user data in a list with the new fields
        user_list = []
        for user in users:
            user_data = {
                'id': user.id,
                'login': user.login,
                'title': user.title,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,                  # Added email
                'valid_id': user.valid_id,
                'customer_id': user.customer_id,      # Added customer_id
                'phone': user.phone,                  # Added phone
                'fax': user.fax,                      # Added fax
                'mobile': user.mobile,                # Added mobile
                'street': user.street,                # Added street
                'zip': user.zip,                      # Added zip
                'city': user.city,                    # Added city
                'country': user.country,              # Added country
                'comments': user.comments,            # Added comments
                'create_by': user.create_by,
                'change_by': user.change_by,
                'create_time': user.create_time.isoformat(),
                'change_time': user.change_time.isoformat(),
            }
            user_list.append(user_data)

        return user_list

    except CommanErrorException as e:
        logger.error(f"HTTP error: {e.detail}")
        raise e  # Re-raise HTTPException for FastAPI to handle it correctly

    except Exception as e:
        logger.exception("Failed to perform user search.")
        raise CommanErrorException("An unexpected error occurred.")


def customer_user_update(db: Session, user_id: int, user: CustomerUserSchema, change_user_id: int):
    # Fetch existing user from the database
    existing_user = db.query(CustomerUser).filter(CustomerUser.id == user_id).first()
    
    if not existing_user:
        logger.error(f"User with ID '{user_id}' not found.")
        raise CommanErrorException(f"User with ID '{user_id}' not found.")
    
    # Check required fields
    required_fields = ["first_name", "last_name", "login", "email", "valid_id", "customer_id", "phone", "fax", "mobile", "street", "zip", "city", "country", "comments"]
    for field in required_fields:
        if not getattr(user, field, None):
            logger.error(f"Need {field}!")
            raise CommanErrorException(f"Need {field}!")

    # Check if email address is valid
    if not is_valid_email(user.email):
        logger.error(f"Email address ({user.email}) not valid!")
        raise CommanErrorException(f"Email address ({user.email}) not valid!")

    exist_preferences = get_all_preferences(db, user_id)
    
    # Check if email is already used (only if the email has changed)
    if user.email != exist_preferences.get('UserEmail'):
        if email_exists(db, user.email):
            logger.error(f"Email address ({user.email}) is already used by another user.")
            raise EmailAlreadyExistsError(f"Email address ({user.email}) is already used.")
    
    # Check if user with this login already exists (only if the login has changed)
    if user.login != existing_user.login and UserLoginExistsCheck(db, user.login):
        logger.error(f"A user with the username '{user.login}' already exists.")
        raise LoginAlreadyExistsError(f"A user with the username '{user.login}' already exists.")
    
    # Update the user data
    existing_user.first_name = user.first_name
    existing_user.last_name = user.last_name
    existing_user.login = user.login
    existing_user.email = user.email
    existing_user.valid_id = user.valid_id
    existing_user.customer_id = user.customer_id  # Update customer_id
    existing_user.phone = user.phone  # Update phone
    existing_user.fax = user.fax  # Update fax
    existing_user.mobile = user.mobile  # Update mobile
    existing_user.street = user.street  # Update street
    existing_user.zip = user.zip  # Update zip
    existing_user.city = user.city  # Update city
    existing_user.country = user.country  # Update country
    existing_user.comments = user.comments  # Update comments
    existing_user.change_by = change_user_id
    existing_user.change_time = func.now()

    # Update password if provided
    if user.password:
        existing_user.pw = hash_password(user.password)

    db.commit()
    db.refresh(existing_user)

    # Update preferences (if applicable)

    # Prepare updated user data
    user_data = {
        'id': existing_user.id,
        'title': existing_user.title,
        'first_name': existing_user.first_name,
        'last_name': existing_user.last_name,
        'login': existing_user.login,
        'valid_id': existing_user.valid_id,
        'create_by': existing_user.create_by,
        'change_by': existing_user.change_by,
        'create_time': existing_user.create_time.isoformat(),
        'change_time': existing_user.change_time.isoformat(),
        'email': existing_user.email,
        'mobile': existing_user.mobile,
        'customer_id': existing_user.customer_id,  # Added customer_id to user_data
        'phone': existing_user.phone,  # Added phone to user_data
        'fax': existing_user.fax,  # Added fax to user_data
        'street': existing_user.street,  # Added street to user_data
        'zip': existing_user.zip,  # Added zip to user_data
        'city': existing_user.city,  # Added city to user_data
        'country': existing_user.country,  # Added country to user_data
        'comments': existing_user.comments  # Added comments to user_data
    }
    
    Delete_user_cache(existing_user.login, existing_user.id)
    
    # Update the cache with the updated user data
    cache.set(f"customeruser:{existing_user.login}", user_data, expire=3600)  # Store updated user object in cache
    cache.set(f"customeruser:{existing_user.id}", user_data, expire=3600)  # Store updated user object in cache

    return user_data


def Delete_user_cache(login:str = None, user_id:int = None):
    cache.delete(f"user:{login}")
    cache.delete(f"user:{user_id}")
    cache.delete(f"preferences:{user_id}")
    cache.delete(f"preferences:{login}")
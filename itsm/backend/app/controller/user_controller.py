from sqlalchemy.orm import Session
from app.models.user import User
from app.models.user_preferences import UserPreference
from app.schemas.user import UserCreate
from app.utils import hash_password, generate_random_password
from app.core.logging import get_logger
from sqlalchemy import func
from app.core.cache import Cache
from sqlalchemy import select
from math import ceil
logger = get_logger(__name__)
cache = Cache()

class EmailAlreadyExistsError(Exception):
    pass

class LoginAlreadyExistsError(Exception):
    pass

class CommanErrorException(Exception):
    pass

def user_add(db: Session, user: UserCreate, change_user_id: int):
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
    existing_user = UserLoginExistsCheck(db,user.login)
    if existing_user:
        logger.error(f"A user with the username '{user.login}' already exists.")
        raise LoginAlreadyExistsError(f"A user with the username '{user.login}' already exists.")

    # Generate password if not provided
    if not user.password:
        user.password = generate_random_password()
    # Create new user
    new_user = User(
        title=user.title,
        first_name=user.first_name,
        last_name=user.last_name,
        login=user.login,
        pw=hash_password(user.password),
        valid_id=user.valid_id,
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
    preferences = {
        'UserEmail': user.email,
        'UserMobile': user.mobile
    }
    
    for key, value in preferences.items():
        set_preferences(db, user_id, key, value)
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
        'email': preferences.get('UserEmail'),
        'mobile': preferences.get('UserMobile')
    }
    # logger.info(f"User: '{user.login}' ID: '{new_user.id}' created successfully ({change_user_id})!")
    cache.set(f"user:{user.login}", user_data, expire=3600)  # Store user object in cache
    return user_data

def is_valid_email(email: str) -> bool:
    # Implement email validation logic
    return True  # Assuming email validation is correct

def email_exists(db: Session, email: str) -> bool:
    # Check if email is in the UserPreference table
    preference_exists = db.query(UserPreference).filter(UserPreference.preferences_key == 'UserEmail', UserPreference.preferences_value == email.encode('utf-8')).first()
    if preference_exists:
        return True

    return False

def get_user_data(db: Session, identifier):
    cache_key = f"user:{identifier}"
    cached_user = cache.get(cache_key)
    print(f"cached_user {cached_user}")

    if cached_user:
        return cached_user

    # Fetch user data from the database
    user_data = None
    if isinstance(identifier, int):
        user_data = db.query(User).filter(User.id == identifier).first()
    elif isinstance(identifier, str):
        user_data = db.query(User).filter(User.login == identifier).first()
    if user_data:
        # Fetch user preferences
        preferences = get_all_preferences(db,user_data.id)

        # Prepare response data
        response_data = {
            'id': user_data.id,
            'login': user_data.login,
            'title': user_data.title,
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'valid_id': user_data.valid_id,
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
    db.query(UserPreference).filter(UserPreference.user_id == user_id, UserPreference.preferences_key == key).delete()

    # Insert new data
    new_preference = UserPreference(
        user_id=user_id,
        preferences_key=key,
        preferences_value=value.encode('utf-8') if value else None  # Convert string to bytes
    )
    db.add(new_preference)
    db.commit()

def get_preferences(db: Session, user_id: int, key: str) -> str:
    # Create a select query to retrieve the preference based on user_id and key
    stmt = select(UserPreference.preferences_value).where(
        UserPreference.user_id == user_id,
        UserPreference.preferences_key == key
    )
    
    # Execute the query and fetch the first result
    result = db.execute(stmt).scalar_one_or_none()

    # If result is found, decode it (as it's stored as bytes); otherwise, return None
    if result:
        return result.decode('utf-8')  # Convert bytes to string
    return None  # Return None if no preference is found

def get_all_preferences(db: Session, user_id: int) -> dict:
    cache_key = f"preferences:{user_id}"
    cached_preferences = cache.get(cache_key)
    logger.info(f"Fetching preferences for user {user_id} from cache: {cached_preferences}")

    if cached_preferences:
        return cached_preferences

    try:
        # Create a select query to retrieve all preferences based on user_id
        stmt = select(UserPreference.preferences_key, UserPreference.preferences_value).where(
            UserPreference.user_id == user_id
        )

        # Execute the query and fetch all results
        result = db.execute(stmt).all()

        if not result:
            logger.info(f"No preferences found for user {user_id}.")
            return {}

        # Convert the result into a dictionary, decoding the values from bytes to strings
        preferences = {
            row[0]: row[1].decode('utf-8') if row[1] else None
            for row in result
        }
        
        # Cache the preferences
        cache.set(cache_key, preferences, expire=3600)
        logger.info(f"Caching preferences for user {user_id}: {preferences}")
        
        return preferences

    except Exception as e:
        logger.error(f"Error fetching preferences for user {user_id}: {str(e)}")
        return {}


def get_user_hash_pwd(db: Session, login: str) -> str:
    existing_user_password = db.query(User.pw).filter(User.login == login).first()
    
    if existing_user_password:
        return existing_user_password[0]  # Return the first element of the tuple
    return None

def UserLoginExistsCheck(db: Session, user_login: str, user_id: int = None) -> bool:
    query = select(User.id).where(User.login == user_login)
    result = db.execute(query).fetchall()

    # If a user login is found
    for row in result:
        existing_user_id = row[0]
        if not user_id or user_id != existing_user_id:
            return True  # User login exists, and user_id doesn't match

    return False  # User login does not exist or matches the current user

def get_user_list(db: Session, page_no: int = 1, count_per_page: int = 10):
    try:
        # Validate input
        if page_no < 1 or count_per_page < 1:
            logger.error("Page number and count per page must be greater than zero.")
            raise CommanErrorException("Page number and count per page must be greater than zero.")

        # Calculate the offset (how many records to skip)
        offset_value = (page_no - 1) * count_per_page

        # Get the total number of users
        total_users = db.query(User).count()

        # Calculate the total number of pages
        total_pages = ceil(total_users / count_per_page)

        # Select the users for the given page
        stmt = select(User).offset(offset_value).limit(count_per_page)
        result = db.execute(stmt).scalars().all()

        # Prepare the user data in a list
        user_list = []
        for user in result:
            user_data = {
                'id': user.id,
                'title': user.title,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'login': user.login,
                'valid_id': user.valid_id,
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
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.user_preferences import UserPreference
from app.schemas.user import UserCreate
from app.utils import hash_password, generate_random_password
from app.core.logging import get_logger
from sqlalchemy import func
from app.core.cache import Cache

logger = get_logger(__name__)
cache = Cache()

class EmailAlreadyExistsError(Exception):
    pass

class LoginAlreadyExistsError(Exception):
    pass

def user_add(db: Session, user: UserCreate, change_user_id: int):
    print("started user_add")
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
    existing_user = db.query(User).filter(User.login == user.login).first()
    if existing_user:
        logger.error(f"A user with the username '{user.login}' already exists.")
        raise LoginAlreadyExistsError(f"A user with the username '{user.login}' already exists.")

    # Generate password if not provided
    if not user.password:
        user.password = generate_random_password()
    print("started before create user")
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
    print("started after create user")
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
    
    logger.info(f"User: '{user.login}' ID: '{new_user.id}' created successfully ({change_user_id})!")
    cache.set(f"user:{user.login}", new_user, ttl=3600)  # Store user object in cache
    return new_user.id

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
        preferences = {}
        user_email = db.query(UserPreference).filter(
            UserPreference.user_id == user_data.id,
            UserPreference.preferences_key == 'UserEmail'
        ).first()
        user_mobile = db.query(UserPreference).filter(
            UserPreference.user_id == user_data.id,
            UserPreference.preferences_key == 'UserMobile'
        ).first()

        # Set preferences to return
        if user_email:
            preferences['email'] = user_email.preferences_value.decode('utf-8')
        if user_mobile:
            preferences['mobile'] = user_mobile.preferences_value.decode('utf-8')

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
            'email': preferences.get('email'),
            'mobile': preferences.get('mobile')
        }

        # Store in cache if found
        cache.set(cache_key, response_data, ttl=3600)  # Cache for 1 hour

        return response_data

    return None

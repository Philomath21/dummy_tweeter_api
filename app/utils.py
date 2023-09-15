from passlib.context import CryptContext

# Set the algorhithm as bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Verify password from login request
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Create hashed password
def get_password_hash(password: str):
    return pwd_context.hash(password)


# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user
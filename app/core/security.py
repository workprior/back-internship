from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token/")


def verify_password(plain_password, hashed_password):
    if plain_password is None:
        return None
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    if password is None:
        return None
    return pwd_context.hash(password)

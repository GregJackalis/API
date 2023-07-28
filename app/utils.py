#script for utilites

#for password hashing
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

def hashing(password: str):
    return pwd_context.hash(password)

def verifying_hashed_passwords(original_password, auth_password):
    return pwd_context.verify(original_password, auth_password)

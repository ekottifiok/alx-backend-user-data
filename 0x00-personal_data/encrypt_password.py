from bcrypt import checkpw, hashpw, gensalt


def hash_password(password: str) -> bytes:
    return hashpw(bytes(password, "utf-8"), gensalt())

def is_valid(hashed_password: bytes, password: str) -> bool:
    return checkpw(bytes(password, 'utf-8'), hashed_password)
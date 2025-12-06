import bcrypt

def hash_pwd(password: str, rounds=15) -> bytes:
	pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds))
	return pwd

def verify_pwd(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
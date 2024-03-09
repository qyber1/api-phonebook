import hashlib


class PasswordManager:
    @classmethod
    def hash(cls, password: str):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    @classmethod
    def verify(cls, hashed_password: str, password_input: str):
        # Проверка пароля без соли
        return hashed_password == hashlib.sha256(password_input.encode()).hexdigest()






import bcrypt

class Security:

    @staticmethod

    def hash_password(password_plane: str) -> str:
        password_bytes = password_plane.encode("utf-8")
        salt = bcrypt.gensalt()
        hash_bytes = bcrypt.hashpw(password_bytes, salt)
        return hash_bytes.decode("utf-8")

    @staticmethod

    def verify_passwor (password_plane: str, password_hash: str) -> bool:

        password_bytes = password_plane.encode("utf-8")
        hash_bytes = password_hash.encode("utf-8")

        return bcrypt.checkpw(password_bytes, hash_bytes)

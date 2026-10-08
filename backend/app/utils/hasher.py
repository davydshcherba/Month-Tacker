from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

class Hasher:
    def verify_password(plain_password, hashed_password):
        return password_hash.verify(plain_password, hashed_password)

    def get_password_hash(pas):
        return password_hash.hash(pas)

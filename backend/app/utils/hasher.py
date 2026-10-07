from pwdlib import PasswordHash


class Hasher:
    # def verify_password(plain_password, hashed_password):
    #     return password_hash.verify(plain_password, hashed_password)

    def get_password_hash(pas):
        password_hash = PasswordHash.recommended()
        return password_hash.hash(pas)

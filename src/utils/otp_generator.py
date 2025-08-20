import string
import secrets


def generate_otp(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    otp = ''.join(secrets.choice(characters) for _ in range(length))
    return otp


if __name__ == '__main__':
    print(generate_otp())

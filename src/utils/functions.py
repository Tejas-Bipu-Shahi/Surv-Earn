import re
from string import punctuation


def is_valid_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_strong_password(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, 'Password must be at least 8 characters long'

    lowercase, uppercase, symbol, digit = False, False, False, False
    for x in password:
        if all((lowercase, uppercase, symbol, digit)):
            return True, 'Valid password'
        if x.islower():
            lowercase = True
        elif x.isupper():
            uppercase = True
        elif x.isdigit():
            digit = True
        elif x in punctuation:
            symbol = True

    if not lowercase:
        return False, 'Password must contain at least one lowercase letter'
    if not uppercase:
        return False, 'Password must contain at least one uppercase letter'
    if not symbol:
        return False, 'Password must contain at least one symbol'
    if not digit:
        return False, 'Password must contain at least one digit'

    return True, 'Will Never Reach This Line'


if __name__ == '__main__':
    print(is_valid_email('hell_.o@world.cos'))
    print(is_strong_password('hellOw#orl79d'))

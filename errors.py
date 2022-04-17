class PasswordError(Exception):
    def __init__(self, message):
        self.message = message


class LengthError(PasswordError):
    def __init__(self, message):
        self.message = message


class LetterError(PasswordError):
    def __init__(self, message):
        self.message = message


class DigitError(PasswordError):
    def __init__(self, message):
        self.message = message


class SequenceError(PasswordError):
    def __init__(self, message):
        self.message = message


def check_password(line):
    bad = 'qwertyuiop asdfghjkl zxcvbnm' \
          'йцукенгшщзхъ фывапролджэё ячсмитьбю'
    lowline = line.lower()
    if len(line) < 9:
        raise LengthError("Passwords' length must be at least 9 symbols")
    if not any(_.isdigit() for _ in line):
        raise DigitError("Password must contain at least 1 digit")
    if not any(_.islower() for _ in line) or not any(_.isupper() for _ in line):
        raise LetterError("Password must contain both uppercase and lowercase symbols")
    if any(lowline[i:i + 3] in bad for i in range(len(line) - 2)):
        raise SequenceError("Your password contains prohibited symbols sequence")
    return True
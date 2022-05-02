from errors import *


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

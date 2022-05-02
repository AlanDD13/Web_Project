class PasswordError(Exception):
    def __init__(self, message):
        self.message = message


class LengthError(PasswordError):
    def __init__(self, message):
        super().__init__(message)


class LetterError(PasswordError):
    def __init__(self, message):
        super().__init__(message)


class DigitError(PasswordError):
    def __init__(self, message):
        super().__init__(message)


class SequenceError(PasswordError):
    def __init__(self, message):
        super().__init__(message)


class ConnectionError(Exception):
    def __init__(self, message):
        self.message = message

class WebSiteConnectionError(ConnectionError):
    def __init__(self, message):
        super().__init__(message)


class ArticleConnectionError(ConnectionError):
    def __init__(self, message):
        super().__init__(message)

class UserNotFoundException(Exception):
    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        return self.message

class UnauthorizedException(Exception):
    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        return self.message

class InsufficientTweetsError(Exception):
    def __init__(self, message=''):
        self.message = message
    
    def __str__(self):
        return self.message

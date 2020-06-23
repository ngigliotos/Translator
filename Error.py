class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class InputError(Error):

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

    def __str__(self):
        print(self.expression, self.message)
        return ''

class UnknownWordError(Error):

    def __init__(self, expression, message, syllable):
        self.expression = expression
        self.message = message
        self.syllable = syllable

    def __str__(self):
        print(self.message)
        print(self.expression)
        print(self.syllable)
        return ''

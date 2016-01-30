from validate_email import validate_email

class ErrorHandler:
	def checkEmail(self, email):
		if not validate_email(email):
			raise ValueError("This is an invalid email")
		return email


class ErrorWithCode(Exception):
    def __init__(self, code):
        self.code = code
    def __str__(self):
        return repr(self.code)
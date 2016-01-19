from validate_email import validate_email

class ErrorHandler:
	def checkEmail(self, email):
		if not validate_email(email):
			raise ValueError("This is an invalid email")
		return email
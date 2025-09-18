import phonenumbers

class PhoneNumberValidator:
    """
    Utility class for validating phone numbers.

    Usage:
        if PhoneNumberValidator.validate("+919876543210"):
            print("Valid!")
        else:
            print("Invalid!")
    """

    @staticmethod
    def validate(phone_number: str) -> bool:
        """Return True if the phone number is valid, False otherwise."""
        try:
            number = phonenumbers.parse(phone_number, None)  # expects country code
            return phonenumbers.is_valid_number(number)
        except phonenumbers.NumberParseException:
            return False

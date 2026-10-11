
class Validator:

    @staticmethod
    def is_valid_user_id(user_id):

        if not user_id:
            return False, "User ID cannot be empty."

        if " " in user_id:
            return False, "Spaces are not allowed."

        if not user_id.replace("_", "").isalnum():
            return False, "Only letters, numbers and underscores are allowed."

        if len(user_id) < 6:
            return False, "User ID must be at least 6 characters."

        if len(user_id) > 20:
            return False, "User ID cannot be exceed 20 characters."

        if not any(char.isdigit() for char in user_id):
            return False, "User ID must contain at least one digit."

        return True, ""

    @staticmethod
    def is_valid_pin(new_pin, confirm_pin):
        if not new_pin.isdigit() or not confirm_pin.isdigit():
            return False, "PIN must contain only digits."

        if len(new_pin) != 4 or len(confirm_pin) != 4:
            return False, "PIN must be exactly 4 digits."

        if new_pin != confirm_pin:
            return False, "\nPINs do not match.\nPlease Try Again."

        return True, ""


    @staticmethod
    def is_valid_amount(amount):

        if amount % 100 != 0:
            return False, "Please enter a valid amount."

        return True, ""


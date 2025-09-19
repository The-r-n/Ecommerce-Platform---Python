# File: customer.py
# Creation Date: 19/04/2025
# Last Modified Date: 19/04/2025
# Description: This file contains the Customer class, which inherits from the User class.

from user import User

class Customer(User):
    """
    Represents a customer in the e-commerce system, inheriting from User.
    """
    def __init__(self, user_id="", user_name="", user_password="",
                 user_register_time="00-00-0000_00:00:00", user_role="customer",
                 user_email="", user_mobile=""):
        """
        Constructs a Customer object.

        Args:
            user_id (str): The unique ID of the user.
            user_name (str): The username.
            user_password (str): The user's password.
            user_register_time (str): The time the user registered.
            user_role (str): The role of the user (defaults to 'customer').
            user_email (str): The customer's email address.
            user_mobile (str): The customer's mobile number.
        """
        super().__init__(user_id, user_name, user_password, user_register_time, user_role)
        self.user_email = user_email
        self.user_mobile = user_mobile

    def __str__(self):
        """
        Returns the customer information as a formatted string dictionary.

        Returns:
            str: A string representation of the Customer object.
        """
        user_dict = super().__str__()
        # The parent __str__ returns a string representation of a dict, so we need to evaluate it
        user_data = eval(user_dict)
        user_data['user_email'] = self.user_email
        user_data['user_mobile'] = self.user_mobile
        return str(user_data)

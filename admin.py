# File: admin.py
# Creation Date: 19/04/2025
# Last Modified Date: 19/04/2025
# Description: This file contains the Admin class, which inherits from the User class.

from user import User

class Admin(User):
    """
    Represents an admin in the e-commerce system, inheriting from User.
    """
    def __init__(self, user_id="", user_name="", user_password="",
                 user_register_time="00-00-0000_00:00:00", user_role="admin"):
        """
        Constructs an Admin object.

        Args:
            user_id (str): The unique ID of the user.
            user_name (str): The username.
            user_password (str): The user's password.
            user_register_time (str): The time the user registered.
            user_role (str): The role of the user (defaults to 'admin').
        """
        super().__init__(user_id, user_name, user_password, user_register_time, user_role)
    
    # The __str__ method from the parent User class is sufficient and doesn't need to be overridden.

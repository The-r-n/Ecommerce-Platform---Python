# user.py
# Creation Date: 18/04/2025
# Last Modified Date: 18/04/2025
# Description: This file contains the User class, which serves as a base class for Customer and Admin.

import datetime

class User:
    """
    The base class for all users in the system.
    """
    def __init__(self, user_id="", user_name="", user_password="",
                 user_register_time="00-00-0000_00:00:00", user_role="customer"):
        """
        Constructs a User object.

        Args:
            user_id (str): The unique ID of the user.
            user_name (str): The username.
            user_password (str): The user's password.
            user_register_time (str): The time the user registered.
            user_role (str): The role of the user ('customer' or 'admin').
        """
        self.user_id = user_id
        self.user_name = user_name
        self.user_password = user_password
        self.user_register_time = user_register_time
        self.user_role = user_role

    def __str__(self):
        """
        Returns the user information as a formatted string dictionary.

        Returns:
            str: A string representation of the User object.
        """
        return str({
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_password': self.user_password,
            'user_register_time': self.user_register_time,
            'user_role': self.user_role
        })

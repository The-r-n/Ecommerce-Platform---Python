# File: admin_operation.py
# Creation Date: 21/04/2025
# Last Modified Date: 21/04/2025
# Description: This file contains the AdminOperation class.

import os
import time
from admin import Admin
from user_operation import UserOperation

class AdminOperation:
    """
    Contains all the operations related to the admin.
    """
    users_file_path = 'data/users.txt'

    def register_admin(self):
        """
        Manually creates a default admin account if it does not already exist.
        This should be called every time the system runs.
        """
        user_op = UserOperation()
        
        # Check if the default admin 'admin' already exists
        if user_op.check_username_exist('admin'):
            return # Admin already exists, do nothing

        # If admin does not exist, create it
        admin_password = "admin_password1" # A default password
        
        new_admin = Admin(
            user_id=user_op.generate_unique_user_id(),
            user_name='admin',
            user_password=user_op.encrypt_password(admin_password),
            user_register_time=time.strftime("%d-%m-%Y_%H:%M:%S"),
            user_role='admin'
        )

        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.users_file_path), exist_ok=True)

        # Append the new admin to the users file
        with open(self.users_file_path, 'a', encoding='utf-8') as f:
            f.write(str(new_admin) + '\n')
        
        # print(f"Default admin 'admin' with password '{admin_password}' created.")

# File: user_operation.py
# Creation Date: 20/04/2025
# Last Modified Date: 20/04/2025
# Description: This file contains the UserOperation class, which handles all user-related logic.

import os
import random
import string
import re
from customer import Customer
from admin import Admin

class UserOperation:
    """
    Contains all the operations related to a user.
    Note: As per the spec, this class does not have __init__ or __str__ methods.
    """
    
    users_file_path = 'data/users.txt'

    def _read_users(self):
        """Helper method to read all users from the users.txt file."""
        if not os.path.exists(self.users_file_path):
            # Create the data directory and file if they don't exist
            os.makedirs(os.path.dirname(self.users_file_path), exist_ok=True)
            with open(self.users_file_path, 'w', encoding='utf-8') as f:
                pass # Just create the file
            return []
        
        with open(self.users_file_path, 'r', encoding='utf-8') as f:
            users = []
            for line in f:
                try:
                    users.append(eval(line.strip()))
                except:
                    # Handle potential empty lines or malformed data
                    continue
            return users

    def generate_unique_user_id(self):
        """
        Generates and returns a 10-digit unique user id starting with 'u_'.
        """
        users = self._read_users()
        existing_ids = {user['user_id'] for user in users}
        
        while True:
            new_id = f"u_{random.randint(0, 9999999999):010d}"
            if new_id not in existing_ids:
                return new_id

    def encrypt_password(self, user_password):
        """
        Encodes a user-provided password.
        """
        random_str_len = len(user_password) * 2
        random_chars = string.ascii_letters + string.digits
        random_str = ''.join(random.choice(random_chars) for _ in range(random_str_len))
        
        encrypted = ""
        pass_index = 0
        rand_index = 0
        
        while pass_index < len(user_password):
            encrypted += random_str[rand_index:rand_index+2]
            encrypted += user_password[pass_index]
            rand_index += 2
            pass_index += 1
            
        return f"^{encrypted}^${random_str[rand_index:]}$"

    def decrypt_password(self, encrypted_password):
        """
        Decodes the encrypted password.
        """
        if not (encrypted_password.startswith('^') and encrypted_password.endswith('$')):
             return "" # Not a valid encrypted format
        
        # Strip the start and end markers
        content = encrypted_password[1:-1]
        
        decrypted = ""
        i = 0
        while i < len(content):
            # Skip 2 random chars, get 1 password char
            if (i+2) < len(content):
                decrypted += content[i+2]
            i += 3
            
        return decrypted

    def check_username_exist(self, user_name):
        """
        Verifies whether a user is already registered.
        """
        users = self._read_users()
        return any(user['user_name'] == user_name for user in users)

    def validate_username(self, user_name):
        """
        Validates the user's name. Must be >= 5 chars and contain only letters or underscores.
        """
        return len(user_name) >= 5 and bool(re.match("^[A-Za-z_]+$", user_name))

    def validate_password(self, user_password):
        """
        Validates the user's password. Must be >= 5 chars and contain at least one letter and one number.
        """
        return (len(user_password) >= 5 and
                re.search("[a-zA-Z]", user_password) and
                re.search("[0-9]", user_password))

    def login(self, user_name, user_password):
        """
        Verifies the username and password to authorize system access.
        """
        users = self._read_users()
        for user_data in users:
            if user_data['user_name'] == user_name:
                stored_password_encrypted = user_data['user_password']
                stored_password_decrypted = self.decrypt_password(stored_password_encrypted)
                
                if stored_password_decrypted == user_password:
                    # Password matches, create and return the correct object type
                    if user_data['user_role'] == 'admin':
                        return Admin(**{k: v for k, v in user_data.items() if k in Admin.__init__.__code__.co_varnames})
                    else: # It's a customer
                        return Customer(**{k: v for k, v in user_data.items() if k in Customer.__init__.__code__.co_varnames})
        
        # User not found or password incorrect
        return None

# File: customer_operation.py
# Creation Date: 20/04/2025
# Last Modified Date: 20/04/2025
# Description: This file contains the CustomerOperation class.

import re
import os
import time
import math
from customer import Customer
from user_operation import UserOperation

class CustomerOperation:
    """
    Contains all the operations related to the customer.
    """
    users_file_path = 'data/users.txt'
    
    def _read_users(self):
        """Helper method to read all users from the users.txt file."""
        # This is duplicated from UserOperation to make this class self-contained in its file operations
        if not os.path.exists(self.users_file_path):
            os.makedirs(os.path.dirname(self.users_file_path), exist_ok=True)
            with open(self.users_file_path, 'w', encoding='utf-8') as f:
                pass
            return []
        
        with open(self.users_file_path, 'r', encoding='utf-8') as f:
            users = []
            for line in f:
                try:
                    users.append(eval(line.strip()))
                except:
                    continue
            return users

    def _write_users(self, users_list):
        """Helper method to write a list of users back to the file."""
        with open(self.users_file_path, 'w', encoding='utf-8') as f:
            for user in users_list:
                f.write(str(user) + '\n')

    def validate_email(self, user_email):
        """
        Validates the provided email address format.
        """
        # A simple regex for email validation
        return bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", user_email))

    def validate_mobile(self, user_mobile):
        """
        Validates the provided mobile number format.
        """
        return bool(re.match(r"^(04|03)\d{8}$", user_mobile))

    def register_customer(self, user_name, user_password, user_email, user_mobile):
        """
        Saves the information of the new customer into the data/users.txt file.
        """
        user_op = UserOperation()

        # Perform all validations
        if not user_op.validate_username(user_name): return False
        if user_op.check_username_exist(user_name): return False
        if not user_op.validate_password(user_password): return False
        if not self.validate_email(user_email): return False
        if not self.validate_mobile(user_mobile): return False

        # All checks passed, proceed with registration
        new_customer = Customer(
            user_id=user_op.generate_unique_user_id(),
            user_name=user_name,
            user_password=user_op.encrypt_password(user_password),
            user_register_time=time.strftime("%d-%m-%Y_%H:%M:%S"),
            user_email=user_email,
            user_mobile=user_mobile
        )

        with open(self.users_file_path, 'a', encoding='utf-8') as f:
            f.write(str(new_customer) + '\n')
            
        return True

    def update_profile(self, attribute_name, value, customer_object):
        """
        Updates the given customer object's attribute value.
        """
        all_users = self._read_users()
        user_found = False

        for i, user_data in enumerate(all_users):
            if user_data['user_id'] == customer_object.user_id:
                # Validate the new value before updating
                if attribute_name == 'user_password' and not UserOperation().validate_password(value):
                    return False
                if attribute_name == 'user_email' and not self.validate_email(value):
                    return False
                if attribute_name == 'user_mobile' and not self.validate_mobile(value):
                    return False

                # Encrypt password if it's being updated
                if attribute_name == 'user_password':
                    value = UserOperation().encrypt_password(value)
                
                # Update the attribute in the dictionary
                all_users[i][attribute_name] = value
                
                # Also update the attribute in the passed customer_object
                setattr(customer_object, attribute_name, value)
                
                user_found = True
                break
        
        if user_found:
            self._write_users(all_users)
            return True
        
        return False

    def delete_customer(self, customer_id):
        """
        Deletes the customer from the data/users.txt file.
        """
        all_users = self._read_users()
        original_count = len(all_users)
        
        users_after_deletion = [user for user in all_users if user.get('user_id') != customer_id]
        
        if len(users_after_deletion) < original_count:
            self._write_users(users_after_deletion)
            return True
            
        return False

    def get_customer_list(self, page_number):
        """
        Retrieves one page of customers from the data/users.txt.
        """
        all_users = self._read_users()
        customers_data = [user for user in all_users if user.get('user_role') == 'customer']
        
        items_per_page = 10
        total_pages = math.ceil(len(customers_data) / items_per_page)
        
        if page_number < 1 or page_number > total_pages:
            return ([], page_number, total_pages) # Return empty list if page number is out of bounds

        start_index = (page_number - 1) * items_per_page
        end_index = start_index + items_per_page
        
        page_customers_data = customers_data[start_index:end_index]
        
        customer_objects = [Customer(**data) for data in page_customers_data]

        return (customer_objects, page_number, total_pages)

    def delete_all_customers(self):
        """
        Removes all the customers from the data/users.txt file.
        """
        all_users = self._read_users()
        admins_only = [user for user in all_users if user.get('user_role') == 'admin']
        self._write_users(admins_only)

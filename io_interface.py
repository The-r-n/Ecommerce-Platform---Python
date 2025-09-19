# File: io_interface.py
# Creation Date: 25/04/2025
# Last Modified Date: 25/04/2025
# Description: This file contains the IOInterface class for all user interactions.

class IOInterface:
    """
    Handles all I/O operations. All input()/print() should be in this class.
    """

    def get_user_input(self, message, num_of_args):
        """
        Accepts and processes user input.
        """
        raw_input = input(message).strip().split()
        
        args = raw_input[:num_of_args]
        
        # Pad with empty strings if user provided fewer args than required
        while len(args) < num_of_args:
            args.append("")
            
        return args

    def main_menu(self):
        """
        Displays the main login/register menu.
        """
        print("\n" + "="*40)
        print("    Welcome to the E-Commerce Platform!")
        print("="*40)
        print("1. Login")
        print("2. Register")
        print("3. Quit")
        print("-"*40)

    def admin_menu(self):
        """
        Displays the menu for logged-in administrators.
        """
        print("\n" + "="*40)
        print("              Admin Dashboard")
        print("="*40)
        print("1. Show products (e.g., '1' or '1 2' for page 2)")
        print("2. Show customers (e.g., '2' or '2 3' for page 3)")
        print("3. Show orders (e.g., '3' or '3 4' for page 4)")
        print("4. Generate test data")
        print("5. Generate all statistical figures")
        print("6. Delete all data")
        print("7. Logout")
        print("-"*40)

    def customer_menu(self):
        """
        Displays the menu for logged-in customers.
        """
        print("\n" + "="*40)
        print("             Customer Dashboard")
        print("="*40)
        print("1. Show profile")
        print("2. Update profile (e.g., '2 email new@email.com')")
        print("3. Show products (e.g., '3 keyword' or '3')")
        print("4. Show history orders (e.g., '4' or '4 2' for page 2)")
        print("5. Generate all my consumption figures")
        print("6. Logout")
        print("-"*40)

    def show_list(self, user_role, list_type, data_tuple):
        """
        Prints a formatted list of objects (Customers, Products, or Orders).
        """
        object_list, page_number, total_pages = data_tuple
        
        if not object_list:
            print(f"\nNo {list_type}s found.")
            return

        print(f"\n--- Showing {list_type}s ---")
        print(f"Page: {page_number}/{total_pages}\n")

        for i, obj in enumerate(object_list):
            print(f"[{i+1}] " + str(obj))
        
        print(f"\n--- End of {list_type}s ---")

    def print_error_message(self, error_source, error_message):
        """
        Prints a formatted error message.
        """
        print(f"\n[ERROR] in {error_source}: {error_message}")

    def print_message(self, message):
        """
        Prints a standard message.
        """
        print(f"\n[INFO] {message}")

    def print_object(self, target_object):
        """
        Prints a single object using its __str__ method.
        """
        if target_object:
            print("\n" + str(target_object))
        else:
            self.print_error_message("print_object", "Object not found.")

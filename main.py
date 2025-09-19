# File: main.py
# Creation Date: 25/04/2025
# Last Modified Date: 25/04/2025
# Description: This is the main entry point for the e-commerce application.

# Import all necessary classes
from io_interface import IOInterface
from user_operation import UserOperation
from customer_operation import CustomerOperation
from admin_operation import AdminOperation
from product_operation import ProductOperation
from order_operation import OrderOperation

def main():
    """
    The main control function for the application.
    """
    # Initialize all operation and interface classes
    io = IOInterface()
    user_op = UserOperation()
    cust_op = CustomerOperation()
    admin_op = AdminOperation()
    prod_op = ProductOperation()
    order_op = OrderOperation()

    # --- Initial System Setup ---
    # 1. Ensure a default admin account exists
    admin_op.register_admin()
    # 2. Extract product data from CSVs into products.txt
    # This runs once to populate our main product file from the source CSVs.
    if not prod_op._read_products(): # Only run if products.txt is empty
        io.print_message("First time setup: Extracting product data from source files...")
        prod_op.extract_products_from_files()
        io.print_message("Product extraction complete.")

    logged_in_user = None

    # --- Main Application Loop ---
    while True:
        # --- Logged-Out State ---
        if logged_in_user is None:
            io.main_menu()
            choice, *_ = io.get_user_input("Enter your choice: ", 1)

            if choice == '1': # Login
                username, password, *_ = io.get_user_input("Enter username and password (space-separated): ", 2)
                user_obj = user_op.login(username, password)
                if user_obj:
                    logged_in_user = user_obj
                    io.print_message(f"Welcome back, {logged_in_user.user_name}!")
                else:
                    io.print_error_message("Login", "Invalid username or password.")
            
            elif choice == '2': # Register
                io.print_message("Please enter your details to register.")
                username, password, email, mobile, *_ = io.get_user_input("Enter username, password, email, mobile (space-separated): ", 4)
                success = cust_op.register_customer(username, password, email, mobile)
                if success:
                    io.print_message("Registration successful! You can now log in.")
                else:
                    io.print_error_message("Registration", "Failed. Username may exist, or details are invalid.")

            elif choice == '3': # Quit
                io.print_message("Thank you for using the platform. Goodbye!")
                break
            
            else:
                io.print_error_message("Main Menu", "Invalid choice. Please try again.")
        
        # --- Admin Logged-In State ---
        elif logged_in_user.user_role == 'admin':
            io.admin_menu()
            args = io.get_user_input("Enter choice and arguments: ", 2)
            choice, param = args[0], args[1]

            try:
                if choice == '1': # Show products
                    page = int(param) if param.isdigit() else 1
                    prod_list_tuple = prod_op.get_product_list(page)
                    io.show_list('admin', 'Product', prod_list_tuple)

                elif choice == '2': # Show customers
                    page = int(param) if param.isdigit() else 1
                    cust_list_tuple = cust_op.get_customer_list(page)
                    io.show_list('admin', 'Customer', cust_list_tuple)

                elif choice == '3': # Show orders
                    # Admin needs to see all orders. We'll need to adapt get_order_list or create a new method.
                    # For now, let's show orders of a specific test user if available.
                    io.print_message("Admin 'Show Orders' shows all orders. This is a complex feature.")
                    io.print_message("Functionality to show ALL orders is not specified, showing for first customer.")
                    customers_tuple = cust_op.get_customer_list(1)
                    if customers_tuple[0]:
                        first_customer_id = customers_tuple[0][0].user_id
                        page = int(param) if param.isdigit() else 1
                        order_list_tuple = order_op.get_order_list(first_customer_id, page)
                        io.show_list('admin', f'Order for user {first_customer_id}', order_list_tuple)
                    else:
                        io.print_message("No customers to show orders for.")


                elif choice == '4': # Generate test data
                    io.print_message("Generating test data... This may take a moment.")
                    order_op.generate_test_order_data()
                    io.print_message("Test data generation complete.")

                elif choice == '5': # Generate all statistical figures
                    io.print_message("Generating all statistical figures...")
                    prod_op.generate_category_figure()
                    prod_op.generate_discount_figure()
                    prod_op.generate_likes_count_figure()
                    prod_op.generate_discount_likes_count_figure()
                    order_op.generate_all_customers_consumption_figure()
                    order_op.generate_all_top_10_best_sellers_figure()
                    io.print_message("All figures generated in 'data/figure' folder.")

                elif choice == '6': # Delete all data
                    confirm, *_ = io.get_user_input("Type 'CONFIRM' to delete all customers, products, and orders: ", 1)
                    if confirm == 'CONFIRM':
                        cust_op.delete_all_customers()
                        prod_op.delete_all_products()
                        order_op.delete_all_orders()
                        io.print_message("All customer, product, and order data has been deleted.")
                    else:
                        io.print_message("Deletion cancelled.")

                elif choice == '7': # Logout
                    logged_in_user = None
                    io.print_message("You have been logged out.")
                
                else:
                    io.print_error_message("Admin Menu", "Invalid choice.")

            except Exception as e:
                io.print_error_message("Admin Operation", f"An unexpected error occurred: {e}")

        # --- Customer Logged-In State ---
        elif logged_in_user.user_role == 'customer':
            io.customer_menu()
            args = io.get_user_input("Enter choice and arguments: ", 3)
            choice, param1, param2 = args[0], args[1], args[2]

            try:
                if choice == '1': # Show profile
                    io.print_object(logged_in_user)
                
                elif choice == '2': # Update profile
                    attr_name, value = param1, param2
                    if attr_name and value:
                        # Restrict updatable attributes
                        allowed_attrs = ['user_password', 'user_email', 'user_mobile']
                        if attr_name in allowed_attrs:
                            success = cust_op.update_profile(attr_name, value, logged_in_user)
                            if success:
                                io.print_message("Profile updated successfully.")
                            else:
                                io.print_error_message("Update Profile", "Invalid value. Please check format.")
                        else:
                            io.print_error_message("Update Profile", "You can only update 'user_password', 'user_email', or 'user_mobile'.")
                    else:
                        io.print_error_message("Update Profile", "Please provide attribute and value (e.g., '2 user_email new@a.com').")

                elif choice == '3': # Show products
                    keyword = param1
                    if keyword: # Search by keyword
                        product_list = prod_op.get_product_list_by_keyword(keyword)
                        io.show_list('customer', f"Product matching '{keyword}'", (product_list, 1, 1))
                    else: # Show paginated list
                        product_list_tuple = prod_op.get_product_list(1)
                        io.show_list('customer', 'Product', product_list_tuple)
                
                elif choice == '4': # Show history orders
                    page = int(param1) if param1.isdigit() else 1
                    order_list_tuple = order_op.get_order_list(logged_in_user.user_id, page)
                    io.show_list('customer', 'Order', order_list_tuple)

                elif choice == '5': # Generate all my consumption figures
                    io.print_message("Generating your consumption figure...")
                    order_op.generate_single_customer_consumption_figure(logged_in_user.user_id)
                    io.print_message(f"Figure saved to 'data/figure/single_customer_consumption_{logged_in_user.user_id}.png'")

                elif choice == '6': # Logout
                    logged_in_user = None
                    io.print_message("You have been logged out.")

                else:
                    io.print_error_message("Customer Menu", "Invalid choice.")

            except Exception as e:
                io.print_error_message("Customer Operation", f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()

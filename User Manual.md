**E-Commerce Shopping Program**


Welcome! Think of this as a pretend online shop that runs on your computer. It's a simple program where you can create an account, browse items, and pretend to place orders.

There are two kinds of users in this shop:

  * **A Customer:** This is you! You can create your own account, look at all the products, and see a history of the orders you've placed.
  * **An Admin:** This is the "shop manager." The Admin has special powers, like seeing a list of all customers, looking at every order, and even creating charts and reports about how the shop is doing.

This guide will walk you through how to use the program, step by step.



**Before You Start: Getting Everything Ready**

This program doesn't have fancy buttons or graphics. Instead, you'll interact with it by typing commands into a special window on your computer called a **terminal** or **command prompt**.

**Here’s what you need to do to get started:**

1.  **Gather Your Files:** Make sure all the project files (`main.py`, `user.py`, all the `.csv` files, etc.) are all together in one folder on your computer.

2.  **Open the Terminal:**

      * On **Windows**, search for "Command Prompt" or "PowerShell" and open it.
      * On a **Mac**, search for "Terminal" and open it.

3.  **Navigate to Your Folder:** In the terminal, you need to tell it to go to the folder where you saved the project files. You'll do this using the `cd` (change directory) command. For example, if your folder is on the Desktop, you might type `cd Desktop/ECommerce-Project`.

4.  **Start the Program:** Once you're in the right folder, type the following command and press **Enter**:

    ```
    python main.py
    ```

The very first time you run this, the program will do two things automatically in the background:

  * It will create the special "Admin" (shop manager) account for you.
  * It will read all the product information from the spreadsheet files (`.csv`) and organize it into one master list for the shop to use.

You will then see the first menu on your screen!


-----
**The First Screen: Your Starting Point**

This is the main menu. You have three choices. To pick one, just type the number and press **Enter**.

**Choice 1: Log In**

  * **What it's for:** Use this if you already have an account and want to access it.
  * **How to do it:**
    1.  Type `1` and press **Enter**.
    2.  The program will ask for your username and password. Type them both on the same line, separated by a single space, and then press **Enter**.
    <!-- end list -->
      * **To log in as the Shop Manager (Admin):**
          * Username: `admin`
          * Password: `admin_password1`
      * **Example of what to type:** `admin admin_password1`

**Choice 2: Register (Create a New Customer Account)**

  * **What it's for:** Use this to create your own personal customer account.

  * **How to do it:**

    1.  Type `2` and press **Enter**.
    2.  The program will ask for four pieces of information. You need to type them all on one line, separated by spaces. The order is: `username password email mobile_number`.

  * **Rules for Your Information:**

      * **Username:** At least 5 characters long. Can only use letters (a-z) and underscores (\_).
      * **Password:** At least 5 characters long. Must include at least one letter and at least one number (e.g., `shopping123`).
      * **Email:** Must look like a real email address (e.g., `my_email@example.com`).
      * **Mobile Number:** Must be exactly 10 numbers long and start with either `04` or `03`.

  * **Example of what to type:** `my_username MyPassword123 me@email.com 0411222333`

  * **What happens next?**

      * If you followed all the rules, you'll see a success message\! You can now log in with your new account.
      * If you made a mistake (like using a username that's already taken or a password that's too simple), the program will show an error message, and you can try again.

**Choice 3: Quit**

  * **What it's for:** To close the program.
  * **How to do it:** Type `3` and press **Enter**.



-----

**The Admin Dashboard: Managing the Shop**

If you log in as the Admin, you'll see a special menu with powerful tools.

  * **To See a List of Products (Command 1):**

      * Type `1` to see the first page of products.
      * To see a different page, type `1`, a space, and the page number. Example: `1 2` shows page two.

  * **To See a List of Customers (Command 2):**

      * Works just like seeing products. Example: `2 3` shows the third page of customers.

  * **To See a List of Orders (Command 3):**

      * Works the same way. Example: `3` shows the first page of all orders.

  * **To Generate Test Data (Command 4):**

      * **What it is:** This is a fun tool for testing. If you type `4`, the program will instantly create 10 new fake customer accounts and pretend they've placed hundreds of orders.
      * **Why use it?** It fills the shop with data so that the reports (see next step) look interesting and have information to show.

  * **To Generate Statistical Reports (Command 5):**

      * **What it is:** This is the most powerful tool for the Admin. When you type `5`, the program analyzes all the shop's data and creates **six picture files (charts and graphs)**.
      * **Where to find them:** These picture files are saved in the `data/figure` folder inside your project folder. You can open them to see things like which products are the most popular and which months had the most sales.

  * **To Delete All Data (Command 6):**

      * **WARNING:** This is a permanent action\! It will erase all customers (except the Admin), all products, and all orders.
      * **How it works:** Type `6`. The program will ask you to confirm by typing the word `CONFIRM`. This is a safety measure to make sure you don't do it by accident.

  * **To Logout (Command 7):**

      * Type `7` to sign out and return to the main starting screen.


-----

**The Customer Dashboard: Your Shopping Hub**

When you log in with your own customer account, you'll see your personal menu.

  * **To See Your Profile (Command 1):**

      * Type `1` to see all the information you entered when you registered.

  * **To Update Your Profile (Command 2):**

      * **What it's for:** To change your password, email, or mobile number.
      * **How to do it:** You need to type `2`, then what you want to change, then the new value.
      * **Example:** To change your email, you would type: `2 user_email new_email@provider.com`
      * You can only change `user_password`, `user_email`, or `user_mobile`.

  * **To Look at Products (Command 3):**

      * **To browse all products:** Just type `3` to see the first page.
      * **To search for a specific product:** Type `3`, a space, and then a keyword. The program will show you all products with that word in their name.
      * **Example:** `3 shirt`

  * **To See Your Order History (Command 4):**

      * Type `4` to see the first page of all the orders you've placed.
      * To see other pages, add the page number. Example: `4 2`

  * **To See Your Spending Report (Command 5):**

      * **What it is:** Similar to the Admin reports, but this one is just for you.
      * **How it works:** Type `5`. The program will create a special chart that shows how much you've "spent" in the shop each month. You can find this picture file in the `data/figure` folder.

  * **To Logout (Command 6):**

      * Type `6` to sign out and go back to the main starting screen.
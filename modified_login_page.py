from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random
import MySQLdb
from PIL import ImageTk,Image
from dotenv import load_dotenv
import os
from password_hashing import hash_password, verify_password
from customer import Customer
from employee import Employee

class Login:
    def __init__(self, root, mycursor, mydb):
        self.root = root
        self.mycursor = mycursor
        self.mydb = mydb

    def update_account_combobox(self, account_combobox, customer_id):
        self.mycursor.execute("SELECT accountid FROM account WHERE customerid = %s", (customer_id,))
        account_ids = self.mycursor.fetchall()
        account_ids = [account_id[0] for account_id in account_ids]
        account_combobox['values'] = account_ids
        account_combobox.set('')  # Set to an empty string to clear the selection

    def login_validator(self, username, password, type_of_login):
        login_table = type_of_login+"login"

        # Check if the username exists in the specified login table
        self.mycursor.execute(f"SELECT * FROM {login_table} WHERE username = %s", (username,))
        user_data = self.mycursor.fetchone()

        if not user_data:
            messagebox.showinfo("Error", "Invalid username.")
            return False

        # Verify the provided password against the stored hashed password
        stored_hashed_password = user_data[2]  # The hashed password is in the third column
        if not verify_password(password, stored_hashed_password.encode('utf-8')):
            messagebox.showinfo("Error", "Incorrect password.")
            return False

        # If both username and password are valid, return True
        return True
        
    def enter_balance(self, customer_id, account_combobox):
        enterbalance = Toplevel(self.root)
        enterbalance.title("Enter balance")
        enterbalance.resizable(width=False, height=False)
        print("Entered enter balance")
        def generate_unique_account_number():
            while True:
                # Generate a random 8-digit account number
                account_number = str(random.randint(10000000, 99999999))
                #Check if the account number already exists in the database
                self.mycursor.execute("SELECT COUNT(*) FROM account WHERE accountid = %s", (account_number,))
                count = self.mycursor.fetchone()[0]

                # If the count is 0, the account number is unique
                if count == 0:
                    return account_number
        
        def create_handler(balance, account_number, customer_id):
            
            try:
                # Retrieve a random branch ID from the 'branch' table
                self.mycursor.execute("SELECT branchid FROM branch ORDER BY RAND() LIMIT 1")
                branch_id = self.mycursor.fetchone()[0]

                # List of account types
                account_types = ['savings', 'current', 'fixed deposit', 'recurring deposit']

                # Randomly select an account type
                account_type = random.choice(account_types)
                status = "active"

                try:
                    balance = float(balance)
                except ValueError:
                    messagebox.showerror("Error", "Invalid input. Please enter a valid decimal number.")
                # Insert the new account information into the 'account' table
                sql = "INSERT INTO account (accountid, customerid, branchid, balance, accounttype, status) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (account_number, customer_id, branch_id, float(balance), account_type, status)

                self.mycursor.execute(sql, values)
                self.mydb.commit()
                messagebox.showinfo("Success", "Account created successfully!!")
                enterbalance.destroy()
                print("Account created successfully!")

                self.update_account_combobox(account_combobox, customer_id)
            
            except MySQLdb.Error as e:
                messagebox.showinfo(f"Error: {e}")

        account_number = str(generate_unique_account_number())
        ttk.Label(enterbalance, text="Your assigned account number is " +account_number).pack(pady=10)
        
        ttk.Label(enterbalance, text="Enter the money you want to deposit:").pack(pady=10)
        balance = ttk.Entry(enterbalance)
        balance.pack(pady=10)

        ttk.Button(enterbalance, text="Create", command=lambda: create_handler(balance.get(), account_number, customer_id)).pack(pady=10)



    def list_of_accounts(self, username, rol):
        listofacc = Toplevel(self.root)
        listofacc.title("Select Account")
        listofacc.resizable(width=False, height=False)

        img_path = "images/brick_background.jpeg"
        cropped_and_resized_image = self.crop_and_resize_image(img_path, listofacc.winfo_screenwidth(), listofacc.winfo_screenheight())

        background_label = ttk.Label(listofacc, image=cropped_and_resized_image)
        background_label.place(relwidth=1, relheight=1)
        
        # Fetch customer ID based on the username
        self.mycursor.execute("SELECT c.customerid FROM customer c,customerlogin cl WHERE username = %s and c.customerid = cl.customerid", (username,))
        customer_id = self.mycursor.fetchone()[0]

        # Fetch accounts associated with the customer ID
        self.mycursor.execute("SELECT accountid FROM account WHERE customerid = %s", (customer_id,))
        account_ids = self.mycursor.fetchall()

        # Convert the list of tuples to a list of account IDs
        account_ids = [account_id[0] for account_id in account_ids]

        # Label and Combobox
        ttk.Label(listofacc, text="Select the account you want to login with").pack(pady=10)
        account_combobox = ttk.Combobox(listofacc, values=account_ids)
        account_combobox.pack(pady=10)

        ttk.Button(listofacc, text="+Create a new account", command=lambda:self.enter_balance(customer_id, account_combobox)).pack(pady=10)

        # Function to handle account selection
        def login_with_selected_account():
            selected_account = account_combobox.get()
            self.mycursor.execute("SELECT status FROM account WHERE accountid = %s", (selected_account,))
            status = self.mycursor.fetchone()[0]
            if selected_account:
                if status == "active":
                    # Handle the login with the selected account
                    print(f"Logging in with account: {selected_account}")
                    Customer(self.mydb, self.mycursor, customer_id, selected_account)
                else:
                    messagebox.showinfo("Error", f"account {selected_account} is not active\nstatus:{status}")
                listofacc.destroy()
                rol.destroy()

        # Button to trigger the account selection
        ttk.Button(listofacc, text="Login", command=login_with_selected_account).pack(pady=10)
        listofacc.attributes('-transparent', 'white')
        listofacc.wm_attributes('-topmost', 1)
        listofacc.mainloop

    def customer_login(self, rol):
        customer_log = Toplevel(self.root)
        customer_log.title("Customer Login Page")
        customer_log.resizable(width=False, height=False)
        img_path = "images/hacker_background.png"
        cropped_and_resized_image = self.crop_and_resize_image(img_path, customer_log.winfo_screenwidth(), customer_log.winfo_screenheight())

        background_label = ttk.Label(customer_log, image=cropped_and_resized_image)
        background_label.place(relwidth=1, relheight=1)
        lb1 = ttk.Label(customer_log, text="Welcome Back")
        lb1.pack(pady=10)
        ttk.Label(customer_log, text="Username:").pack(pady=(0, 10))
        username_entry = ttk.Entry(customer_log)
        username_entry.pack(pady=(0, 10))
        ttk.Label(customer_log, text="Password:").pack(pady=(0, 10))
        password_entry = ttk.Entry(customer_log, show="*")
        password_entry.pack(pady=(0, 10))

        def customer_checker(username, password):
            if not username or not password:
                messagebox.showinfo("Error", "Please enter both username and password.")
            else:
                result = self.login_validator(username, password, "customer")
                if result:
                    customer_log.destroy()
                    self.list_of_accounts(username, rol)

        ttk.Button(customer_log, text="Login", command=lambda:customer_checker(username_entry.get(), password_entry.get())).pack(pady=10)
        customer_log.attributes('-transparent', '#ab23ff')
        customer_log.wm_attributes('-topmost', 1)
        customer_log.mainloop


    def employee_login(self):
        employee_log = Toplevel(self.root)
        employee_log.title("Employee Login Page")
        employee_log.resizable(width=False, height=False)

        ttk.Label(employee_log, text="Username:").pack()

        username_entry = ttk.Entry(employee_log)
        username_entry.pack()
        ttk.Label(employee_log, text="Password:").pack()
        password_entry = ttk.Entry(employee_log, show="*")
        password_entry.pack()
        def employee_checker(username, password):
            if not username or not password:
                messagebox.showinfo("Error", "Please enter both username and password.")
            else:
                result = self.login_validator(username, password, "employee")
                self.mycursor.execute(f"SELECT el.EmployeeId, roleid, status FROM employeelogin el, employee e WHERE username = %s and el.employeeid = e.employeeid", (username,))
                result_tuple = self.mycursor.fetchone()
                if result and result_tuple:
                    employee_id, role_id, status = result_tuple
                    employee_log.destroy()
                    if status != "dismissed":
                        Employee(self.mydb, self.mycursor, employee_id, role_id)
                        print("Employee login success")
                    else:
                        messagebox.showerror("Error", f"Employee with {employee_id} is dismissed and cannot access the system")

        ttk.Button(employee_log, text="Login", command=lambda:employee_checker(username_entry.get(), password_entry.get())).pack(pady=10)
        employee_log.mainloop()

    def customer_register(self):
        customer_reg = Toplevel(self.root)
        customer_reg.title("Customer Registration")
        customer_reg.geometry("350x524")
        customer_reg.resizable(width=False, height=False)
        img_path = "images/abstract_background.jpeg"
        cropped_and_resized_image = self.crop_and_resize_image(img_path, customer_reg.winfo_screenwidth(), customer_reg.winfo_screenheight())

        background_label = ttk.Label(customer_reg, image=cropped_and_resized_image)
        background_label.place(relwidth=1, relheight=1)

        def generate_unique_customer_id():
            # Generate a random CustomerID until a unique one is found
            self.mycursor.execute("SELECT customerid FROM customer")
            existing_customer_ids = [row[0] for row in self.mycursor.fetchall()]
            while True:
                customer_id = random.randint(1000, 9999)
                if customer_id not in existing_customer_ids:
                    return customer_id

        # Function to validate and register the customer
        def register_customer():
            try:
                # Get values from the Entry widgets
                first_name = first_name_entry.get()
                last_name = last_name_entry.get()
                address = address_entry.get()
                phone_number = phone_entry.get()
                username = username_entry.get()
                password = password_entry.get()
                password_again = password_again_entry.get()

                # Validate if all fields are filled
                if not all([first_name, last_name, address, phone_number]):
                    messagebox.showerror("Error", "Please fill in all fields.")
                    return
                
                if password != password_again:
                    messagebox.showerror("Error", "Passwords do not match.")
                    return

                # Generate a unique CustomerID
                customer_id = generate_unique_customer_id()

                # Hash the password
                hashed_password = hash_password(password)

                # Insert data into the customer table
                self.mycursor.execute("INSERT INTO customer (customerid, Fname, Lname, address, phoneno) VALUES (%s, %s, %s, %s, %s)",
                                (customer_id, first_name, last_name, address, phone_number))

                # Insert data into the customerlogin table
                self.mycursor.execute("INSERT INTO customerlogin (customerid, username, passwordhash) VALUES (%s, %s, %s)",
                                (customer_id, username, hashed_password))

                # Commit the changes
                self.mydb.commit()
                messagebox.showinfo("Success", f"Customer registered!!, Customer ID: {customer_id}")

                # Close the registration window after successful registration
                customer_reg.destroy()
                # Widgets for customer registration
            except MySQLdb.Error as e:
                messagebox.showinfo(f"Error: {e}, enter valid phonenumber")

        ttk.Label(customer_reg, text="First Name:").pack(pady=(5, 10))
        first_name_entry = ttk.Entry(customer_reg)
        first_name_entry.pack(pady=(0, 10))

        ttk.Label(customer_reg, text="Last Name:").pack(pady=(0, 10))
        last_name_entry = ttk.Entry(customer_reg)
        last_name_entry.pack(pady=(0, 10))

        ttk.Label(customer_reg, text="Address:").pack(pady=(0, 10))
        address_entry = ttk.Entry(customer_reg)
        address_entry.pack(pady=(0, 10))

        ttk.Label(customer_reg, text="Phone Number:").pack(pady=(0, 10))
        phone_entry = ttk.Entry(customer_reg)
        phone_entry.pack(pady=(0, 10))

        ttk.Label(customer_reg, text="Choose a username:").pack(pady=(0, 10))
        username_entry = ttk.Entry(customer_reg)
        username_entry.pack(pady=(0, 10))

        ttk.Label(customer_reg, text="Set a password").pack(pady=(0, 10))
        password_entry = ttk.Entry(customer_reg, show="*")
        password_entry.pack(pady=(0, 10))

        ttk.Label(customer_reg, text="Confirm password").pack(pady=(0, 10))
        password_again_entry = ttk.Entry(customer_reg, show="*")
        password_again_entry.pack(pady=(0, 10))
        
        ttk.Button(customer_reg, text="Register", command=register_customer).pack(pady=10)
        register_customer.attributes('-transparent', 'white')
        register_customer.wm_attributes('-topmost', 1)
        register_customer.mainloop
        
    def crop_and_resize_image(self, image_path, width, height):
            original_image = Image.open(image_path)
            cropped_image = original_image.crop((0, 0, width, height))
            resized_image = cropped_image.resize((width, height))
            return ImageTk.PhotoImage(resized_image)

    def register_or_login(self):
        reg_or_log = Toplevel(self.root)
        reg_or_log.title("Welcome to Your App")

        ttk.Label(reg_or_log, text="Welcome Back! Ready to Dive In?", font=('Helvetica', 14)).pack(pady=10)
        ttk.Button(reg_or_log, text="Sign In", command=lambda: self.customer_login(reg_or_log)).pack(pady=5)

        ttk.Label(reg_or_log, text="New here? Let's get started!", font=('Helvetica', 14)).pack(pady=10)
        ttk.Button(reg_or_log, text="Get Started", command=self.customer_register).pack(pady=5)

        reg_or_log.mainloop()
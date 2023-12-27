from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import random
import MySQLdb
from dotenv import load_dotenv
import os
from password_hashing import hash_password, verify_password
import tkinter as tk
from PIL import Image, ImageTk

class Customer(tk.Tk):
    def __init__(self, mydb, mycursor, cust_id, acc_id):
        self.mycursor = mycursor
        self.mydb = mydb
        self.cust_id = cust_id
        self.acc_id = acc_id
        super().__init__()
        self.title("Customer Actions")
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))  # Full screen

        # Add main heading
        main_heading = Label(self, text="Customer Actions", font=("Arial", 24, "bold"), padx=20, pady=10, bg="lightblue")
        main_heading.pack(pady=20)

        # Add buttons with simple colors
        tk.Button(self, text="Transaction", font=("Arial", 16), bg="skyblue", padx=20, pady=10,command=self.transaction).pack(pady=20)
        tk.Button(self, text="Withdraw", font=("Arial", 16), bg="skyblue", padx=20, pady=10,command=self.withdraw).pack(pady=20)
        tk.Button(self, text="Deposit", font=("Arial", 16), bg="skyblue", padx=20, pady=10,command=self.deposit).pack(pady=20)
        tk.Button(self, text="Request Loan", font=("Arial", 16), bg="skyblue", padx=20, pady=10,command=self.request_loan).pack(pady=20)
        tk.Button(self, text="show info", font=("Arial", 16), bg="skyblue", padx=20, pady=10,command=self.customer_info).pack(pady=20)
        tk.Button(self, text="show transaction history", font=("Arial", 16), bg="skyblue", padx=20, pady=10,command=self.h_t).pack(pady=20)


    def transaction(self):
        transaction_window = Toplevel()
        transaction_window.title("Transaction")
        transaction_window.geometry("{0}x{1}+0+0".format(transaction_window.winfo_screenwidth(), transaction_window.winfo_screenheight()))
        img = Image.open("images/transaction1.jpg").resize((transaction_window.winfo_screenwidth(), transaction_window.winfo_screenheight()))
        image_obj = ImageTk.PhotoImage(img)
        
        transaction_label = Label(transaction_window, image=image_obj)
        transaction_label.place(relwidth=1, relheight=1)

        def generate_unique_transaction_id():
        # Generate a random TransactionID until a unique one is found
            self.mycursor.execute("SELECT transactionid FROM transaction")
            existing_transaction_ids = [row[0] for row in self.mycursor.fetchall()]
            while True:
                transaction_id = random.randint(1000, 9999)
                if transaction_id not in existing_transaction_ids:
                    return transaction_id 

        def submit_transaction():
            from_account_id = self.acc_id
            to_account_id = to_account_id_entry.get()
            emp_id = emp_id_entry.get()
            amount = amount_entry.get()
            if not emp_id:
                emp_id = None
    
            # Check if the to_account_id exists
            check_to_query = f"SELECT * FROM account WHERE AccountID = {to_account_id};"
            self.mycursor.execute(check_to_query)
            to_account_exists = self.mycursor.fetchone()
            if to_account_exists and to_account_exists[5] == "active" and to_account_id != from_account_id:
                # Check if there's enough amount in the from_account_id
                print(from_account_id)
                check_amount_query = f"SELECT Balance FROM account WHERE AccountID = {from_account_id};"
                self.mycursor.execute(check_amount_query)
                from_account_amount = self.mycursor.fetchone()[0]
                print(from_account_amount)

                if from_account_amount >= float(amount):
                    # Deduct amount from from_account_id
                    update_from_query = f"UPDATE account SET Balance = Balance - {amount} WHERE AccountID = {from_account_id};"
                    self.mycursor.execute(update_from_query)
                    time_v = datetime.now()
                    transaction_id = generate_unique_transaction_id()
                    insert_query = "INSERT INTO transaction (TransactionID,SourceAccountID,DestinationAccountID,Amount,AssistedBy,TimeStamp) VALUES (%s, %s, %s, %s, %s, %s);"
                    values = (transaction_id, from_account_id, to_account_id, amount, emp_id, time_v)
                    self.mycursor.execute(insert_query, values)
                    # Add amount to to_account_id
                    update_to_query = f"UPDATE account SET Balance = Balance + {amount} WHERE AccountID = {to_account_id};"
                    self.mycursor.execute(update_to_query)

                    self.mydb.commit()

                    messagebox.showinfo("Success", f"Transaction successful!\nAmount {amount} transferred from AccountID {from_account_id} to AccountID {to_account_id}.")
                    transaction_window.destroy()

                else:
                    messagebox.showerror("Error", f"Insufficient balance in AccountID {from_account_id}.")
                    transaction_window.destroy()
            elif to_account_exists[5] != "active":
                if to_account_exists[5] == "deactivated":
                    messagebox.showerror("Error", f"Cannot Process Transaction, Account {to_account_id} is deactivated.")
                else:
                    messagebox.showerror("Error", f"Cannot Process Transaction, Account {to_account_id} is closed.")
            elif to_account_id == from_account_id:
                messagebox.showerror("Error", f"Cannot Process Transaction to the same account.")
            else:
                messagebox.showerror("Error", "Invalid AccountID(s). Please check and try again.")
                transaction_window.destroy()

        Label(transaction_window, text="Transaction", font=("Arial", 24, "bold"), padx=20, pady=10, bg="#f2b79b").pack(pady=20)

        # Employee ID entry
        Label(transaction_window, text="Emp ID(optional):", font=("Arial", 16)).pack(pady=10)

        emp_id_entry = Entry(transaction_window, font=("Arial", 14))
        emp_id_entry.pack(pady=10)
        
        # To Account ID entry
        Label(transaction_window, text="Transfer to Account ID:", font=("Arial", 16)).pack(pady=10)

        to_account_id_entry = Entry(transaction_window, font=("Arial", 14))
        to_account_id_entry.pack(pady=10)

        # Amount entry
        Label(transaction_window, text="Amount:", font=("Arial", 16)).pack(pady=10)

        amount_entry = Entry(transaction_window, font=("Arial", 14))
        amount_entry.pack(pady=10)

        # Submit button
        Button(transaction_window, text="Submit", font=("Arial", 16, "bold"), command=submit_transaction, bg="tomato", padx=20, pady=10).pack(pady=20)

        transaction_window.mainloop()

    def withdraw(self):
        withdraw_window = Toplevel()
        withdraw_window.title("Withdraw")
        withdraw_window.geometry("{0}x{1}+0+0".format(withdraw_window.winfo_screenwidth(), withdraw_window.winfo_screenheight()))

        img = Image.open("images/withdrawl.jpg").resize((withdraw_window.winfo_screenwidth(), withdraw_window.winfo_screenheight()))
        image_obj = ImageTk.PhotoImage(img)
        
        transaction_label = Label(withdraw_window, image=image_obj)
        transaction_label.place(relwidth=1, relheight=1)

        def submit_withdraw():
            account_id = self.acc_id
            amount = amount_entry.get()

            # Check if there's enough amount to withdraw
            check_amount_query = f"SELECT Balance FROM account WHERE AccountID = {account_id};"
            self.mycursor.execute(check_amount_query)
            account_balance = self.mycursor.fetchone()[0]

            if account_balance >= float(amount):
                # Update account balance after withdrawal
                update_query = f"UPDATE account SET Balance = Balance - {amount} WHERE AccountID = {account_id};"
                self.mycursor.execute(update_query)
                self.mydb.commit()

                messagebox.showinfo("Success", f"Withdrawal successful!\nAmount {amount} withdrawn from AccountID {account_id}.")
                withdraw_window.destroy()

            else:
                messagebox.showerror("Error", f"Insufficient balance in AccountID {account_id}.")
                withdraw_window.destroy()

        Label(withdraw_window, text="Update Account Status", font=("Arial", 24, "bold"), padx=20, pady=10, bg="#93edba").pack(pady=20)

        # Amount entry
        Label(withdraw_window, text="Amount:", font=("Arial", 16)).pack(pady=10)

        amount_entry = Entry(withdraw_window, font=("Arial", 14))
        amount_entry.pack(pady=10)

        # Submit button
        Button(withdraw_window, text="Submit", font=("Arial", 16, "bold"), command=submit_withdraw, bg="tomato", padx=20, pady=10).pack(pady=20)

        withdraw_window.mainloop()


    def deposit(self):
        deposit_window = Toplevel()
        deposit_window.title("Deposit")
        deposit_window.geometry("{0}x{1}+0+0".format(deposit_window.winfo_screenwidth(), deposit_window.winfo_screenheight()))

        img = Image.open("images/deposit.jpg").resize((deposit_window.winfo_screenwidth(), deposit_window.winfo_screenheight()))
        image_obj = ImageTk.PhotoImage(img)
        
        transaction_label = Label(deposit_window, image=image_obj)
        transaction_label.place(relwidth=1, relheight=1)

        def submit_deposit():
            account_id = self.acc_id
            amount = amount_entry.get()

            # Update account balance after deposit
            update_query = f"UPDATE account SET Balance = Balance + {amount} WHERE AccountID = {account_id};"
            self.mycursor.execute(update_query)
            self.mydb.commit()

            messagebox.showinfo("Success", f"Deposit successful!\nAmount {amount} deposited to AccountID {account_id}.")
            deposit_window.destroy()

        Label(deposit_window, text="Update Account Status", font=("Arial", 24, "bold"), padx=20, pady=10, bg="#f781e4").pack(pady=20)

        # Amount entry
        Label(deposit_window, text="Amount:", font=("Arial", 16)).pack(pady=10)

        amount_entry = Entry(deposit_window, font=("Arial", 14))
        amount_entry.pack(pady=10)

        # Submit button
        Button(deposit_window, text="Submit", font=("Arial", 16, "bold"), command=submit_deposit, bg="tomato", padx=20, pady=10).pack(pady=20)

        deposit_window.mainloop()


    def validate_password(self, password):
            # Check if the username exists in the specified login table
            self.mycursor.execute(f"SELECT * FROM customerlogin cl, customer c WHERE cl.customerid = c.customerid and c.customerid = %s", (self.cust_id,))
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
    
    def request_loan(self):
        loan_window = Toplevel()
        loan_window.title("Customer Information")
        loan_window.geometry("{0}x{1}+0+0".format(loan_window.winfo_screenwidth(), loan_window.winfo_screenheight()))

        img = Image.open("images/customer_loan.webp").resize((loan_window.winfo_screenwidth(), loan_window.winfo_screenheight()))
        image_obj = ImageTk.PhotoImage(img)
        
        transaction_label = Label(loan_window, image=image_obj)
        transaction_label.place(relwidth=1, relheight=1)

        def interest_rate_slab():
            pass
        def generate_unique_loan_id():
        # Generate a random LoanID until a unique one is found
            self.mycursor.execute("SELECT loanid FROM loan")
            existing_loan_ids = [row[0] for row in self.mycursor.fetchall()]
            while True:
                loan_id = random.randint(1000, 9999)
                if loan_id not in existing_loan_ids:
                    return loan_id 
    
        def req_loan():
            interest_rate = 8.45
            amount = amount_entry.get()
            loan_id = generate_unique_loan_id()
            approval_status = "pending"
            employee_id = None 
            insert_query = "INSERT INTO loan (loanid,customerid,employeeid,Amount,interestrate,approvalstatus) VALUES (%s, %s, %s, %s, %s, %s);"
            values = (loan_id, self.cust_id, employee_id, amount, interest_rate, approval_status)
            self.mycursor.execute(insert_query, values)
            self.mydb.commit()
            messagebox.showinfo("Success", f"New Loan request of amount {amount} is successful, Loan id: {loan_id}")
            loan_window.destroy()

        Label(loan_window, text="Update Account Status", font=("Arial", 24, "bold"), padx=20, pady=10, bg="#7dad58").pack(pady=20)

        Label(loan_window, text="Enter the amount: ", font=("Arial", 16)).pack(pady=10)
        amount_entry = Entry(loan_window, font=("Arial", 14))
        amount_entry.pack(pady=10)

        Button(loan_window, text="Submit", font=("Arial", 16, "bold"), command=req_loan, bg="tomato", padx=20, pady=10).pack(pady=20)

        loan_window.mainloop()
    

    def customer_info(self):
        info_window = Toplevel()
        info_window.title("Customer Information")
        info_window.geometry("{0}x{1}+0+0".format(info_window.winfo_screenwidth(), info_window.winfo_screenheight()))

        img = Image.open("images/customer_information.jpg").resize((info_window.winfo_screenwidth(), info_window.winfo_screenheight()))
        image_obj = ImageTk.PhotoImage(img)
        
        transaction_label = Label(info_window, image=image_obj)
        transaction_label.place(relwidth=1, relheight=1)


        def display_info():
            customer_id = self.cust_id

            # Query to get customer information
            info_query = f"SELECT * FROM customer WHERE CustomerID = {customer_id};"
            self.mycursor.execute(info_query)
            customer_info = self.mycursor.fetchone()

            if self.validate_password(password_entry.get()):
                # Create a treeview to display customer information
                tree = ttk.Treeview(info_window)
                tree["columns"] = ("Attribute", "Value")
                tree.column("#0", width=0, stretch=NO)  # To hide the default column
                tree.column("Attribute", anchor=CENTER, width=150)
                tree.column("Value", anchor=CENTER, width=150)

                tree.heading("#0", text="", anchor=CENTER)
                tree.heading("Attribute", text="Attribute", anchor=CENTER)
                tree.heading("Value", text="Value", anchor=CENTER)

                attributes = ["CustomerID", "First Name", "Last Name", "Address", "Phone Number"]
                values = list(customer_info)

                for attribute, value in zip(attributes, values):
                    tree.insert("", END, values=(attribute, value))

                tree.pack(pady=20)

            else:
                messagebox.showerror("Error", "Wrong password. Please enter the correct password!")

        Label(info_window, text="Update Account Status", font=("Arial", 24, "bold"), padx=20, pady=10, bg="#d9be3b").pack(pady=20)

        # Customer ID entry
        Label(info_window, text="Enter Your Password:", font=("Arial", 16)).pack(pady=10)

        password_entry = Entry(info_window, show="*", font=("Arial", 14))
        password_entry.pack(pady=10)

        # Submit button
        Button(info_window, text="Submit", font=("Arial", 16, "bold"), command=display_info, bg="tomato", padx=20, pady=10).pack(pady=20)
        Button(info_window, text="Go Back", command=info_window.destroy, bg="darkslategray", width=15, height=2).pack(pady=10)
        info_window.mainloop()

    
    def h_t(self):
        history_window = Toplevel()
        history_window.title("Transaction History")
        history_window.geometry("{0}x{1}+0+0".format(history_window.winfo_screenwidth(), history_window.winfo_screenheight()))

        img = Image.open("images/transaction_history.jpg").resize((history_window.winfo_screenwidth(), history_window.winfo_screenheight()))
        image_obj = ImageTk.PhotoImage(img)
        
        transaction_label = Label(history_window, image=image_obj)
        transaction_label.place(relwidth=1, relheight=1)

        def display_history():
            if self.validate_password(password_entry.get()):
                # SQL query to retrieve transaction history
                query = f"SELECT TransactionID, DestinationAccountID, Amount, AssistedBy, TimeStamp FROM transaction WHERE SourceAccountID = {self.acc_id};"
                self.mycursor.execute(query)
                transactions = self.mycursor.fetchall()

                # Create a treeview to display transaction history
                tree = ttk.Treeview(history_window, columns=("TransactionID", "Destination AccountID", "Amount", "Assisted By", "Time Stamp"), show="headings", height=len(transactions), style="Treeview.Grey.Treeview")
                tree.pack(padx=10, pady=10)

                # Set column headings
                for col in ("TransactionID", "Destination AccountID", "Amount", "Assisted By", "Time Stamp"):
                    tree.heading(col, text=col)

                # Insert data into the treeview
                for i, transaction in enumerate(transactions):
                    tags = ("Treeview.White.Treeview", "Treeview.Grey.Treeview")[i % 2]
                    tree.insert("", END, values=transaction, tags=tags)

                # Configure styles for grey and white backgrounds
                tree.tag_configure("Treeview.Grey.Treeview", background="#dfdfdf")
                tree.tag_configure("Treeview.White.Treeview", background="white")

                # Center the values directly under the attributes
                for col in ("TransactionID", "Destination AccountID", "Amount", "Assisted By", "Time Stamp"):
                    tree.column(col, anchor=CENTER)

                # Adjust column width to fit content
                for col in ("TransactionID", "Destination AccountID", "Amount", "Assisted By", "Time Stamp"):
                    tree.column(col, minwidth=0, stretch=NO)
                    tree.heading(col, text=col)

                # Add a scrollbar
                scrollbar = ttk.Scrollbar(history_window, orient=VERTICAL, command=tree.yview)
                scrollbar.pack(side=RIGHT, fill=Y)

                tree.config(yscrollcommand=scrollbar.set)

            else:
                messagebox.showerror("Error", "Wrong password. Please enter the correct password!")

        Label(history_window, text="Update Account Status", font=("Arial", 24, "bold"), padx=20, pady=10, bg="#5585e6").pack(pady=20)

        # Password entry
        Label(history_window, text="Enter Your Password:", font=("Arial", 16)).pack(pady=10)

        password_entry = Entry(history_window, show="*", font=("Arial", 14))
        password_entry.pack(pady=10)

        # Submit button
        Button(history_window, text="Submit", font=("Arial", 16, "bold"), command=display_history, bg="tomato", padx=20, pady=10).pack(pady=20)
        Button(history_window, text="Go Back", command=history_window.destroy, bg="darkslategray", width=15, height=2).pack(pady=10)
        history_window.mainloop()
    
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


class Employee(tk.Tk):
    def __init__(self, mydb, mycursor, emp_id, role_id):
        self.mycursor = mycursor
        self.mydb = mydb
        self.emp_id = emp_id
        self.role_id = role_id
        super().__init__()
        self.title("Employee Actions")

        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))  # Full screen

        # Add main heading
        Label(self, text="Employee Actions", font=("Arial", 24, "bold"), padx=20, pady=10, bg="lightgreen").pack(pady=20)

        role_label = Label(self, text="Employee Role: System Administrator", font=("Arial", 12, ))
        role_label.pack(pady=10)

        # Add buttons with simple colors
        update_customer_info_button = Button(self, text="Update Customer Info", font=("Arial", 16), bg="lightgreen", padx=20, pady=10,command=self.update_cust)
        update_account_status_button = Button(self, text="Update Account Status", font=("Arial", 16), bg="lightgreen", padx=20, pady=10,command=self.update_account_status)
        loan_approval_button = Button(self, text="Loan Approval", font=("Arial", 16), bg="lightgreen", padx=20, pady=10,command=self.loan_click)
        dismiss_employee_button = Button(self, text="Dismiss Employee", font=("Arial", 16), bg="lightgreen", padx=20, pady=10,command=self.dismiss_employee)
        show_info_button = Button(self, text="Show Info", font=("Arial", 16), bg="lightgreen", padx=20, pady=10,command=self.employee_info)
        assisted_trans_button = Button(self, text="Show Assisted Transactions", font=("Arial", 16), bg="lightgreen", padx=20, pady=10,command=self.assis_trans)
        update_customer_info_button.pack(pady=20)
        update_account_status_button.pack(pady=20)
        loan_approval_button.pack(pady=20)
        dismiss_employee_button.pack(pady=20)
        show_info_button.pack(pady=20)
        assisted_trans_button.pack(pady=20)

        if self.role_id == 1:
            loan_approval_button.pack_forget()
            dismiss_employee_button.pack_forget()
            role_label.config(text="Employee Role: Customer Service Representative")

        if self.role_id == 2:
            update_customer_info_button.pack_forget()
            update_account_status_button.pack_forget()
            dismiss_employee_button.pack_forget()
            role_label.config(text="Employee Role: Loan Officer")

        if self.role_id == 3:
            loan_approval_button.pack_forget()
            role_label.config(text="Employee Role: Branch Manager")

    def update_cust(self):
        def submit_update():
            cust_id = cust_id_entry.get()
            check_to_query = f"SELECT * FROM customer WHERE CustomerID = {cust_id};"
            self.mycursor.execute(check_to_query)
            cust_exists = self.mycursor.fetchone()
            if cust_exists:
                cust_id = cust_id_entry.get()
                selected_attribute = attribute_var.get()
                new_value = new_value_entry.get()
                table_name = "customer"
                sql_statement = f"UPDATE {table_name} SET {selected_attribute}='{new_value}' WHERE CustomerID={cust_id}"
                self.mycursor.execute(sql_statement)
                self.mydb.commit()
                print(f"Executing SQL statement: {sql_statement}")
                messagebox.showinfo("Success", f"Attribute {selected_attribute} updated, Successfully")
            else:
                messagebox.showerror("Error", "Invalid CustomerID. Please check and try again.")


        update_window = Toplevel()
        update_window.title("Update Customer Info")
        update_window.geometry("{0}x{1}+0+0".format(update_window.winfo_screenwidth(), update_window.winfo_screenheight()))  # Full screen

        img = Image.open("images/update_customer_information (1).jpg").resize((update_window.winfo_screenwidth(), update_window.winfo_screenheight()))
        image_obj = ImageTk.PhotoImage(img)
        
        transaction_label = Label(update_window, image=image_obj)
        transaction_label.place(relwidth=1, relheight=1)


        # Add main heading
        Label(update_window, text="Update Customer Information", font=("Arial", 24, "bold"), padx=20, pady=10, bg="lightblue").pack(pady=20)

        # Customer ID entry
        Label(update_window, text="Enter Customer ID:", font=("Arial", 16), padx=0, pady=0).pack()

        cust_id_entry = Entry(update_window, font=("Arial", 14))
        cust_id_entry.pack(pady=10)

        # Dropdown for attribute selection
        Label(update_window, text="Select Attribute to Update:", font=("Arial", 16), padx=0, pady=0).pack()

        attributes = ["Fname", "Lname", "Address", "PhoneNo"]
        attribute_var = StringVar(update_window)
        attribute_var.set(attributes[0])  # default value

        attribute_dropdown = ttk.Combobox(update_window, textvariable=attribute_var, values=attributes, font=("Arial", 14))
        attribute_dropdown.pack(pady=10)

        # Entry for new value
        Label(update_window, text="Enter New Value:", font=("Arial", 16), padx=0, pady=0).pack()

        new_value_entry = Entry(update_window, font=("Arial", 14))
        new_value_entry.pack(pady=10)

        # Submit button
        Button(update_window, text="Submit", font=("Arial", 16, "bold"), command=submit_update, bg="skyblue", padx=20, pady=10).pack(pady=20)

        update_window.mainloop()

    
    def update_account_status(self):
        update_status_window = Toplevel()
        update_status_window.title("Update Account Status")
        update_status_window.geometry("{0}x{1}+0+0".format(update_status_window.winfo_screenwidth(), update_status_window.winfo_screenheight()))  # Full screen
        
        img = Image.open("images/update_account_status.jpg").resize((update_status_window.winfo_screenwidth(), update_status_window.winfo_screenheight()))
        image_obj = ImageTk.PhotoImage(img)
        
        transaction_label = Label(update_status_window, image=image_obj)
        transaction_label.place(relwidth=1, relheight=1)

        # Function to fetch the current account status from the database
        def get_account_status():
            try:
                account_id = account_id_entry.get()
                self.mycursor.execute("SELECT status FROM account WHERE accountid = %s", (account_id,))
                result = self.mycursor.fetchone()
                return result[0] if result else None
            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch account status: {e}")
                return None

        # Function to update account status in the database
        def update_account_status(new_status):
            try:
                account_id = account_id_entry.get()
                self.mycursor.execute("UPDATE account SET status = %s WHERE accountid = %s", (new_status, account_id))
                self.mydb.commit()
                messagebox.showinfo("Success", f"Account {account_id} status updated to {new_status}")
                update_buttons()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update account status: {e}")
        
        def submit_status():
            current_status = get_account_status()
            status_label.config(text=f"Current account Status: {current_status}")
            update_buttons()

        # Function to handle button click events
        def activate_button_click():
            update_account_status("active")

        def deactivate_button_click():
            update_account_status("deactivated")

        def close_button_click():
            update_account_status("closed")

        # Function to update buttons based on the current account status
        def update_buttons():
            current_status = get_account_status()
            activate_button.config(state=tk.NORMAL if current_status == "deactivated" else tk.DISABLED)
            deactivate_button.config(state=tk.NORMAL if current_status == "active" else tk.DISABLED)
            close_button.config(state=tk.NORMAL if current_status == "active" else tk.DISABLED)
            status_label.config(text=f"Current account Status: {get_account_status()}")
            if current_status == "active":
                status_label.config(background="green")
            elif current_status == "deactivated":
                status_label.config(background="red")
            else:
                status_label.config(background="grey")

        Label(update_status_window, text="Update Account Status", font=("Arial", 24, "bold"), padx=20, pady=10, bg="yellow").pack(pady=20)

        Label(update_status_window, text="Enter the account id:", font=("Arial", 16)).pack(pady=10)
        # Entry widget for Account ID
        account_id_entry = ttk.Entry(update_status_window)
        account_id_entry.pack(pady=10)

        Button(update_status_window, text="Submit", font=("Arial", 16, "bold"), command=submit_status, bg="tomato", padx=20, pady=10).pack(pady=20)

        # Label to display current account status
        status_label = Label(update_status_window, text=f"Current account Status: {get_account_status()}")
        status_label.pack(pady=10)

        # Buttons for different operations based on the account status
        activate_button = Button(update_status_window, font=("Arial", 14, ), text="Activate", command=activate_button_click, padx=15, pady=7, state=tk.DISABLED)
        activate_button.pack(padx=5)

        deactivate_button = Button(update_status_window, font=("Arial", 14, ), text="Deactivate", command=deactivate_button_click, padx=15, pady=7, state=tk.DISABLED)
        deactivate_button.pack(padx=5)

        close_button = Button(update_status_window, font=("Arial", 14, ), text="Close", command=close_button_click, padx=15, pady=7, state=tk.DISABLED)
        close_button.pack(padx=5)

        # Initial update of buttons
        update_buttons()

        update_status_window.mainloop()
        

    def loan_click(self):
        loan_window = Toplevel()
        loan_window.title("Loan Information")
        loan_window.geometry("{0}x{1}+0+0".format(loan_window.winfo_screenwidth(), loan_window.winfo_screenheight()))

        img = Image.open("images/loan_approval.png").resize((loan_window.winfo_screenwidth(), loan_window.winfo_screenheight()))
        image_obj = ImageTk.PhotoImage(img)
        
        transaction_label = Label(loan_window, image=image_obj)
        transaction_label.place(relwidth=1, relheight=1)

        def submit_loan():
            loan_id = loan_id_entry.get()

            # Query to get loan status
            status_query = f"SELECT ApprovalStatus FROM loan WHERE LoanId = {loan_id};"
            self.mycursor.execute(status_query)
            status_result = self.mycursor.fetchone()

            # Clear previous status and approval buttons
            status_label.config(text="", font=("Arial", 14), bg="lightgray", relief="solid", padx=10, pady=5)
            approve_button.pack_forget()
            reject_button.pack_forget()

            if status_result:
                loan_status = status_result[0]

                # Display loan status in a box
                status_label.config(text=f"Loan Status: {loan_status}", font=("Arial", 14), bg="lightgray", relief="solid", padx=10, pady=5)
                status_label.pack()

                # If status is 'pending', show approval buttons
                if loan_status == 'pending':
                    approve_button.pack(pady=10, padx=10, anchor=CENTER)
                    reject_button.pack(pady=10, padx=10, anchor=CENTER)
            else:
                messagebox.showerror("Error", f"Loan with ID {loan_id} not found.")
                loan_window.destroy()

        def approve_loan():
            loan_id = loan_id_entry.get()

            # Update ApprovalStatus to 'approved'
            update_query = f"UPDATE loan SET ApprovalStatus = 'approved', employeeid = {self.emp_id} WHERE LoanId = {loan_id};"
            self.mycursor.execute(update_query)
            self.mydb.commit()

            messagebox.showinfo("Success", f"Loan with ID {loan_id} approved successfully.")
            loan_window.destroy()

        def reject_loan():
            loan_id = loan_id_entry.get()

            # Update ApprovalStatus to 'rejected'
            update_query = f"UPDATE loan SET ApprovalStatus = 'rejected', employeeid = {self.emp_id} WHERE LoanId = {loan_id};"
            self.mycursor.execute(update_query)
            self.mydb.commit()

            messagebox.showinfo("Success", f"Loan with ID {loan_id} rejected successfully.")
            loan_window.destroy()

        Label(loan_window, text="Loan Approval", font=("Arial", 24, "bold"), padx=20, pady=10, bg="orange").pack(pady=20)

        # Loan ID entry
        Label(loan_window, text="Enter Loan ID:", font=("Arial", 16)).pack(pady=10)

        loan_id_entry = Entry(loan_window, font=("Arial", 14))
        loan_id_entry.pack(pady=10)

        # Submit button
        Button(loan_window, text="Submit", font=("Arial", 16), command=submit_loan, bg="tomato", padx=20, pady=10).pack(pady=20)

        # Loan status label (initially hidden)
        status_label = Label(loan_window, text="", font=("Arial", 14), bg="lightgray", relief="solid", padx=10, pady=5)

        # Approval buttons (initially hidden)
        approve_button = Button(loan_window, text="Approve", font=("Arial", 16), command=approve_loan, bg="green", padx=20, pady=10)
        reject_button = Button(loan_window, text="Reject", font=("Arial", 16), command=reject_loan, bg="red", padx=20, pady=10)

        loan_window.mainloop()


    def dismiss_employee(self):
        def submit_dismiss():
            emp_id = emp_id_entry.get()

            # Check if the employee exists before attempting dismissal
            check_query = f"SELECT * FROM employee WHERE EmployeeId = {emp_id};"
            self.mycursor.execute(check_query)
            emp_exists = self.mycursor.fetchone()

            if emp_exists:
                try:
                    # Check if the employee is a branch manager
                    if emp_exists[4] == 3 or emp_exists[4] == 4:
                        messagebox.showerror("Error", "Branch Managers and System Administrators cannot be dismissed.")
                    elif emp_exists[6] == "dismissed":
                        messagebox.showerror("Error", f"employee {emp_id} is already dismissed.")
                    else:
                        # Update the status attribute to "dismissed"
                        dismiss_query = f"UPDATE employee SET status = 'dismissed' WHERE EmployeeId = {emp_id};"
                        self.mycursor.execute(dismiss_query)
                        self.mydb.commit()

                        messagebox.showinfo("Success", f"Employee with ID {emp_id} dismissed successfully!")
                        dismiss_window.destroy()
                except Exception as e:
                    self.mydb.rollback()
                    messagebox.showerror("Failure", f"Failed to dismiss Employee with ID {emp_id}. Error: {str(e)}")
                    dismiss_window.destroy()
            else:
                messagebox.showerror("Failure", f"Employee with ID {emp_id} does not exist.")
                dismiss_window.destroy()

        dismiss_window = Toplevel()
        dismiss_window.title("Dismiss Employee")
        dismiss_window.geometry("{0}x{1}+0+0".format(dismiss_window.winfo_screenwidth(), dismiss_window.winfo_screenheight()))  # Full screen

        img = Image.open("images/dismiss_employee.webp").resize((dismiss_window.winfo_screenwidth(), dismiss_window.winfo_screenheight()))
        image_obj = ImageTk.PhotoImage(img)
        
        transaction_label = Label(dismiss_window, image=image_obj)
        transaction_label.place(relwidth=1, relheight=1)


        # Add main heading
        Label(dismiss_window, text="Dismiss Employee", font=("Arial", 24, "bold"), padx=20, pady=10, bg="lightcoral").pack(pady=20)

        # Employee ID entry
        Label(dismiss_window, text="Enter Employee ID:", font=("Arial", 16), padx=0, pady=0).pack()

        emp_id_entry = Entry(dismiss_window, font=("Arial", 14))
        emp_id_entry.pack(pady=10)

        # Submit button
        Button(dismiss_window, text="Submit", font=("Arial", 16, "bold"), command=submit_dismiss, bg="tomato", padx=20, pady=10).pack(pady=20)

        dismiss_window.mainloop()


    def validate_password(self, password):
        # Check if the username exists in the specified login table
        self.mycursor.execute(f"SELECT * FROM employeelogin el, employee e WHERE el.employeeid = e.employeeid and e.employeeid = %s", (self.emp_id,))
        emp_data = self.mycursor.fetchone()

        if not emp_data:
            messagebox.showinfo("Error", "Invalid username.")
            return False

        # Verify the provided password against the stored hashed password
        stored_hashed_password = emp_data[2]  # The hashed password is in the third column
        if not verify_password(password, stored_hashed_password.encode('utf-8')):
            return False

        # If both username and password are valid, return True
        return True
    
    def employee_info(self):
        info_window = Toplevel()
        info_window.title("Employee Information")
        info_window.geometry("{0}x{1}+0+0".format(info_window.winfo_screenwidth(), info_window.winfo_screenheight()))

        img = Image.open("images/employee_information.jpeg").resize((info_window.winfo_screenwidth(), info_window.winfo_screenheight()))
        image_obj = ImageTk.PhotoImage(img)
        
        transaction_label = Label(info_window, image=image_obj)
        transaction_label.place(relwidth=1, relheight=1)

        def display_info():
            emp_id = self.emp_id

            # Query to get employee information
            info_query = f"SELECT * FROM employee WHERE EmployeeID = {emp_id};"
            self.mycursor.execute(info_query)
            employee_info = self.mycursor.fetchone()

            if self.validate_password(password_entry.get()):
                # Create a treeview to display employee information
                tree = ttk.Treeview(info_window)
                tree["columns"] = ("Attribute", "Value")
                tree.column("#0", width=0, stretch=NO)  # To hide the default column
                tree.column("Attribute", anchor=CENTER, width=150)
                tree.column("Value", anchor=CENTER, width=150)

                tree.heading("#0", text="", anchor=CENTER)
                tree.heading("Attribute", text="Attribute", anchor=CENTER)
                tree.heading("Value", text="Value", anchor=CENTER)

                attributes = ["Employee ID", "First Name", "Last Name", "Salary","Role ID","Branch ID"]
                values = list(employee_info)

                for attribute, value in zip(attributes, values):
                    tree.insert("", END, values=(attribute, value))

                tree.pack(pady=20)

            else:
                messagebox.showerror("Error", "Wrong password. Please enter the correct password!")

        # employee ID entry
        Label(info_window, text="Employee Information", font=("Arial", 24, "bold"), padx=20, pady=10, bg="violet").pack(pady=20)

        Label(info_window, text="Enter Your Password:", font=("Arial", 16)).pack(pady=10)

        password_entry = Entry(info_window, show="*", font=("Arial", 14))
        password_entry.pack(pady=10)

        # Submit button
        Button(info_window, text="Submit", font=("Arial", 16, "bold"), command=display_info, bg="tomato", padx=20, pady=10).pack(pady=20)
        Button(info_window, text="Go Back", command=info_window.destroy, bg="darkslategray", width=15, height=2).pack(pady=10)
        info_window.mainloop()


    def assis_trans(self):
        history_window = Toplevel()
        history_window.title("Assisted Transaction")
        history_window.geometry("{0}x{1}+0+0".format(history_window.winfo_screenwidth(), history_window.winfo_screenheight()))

        img = Image.open("images/assist_transaction.jpeg").resize((history_window.winfo_screenwidth(), history_window.winfo_screenheight()))
        image_obj = ImageTk.PhotoImage(img)
        
        transaction_label = Label(history_window, image=image_obj)
        transaction_label.place(relwidth=1, relheight=1)

        def display_history():
            emp_id = self.emp_id
            if self.validate_password(password_entry.get()):
                # SQL query to retrieve assist history
                query = f"SELECT TransactionID, SourceAccountID, DestinationAccountID, Amount, TimeStamp FROM transaction WHERE AssistedBy = {emp_id};"
                self.mycursor.execute(query)
                transactions = self.mycursor.fetchall()

                # Create a treeview to display assist history
                tree = ttk.Treeview(history_window, columns=("Transaction_ID", "Source_Account_ID", "Destination_AccountID", "Amount", "Time_Stamp"), show="headings", height=len(transactions))
                tree.pack(padx=10, pady=10)

                # Set column headings
                for col in ("Transaction_ID", "Source_Account_ID", "Destination_AccountID", "Amount", "Time_Stamp"):
                    tree.heading(col, text=col)

                # Insert data into the treeview
                # Insert data into the treeview with alternating background colors
                for i, transaction in enumerate(transactions):
                    tags = ("Treeview.Grey.Treeview", "Treeview.White.Treeview")[i % 2]
                    tree.insert("", END, values=transaction, tags=tags)

                # Configure styles for grey and white backgrounds
                tree.tag_configure("Treeview.Grey.Treeview", background="#dfdfdf")
                tree.tag_configure("Treeview.White.Treeview", background="white")


                # Center the values directly under the attributes
                for col in ("Transaction_ID", "Source_Account_ID", "Destination_AccountID", "Amount", "Time_Stamp"):
                    tree.column(col, anchor=CENTER)

                # Adjust column width to fit content
                for col in ("Transaction_ID", "Source_Account_ID", "Destination_AccountID", "Amount", "Time_Stamp"):
                    tree.column(col, minwidth=0, stretch=NO)
                    tree.heading(col, text=col)

                # Add a scrollbar
                scrollbar = ttk.Scrollbar(history_window, orient=VERTICAL, command=tree.yview)
                scrollbar.pack(side=RIGHT, fill=Y)

                tree.config(yscrollcommand=scrollbar.set)
                
            else:
                messagebox.showerror("Error", "Wrong password. Please enter the correct password!")

        Label(history_window, text="Show Assisted Trasactions", font=("Arial", 24, "bold"), padx=20, pady=10, bg="lightblue").pack(pady=20)

        # Password entry
        Label(history_window, text="Enter Your Password:", font=("Arial", 16)).pack(pady=10)

        password_entry = Entry(history_window, show="*" ,font=("Arial", 14))
        password_entry.pack(pady=10)

        # Submit button
        Button(history_window, text="Submit", font=("Arial", 16, "bold"), command=display_history, bg="tomato", padx=20, pady=10).pack(pady=20)
        Button(history_window, text="Go Back", command=history_window.destroy, bg="darkslategray", width=15, height=2).pack(pady=10)
        history_window.mainloop()

    

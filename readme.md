# Banking Management System

The Banking Management System is a comprehensive project that uses MySQL as the database management system and Tkinter for the graphical user interface.

## Features

- **Customer Actions:**
  - Transaction: Transfer money between accounts.
  - Withdraw: Withdraw money from an account.
  - Deposit: Deposit money into an account.
  - Request for Loan: Customers can request loans; approval required.
  - Show Customer Information: View details about a customer.
  - Show Transaction History: View transaction history for each account.

- **Employee Actions:**
  - Update Customer Information: Modify customer details.
  - Update Account Status: Change account status (Active, Deactivated, Closed).
  - Loan Approval: Approve or reject loan requests.
  - Dismiss Employee: Terminate employment.
  - Show Employee Details: Display information about an employee.
  - Show Assisted Transaction History: View transaction history assisted by an employee.

- **Employee Roles:**
  - **Customer Service Representative/Teller:**
    - Actions Allowed: Everything except loan approval and employee dismissal.

  - **Loan Officer:**
    - Actions Allowed: Loan approval, Show Employee Details, Show Assisted Transaction History.

  - **Branch Manager:**
    - Actions Allowed: All actions except loan approval.

  - **System Administrators (Developers):**
    - Actions Allowed: All actions.
    - Note: Only two system administrators (developers) in the database.

- **Security and Error Management:**
  - Implement secure authentication mechanisms.
  - Protect sensitive information, such as passwords.
  - Handle errors gracefully to ensure a smooth user experience.


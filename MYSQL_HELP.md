# MySQL Setup Guide

I've updated the code, but the database connection is failing because the MySQL server is not running or the password is incorrect.

### Step 1: Start MySQL
1.  Open **Windows Services** (search for "Services" in the Start menu).
2.  Find **MySQL80** (or similar) in the list.
3.  Right-click it and select **Start**.

### Step 2: Update Credentials
1.  Open the file: `backend/.env`
2.  Change `your_password` to your actual MySQL root password.
3.  If you haven't set a password, leave it empty: `MYSQL_PASSWORD=`

### Step 3: Run the Server
Once you've done the above, I will be able to start the server successfully. You will then see the tables appear in **MySQL Workbench**!

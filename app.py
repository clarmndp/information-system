import tkinter as tk
from tkinter import messagebox
import mariadb

# function to connect to the database
def connect_db(user_type):
    if user_type == "admin":
        user = "admin_user"
        password = "admin_password"
    elif user_type == "casual":
        user = "casual_user"
        password = "casual_password"
    else:
        raise ValueError("Invalid user type")

    try:
        conn = mariadb.connect(
            user= user,
            password= password,
            host="localhost",
            port=3306,
            database="food"
        )
        return conn
    except mariadb.Error as e:
        messagebox.showerror("Database Connection Error", f"Error connecting to MariaDB Platform: {e}")
        return None


#Login Page
    #verify if user id admin or casual (usertype)
    admin_conn = connect_db("admin")
    casual_conn = connect_db("casual")

#Features
    #add your features here



# Tkinter application
root = tk.Tk()
root.title("Food Information System")

root.mainloop()
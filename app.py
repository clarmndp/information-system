import tkinter as tk
from tkinter import messagebox
from tkinter import *
import mariadb

# function to connect to the database
def connect_db(user_type):
    if user_type == "admin":
        user = "foodie"
        password = "chefP!"
    elif user_type == "casual":
        user = "pares"
        password = "diwataP"
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
        messagebox.showinfo("Database Connection", f"Successfully connected to the database as {user_type}.")
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

name_var = tk.StringVar()
passw_var = tk.StringVar()

def submit():
    name = name_var.get()
    password = passw_var.get()
    print("The name is : " + name)
    print("The password is : " + password)
    name_var.set("")
    passw_var.set("")

    if name == 'foodie' and password == 'chefP!':
        admin = connect_db("admin")
    if name == 'pares' and password == 'diwataP':
        casual_conn = connect_db("casual")

# Login Page
myLabel = Label(root, text="LogIn", font=('calibre', 10, 'bold'))
myLabel.grid(row=0, column=0, columnspan=2, pady=10)

name_label = tk.Label(root, text='Username', font=('calibre', 10, 'bold'))
name_entry = tk.Entry(root, textvariable=name_var, font=('calibre', 10, 'normal'))

passw_label = tk.Label(root, text='Password', font=('calibre', 10, 'bold'))
passw_entry = tk.Entry(root, textvariable=passw_var, font=('calibre', 10, 'normal'), show='*')

sub_btn = tk.Button(root, text='Submit', command=submit)

name_label.grid(row=1, column=0, pady=5)
name_entry.grid(row=1, column=1, pady=5)
passw_label.grid(row=2, column=0, pady=5)
passw_entry.grid(row=2, column=1, pady=5)
sub_btn.grid(row=3, column=1, pady=10)


root.mainloop()
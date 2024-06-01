import tkinter as tk
from tkinter import *
from tkinter import messagebox
import mariadb

# function to connect to the MariaDB database
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

#Features
    #add your features here


# Tkinter application
root = tk.Tk()
root.title("Food Information System")

#function to perform SELECT statements
def execute_query():
    query = queryEntry.get()
    conn = connect_db("admin")
    if conn:
        cur = conn.cursor()
        try:
            cur.execute(query)
            if query.lower().startswith("select"):
                results = cur.fetchall()
                print(results)
                resultText.delete(1.0, tk.END)
                for row in results:
                    resultText.insert(tk.END, f"{row}\n")
            else:
                conn.commit()
                messagebox.showinfo("Success", "Query executed successfully.")
        except mariadb.Error as e:
            messagebox.showerror("Query Error", f"Error executing query: {e}")
        finally:
            conn.close()


name_var = tk.StringVar()
passw_var = tk.StringVar()

#function to submit user credentials to establish mariadb connection
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

#username
name_label = tk.Label(root, text='Username', font=('calibre', 10, 'bold'))
name_entry = tk.Entry(root, textvariable=name_var, font=('calibre', 10, 'normal'))

#password
passw_label = tk.Label(root, text='Password', font=('calibre', 10, 'bold'))
passw_entry = tk.Entry(root, textvariable=passw_var, font=('calibre', 10, 'normal'), show='*')

sub_btn = tk.Button(root, text='Submit', command=submit)

#styling 
name_label.grid(row=1, column=0, pady=5)
name_entry.grid(row=1, column=1, pady=5)
passw_label.grid(row=2, column=0, pady=5)
passw_entry.grid(row=2, column=1, pady=5)
sub_btn.grid(row=3, column=1, pady=10)

#Reports
queryLabel = tk.Label(root, text="Enter SQL SELECT query to be generated:")
queryLabel.grid(pady=10)

#Reports - SELECT statements input field
queryEntry = tk.Entry(root, width=50)
queryEntry.grid(pady=10)
#Reports - execute SELECT statements to generate reports
queryButton = tk.Button(root, text="Show Reports", command=execute_query)
queryButton.grid(pady=10)

#Reports - display reports in a text field
resultText = tk.Text(root, height=15, width=80)
resultText.grid(pady=10)

root.mainloop()
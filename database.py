import tkinter as tk
import mariadb

#connect to mariadb server
def connect_db():
    try:
        conn = mariadb.connect(
            user="insert_username_here",
            password="insert_password_here",
            host="localhost",
            port=3306,
            database="insert_database_here"
        )
        return conn
    except mariadb.Error as e:
        messagebox.showerror("Database Connection Error", f"Error connecting to MariaDB Platform: {e}")
        return None

#Features
    #deploy database functionalities here


# Tkinter app
root = tk.Tk()
root.title("Food Information System")
root.geometry("400x400")
root.mainloop()
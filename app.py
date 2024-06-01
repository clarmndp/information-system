import tkinter as tk
from tkinter import *
from tkinter import messagebox
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
        return conn
    except mariadb.Error as e:
        messagebox.showerror("Database Connection Error", f"Error connecting to MariaDB Platform: {e}")
        return None


#Login Page
    #verify if user id admin or casual (usertype)

#Features
    #add your features here

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

# Tkinter application
root = tk.Tk()
root.title("Food Information System")

queryLabel = tk.Label(root, text="Enter the reports you want to view:")
queryLabel.pack(pady=10)

queryEntry = tk.Entry(root, width=50)
queryEntry.pack(pady=10)

queryButton = tk.Button(root, text="Show", command=execute_query)
queryButton.pack(pady=10)

resultText = tk.Text(root, height=15, width=80)
resultText.pack(pady=10)

root.mainloop()
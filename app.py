import tkinter as tk
from tkinter import *
from tkinter import messagebox
import mariadb

#MariaDB connection variable to be used for SQL commands
dbConn = None

# function to connect to the MariaDB database
def connect_db(user_type):
    global dbConn
    if user_type == "Admin":
        user = "foodie"
        password = "chefP!"
    elif user_type == "Casual":
        user = "pares"
        password = "diwataP"
    else:
        raise ValueError("Invalid user type")

    try:
        dbConn = mariadb.connect(
            user = user,
            password = password,
            host = "localhost",
            port = 3306,
            database = "food"
        )
        messagebox.showinfo("Database Connection", f"Successfully connected to the database as {user_type}.")
    except mariadb.Error as e:
        messagebox.showerror("Database Connection Error", f"Error connecting to MariaDB Platform: {e}")
        dbConn = None
    

#function to determine if user credentials is admin/user to establish mariadb connection
def loginConn(username, password): 
    if username == 'foodie' and password == 'chefP!':
        connect_db("Admin")
        return AdminPage
    elif username == 'pares' and password == 'diwataP':
        connect_db("Casual")
        return CasualPage
    else:
        messagebox.showerror("Login Error", "Invalid username or password")
        return None


#GUI Main Page Frame
class tkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs): 
         
        tk.Tk.__init__(self, *args, **kwargs)
         
        mainContainer = tk.Frame(self)  
        mainContainer.pack(side = "top", fill = "both", expand = True) 
  
        mainContainer.grid_rowconfigure(0, weight = 1)
        mainContainer.grid_columnconfigure(0, weight = 1)
  
        self.frames = {}  

        for F in (LoginPage, AdminPage, CasualPage):
  
            frame = F(mainContainer, self)
  
            #initialized pages/ frames to be displayed in container
            self.frames[F] = frame 
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(LoginPage)
  
    #display the current frame passed as parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Login Page
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #login credentials
        self.name_var = tk.StringVar()
        self.passw_var = tk.StringVar()

        #page title label
        loginLabel = tk.Label(self, text="Bite Bank", font=('calibre', 10, 'bold'))
        loginLabel.grid(row=0, column=0, columnspan=2, pady=10)

        #username
        nameLabel = tk.Label(self, text='Username', font=('calibre', 10, 'bold'))
        nameLabel.grid(row=1, column=0, pady=5)
        nameEntry = tk.Entry(self, textvariable = self.name_var, font=('calibre', 10, 'normal'))
        nameEntry.grid(row=1, column=1, pady=5)

        #password
        passLabel = tk.Label(self, text='Password', font=('calibre', 10, 'bold'))
        passLabel.grid(row=2, column=0, pady=5)
        passEntry = tk.Entry(self, textvariable = self.passw_var, font=('calibre', 10, 'normal'), show='*')
        passEntry.grid(row=2, column=1, pady=5)  
        
        #function to rooute user to admin page or casual page
        def directClientToPage():
            name = self.name_var.get()
            password = self.passw_var.get()
            userType = loginConn(name, password)
            if userType:
                controller.show_frame(userType)

        submitBtn = tk.Button(self, text='Submit', command=directClientToPage)
        submitBtn.grid(row=3, column=1, pady=10)

class AdminPage(tk.Frame):  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # self.estabId = tk.IntVar()
        self.estabLoc = tk.StringVar()
        self.estabRating = tk.IntVar()
        self.estabName = tk.StringVar()

        # addEstabIdText = tk.Label(self, text="Enter food establishment ID:")
        # # addEstabIdText.grid(pady=10)
        # addEstabIdEntry = tk.Entry(self, textvariable=self.estabId, width=50)
        # addEstabIdEntry.grid(pady=10)

        addEstabLocText = tk.Label(self, text="Enter food establishment Location:")
        addEstabLocText.grid(pady=10)
        addEstabLocEntry = tk.Entry(self, textvariable=self.estabLoc, width=50)
        addEstabLocEntry.grid(pady=10)

        addEstabRatingText = tk.Label(self, text="Enter food establishment rating:")
        addEstabRatingText.grid(pady=10)
        addEstabRatingEntry = tk.Entry(self, textvariable=self.estabRating, width=50)
        addEstabRatingEntry.grid(pady=10)

        addEstabNameText = tk.Label(self, text="Enter food establishment name:")
        addEstabNameText.grid(pady=10)
        addEstabNameEntry = tk.Entry(self, textvariable=self.estabName, width=50)
        addEstabNameEntry.grid(pady=10)

        addEstablishmentButton = tk.Button(self, text="Add Food Establishment", command=self.addEstablishment)
        addEstablishmentButton.grid(pady=10)

    # Function for adding the food establishment to the MariaDB
    def addEstablishment(self):
        # id = self.estabId.get()
        loc = self.estabLoc.get()
        rate = self.estabRating.get()
        name = self.estabName.get()
        if dbConn:
            query = 'INSERT INTO food_establishment VALUES (NULL,%s,%d,%s)'
            items = (loc, rate, name)
            cur = dbConn.cursor()
            try:
                cur.execute(query, items)
                dbConn.commit()
                messagebox.showinfo("Success", "Food establishment added successfully.")
            except mariadb.Error as e:
                messagebox.showerror("Query Error", f"Error executing query: {e}")
            finally:
                cur.close()
        else:
            messagebox.showerror("Database Error", "No database connection established.")

  
class CasualPage(tk.Frame):  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #add your features here


#Tkinter application
root = tkinterApp()
root.title("Bite Bank")
root.mainloop()
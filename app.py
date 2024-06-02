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

        for F in (LoginPage, AdminPage, CasualPage, AddFoodEstablishment, DeleteFoodEstablishment, EditFoodEstablishment, ReportsPage, FoodItemAdd,FoodItemEdit,FoodItemDelete, 
        ViewItemEstablishment, ViewItemBasedType):
  
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

          # show add text and add button
        textVar = tk.StringVar()
        textVar.set("ADD")

        addSomethingLabel = tk.Label(self,textvariable=textVar)
        addSomethingLabel.grid(row=0, column=1, columnspan=2, pady=10)
        #addSomethingLabel.pack()

        itemAddButton = tk.Button(self, text="Item", command=lambda: controller.show_frame(FoodItemAdd))
        itemAddButton.grid(row=1, column=1, pady=5, padx=10)
        #itemAddButton.pack(row=0, column=0,pady=15)

        establishmentAddButton = tk.Button(self, text="Establishment", command=lambda: controller.show_frame(AddFoodEstablishment))
        establishmentAddButton.grid(row=1, column=2, pady=5, padx=10)
        #establishmentAddButton.pack(pady=15)

        # show update text and update button
        textVar2 = tk.StringVar()
        textVar2.set("UPDATE")

        updateSomethingLabel = tk.Label(self,textvariable=textVar2)
        updateSomethingLabel.grid(row=2, column=1, columnspan=2, pady=10)

        itemEditButton = tk.Button(self, text="Item", command=lambda: controller.show_frame(FoodItemEdit))
        itemEditButton.grid(row=3, column=1, pady=5, padx=10)

        establishmentEditButton = tk.Button(self, text="Establishment", command=lambda: controller.show_frame(EditFoodEstablishment))
        establishmentEditButton.grid(row=3, column=2,  pady=5, padx=10)
        # show delete text and delete button
        textVar3 = tk.StringVar()
        textVar3.set("DELETE")

        deleteSomethingLabel = tk.Label(self,textvariable=textVar3)
        deleteSomethingLabel.grid(row=4, column=1, columnspan=2, pady=10)

        itemDeleteButton = tk.Button(self, text="Item", command=lambda: controller.show_frame(FoodItemDelete))
        itemDeleteButton.grid(row=5, column=1, pady=5, padx=10)

        establishmentDeleteButton = tk.Button(self, text="Establishment", command=lambda: controller.show_frame(DeleteFoodEstablishment))
        establishmentDeleteButton.grid(row=5, column=2, pady=5, padx=10)

        reportsLabel = tk.Label(self, text='Reports', font=('calibre', 10, 'bold'))
        reportsLabel.grid(row=6, column=0, pady=5)
        reportsBtn = tk.Button(self, text = 'Go', command=lambda: controller.show_frame(ReportsPage))
        reportsBtn.grid(row=6, column=1, columnspan=2, pady=5)

  
class AddFoodEstablishment(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.estabLoc = tk.StringVar()
        self.estabRating = tk.IntVar()
        self.estabName = tk.StringVar()

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
        
        itemReturnButton = tk.Button(self, text="Return", command=lambda: controller.show_frame(AdminPage))
        itemReturnButton.grid(pady=10)

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


class EditFoodEstablishment(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.toUpdate = tk.StringVar()
        self.newValue = tk.StringVar()
        self.estabID = tk.IntVar()

        editToUpdateText = tk.Label(self, text="What will you change? (establishment_name, location, rating) ")
        editToUpdateText.grid(pady=10)
        editToUpdateEntry = tk.Entry(self, textvariable=self.toUpdate, width=50)
        editToUpdateEntry.grid(pady=10)

        editNewValueText = tk.Label(self, text="Enter new Value.")
        editNewValueText.grid(pady=10)
        editNewValueEntry = tk.Entry(self, textvariable=self.newValue, width=50)
        editNewValueEntry.grid(pady=10)

        estabIDText = tk.Label(self, text="From what establishment ID?")
        estabIDText.grid(pady=10)
        editItemIDEntry = tk.Entry(self, textvariable=self.estabID, width=50)
        editItemIDEntry.grid(pady=10)

        addItemButton = tk.Button(self, text="Edit Food Item", command=self.editItem)
        addItemButton.grid(pady=10)

        itemReturnButton = tk.Button(self, text="Return", command=lambda: controller.show_frame(AdminPage))
        itemReturnButton.grid(pady=10)

    def editItem(self):

        toUpdate = self.toUpdate.get()
        newValue = self.newValue.get()
        estabID = self.estabID.get()

        if dbConn:
            query = f'UPDATE food_establishment SET {toUpdate} = %s WHERE establishment_id = %d'
            items = (newValue,estabID)
            cur = dbConn.cursor()
            try:
                cur.execute(query, items)
                dbConn.commit()
                messagebox.showinfo("Success", "Food Establishment edited successfully.")
            except mariadb.Error as e:
                messagebox.showerror("Query Error", f"Error executing query: {e}")
            finally:
                cur.close()
        else:
            messagebox.showerror("Database Error", "No database connection established.")

class DeleteFoodEstablishment(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
    
        self.estabId = tk.StringVar()
        
        deleteEstab = tk.Label(self, text="Enter food establishment ID you want to delete:")
        deleteEstab.grid(pady=10)
        estabIdEntry = tk.Entry(self, textvariable=self.estabId, width=50)
        estabIdEntry.grid(pady=10)

        deleteButton = tk.Button(self, text="Delete Food Establishment", command=self.deleteEstablishment)
        deleteButton.grid(pady=10)

        itemReturnButton = tk.Button(self, text="Return", command=lambda: controller.show_frame(AdminPage))
        itemReturnButton.grid(pady=10)

    def deleteEstablishment(self):
        estabID = self.estabId.get()
        if dbConn:
            query = f'DELETE FROM food_establishment WHERE establishment_id = {estabID}'
            cur = dbConn.cursor()
            try:
                cur.execute(query)
                dbConn.commit()
                messagebox.showinfo("Success", "Food Establishment deleted successfully.")
            except mariadb.Error as e:
                messagebox.showerror("Query Error", f"Error executing query: {e}")
            finally:
                cur.close()
        else:
            messagebox.showerror("Database Error", "No database connection established.")

class FoodItemAdd(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.itemName = tk.StringVar()
        self.itemPrice = tk.IntVar()
        self.itemFoodType = tk.StringVar()
        self.itemIngredient = tk.StringVar()
        self.itemEstabId = tk.IntVar()

        addItemNameText = tk.Label(self, text="Enter food item Name: ")
        addItemNameText.grid(pady=10)
        addItemNameEntry = tk.Entry(self, textvariable=self.itemName, width=50)
        addItemNameEntry.grid(pady=10)

        addItemPriceText = tk.Label(self, text="Enter food item Price: ")
        addItemPriceText.grid(pady=10)
        addItemPriceEntry = tk.Entry(self, textvariable=self.itemPrice, width=50)
        addItemPriceEntry.grid(pady=10)

        addItemFoodTypeText = tk.Label(self, text="Enter food item's Food Type: ")
        addItemFoodTypeText.grid(pady=10)
        addItemFoodTypeEntry = tk.Entry(self, textvariable=self.itemFoodType, width=50)
        addItemFoodTypeEntry.grid(pady=10)

        addItemIngredientText = tk.Label(self, text="Enter food item's Ingredient/s: ")
        addItemIngredientText.grid(pady=10)
        addItemIngredientEntry = tk.Entry(self, textvariable=self.itemIngredient, width=50)
        addItemIngredientEntry.grid(pady=10)

        addItemEstabIdText = tk.Label(self, text="Enter food item's Establishment ID: ")
        addItemEstabIdText.grid(pady=10)
        addItemEstabIdEntry = tk.Entry(self, textvariable=self.itemEstabId, width=50)
        addItemEstabIdEntry.grid(pady=10)

        addItemButton = tk.Button(self, text="Add Food Item", command=self.addItem)
        addItemButton.grid(pady=10)

        itemReturnButton = tk.Button(self, text="Return", command=lambda: controller.show_frame(AdminPage))
        itemReturnButton.grid(pady=10)

    #add food item to the database
    def addItem(self):
        name = self.itemName.get()
        price = self.itemPrice.get()
        type = self.itemFoodType.get()
        ingredient = self.itemIngredient.get()
        estabId = self.itemEstabId.get()
        if dbConn:
            query = 'INSERT INTO food_item (name,price,food_type,ingredient,establishment_id) VALUES (%s,%d,%s,%s,%d)'
            items = (name, price, type, ingredient, estabId)
            cur = dbConn.cursor()
            try:
                cur.execute(query, items)
                dbConn.commit()
                messagebox.showinfo("Success", "Food item added successfully.")
            except mariadb.Error as e:
                messagebox.showerror("Query Error", f"Error executing query: {e}")
            finally:
                cur.close()
        else:
            messagebox.showerror("Database Error", "No database connection established.")

class FoodItemEdit(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.toUpdate = tk.StringVar()
        self.newValue = tk.StringVar()
        self.itemID = tk.IntVar()
        
        #page title label
        adminLabel = tk.Label(self, text="Admin Dashboard", font=('calibre', 20, 'bold'))
        adminLabel.grid(row=0, column=0, columnspan=2, pady=10)
        
        editToUpdateText = tk.Label(self, text="What will you change? (name, price, food_type, ingredient, establishment_id) ")
        editToUpdateText.grid(pady=10)
        editToUpdateEntry = tk.Entry(self, textvariable=self.toUpdate, width=50)
        editToUpdateEntry.grid(pady=10)

        editNewValueText = tk.Label(self, text="Enter new Value.")
        editNewValueText.grid(pady=10)
        editNewValueEntry = tk.Entry(self, textvariable=self.newValue, width=50)
        editNewValueEntry.grid(pady=10)

        editItemIDText = tk.Label(self, text="From what item ID?")
        editItemIDText.grid(pady=10)
        editItemIDEntry = tk.Entry(self, textvariable=self.itemID, width=50)
        editItemIDEntry.grid(pady=10)

        addItemButton = tk.Button(self, text="Edit Food Item", command=self.editItem)
        addItemButton.grid(pady=10)

        itemReturnButton = tk.Button(self, text="Return", command=lambda: controller.show_frame(AdminPage))
        itemReturnButton.grid(pady=10)

    #add food item to the database
    def editItem(self):

        toUpdate = self.toUpdate.get()
        newValue = self.newValue.get()
        itemID = self.itemID.get()

        if dbConn:
            query = f'UPDATE food_item SET {toUpdate} = %s WHERE item_id = %d' # used f string to be able to embed toUpdate so no errors
            items = (newValue,itemID)
            cur = dbConn.cursor()
            try:
                cur.execute(query, items)
                dbConn.commit()
                messagebox.showinfo("Success", "Food item edited successfully.")
            except mariadb.Error as e:
                messagebox.showerror("Query Error", f"Error executing query: {e}")
            finally:
                cur.close()
        else:
            messagebox.showerror("Database Error", "No database connection established.")

class FoodItemDelete(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.itemID = tk.IntVar()

        editItemIDText = tk.Label(self, text="What is the Food Item's Id that you will delete")
        editItemIDText.grid(pady=10)
        editItemIDEntry = tk.Entry(self, textvariable=self.itemID, width=50)
        editItemIDEntry.grid(pady=10)

        addItemButton = tk.Button(self, text="Delete Food Item", command=self.deleteItem)
        addItemButton.grid(pady=10)

        itemReturnButton = tk.Button(self, text="Return", command=lambda: controller.show_frame(AdminPage))
        itemReturnButton.grid(pady=10)

    #add food item to the database
    def deleteItem(self):

        itemID = self.itemID.get()

        if dbConn:
            query = f'DELETE FROM food_item WHERE item_id = {itemID}'
            cur = dbConn.cursor()
            try:
                cur.execute(query)
                dbConn.commit()
                messagebox.showinfo("Success", "Food item deleted successfully.")
            except mariadb.Error as e:
                messagebox.showerror("Query Error", f"Error executing query: {e}")
            finally:
                cur.close()
        else:
            messagebox.showerror("Database Error", "No database connection established.")




class CasualPage(tk.Frame):  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        viewItemInEstablishment = tk.Button(self, text="View Items in a Food Establishment",command=lambda: controller.show_frame(ViewItemEstablishment))
        viewItemInEstablishment.grid(pady=10)

        viewItemFoodTypeEstablishment = tk.Button(self, text="View Items with their Food Type in a Food Establishment",command=lambda: controller.show_frame(ViewItemBasedType))
        viewItemFoodTypeEstablishment.grid(pady=10)


        


class ViewItemEstablishment(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.estabId = tk.StringVar()
        
        viewItemEstab = tk.Label(self, text="Enter food establishment ID:")
        viewItemEstab.grid(pady=10)
        estabIdEntry = tk.Entry(self, textvariable=self.estabId, width=50)
        estabIdEntry.grid(pady=10)


        def viewItems():
            estabID = self.estabId.get()

            if dbConn:
                query = f'SELECT * FROM food_item i LEFT JOIN food_establishment e ON i.establishment_id = e.establishment_id WHERE i.establishment_id = {estabID}'
                cur = dbConn.cursor()
                try:
                    cur.execute(query)
                    results = cur.fetchall()
                    reportsContainer.delete(1.0, tk.END)
                    for row in results:
                        reportsContainer.insert(tk.END, f"{row}\n")
                    dbConn.commit()
                    messagebox.showinfo("Success", "Food item fetch successfully.")
                except mariadb.Error as e:
                    messagebox.showerror("Query Error", f"Error executing query: {e}")
                finally:
                    cur.close()
            else:
                messagebox.showerror("Database Error", "No database connection established.")

        deleteButton = tk.Button(self, text="View Food Items", command=viewItems)
        deleteButton.grid(pady=10)

        #display results/reports here
        reportsContainer = tk.Text(self, height=15, width=50)
        reportsContainer.grid(pady=10)

        returnBtn = tk.Button(self, text='Return', command=lambda: controller.show_frame(CasualPage))
        returnBtn.grid(pady=10)

class ViewItemBasedType(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)

        self.estabId = tk.StringVar()
        self.foodType = tk.StringVar() 
        
        viewItemEstab = tk.Label(self, text="Enter food establishment ID:")
        viewItemEstab.grid(pady=10)
        estabIdEntry = tk.Entry(self, textvariable=self.estabId, width=50)
        estabIdEntry.grid(pady=10)

        viewItemEstab = tk.Label(self, text="Enter the type of :")
        viewItemEstab.grid(pady=10)
        estabIdEntry = tk.Entry(self, textvariable=self.foodType, width=50)
        estabIdEntry.grid(pady=10)


        def viewItems():
            estabID = self.estabId.get()
            foodType = self.foodType.get()

            if dbConn:
                query = f'SELECT * FROM food_item i LEFT JOIN food_establishment e ON i.establishment_id = e.establishment_id WHERE i.establishment_id = %s AND i.food_type=%s'
                items = (estabID, foodType)
                cur = dbConn.cursor()
                try:
                    cur.execute(query,items)
                    results = cur.fetchall()
                    reportsContainer.delete(1.0, tk.END)
                    for row in results:
                        reportsContainer.insert(tk.END, f"{row}\n")
                    dbConn.commit()
                    messagebox.showinfo("Success", "Food item fetch successfully.")
                except mariadb.Error as e:
                    messagebox.showerror("Query Error", f"Error executing query: {e}")
                finally:
                    cur.close()
            else:
                messagebox.showerror("Database Error", "No database connection established.")

        
        deleteButton = tk.Button(self, text="View Food Items", command=viewItems)
        deleteButton.grid(pady=10)

        #display results/reports here
        reportsContainer = tk.Text(self, height=15, width=50)
        reportsContainer.grid(pady=10)

        returnBtn = tk.Button(self, text='Return', command=lambda: controller.show_frame(CasualPage))
        returnBtn.grid(pady=10)
        #add your features here
class ReportsPage(tk.Frame):  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.query_var = tk.StringVar()

        #page title label
        reportsLabel = tk.Label(self, text='Reports Page', font=('calibre', 20, 'bold'))
        reportsLabel.grid(pady=10)

        #select query input
        queryLabel = tk.Label(self, text='Input SQL SELECT statements \n for reports to generate', font=('calibre', 10))
        queryLabel.grid(pady=10)
        queryEntry = tk.Entry(self, textvariable = self.query_var, width=40, font=('calibre', 10, 'normal'))
        queryEntry.grid(pady=10)
        
        def generateReport():
            query = queryEntry.get()
            # global dbConn
            if dbConn:
                cur = dbConn.cursor()
                try:
                    cur.execute(query)
                    if query.lower().startswith("select"):
                        results = cur.fetchall()
                        reportsContainer.delete(1.0, tk.END)
                        for row in results:
                            reportsContainer.insert(tk.END, f"{row}\n")
                    else:
                       dbConn.commit()
                       messagebox.showinfo("Success", "Query executed successfully.")
                except mariadb.Error as e:
                   messagebox.showerror("Query Error", f"Error executing query: {e}")
                finally:
                    cur.close()

        #execute SQL statement
        generateBtn = tk.Button(self, text='Generate Reports', command=generateReport)
        generateBtn.grid(pady=10)

        #display results/reports here
        reportsContainer = tk.Text(self, height=15, width=50)
        reportsContainer.grid(pady=10)

        returnBtn = tk.Button(self, text='Return', command=lambda: controller.show_frame(AdminPage))
        returnBtn.grid(pady=10)


#Tkinter application
root = tkinterApp()
root.title("Bite Bank")
root.mainloop()
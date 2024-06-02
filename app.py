import tkinter as tk
from tkinter import *
from tkinter import messagebox
import mariadb

#MariaDB connection variable to be used for SQL commands
dbConn = None

#global userType for page rerouting
userType = None

# function to connect to the MariaDB database
def connect_db(user_type):
    global dbConn
    global userType
    if user_type == "Admin":
        user = "foodie"
        password = "chefP!"
        userType = AdminPage
    elif user_type == "Casual":
        user = "pares"
        password = "diwataP"
        userType = CasualPage
    else:
        userType = None
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

        for F in (LoginPage, AdminPage, CasualPage, SearchPage, FoodItemAdd, FoodItemEdit, FoodItemDelete, ItemReviewAdd, EstabReviewAdd, ReviewUpdate, ReviewDelete, AddFoodEstablishment, DeleteFoodEstablishment, EditFoodEstablishment, ViewItemEstablishment, ViewItemBasedType, ViewFoodEstablishment, ViewEstabReview, ViewItemReview, ViewReviews, ViewEstablishmentBasedRating, ViewItemsBasedPrice, ViewItemsPriceRangeEstab):
  
            frame = F(mainContainer, self)
  
            #initialized pages/ frames to be displayed in container
            self.frames[F] = frame 
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(LoginPage)
  
    #display the current frame passed as parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

#LOGIN PAGE
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
        
        #function to route user to admin page or casual page
        def directClientToPage():
            name = self.name_var.get()
            password = self.passw_var.get()
            userType = loginConn(name, password)
            if userType:
                controller.show_frame(userType)

        submitBtn = tk.Button(self, text='Submit', command=directClientToPage)
        submitBtn.grid(row=3, column=1, pady=10)

#ADMIN PAGE
class AdminPage(tk.Frame):  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #page title label
        adminLabel = tk.Label(self, text="Admin Dashboard", font=('calibre', 20, 'bold'))
        adminLabel.grid(row=0, column=0, columnspan=2, pady=10)

        #Add Features
        userAddLabel = tk.Label(self, text="Add", font=('calibre', 10, 'bold'))
        userAddLabel.grid(row=1, column=0, columnspan=2, pady=10)

        #add food item button
        itemAddButton = tk.Button(self, text="Food Item", command=lambda: controller.show_frame(FoodItemAdd))
        itemAddButton.grid(row=2, column=0, pady=5)

        #add food establishment button
        establishmentAddButton = tk.Button(self, text="Food Establishment", command=lambda: controller.show_frame(AddFoodEstablishment))
        establishmentAddButton.grid(row=2, column=1, pady=5, padx=10)

        #Update Features
        userUpdateLabel = tk.Label(self, text="Update", font=('calibre', 10, 'bold'))
        userUpdateLabel.grid(row=3, column=0, columnspan=2, pady=10)
        
        #edit food item button
        itemEditButton = tk.Button(self, text="Food Item", command=lambda: controller.show_frame(FoodItemEdit))
        itemEditButton.grid(row=4, column=0, pady=5, padx=10)

        #edit food establishment button
        establishmentEditButton = tk.Button(self, text="Food Establishment", command=lambda: controller.show_frame(EditFoodEstablishment))
        establishmentEditButton.grid(row=4, column=1,  pady=5, padx=10)

        #Delete Features
        userDeleteLabel = tk.Label(self, text="Delete", font=('calibre', 10, 'bold'))
        userDeleteLabel.grid(row=5, column=0, columnspan=2, pady=10)

        #delete food item button
        itemDeleteButton = tk.Button(self, text="Item", command=lambda: controller.show_frame(FoodItemDelete))
        itemDeleteButton.grid(row=6, column=0, pady=5, padx=10)

        #delete food establishment button
        establishmentDeleteButton = tk.Button(self, text="Establishment", command=lambda: controller.show_frame(DeleteFoodEstablishment))
        establishmentDeleteButton.grid(row=6, column=1, pady=5, padx=10)

        #Search Features
        reportsLabel = tk.Label(self, text='Search', font=('calibre', 10, 'bold'))
        reportsLabel.grid(row=7, column=0, pady=5)
        reportsBtn = tk.Button(self, text = 'View', command=lambda: controller.show_frame(SearchPage))
        reportsBtn.grid(row=7, column=1, columnspan=2, pady=5)

#ADD FOOD ESTABLISHMENT PAGE
class AddFoodEstablishment(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #variables
        self.estabLoc = tk.StringVar()
        self.estabRating = tk.IntVar()
        self.estabName = tk.StringVar()

        #page title label
        updateFoodEstabLabel = tk.Label(self, text="Add Food Establishment", font=('calibre', 20, 'bold'))
        updateFoodEstabLabel.grid(pady=10)

        #location
        addEstabLocText = tk.Label(self, text="Enter Location:")
        addEstabLocText.grid(pady=10)
        addEstabLocEntry = tk.Entry(self, textvariable=self.estabLoc, width=50)
        addEstabLocEntry.grid(pady=10)

        #rating
        addEstabRatingText = tk.Label(self, text="Enter Rating:")
        addEstabRatingText.grid(pady=10)
        addEstabRatingEntry = tk.Entry(self, textvariable=self.estabRating, width=50)
        addEstabRatingEntry.grid(pady=10)

        #establishment name
        addEstabNameText = tk.Label(self, text="Enter food establishment name:")
        addEstabNameText.grid(pady=10)
        addEstabNameEntry = tk.Entry(self, textvariable=self.estabName, width=50)
        addEstabNameEntry.grid(pady=10)

        #execute query
        addEstablishmentButton = tk.Button(self, text="Add", command=self.addEstablishment)
        addEstablishmentButton.grid(pady=10)
        
        #return to previous page
        itemReturnButton = tk.Button(self, text="Return", command=lambda: controller.show_frame(AdminPage))
        itemReturnButton.grid(pady=10)

    # Function for adding the food establishment to the MariaDB
    def addEstablishment(self):
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

#EDIT FOOD ESTABLISHMENT PAGE
class EditFoodEstablishment(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #var
        self.toUpdate = tk.StringVar()
        self.newValue = tk.StringVar()
        self.estabID = tk.IntVar()

        #page title label
        updateFoodEstabLabel = tk.Label(self, text="Update Food Establishment", font=('calibre', 20, 'bold'))
        updateFoodEstabLabel.grid(pady=10)

        #input fields for updating estab attributes
        editToUpdateText = tk.Label(self, text="What will you change? Choose from establishment_name, location or rating.")
        editToUpdateText.grid(pady=10)
        editToUpdateEntry = tk.Entry(self, textvariable=self.toUpdate, width=50)
        editToUpdateEntry.grid(pady=10)

        #new value of attributes
        editNewValueText = tk.Label(self, text="Enter New Value:")
        editNewValueText.grid(pady=10)
        editNewValueEntry = tk.Entry(self, textvariable=self.newValue, width=50)
        editNewValueEntry.grid(pady=10)

        #searches for matching establishment id
        estabIDText = tk.Label(self, text="Enter Food Establishment ID:")
        estabIDText.grid(pady=10)
        editItemIDEntry = tk.Entry(self, textvariable=self.estabID, width=50)
        editItemIDEntry.grid(pady=10)

        #execute query
        addItemButton = tk.Button(self, text="Update", command=self.editItem)
        addItemButton.grid(pady=10)

        #return to previous page
        itemReturnButton = tk.Button(self, text="Return", command=lambda: controller.show_frame(AdminPage))
        itemReturnButton.grid(pady=10)
    
    #SQL command function
    def editItem(self):
        
        #var
        toUpdate = self.toUpdate.get()
        newValue = self.newValue.get()
        estabID = self.estabID.get()

        #establish MariaDB connection first before executing SQL commands
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

#DELETE FOOD ESTABLISHMENT PAGE
class DeleteFoodEstablishment(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #var
        self.estabId = tk.StringVar()

        #page title label
        deleteFoodEstabLabel = tk.Label(self, text="Delete Food Establishment", font=('calibre', 20, 'bold'))
        deleteFoodEstabLabel.grid(pady=10)
        
        #input fields
        deleteEstab = tk.Label(self, text="Enter Food Establishment ID:")
        deleteEstab.grid(pady=10)
        estabIdEntry = tk.Entry(self, textvariable=self.estabId, width=50)
        estabIdEntry.grid(pady=10)

        #execute query
        deleteButton = tk.Button(self, text="Delete", command=self.deleteEstablishment)
        deleteButton.grid(pady=10)

        #return to previous page
        itemReturnButton = tk.Button(self, text="Return", command=lambda: controller.show_frame(AdminPage))
        itemReturnButton.grid(pady=10)

    #SQL command function
    def deleteEstablishment(self):

        #var
        estabID = self.estabId.get()

        #establish MariaDB connection
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

#ADD FOOD ITEM PAGE
class FoodItemAdd(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #page title label
        addFoodItemLabel = tk.Label(self, text="Edit Food Item", font=('calibre', 20, 'bold'))
        addFoodItemLabel.grid(pady=10)

        #var
        self.itemName = tk.StringVar()
        self.itemPrice = tk.IntVar()
        self.itemFoodType = tk.StringVar()
        self.itemIngredient = tk.StringVar()
        self.itemEstabId = tk.IntVar()

        #name
        addItemNameText = tk.Label(self, text="Enter Food Item Name:")
        addItemNameText.grid(pady=10)
        addItemNameEntry = tk.Entry(self, textvariable=self.itemName, width=50)
        addItemNameEntry.grid(pady=10)

        #price
        addItemPriceText = tk.Label(self, text="Enter Food Item Price:")
        addItemPriceText.grid(pady=10)
        addItemPriceEntry = tk.Entry(self, textvariable=self.itemPrice, width=50)
        addItemPriceEntry.grid(pady=10)

        #food type
        addItemFoodTypeText = tk.Label(self, text="Enter Food Item's Food Type:")
        addItemFoodTypeText.grid(pady=10)
        addItemFoodTypeEntry = tk.Entry(self, textvariable=self.itemFoodType, width=50)
        addItemFoodTypeEntry.grid(pady=10)

        #ingredients
        addItemIngredientText = tk.Label(self, text="Enter Food Item's Ingredient/s:")
        addItemIngredientText.grid(pady=10)
        addItemIngredientEntry = tk.Entry(self, textvariable=self.itemIngredient, width=50)
        addItemIngredientEntry.grid(pady=10)

        #establishment id (foreign key)
        addItemEstabIdText = tk.Label(self, text="Enter Food Item's Associated Establishment ID: ")
        addItemEstabIdText.grid(pady=10)
        addItemEstabIdEntry = tk.Entry(self, textvariable=self.itemEstabId, width=50)
        addItemEstabIdEntry.grid(pady=10)

        #execute query
        addItemButton = tk.Button(self, text="Add Food Item", command=self.addItem)
        addItemButton.grid(pady=10)

        #return to previous page
        itemReturnButton = tk.Button(self, text="Return", command=lambda: controller.show_frame(AdminPage))
        itemReturnButton.grid(pady=10)

    #SQL command function
    def addItem(self):
        
        #var
        name = self.itemName.get()
        price = self.itemPrice.get()
        type = self.itemFoodType.get()
        ingredient = self.itemIngredient.get()
        estabId = self.itemEstabId.get()

        #establish MariaDB connection first
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

#EDIT FOOD ITEM PAGE
class FoodItemEdit(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #var
        self.toUpdate = tk.StringVar()
        self.newValue = tk.StringVar()
        self.itemID = tk.IntVar()
        
        #page title label
        editFoodItemLabel = tk.Label(self, text="Edit Food Item", font=('calibre', 20, 'bold'))
        editFoodItemLabel.grid(pady=10)
        
        #input fields
        editToUpdateText = tk.Label(self, text="What will you change? Choose from name, price, food_type, ingredient, or establishment_id.")
        editToUpdateText.grid(pady=10)
        editToUpdateEntry = tk.Entry(self, textvariable=self.toUpdate, width=50)
        editToUpdateEntry.grid(pady=10)

        #new values for attributes
        editNewValueText = tk.Label(self, text="Enter New Value.")
        editNewValueText.grid(pady=10)
        editNewValueEntry = tk.Entry(self, textvariable=self.newValue, width=50)
        editNewValueEntry.grid(pady=10)

        #searches for matching food item id
        editItemIDText = tk.Label(self, text="Enter Food Item ID:")
        editItemIDText.grid(pady=10)
        editItemIDEntry = tk.Entry(self, textvariable=self.itemID, width=50)
        editItemIDEntry.grid(pady=10)

        #execute query
        addItemButton = tk.Button(self, text="Edit Food Item", command=self.editItem)
        addItemButton.grid(pady=10)

        #return to previous page
        itemReturnButton = tk.Button(self, text="Return", command=lambda: controller.show_frame(AdminPage))
        itemReturnButton.grid(pady=10)

    #SQL command function
    def editItem(self):
        
        #var
        toUpdate = self.toUpdate.get()
        newValue = self.newValue.get()
        itemID = self.itemID.get()

        #establish MariaDB connection first
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

#DELETE FOOD ITEM PAGE
class FoodItemDelete(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #var
        self.itemID = tk.IntVar()

        #page title label
        deleteFoodItemLabel = tk.Label(self, text="Delete Food Item", font=('calibre', 20, 'bold'))
        deleteFoodItemLabel.grid(pady=10)

        #searches for matching food item id
        editItemIDText = tk.Label(self, text="Enter Food Item ID:")
        editItemIDText.grid(pady=10)
        editItemIDEntry = tk.Entry(self, textvariable=self.itemID, width=50)
        editItemIDEntry.grid(pady=10)

        #execute query
        addItemButton = tk.Button(self, text="Delete Food Item", command=self.deleteItem)
        addItemButton.grid(pady=10)

        #return to previous page
        itemReturnButton = tk.Button(self, text="Return", command=lambda: controller.show_frame(AdminPage))
        itemReturnButton.grid(pady=10)

    #SQL command function
    def deleteItem(self):
        
        #var
        itemID = self.itemID.get()

        #establish MariaDB connection first
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

#CASUAL USER PAGE
class CasualPage(tk.Frame):  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #page title label
        casualLabel = tk.Label(self, text="User Dashboard", font=('calibre', 20, 'bold'))
        casualLabel.grid(row=0, column=0, columnspan=2, pady=10)

        #Add Review
        casualAddLabel = tk.Label(self, text="Add a Food Review", font=('calibre', 10, 'bold'))
        casualAddLabel.grid(row=1, column=0, columnspan=2, pady=10)

        #add food item review
        itemAddReviewButton = tk.Button(self, text="Food Item", command=lambda: controller.show_frame(ItemReviewAdd))
        itemAddReviewButton.grid(row=2, column=0, pady=5)

        #add food estab review
        estabAddReviewButton = tk.Button(self, text="Food Establishment", command=lambda: controller.show_frame(EstabReviewAdd))
        estabAddReviewButton.grid(row=2, column=1, pady=5)

        #Update Review
        casualUpdateLabel = tk.Label(self, text="Update a Food Review", font=('calibre', 10, 'bold'))
        casualUpdateLabel.grid(row=4, column=0, columnspan=2, pady=10)

        #update food review
        reviewUpdateButton = tk.Button(self, text="View", command=lambda: controller.show_frame(ReviewUpdate))
        reviewUpdateButton.grid(row=5, column=0, columnspan=2, pady=5)

        #Delete Review
        casualDeleteLabel = tk.Label(self, text="Delete a Food Review", font=('calibre', 10, 'bold'))
        casualDeleteLabel.grid(row=6, column=0, columnspan=2, pady=10)

        #delete food review button
        estabDeleteButton = tk.Button(self, text="View", command=lambda: controller.show_frame(ReviewDelete))
        estabDeleteButton.grid(row=7, column=0, columnspan=2, pady=5)
        
        #route to Reports page
        reportsLabel = tk.Label(self, text='Reports', font=('calibre', 10, 'bold'))
        reportsLabel.grid(row=8, column=0, pady=5)
        reportsBtn = tk.Button(self, text = 'View', command=lambda: controller.show_frame(SearchPage))
        reportsBtn.grid(row=8, column=1, columnspan=2, pady=5)

#ADD FOOD ITEM REVIEW PAGE
class ItemReviewAdd(tk.Frame):  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #page title label
        itemReviewAddLabel = tk.Label(self, text="Edit Food Item", font=('calibre', 20, 'bold'))
        itemReviewAddLabel.grid(pady=10)

        #input field variables
        self.feedback = tk.StringVar()
        self.date = tk.StringVar()
        self.rating = tk.IntVar()
        self.establishment_id = tk.IntVar()
        self.item_id = tk.IntVar()

        #input fields
        #feedback
        feedbackLabel = tk.Label(self, text="Feedback:")
        feedbackLabel.grid(pady=10)
        feedbackEntry = tk.Entry(self, textvariable=self.feedback, width=50)
        feedbackEntry.grid(pady=10)

        #date
        dateLabel = tk.Label(self, text="Date of Review (YYYY-MM-DD):")
        dateLabel.grid(pady=10)
        dateEntry = tk.Entry(self, textvariable=self.date, width=50)
        dateEntry.grid(pady=10)

        #rating
        ratingLabel = tk.Label(self, text="Rating (1-5):")
        ratingLabel.grid(pady=10)
        ratingEntry = tk.Entry(self, textvariable=self.rating, width=50)
        ratingEntry.grid(pady=10)

        #item id
        itemIdLabel = tk.Label(self, text="Item ID:")
        itemIdLabel.grid(pady=10)
        itemIdEntry = tk.Entry(self, textvariable=self.item_id, width=50)
        itemIdEntry.grid(pady=10)

        #add item reviewbttn
        addButton = tk.Button(self, text="Add Review", command=self.addReview)
        addButton.grid(pady=10)

        #return to user dashboard
        returnButton = tk.Button(self, text="Return", command=lambda: controller.show_frame(CasualPage))
        returnButton.grid(pady=10)

    #SQL command function
    def addReview(self):

        #var
        feedback = self.feedback.get()
        date = self.date.get()
        rating = self.rating.get()
        user_id = 1
        item_id = self.item_id.get()

        if dbConn:
            query = 'INSERT INTO food_review (feedback, date_of_review, rating, user_id, item_id) VALUES (%s, %s, %d, %d, %d)'
            review = (feedback, date, rating, user_id, item_id)
            cur = dbConn.cursor()
            try:
                cur.execute(query, review)
                dbConn.commit()
                messagebox.showinfo("Success", "Review added successfully.")
            except mariadb.Error as e:
                messagebox.showerror("Query Error", f"Error executing query: {e}")
            finally:
                cur.close()
        else:
            messagebox.showerror("Database Error", "No database connection established.")

#ADD FOOD ESTABLISHMENT REVIEW PAGE
class EstabReviewAdd(tk.Frame):  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #page title label
        estabReviewAddLabel = tk.Label(self, text="Edit Food Item", font=('calibre', 20, 'bold'))
        estabReviewAddLabel.grid(pady=10)

        #input field variables
        self.feedback = tk.StringVar()
        self.date = tk.StringVar()
        self.rating = tk.IntVar()
        self.user_id = tk.IntVar()
        self.establishment_id = tk.IntVar()
        self.item_id = tk.IntVar()

        #input fields
        #feedback
        feedbackLabel = tk.Label(self, text="Feedback:")
        feedbackLabel.grid(pady=10)
        feedbackEntry = tk.Entry(self, textvariable=self.feedback, width=50)
        feedbackEntry.grid(pady=10)

        #date
        dateLabel = tk.Label(self, text="Date of Review (YYYY-MM-DD):")
        dateLabel.grid(pady=10)
        dateEntry = tk.Entry(self, textvariable=self.date, width=50)
        dateEntry.grid(pady=10)

        #rating
        ratingLabel = tk.Label(self, text="Rating (1-5):")
        ratingLabel.grid(pady=10)
        ratingEntry = tk.Entry(self, textvariable=self.rating, width=50)
        ratingEntry.grid(pady=10)

        #estab id
        estabIdLabel = tk.Label(self, text="Establishment ID:")
        estabIdLabel.grid(pady=10)
        estabIdEntry = tk.Entry(self, textvariable=self.establishment_id, width=50)
        estabIdEntry.grid(pady=10)

        #add item reviewbttn
        addButton = tk.Button(self, text="Add Review", command=self.addReview)
        addButton.grid(pady=10)

        #return to user dashboard
        returnButton = tk.Button(self, text="Return", command=lambda: controller.show_frame(CasualPage))
        returnButton.grid(pady=10)

    #add food review logic
    def addReview(self):
        feedback = self.feedback.get()
        date = self.date.get()
        rating = self.rating.get()
        user_id = 1
        estab_id = self.item_id.get()

        #establish connection to database before executing query
        if dbConn:
            #SQL command
            query = 'INSERT INTO food_review (feedback, date_of_review, rating, user_id, establishment_id) VALUES (%s, %s, %d, %d)'
            review = (feedback, date, rating, user_id, estab_id)
            cur = dbConn.cursor()
            try:
                #execution of SQL command
                cur.execute(query, review)
                dbConn.commit()
                messagebox.showinfo("Success", "Review added successfully.")
            except mariadb.Error as e:
                messagebox.showerror("Query Error", f"Error executing query: {e}")
            finally:
                cur.close()
        else:
            messagebox.showerror("Database Error", "No database connection established.")

#UPDATE FOOD REVIEW PAGE
class ReviewUpdate(tk.Frame):  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #page title label
        reviewUpdateLabel = tk.Label(self, text="Edit Food Item", font=('calibre', 20, 'bold'))
        reviewUpdateLabel.grid(pady=10)

        #update review variables
        self.review_id = tk.IntVar()
        self.user_id = tk.IntVar()
        self.new_feedback = tk.StringVar()
        self.new_rating = tk.IntVar()

        #input fields
        #review id to search
        reviewIdLabel = tk.Label(self, text="Review ID:")
        reviewIdLabel.grid(pady=10)
        reviewIdEntry = tk.Entry(self, textvariable=self.review_id, width=50)
        reviewIdEntry.grid(pady=10)
        #food review must match user id and review id=1

        #new/updated values for feedback
        newValueLabel = tk.Label(self, text="New Feedback:")
        newValueLabel.grid(pady=10)
        newValueEntry = tk.Entry(self, textvariable=self.new_feedback, width=50)
        newValueEntry.grid(pady=10)

        #new/updated value for rating
        ratingLabel = tk.Label(self, text="New Rating (1-5):")
        ratingLabel.grid(pady=10)
        ratingEntry = tk.Entry(self, textvariable=self.new_rating, width=50)
        ratingEntry.grid(pady=10)

        #update bttn for execution of query
        updateButton = tk.Button(self, text="Update Review", command=self.updateReview)
        updateButton.grid(pady=10)

        #return back to user dashboard
        returnButton = tk.Button(self, text="Return", command=lambda: controller.show_frame(CasualPage))
        returnButton.grid(pady=10)

    #update food review logic
    def updateReview(self):
        review_id = self.review_id.get()
        user_id = 1
        new_feedback = self.new_feedback.get()
        new_rating = self.new_rating.get()

        #establish connection to database before executing query
        if dbConn:
            #SQL command
            #dynamically set new review date to current date                VVVVVVVVV
            query = 'UPDATE food_review SET feedback = %s, date_of_review = CURDATE(), rating = %d WHERE review_id = %d AND user_id = %d'
            review = (new_feedback, new_rating, review_id, user_id)
            cur = dbConn.cursor()
            try:
                #execution of SQL command
                cur.execute(query, review)
                dbConn.commit()
                messagebox.showinfo("Success", "Review updated successfully.")
            except mariadb.Error as e:
                messagebox.showerror("Query Error", f"Error executing query: {e}")
            finally:
                cur.close()
        else:
            messagebox.showerror("Database Error", "No database connection established.")

#DELETE FOOD REVIEW PAGE
class ReviewDelete(tk.Frame):  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #page title label
        reviewDeleteLabel = tk.Label(self, text="Edit Food Item", font=('calibre', 20, 'bold'))
        reviewDeleteLabel.grid(pady=10)

        #only need the review id for deletion
        self.review_id = tk.IntVar()

        #input fields
        reviewIdLabel = tk.Label(self, text="Review ID to delete:")
        reviewIdLabel.grid(pady=10)
        reviewIdEntry = tk.Entry(self, textvariable=self.review_id, width=50)
        reviewIdEntry.grid(pady=10)

        #bttn to execute SQL query
        deleteButton = tk.Button(self, text="Delete Review", command=self.deleteReview)
        deleteButton.grid(pady=10)

        #return to user dashboard
        returnButton = tk.Button(self, text="Return", command=lambda: controller.show_frame(CasualPage))
        returnButton.grid(pady=10)

    #delete food review logic
    def deleteReview(self):
        review_id = self.review_id.get()
        user_id = 1
        if dbConn:
            query = 'DELETE FROM food_review WHERE review_id = %d AND user_id = %d'
            cur = dbConn.cursor()
            try:
                cur.execute(query, (review_id,user_id))
                dbConn.commit()
                messagebox.showinfo("Success", "Review deleted successfully.")
            except mariadb.Error as e:
                messagebox.showerror("Query Error", f"Error executing query: {e}")
            finally:
                cur.close()
        else:
            messagebox.showerror("Database Error", "No database connection established.")

#REPORT 1
class ViewFoodEstablishment(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # page title label
        estabLabel = tk.Label(self, text="View Reports", font=('calibre', 20, 'bold'))
        estabLabel.grid(pady=10)

        #function to fetch establishment details
        def viewEstablishment():
            if dbConn:
                query = 'SELECT * FROM food_establishment;'
                cur = dbConn.cursor()
                try:
                    cur.execute(query)
                    results = cur.fetchall()
                    resultContainer.delete(1.0, tk.END)
                    for row in results:
                        resultContainer.insert(tk.END, f"{row}\n")
                    dbConn.commit()
                    messagebox.showinfo("Success", "Food establishments fetched successfully.")
                except mariadb.Error as e:
                    messagebox.showerror("Query Error", f"Error executing query: {e}")
                finally:
                    cur.close()
            else:
                messagebox.showerror("Database Error", "No database connection established.")

        #bttn to execute query
        viewEstabBtn = tk.Button(self, text='View Food Establishments', command=viewEstablishment)
        viewEstabBtn.grid(pady=10)

        #display results here
        resultContainer = tk.Text(self, height=20, width=80)
        resultContainer.grid(pady=10)

        #return to previous page
        returnBtn = tk.Button(self, text='Return', command=lambda: controller.show_frame(SearchPage))
        returnBtn.grid(pady=10)

#REPORT NO.2 MASTER PAGE
class ViewReviews(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # page title label
        reviewsLabel = tk.Label(self, text="View Reviews", font=('calibre', 20, 'bold'))
        reviewsLabel.grid(row=0, column=0, columnspan=2, pady=10)
        
        viewItemReviewBtn = tk.Button(self, text='Food Item Reviews', command=lambda: controller.show_frame(ViewItemReview))
        viewItemReviewBtn.grid(row=1, column=0, pady=10)

        viewEstabReviewBtn = tk.Button(self, text='Food Establishment Reviews', command=lambda: controller.show_frame(ViewEstabReview))
        viewEstabReviewBtn.grid(row=1, column=1, pady=10)

        #return to previous page
        returnBtn = tk.Button(self, text='Return', command=lambda: controller.show_frame(SearchPage))
        returnBtn.grid(pady=10)

#REPORT NO.2 BRANCH#1 PAGE
class ViewItemReview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.reviewItemID = IntVar()

        reviewItemIdLabel = tk.Label(self, text='Enter Food Item ID:')
        reviewItemIdLabel.grid(pady=10)
        reviewItemIdEntry = tk.Entry(self, textvariable=self.reviewItemID, width=50)
        reviewItemIdEntry.grid(pady=5)

        def viewReviews():
            itemID = self.reviewItemID.get()
            if not itemID:
                messagebox.showerror("Input Error", "Please enter a Food Item ID.")
                return

            if dbConn:
                query = "SELECT * FROM food_review WHERE item_id = %d"
                cur = dbConn.cursor()
                try:
                    cur.execute(query, (itemID,))
                    results = cur.fetchall()
                    reviewsContainer.delete(1.0, tk.END)
                    for row in results:
                        reviewsContainer.insert(tk.END, f"{row}\n")
                    dbConn.commit()
                    messagebox.showinfo("Success", "Reviews fetched successfully.")
                except mariadb.Error as e:
                    messagebox.showerror("Query Error", f"Error executing query: {e}")
                finally:
                    cur.close()
            else:
                messagebox.showerror("Database Error", "No database connection established.")

        #button to execute the query
        viewReviewsBtn = tk.Button(self, text='View Reports', command=viewReviews)
        viewReviewsBtn.grid(pady=10)

        #display results here
        reviewsContainer = tk.Text(self, height=20, width=80)
        reviewsContainer.grid(pady=10)

        #buttn to return to the previous page
        returnBtn = tk.Button(self, text='Return', command=lambda: controller.show_frame(ViewReviews))
        returnBtn.grid(pady=10)

#REPORT NO.2 BRANCH#2 PAGE
class ViewEstabReview(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.reviewEstabID = IntVar()

        reviewEstabIdLabel = tk.Label(self, text='Enter Food Establishment ID:')
        reviewEstabIdLabel.grid(pady=10)
        reviewEntryIdEntry = tk.Entry(self, textvariable=self.reviewEstabID, width=50)
        reviewEntryIdEntry.grid(pady=5)
        
        def viewReviews():
            itemID = self.reviewEstabID.get()
            if not itemID:
                messagebox.showerror("Input Error", "Please enter a Food Establishment ID.")
                return

            if dbConn:
                query = "SELECT * FROM food_review WHERE establishment_id = %d"
                cur = dbConn.cursor()
                try:
                    cur.execute(query, (itemID,))
                    results = cur.fetchall()
                    reviewsContainer.delete(1.0, tk.END)
                    for row in results:
                        reviewsContainer.insert(tk.END, f"{row}\n")
                    dbConn.commit()
                    messagebox.showinfo("Success", "Reviews fetched successfully.")
                except mariadb.Error as e:
                    messagebox.showerror("Query Error", f"Error executing query: {e}")
                finally:
                    cur.close()
            else:
                messagebox.showerror("Database Error", "No database connection established.")

        #button to execute the query
        viewReviewsBtn = tk.Button(self, text='View Reports', command=viewReviews)
        viewReviewsBtn.grid(pady=10)

        #display results here
        reviewsContainer = tk.Text(self, height=20, width=80)
        reviewsContainer.grid(pady=10)

        #buttn to return to the previous page
        returnBtn = tk.Button(self, text='Return', command=lambda: controller.show_frame(ViewReviews))
        returnBtn.grid(pady=10)        

#REPORT NO.3 PAGE
class ViewItemEstablishment(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        #var
        self.estabId = tk.StringVar()

        #page title label
        viewItemLabel = tk.Label(self, text="View Food Items in Establishment", font=('calibre', 20, 'bold'))
        viewItemLabel.grid(row=0, column=0, columnspan=2, pady=10)
        
        #searches for matching food establishment id
        viewItemEstab = tk.Label(self, text="Enter Food Establishment ID:")
        viewItemEstab.grid(pady=10)
        estabIdEntry = tk.Entry(self, textvariable=self.estabId, width=50)
        estabIdEntry.grid(pady=10)

        #view report logic
        def viewItems():

            #var
            estabID = self.estabId.get()

            if dbConn:    #change to *
                query = f'SELECT i.name, i.price, i.ingredient FROM food_item i LEFT JOIN food_establishment e ON i.establishment_id = e.establishment_id WHERE i.establishment_id = {estabID}'
                cur = dbConn.cursor()
                try:
                    cur.execute(query)
                    results = cur.fetchall()
                    reportsContainer.delete(1.0, tk.END)
                    for row in results:
                        reportsContainer.insert(tk.END, f"{row}\n")
                    dbConn.commit()
                    messagebox.showinfo("Success", "Food Item fetched successfully.")
                except mariadb.Error as e:
                    messagebox.showerror("Query Error", f"Error executing query: {e}")
                finally:
                    cur.close()
            else:
                messagebox.showerror("Database Error", "No database connection established.")

        #execute command
        deleteButton = tk.Button(self, text="View Reports", command=viewItems)
        deleteButton.grid(pady=10)

        #display results/reports here
        reportsContainer = tk.Text(self, height=20, width=80)
        reportsContainer.grid(pady=10)

        #returns to previous page
        returnBtn = tk.Button(self, text='Return', command=lambda: controller.show_frame(SearchPage))
        returnBtn.grid(pady=10)

#REPORT NO.4 PAGE
class ViewItemBasedType(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)

        #var
        self.estabId = tk.StringVar()
        self.foodType = tk.StringVar() 
        
        #page title labe
        viewItemTypeLabel = tk.Label(self, text="View Food Items by their Food Type", font=('calibre', 20, 'bold'))
        viewItemTypeLabel.grid(row=0, column=0, columnspan=2, pady=10)
        
        #input fields
        viewItemEstab = tk.Label(self, text="Enter Food Establishment ID:")
        viewItemEstab.grid(pady=10)
        estabIdEntry = tk.Entry(self, textvariable=self.estabId, width=50)
        estabIdEntry.grid(pady=10)

        viewItemEstab = tk.Label(self, text="Enter the type of :")
        viewItemEstab.grid(pady=10)
        estabIdEntry = tk.Entry(self, textvariable=self.foodType, width=50)
        estabIdEntry.grid(pady=10)

        #view report logic
        def viewItems():

            #var
            estabID = self.estabId.get()
            foodType = self.foodType.get()

            if dbConn:      #change to *
                query = f'SELECT i.name, i.price, i.ingredient FROM food_item i LEFT JOIN food_establishment e ON i.establishment_id = e.establishment_id WHERE i.establishment_id = %s AND i.food_type=%s'
                items = (estabID, foodType)
                cur = dbConn.cursor()
                try:
                    cur.execute(query,items)
                    results = cur.fetchall()
                    reportsContainer.delete(1.0, tk.END)
                    for row in results:
                        reportsContainer.insert(tk.END, f"{row}\n")
                    dbConn.commit()
                    messagebox.showinfo("Success", "Food Item fetched successfully.")
                except mariadb.Error as e:
                    messagebox.showerror("Query Error", f"Error executing query: {e}")
                finally:
                    cur.close()
            else:
                messagebox.showerror("Database Error", "No database connection established.")

        #execute query
        deleteButton = tk.Button(self, text="View Reports", command=viewItems)
        deleteButton.grid(pady=10)

        #display results/reports here
        reportsContainer = tk.Text(self, height=20, width=80)
        reportsContainer.grid(pady=10)

        #return to previous page
        returnBtn = tk.Button(self, text='Return', command=lambda: controller.show_frame(SearchPage))
        returnBtn.grid(pady=10)

#REPORT NO.5 PAGE

#REPORT NO. 6 PAGE
class ViewEstablishmentBasedRating(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        #page title label
        viewItemLabel = tk.Label(self, text="View High-Rated Food Establishments", font=('calibre', 20, 'bold'))
        viewItemLabel.grid(row=0, column=0, columnspan=2, pady=10)

        #view report logic
        def viewItems():

            if dbConn:    #change to *
                query = 'SELECT * FROM food_establishment WHERE rating >= 4 ORDER BY rating;'
                cur = dbConn.cursor()
                try:
                    cur.execute(query)
                    results = cur.fetchall()
                    reportsContainer.delete(1.0, tk.END)
                    for row in results:
                        reportsContainer.insert(tk.END, f"{row}\n")
                    dbConn.commit()
                    messagebox.showinfo("Success", "Food Establishments fetched successfully.")
                except mariadb.Error as e:
                    messagebox.showerror("Query Error", f"Error executing query: {e}")
                finally:
                    cur.close()
            else:
                messagebox.showerror("Database Error", "No database connection established.")

        #execute command
        executeButton = tk.Button(self, text="View Reports", command=viewItems)
        executeButton.grid(pady=10)

        #display results/reports here
        reportsContainer = tk.Text(self, height=20, width=80)
        reportsContainer.grid(pady=10)

        #returns to previous page
        returnBtn = tk.Button(self, text='Return', command=lambda: controller.show_frame(SearchPage))
        returnBtn.grid(pady=10)

#REPORT NO. 7 PAGE
class ViewItemsBasedPrice(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        #page title label
        viewItemLabel = tk.Label(self, text="View Food Item Prices", font=('calibre', 20, 'bold'))
        viewItemLabel.grid(row=0, column=0, columnspan=2, pady=10)

        #view report logic
        def viewItems():
            if dbConn:    #change to *
                query = 'SELECT * FROM food_item i LEFT JOIN food_establishment e ON i.establishment_id = e.establishment_id ORDER BY price;'
                cur = dbConn.cursor()
                try:
                    cur.execute(query)
                    results = cur.fetchall()
                    reportsContainer.delete(1.0, tk.END)
                    for row in results:
                        reportsContainer.insert(tk.END, f"{row}\n")
                    dbConn.commit()
                    messagebox.showinfo("Success", "Food Item fetched successfully.")
                except mariadb.Error as e:
                    messagebox.showerror("Query Error", f"Error executing query: {e}")
                finally:
                    cur.close()
            else:
                messagebox.showerror("Database Error", "No database connection established.")

        #execute command
        executeButton = tk.Button(self, text="View Reports", command=viewItems)
        executeButton.grid(pady=10)

        #display results/reports here
        reportsContainer = tk.Text(self, height=20, width=80)
        reportsContainer.grid(pady=10)

        #returns to previous page
        returnBtn = tk.Button(self, text='Return', command=lambda: controller.show_frame(SearchPage))
        returnBtn.grid(pady=10)

#REPORT NO. 8 PAGE
class ViewItemsPriceRangeEstab(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #page title label
        viewItemLabel = tk.Label(self, text="View Food Items", font=('calibre', 20, 'bold'))
        viewItemLabel.grid(row=0, column=0, columnspan=2, pady=10)

        #var
        self.minPrice = IntVar()
        self.maxPrice = IntVar()
        self.foodType = StringVar()

        #input fields
        #min price
        minPriceLabel = tk.Label(self, text="Enter Minimum Price:")
        minPriceLabel.grid(row=1, column=0, pady=5)
        minPriceEntry = tk.Entry(self, textvariable=self.minPrice)
        minPriceEntry.grid(row=1, column=1, pady=5)

        #max price
        maxPriceLabel = tk.Label(self, text="Enter Maximum Price:")
        maxPriceLabel.grid(row=2, column=0, pady=5)
        maxPriceEntry = tk.Entry(self, textvariable=self.maxPrice)
        maxPriceEntry.grid(row=2, column=1, pady=5)

        #food type
        foodTypeLabel = tk.Label(self, text="Enter Food Type:")
        foodTypeLabel.grid(row=3, column=0, pady=5)
        foodTypeEntry = tk.Entry(self, textvariable=self.foodType)
        foodTypeEntry.grid(row=3, column=1, pady=5)

        #view report logic
        def viewItems():
            
            #var
            min_price = self.minPrice.get()
            max_price = self.maxPrice.get()
            food_type = self.foodType.get()

            if dbConn:
                query = 'SELECT * FROM food_item i LEFT JOIN food_establishment e ON i.establishment_id = e.establishment_id WHERE 1=1'
                #conditions from input field values
                params = []

                #if present
                if min_price:
                    query += ' AND i.price >= %s'
                    params.append(min_price)
                
                #if present
                if max_price:
                    query += ' AND i.price <= %s'
                    params.append(max_price)
                
                #if present
                if food_type:
                    query += ' AND i.food_type = %s'
                    params.append(food_type)
                
                #final query
                query += ' ORDER BY i.price;'

                cur = dbConn.cursor()
                try:
                    cur.execute(query, params)
                    results = cur.fetchall()
                    reportsContainer.delete(1.0, tk.END)
                    for row in results:
                        reportsContainer.insert(tk.END, f"{row}\n")
                    dbConn.commit()
                    messagebox.showinfo("Success", "Food Items fetched successfully.")
                except mariadb.Error as e:
                    messagebox.showerror("Query Error", f"Error executing query: {e}")
                finally:
                    cur.close()
            else:
                messagebox.showerror("Database Error", "No database connection established.")

        #execute command
        executeButton = tk.Button(self, text="View Reports", command=viewItems)
        executeButton.grid(row=4, column=0, columnspan=2, pady=10)

        #display results/reports here
        reportsContainer = tk.Text(self, height=20, width=80)
        reportsContainer.grid(row=5, column=0, columnspan=2, pady=10)

        #returns to previous page
        returnBtn = tk.Button(self, text='Return', command=lambda: controller.show_frame(SearchPage))
        returnBtn.grid(row=6, column=0, columnspan=2, pady=10)

#SEARCH PAGE
class SearchPage(tk.Frame):  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        global userType

        self.query_var = tk.StringVar()

        #page title label
        reportsLabel = tk.Label(self, text='Reports Page', font=('calibre', 20, 'bold'))
        reportsLabel.grid(pady=10)

        #REPORT 1
        report1Button = tk.Button(self, text=" View All Food Establishments", command=lambda: controller.show_frame(ViewFoodEstablishment))
        report1Button.grid(pady=10)

        #REPORT 2
        report2Button = tk.Button(self, text=" View All Food Reviews", command=lambda: controller.show_frame(ViewReviews))
        report2Button.grid(pady=10)

        #REPORT 3
        report3Button = tk.Button(self, text=" View Food Item From Establishment", command=lambda: controller.show_frame(ViewItemEstablishment))
        report3Button.grid(pady=10)

        #REPORT 4
        report4Button = tk.Button(self, text=" View Food Item Based On Food Type", command=lambda: controller.show_frame(ViewItemBasedType))
        report4Button.grid(pady=10)

        #REPORT 5
        #REPORT 6
        report6Button = tk.Button(self, text=" View High-Rated Food Establishments", command=lambda: controller.show_frame(ViewEstablishmentBasedRating))
        report6Button.grid(pady=10)

        #REPORT 7
        report7Button = tk.Button(self, text=" View Food Items According to Price", command=lambda: controller.show_frame(ViewItemsBasedPrice))
        report7Button.grid(pady=10)

        #REPORT 8
        report8Button = tk.Button(self, text=" View Food Items By Price & Food Type", command=lambda: controller.show_frame(ViewItemsPriceRangeEstab))
        report8Button.grid(pady=10)

        #select query input (for advanced users experienced in MySQL)
        queryLabel = tk.Label(self, text='Advanced Search', font=('calibre', 10))
        queryLabel.grid(pady=10)
        queryEntry = tk.Entry(self, textvariable = self.query_var, width=40, font=('calibre', 10, 'normal'))
        queryEntry.grid(pady=10)
        
        #generate reports
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
        
        #return to previous page
        returnBtn = tk.Button(self, text='Return', command=lambda: controller.show_frame(userType))
        returnBtn.grid(pady=10)

#TKINTER APP
root = tkinterApp()
root.title("Bite Bank")
root.mainloop()
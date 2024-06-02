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

        for F in (LoginPage, AdminPage, CasualPage, ReportsPage, FoodItemAdd, FoodItemEdit, FoodItemDelete, ItemReviewAdd, EstabReviewAdd, ReviewUpdate, ReviewDelete):
  
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
        loginLabel = tk.Label(self, text="Bite Bank", font=('calibre', 20, 'bold'))
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

# Admin Page/Dashboard
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

        #Update Features
        userUpdateLabel = tk.Label(self, text="Update", font=('calibre', 10, 'bold'))
        userUpdateLabel.grid(row=3, column=0, columnspan=2, pady=10)

        #update food item button
        itemEditButton = tk.Button(self, text="Food Item", command=lambda: controller.show_frame(FoodItemEdit))
        itemEditButton.grid(row=4, column=0, pady=5)

        #Delete Features
        userDeleteLabel = tk.Label(self, text="Delete", font=('calibre', 10, 'bold'))
        userDeleteLabel.grid(row=5, column=0, columnspan=2, pady=10)

        #delete food item button
        itemDeleteButton = tk.Button(self, text="Food Item", command=lambda: controller.show_frame(FoodItemDelete))
        itemDeleteButton.grid(row=6, column=0, pady=5)
        
        #route to Reports page
        reportsLabel = tk.Label(self, text='Reports', font=('calibre', 10, 'bold'))
        reportsLabel.grid(row=7, column=0, pady=5)
        reportsBtn = tk.Button(self, text = 'Go', command=lambda: controller.show_frame(ReportsPage))
        reportsBtn.grid(row=7, column=1, columnspan=2, pady=5)

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
        casualUpdateLabel.grid(row=3, column=0, columnspan=2, pady=10)

        #update food review
        reviewUpdateButton = tk.Button(self, text="Go", command=lambda: controller.show_frame(ReviewUpdate))
        reviewUpdateButton.grid(row=4, column=0, columnspan=2, pady=5)

        #Delete Review
        casualDeleteLabel = tk.Label(self, text="Delete a Food Review", font=('calibre', 10, 'bold'))
        casualDeleteLabel.grid(row=5, column=0, columnspan=2, pady=10)

        #delete food review button
        estabDeleteButton = tk.Button(self, text="Go", command=lambda: controller.show_frame(ReviewDelete))
        estabDeleteButton.grid(row=6, column=0, columnspan=2, pady=5)
        
        #route to Reports page
        reportsLabel = tk.Label(self, text='Reports', font=('calibre', 10, 'bold'))
        reportsLabel.grid(row=7, column=0, pady=5)
        reportsBtn = tk.Button(self, text = 'Go', command=lambda: controller.show_frame(ReportsPage))
        reportsBtn.grid(row=7, column=1, columnspan=2, pady=5)

class ItemReviewAdd(tk.Frame):  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

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

    def addReview(self):
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

class EstabReviewAdd(tk.Frame):  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

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

class ReviewUpdate(tk.Frame):  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

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

class ReviewDelete(tk.Frame):  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #only need the review id for deletion
        self.review_id = tk.IntVar()

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
            global dbConn
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
                    dbConn.close()

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
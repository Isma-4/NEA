import tkinter as tk #Library used for creating a GUI
from tkinter import messagebox #Fetch all resources from the library
from tkinter import * 
import sqlite3 #Library used to embed an SQL database into the python program
import uuid #Universally Unique Identifiers - Will be used to create the ID (Primary key) for the user

class GUI():
    def __init__(self):
        self.setupTables() #Calls the method to create the database tables
        self.root = Tk()
        self.root.resizable(width=0,height=0) # size change Not allowed 
        self.root.geometry("220x200")
        self.root.title("Login")
        self.login_button = Button(self.root, width=30, height=6, bg="light green", text="[LOGIN]", command=self.login)
        self.login_button.grid(column=1, row=0)
        self.cnu_button = Button(self.root, width=30, height=6, bg="light blue", text="[SIGN UP]", command=self.signUp)
        self.cnu_button.grid(column=1, row=1)
        self.root.mainloop()

    def setupTables(self):
        self.con = sqlite3.connect("MINI_RPG_NEA_DATABASE.db") #Connects the python program to the sqlite3 database 
        self.cur = self.con.cursor() #Allows for fetching data from query returns and allows for embeded SQL statements within the python code

        #User table
        try: #Tries to create the user table
            self.cur.execute('''CREATE TABLE users (id text, username text, password text)''')
            self.con.commit()
        except: #If table already exists, ignore the error.
            pass

        try: #Tries to create the gamedata table
            self.cur.execute('''CREATE TABLE gamedata (id text, username text, password text)''')
            self.con.commit()
        except: #If table already exists, ignore the error.
            pass
        
    def login(self):
        self.login_button.grid_remove()
        self.cnu_button.grid_remove()

        self.username_label = tk.Label(self.root, text="Username:", width=8, bg="grey")
        self.username_label.grid(column=0, row=0)
        self.password_label = tk.Label(self.root, text="Password:", width=8, bg="grey")
        self.password_label.grid(column=0, row=1)

        self.username_textbox = tk.Text(self.root,width=19, height=1, bg="light green")
        self.username_textbox.grid(column=1, row=0)
        self.password_textbox = tk.Text(self.root,width=19, height=1, bg="light green")
        self.password_textbox.grid(column=1, row=1)

        self.login_button = tk.Button(self.root, text="[LOGIN]", width=22, height=10, bg="light green", command=self.loginVerification)
        self.login_button.grid(column=1, row=2) 

        self.back_button = tk.Button(self.root, text="[BACK]", width=8, height=10, bg="light blue", command=self.back)
        self.back_button.grid(column=0, row=2) 

    def signUp(self):
        self.login_button.grid_remove()
        self.cnu_button.grid_remove()

        self.username_label = tk.Label(self.root, text="Username:", width=8, bg="grey")
        self.username_label.grid(column=0, row=0)
        self.password_label = tk.Label(self.root, text="Password:", width=8, bg="grey")
        self.password_label.grid(column=0, row=1)

        self.username_textbox = tk.Text(self.root,width=19, height=1, bg="light green")
        self.username_textbox.grid(column=1, row=0)
        self.password_textbox = tk.Text(self.root,width=19, height=1, bg="light green")
        self.password_textbox.grid(column=1, row=1)

        self.login_button = tk.Button(self.root, text="[SIGN UP]", width=22, height=10, bg="light green", command=self.signUpVerification)
        self.login_button.grid(column=1, row=2) 

        self.back_button = tk.Button(self.root, text="[BACK]", width=8, height=10, bg="light blue", command=self.back)
        self.back_button.grid(column=0, row=2) 

    def loginVerification(self):
        self.username = self.username_textbox.get("1.0", tk.END)
        self.password = self.password_textbox.get("1.0", tk.END)

        self.res = self.cur.execute("SELECT COUNT('id') FROM users WHERE username='" + self.username + "'")
        if self.res.fetchone()[0] == 1: #Is count of matching username equal to 1? (Does username exist in database?)
            self.res = self.cur.execute("SELECT COUNT('id') FROM users WHERE password='" + self.password + "'")
            if self.res.fetchone()[0] == 1: #Is count of matching password equal to 1? (Does password exist in database?)
                messagebox.showinfo(title="LOG IN", message="Log In Complete, welcome " + self.username)
                self.root.destroy()
            else:
                messagebox.showinfo(title="ERROR", message="Password incorrect")
        else:
            messagebox.showinfo(title="ERROR", message="Username incorrect")

    def signUpVerification(self):
        self.username = self.username_textbox.get("1.0", tk.END)
        self.password = self.password_textbox.get("1.0", tk.END)

        specialChars = ["!","£","$","%","^","&","*","?","#","@"] #List of accepted special chars
        passwordContainsSpecialChar = False #By default this value is set to false
        newUuid = str(uuid.uuid4()) #Creates a new unique identifier which will be used as the primary key for the user

        if len(self.username) >= 4 and len(self.username) <= 20: #Checks if the length of username is valid
            self.res = self.cur.execute("SELECT COUNT('id') FROM users WHERE username='" + self.username + "'") #Returns count of how many IDs match that username in the database
            if self.res.fetchone()[0] == 0: #Is count of matching username equal to 0?
                if len(self.password) >= 4 and len(self.password) <= 12: #Checks if the length of password is valid
                    for char in self.password: #Loop through each character in password
                        if specialChars.count(char) > 0: #Check if the number of times that the current char = one of the special chars is greater than 0
                            passwordContainsSpecialChar = True 
                    if passwordContainsSpecialChar == True: #If entered password contains atleast one special char:
                        self.res = self.cur.execute("SELECT COUNT('id') FROM users WHERE password='" + self.password + "'") #Returns count of how many IDs match that password in the database
                        if self.res.fetchone()[0] == 0: #Is count of matching password equal to 0?
                            self.cur.execute("INSERT INTO users VALUES ('" + newUuid + "','" + self.username + "','" + self.password + "')") #Create new user with the following fields
                            self.con.commit()
                            messagebox.showinfo(title="SIGN UP", message="Sign Up Complete, welcome " + self.username)
                            self.back()


                        else:
                            messagebox.showinfo(title="ERROR", message="Password taken")   
                    else:
                        messagebox.showinfo(title="ERROR", message="Password must containt atleast one of [!,£,$,%,^,&,*,?,#,@]")   
                else:
                    messagebox.showinfo(title="ERROR", message="Password must be between 3 and 12")      
            else:
                messagebox.showinfo(title="ERROR", message="Username taken")
        else:
            messagebox.showinfo(title="ERROR", message="Username must be between 3 and 20 char")

    def back(self):
        self.root.destroy()
        GUI()

GUI()

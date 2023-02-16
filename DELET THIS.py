import tkinter as tk            #Library used for creating a GUI
from tkinter import messagebox  #Fetch all resources from the library
from tkinter import *

root = Tk()                                        #x,y = 96, 96 default
root.resizable(width=0,height=0) # size change Not allowed 
root.geometry("220x200")
root.title("Login")






frame = tk.Frame(root, width=18, height=21 ,bg="black")
frame.grid(column=1, row=0, sticky="nsew")
text = tk.Text(frame, width=18, height=21)
text.grid(column=1, row=0)

scrollbar = tk.Scrollbar(frame, command=text.yview)
scrollbar.grid(column=0, row=0, rowspan=5, sticky="ns" )
text["yscroll"] = scrollbar.set

text.insert(tk.INSERT, "players")

























root.mainloop()
from tkinter import Tk, Button, PhotoImage, Label, LabelFrame, W, E, N, S, Entry, END, StringVar, Scrollbar, Toplevel
from tkinter import ttk # Provides access to tk themed widgets.

class contacts:
    def __init__(self,root): #creating instance having a parameter self
        self.root = root
        self.CreateLeftIcon() #call the function

    def CreateLeftIcon(self):
        photo = PhotoImage(file='icons/CONTACT.gif') #creating variable
        label = Label(image=photo)
        label.image = photo
        label.grid(row=0, column=0)

if __name__ == '__main__':
    root = Tk()
    root.title('My Contacts List')
    application = contacts(root)
    root.mainloop() #to run the application

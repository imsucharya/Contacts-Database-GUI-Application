from tkinter import Tk, Button, PhotoImage, Label, LabelFrame, W, E, N, S, Entry, END, StringVar, Scrollbar, Toplevel
from tkinter import ttk # Provides access to tk themed widgets.
import sqlite3

class contacts:
    db_filename = 'contacts.db'
    
    def __init__(self,root): #creating instance having a parameter self
        self.root = root
        self.CreateGUI() #call the function
        ttk.style = ttk.Style()
        ttk.style.configure("Treeview", font=('Poppins',11))
        ttk.style.configure("Treeview.Heading", font=('Poppins',13,'bold'))

    def ExecuteDBQuery(self, query, parameters=()):
        with sqlite3.connect(self.db_filename) as conn:
            print(conn)
            print('You have successfully connected to the Database')
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result

    def CreateGUI(self):
        self.CreateLeftIcon() 
        self.CreateLabelFrame()
        self.CreateMsgArea( )
        self.CreateTreeView()
        self.CreateScrollBar()
        self.CreateBottomButton()
        self.view_contacts()
        

    def CreateLeftIcon(self):
        photo = PhotoImage(file='icons/CONTACT.gif') 
        label = Label(image=photo)
        label.image = photo
        label.grid(row=0, column=0)

    def CreateLabelFrame(self):
        labelframe = LabelFrame(self.root, text = 'Add New Contact', bg = "#d3cfe8", font = "Poppins 15")
        labelframe.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = 'ew')
        Label(labelframe, text='Name : ', fg = 'black').grid(row=1, column=1, sticky=W, padx=16, pady=3)
        self.namefield = Entry(labelframe)
        self.namefield.grid(row=1,column=2, sticky=W, padx=6, pady=3)
        Label(labelframe, text='Email : ', fg = 'black').grid(row=2, column=1, sticky=W, padx=16, pady=3)
        self.emailfield = Entry(labelframe)
        self.emailfield.grid(row=2,column=2, sticky=W, padx=6, pady=3)
        Label(labelframe, text='Number : ', fg = 'black').grid(row=3, column=1, sticky=W, padx=16, pady=3)
        self.numfield = Entry(labelframe)
        self.numfield.grid(row=3,column=2, sticky=W, padx=6, pady=3)
        Button(labelframe, text='Add Contact', command=self.OnAddContactButtonClicked, bg="#1a191f",fg="white", bd="3").grid(row=4, column=2, sticky=E, padx=5, pady=5)

    def CreateMsgArea(self):
        self.message = Label(text='', fg='red')
        self.message.grid(row=3, column=1, sticky=W)

    def CreateTreeView(self):
        self.tree = ttk.Treeview(height=10, columns = ("email","number"), style='Treeview')
        self.tree.grid(row=6, column=0, columnspan=3)
        self.tree.heading('#0', text='Name', anchor=W)
        self.tree.heading("email", text='Email Address', anchor=W)
        self.tree.heading("number", text='Contact Number', anchor=W)

    def CreateScrollBar(self):
        self.scrollbar = Scrollbar(orient='vertical', command=self.tree.yview)
        self.scrollbar.grid(row=6,column=3,rowspan=10,sticky='sn')

    def CreateBottomButton(self):
        Button(text='Delete Selected', command=self.OnDeleteSelectedButtonClicked, bg="red", fg="white").grid(row=8, column=0, sticky=W, pady=10, padx=20)
        Button(text='Modify Selected', command=self.OnModifySelectedButtonClicked, bg="#695da3", fg="white").grid(row=8, column=1, sticky=W)
    

    def OnAddContactButtonClicked(self):
        self.AddNewContact()

    def OnDeleteSelectedButtonClicked(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'No item selected to delete'
            return
        self.delete_contacts()


    def OnModifySelectedButtonClicked(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'No item selected to modify'
            return
        self.open_modify_window()

        
    def AddNewContact(self):
        if self.new_contacts_validated():
            query = 'INSERT INTO contact_list VALUES(NULL,?,?,?)'
            parameters = (self.namefield.get(), self.emailfield.get(), self.numfield.get())
            self.ExecuteDBQuery(query, parameters)
            self.message['text'] = 'New Contact {} added'.format(self.namefield.get())
            self.namefield.delete(0, END)
            self.emailfield.delete(0, END)
            self.numfield.delete(0, END)
        
        else:
            self.message['text'] = 'Name,Email and nNumber cannot be blank'
            self.view_contacts()


    def new_contacts_validated (self):
        return len(self.namefield.get()) != 0 and len(self.emailfield.get()) != 0 and len(self.numfield.get()) != 0

    
    def view_contacts(self):
        items = self.tree.get_children()
        for item in items:
            self.tree.delete(item)
        query = 'SELECT * FROM contact_list ORDER BY name desc'
        contact_entries = self.ExecuteDBQuery(query)
        for row in contact_entries:
            self.tree.insert('', 0, text=row[1], values=(row[2], row[3]))


    def delete_contacts(self):
       self.message['text'] = ''
       name = self.tree.item(self.tree.selection())['text']
       query = 'DELETE FROM contact_list WHERE name = ?'
       self.ExecuteDBQuery(query, (name,))
       self.message['text'] = 'Contacts for {} deleted'.format(name)
       self.view_contacts()

    def open_modify_window(self):
        name = self.tree.item(self.tree.selection())['text']
        old_number = self.tree.item(self.tree.selection())['values'][1]
        self.transient = Toplevel()
        self.transient.title('Update Contact')
        Label(self.transient, text='Name:').grid(row=0, column=1)
        Entry(self.transient, textvariable=StringVar(
            self.transient, value=name), state='readonly').grid(row=0, column=2)
        Label(self.transient, text='Old Contact Number').grid(row=1, column=1)
        Entry(self.transient, textvariable=StringVar(
            self.transient, value=old_number), state='readonly').grid(row=1, column=2)

        
        Label(self.transient, text='New Phone Number:').grid(row=2, column=1)
        new_phone_number_entry_widget = Entry(self.transient)
        new_phone_number_entry_widget.grid(row=2, column=2)

        Button(self.transient, text='Update Contact', command=lambda: self.update_contacts(new_phone_number_entry_widget.get(), old_number, name)).grid(row=3, column=2, sticky=E)

        self.transient.mainloop()


    def update_contacts(self, newphone, old_phone, name):
        query = 'UPDATE contact_list SET number = ? WHERE number = ? AND name = ?'
        parameters = (newphone, old_phone, name)
        self.ExecuteDBQuery(query, parameters)
        self.transient.destroy()
        self.message['text'] = 'Phone number of {} is modified'.format(name)
        self.view_contacts()



if __name__ == '__main__':
    root = Tk()
    root.title('My Contacts List')
    root.resizable(width=False, height=False)
    application = contacts(root)
    root.mainloop() #to run the application

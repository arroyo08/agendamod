import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

connection = mysql.connector.connect(host='127.0.0.1', user='root', port='3306', password='Arroyo_2025#', database='agenda_py')

c = connection.cursor()

usuarios = []

USER_CREDENTIALS = {"admin": "1234", "empl": "5678"}

def login():
    username = entry_user.get().strip()
    password = entry_pass.get().strip()
    
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        login_window.destroy()
        main_app()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")


def main_app():
    global root, entry_id, entry_fname, entry_lname, entry_email, entry_phone, trv
    root = Tk()

    frame = tk.Frame(root)
    frame_btns = tk.Frame(frame)

    label_id = tk.Label(frame, text="ID:", font=('verdana',14))
    entry_id = tk.Entry(frame, font=('verdana',14))

    label_fname = tk.Label(frame, text="First Name:", font=('verdana',14))
    entry_fname = tk.Entry(frame, font=('verdana',14))

    label_lname = tk.Label(frame, text="Last Name:", font=('verdana',14))
    entry_lname = tk.Entry(frame, font=('verdana',14))

    label_email = tk.Label(frame, text="Email:", font=('verdana',14))
    entry_email = tk.Entry(frame, font=('verdana',14))

    label_phone = tk.Label(frame, text="Phone Number:", font=('verdana',14))  
    entry_phone = tk.Entry(frame, font=('verdana',14))

    button_add = tk.Button(frame_btns, text="Add", font=('verdana',14), bg='green', fg='#ffffff')
    button_edit = tk.Button(frame_btns, text="Edit", font=('verdana',14), bg='blue', fg='#ffffff')
    button_remove = tk.Button(frame_btns, text="Remove", font=('verdana',14), bg='red', fg='#ffffff')
    button_search = tk.Button(frame_btns, text="Search", font=('verdana',14), bg='orange', fg='#ffffff')

    trv = ttk.Treeview(frame, columns=(1,2,3,4,5), height=15, show="headings")
    trv.column(1, anchor=CENTER, stretch=NO, width=100)
    trv.column(2, anchor=CENTER, stretch=NO, width=100)
    trv.column(3, anchor=CENTER, stretch=NO, width=100)
    trv.column(4, anchor=CENTER, stretch=NO, width=100)
    trv.column(5, anchor=CENTER, stretch=NO, width=100)

    trv.heading(1, text="ID")
    trv.heading(2, text="First Name")
    trv.heading(3, text="Last Name")
    trv.heading(4, text="Email")
    trv.heading(5, text="Phone Number")  

    def add():
        user_id=  entry_id.get().strip()
        fname = entry_fname.get().strip() 
        lname = entry_lname.get().strip()
        email = entry_email.get().strip()
        phone = entry_phone.get().strip()  

        vals = (user_id,fname,lname,email,phone)

        if(len(user_id) > 0 and len(fname) > 0 and len(lname) > 0 and len(email) > 0 and len(phone) > 0): 
            c.execute("INSERT INTO `users_2`(`user_id`,`firstname`, `lastname`, `email`, `phone`) VALUES (%s,%s,%s,%s,%s)", vals)  
            connection.commit()
            messagebox.showinfo('Add','User Info Has Been Added')
            displayUsers()
        else:
            messagebox.showwarning('Add','Incorrrect Data')


    def edit():
        user_id = entry_id.get().strip()
        fname = entry_fname.get().strip()
        lname = entry_lname.get().strip()
        email = entry_email.get().strip()
        phone = entry_phone.get().strip()  

        if(len(user_id) > 0 and len(fname) > 0 and len(lname) > 0 and len(email) > 0 and len(phone) > 0): 
            vals = (fname,lname,email,phone,user_id)
            c.execute("UPDATE `users_2` SET `firstname`=%s,`lastname`=%s,`email`=%s,`phone`=%s WHERE `user_id`=%s", vals)  
            connection.commit()
            messagebox.showinfo('Edit','User Info Has Been Edited')
            displayUsers()
        else:
            messagebox.showwarning('Edit','Incorrrect Data')

    def remove():
        user_id = entry_id.get().strip()
        c.execute("DELETE FROM `users_2` WHERE `user_id` = " + user_id)
        connection.commit()
        messagebox.showinfo('Delete','User Info Has Been Deleted')
        displayUsers()

    def search():
        user_id = entry_id.get().strip()
        c.execute("SELECT * FROM `users_2` WHERE `user_id` = " + user_id)
        user = c.fetchone()
        entry_fname.delete(0, END)
        entry_lname.delete(0, END)
        entry_email.delete(0, END)
        entry_phone.delete(0, END)  
        
        if user:
            entry_fname.insert(0, user[1])
            entry_lname.insert(0, user[2])
            entry_email.insert(0, user[3])
            entry_phone.insert(0, user[4])  
        else:
            messagebox.showwarning('User','No User Found')
        

    def displayUsers():
        for row in trv.get_children():
            trv.delete(row)
        
        c.execute("SELECT * FROM `users_2`")
        users = c.fetchall()

        for user in users:
            trv.insert('', END, values=user)
            
    button_add['command'] = add
    button_edit['command'] = edit
    button_remove['command'] = remove
    button_search['command'] = search

    displayUsers()

    label_id.grid(row=0, column=0, sticky='e')
    entry_id.grid(row=0, column=1)

    label_fname.grid(row=1, column=0, sticky='e')
    entry_fname.grid(row=1, column=1)

    label_lname.grid(row=2, column=0, sticky='e')
    entry_lname.grid(row=2, column=1)

    label_email.grid(row=3, column=0, sticky='e')
    entry_email.grid(row=3, column=1)

    label_phone.grid(row=4, column=0, sticky='e')
    entry_phone.grid(row=4, column=1)

    frame_btns.grid(row=5, column=0, columnspan=2)
    button_add.grid(row=0, column=0, padx=10, pady=10)
    button_edit.grid(row=0, column=1, padx=10, pady=10)
    button_remove.grid(row=0, column=2, padx=10, pady=10)
    button_search.grid(row=0, column=3, padx=10, pady=10)


    trv.grid(row=0, column=3, rowspan=5, padx=10, pady=10)

    frame.grid(row=0, column=0)

    root.mainloop()        

login_window = Tk()
login_window.title("Login")

Label(login_window, text="Username:").grid(row=0, column=0)
entry_user = Entry(login_window)
entry_user.grid(row=0, column=1)

Label(login_window, text="Password:").grid(row=1, column=0)
entry_pass = Entry(login_window, show="*")
entry_pass.grid(row=1, column=1)

Button(login_window, text="Login", command=login).grid(row=2, column=0, columnspan=2)

login_window.mainloop()
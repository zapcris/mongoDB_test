from dataclasses import dataclass

import pymongo
from pymongo import MongoClient, errors
import sys
from tkinter import *
from ttkbootstrap.constants import *
from tkinter import StringVar, messagebox
import pandas as pd
import tkinter as tk



# cluster = "mongodb+srv://akshayavhad89:akshay@cluster0.w9kab.mongodb.net/swarm_production?retryWrites=true&w=majority"
# client = MongoClient(cluster)
#
# print(client.list_database_names())
#
# db = client.swarm_production
#
# print(db.list_collection_names())

@dataclass
class PI:
    p_variant: str
    p_qty: int
    cust_name: str


global pV_entry, seq_entry, pI_entry, pQty_entry, cName_entry, clicked, drop, product_variants, orderlist, batch_order

orders = {}
batch_order = {}
orderlist = []
dummylist= [ 1, 2, 3, 4, 5]

def database():
    try:
        # replace username and password into your details
        cluster = "mongodb+srv://akshayavhad89:akshay@cluster0.w9kab.mongodb.net/swarm_production?retryWrites=true&w=majority"


        client = MongoClient(cluster)
        db = client.swarm_production
        # db = client.your_database_name  #other way to create database
        collection = db.orderlist  # create a collection from the database
        return collection  # return database so that functions from button can perform CRUD operation
    except errors.ConfigurationError:
        # database can be accessed only if you have active internet connection, this will prompt user the error,
        # if user is not connected to internet
        print(errors.ConfigurationError)
        messagebox.showerror("Network Error", "No internet connection")


def database2():
    try:
        # replace username and password into your details
        cluster = "mongodb+srv://akshayavhad89:akshay@cluster0.w9kab.mongodb.net/swarm_production?retryWrites=true&w=majority?"
        client = MongoClient(cluster, tls=True, tlsAllowInvalidCertificates=True)
        db = client.swarm_production
        # db = client.your_database_name  #other way to create database
        collection = db.productList  # create a collection from the database

        print("list of collections:", collection)
        return collection  # return database so that functions from button can perform CRUD operation
    except errors.ConfigurationError:
        # database can be accessed only if you have active internet connection, this will prompt user the error,
        # if user is not connected to internet
        messagebox.showerror("Network Error", "No internet connection")


def insert_db():
    document = dict()
    # get the entered details from the user
    document['name'] = pV_entry.get()
    document['sequence'] = seq_entry.get()

    # call the database function and get the collection, so that you can perform C-create/insert operation
    collect = database2()
    collect.insert_one(document)
    messagebox.showinfo("Sucess", "Data Inserted")
    clear()


def insert_order():
    document = dict()
    collect = database()
    collect.insert_one(batch_order)
    messagebox.showinfo("Sucess", "Batch Order Created ")
    clear_orders()


def create_bOrder():
    batch_order['order_no'] = nbatch_entry.get()
    batch_order['order_list'] = orderlist
    insert_order()
    nbatch_entry.delete(0, "end")


def delete_db():
    document = dict()
    document['name'] = pV_entry.get()
    document['sequence'] = seq_entry.get()
    collect = database()

    # call the database function and get the collection, so that you can perform D-delete operation
    collect.delete_one(document)
    messagebox.showinfo("Sucess", "Data Deleted")
    clear()


# this function is used to clear the entry box once the data is inserted and deleted
def clear():
    pV_entry.delete(0, "end")
    seq_entry.delete(0, "end")
    pV_entry.focus_set()


def clear_orders():
    pQty_entry.delete(0, "end")
    cName_entry.delete(0, "end")
    clicked.set(None)


def enlist():
    try:
        # replace username and password into your details
        cluster = "mongodb+srv://akshayavhad89:akshay@cluster0.w9kab.mongodb.net/swarm_production?retryWrites=true&w=majority"
        client = MongoClient(cluster)
        db = client.swarm_production
        # db = client.your_database_name  #other way to create database
        collection = db.productList.distinct("name")  # create a collection from the database
        # print("array from product names:", collection)

        return collection  # return database so that functions from button can perform CRUD operation
    except errors.ConfigurationError:
        # database can be accessed only if you have active internet connection, this will prompt user the error,
        # if user is not connected to internet
        print(errors.ConfigurationError)
        messagebox.showerror("Network Error", "No internet connection")


def correspnd_sequence():
    # global product_variants
    global product_sequence
    global product_dict

    cluster = "mongodb+srv://akshayavhad89:akshay@cluster0.w9kab.mongodb.net/swarm_production?retryWrites=true&w=majority"
    client = MongoClient(cluster)
    db = client.swarm_production
    # cursor = db.productList.find({"name: 12"})
    mycol = db.productList.find()

    for x in mycol:
        product_sequence.append(x['sequence'])
        product_dict[x['name']] = x['sequence']

    #
    print(str(product_dict.get('12')))


def close():
    # win.destroy()
    root.quit()


# Change the label text
def show():
    correspnd_sequence()
    label_pSelected.config(text=clicked.get())
    label2.config(text=product_dict.get(clicked.get()))
    orders['PI'] = clicked.get()
    orders['Sequence'] = product_dict.get(clicked.get())
    orders['Qty'] = pQty_entry.get()
    orders['Customer'] = cName_entry.get()

    order_copy = orders.copy()
    orderlist.append(order_copy)
    print(orderlist)
    clear_orders()


def refresh_dropdown():
    # Reset var and delete all old options
    clicked.set(None)
    drop['menu'].delete(0, "end")
    # Insert list of new options (tk._setit hooks them up to var)
    new_variants = enlist()
    for variant in new_variants:
        drop['menu'].add_command(label=variant, command=tk._setit(clicked, variant))


product_variants = enlist()
product_sequence = []
product_dict = {}

# create a Tkinter GUI application
root = tk.Tk()
root.geometry('830x360+810+200')
root.title("Swarm Production order")
root.resizable(False, False)

# canvas widget is used to design tkinter GUI, you can add background image, bg color, good scroll bar and etc..
canvas = tk.Canvas(bg="green")
canvas.place(x=-1, y=-1, width=440, height=460)

canvas2 = tk.Canvas(bg="black")
canvas2.place(x=440, y=-1, width=440, height=460)

# I suppose this is self-explanary
label_PV = tk.Label(text="Product variant :", font=("arial", 15, "bold")).place(x=10, y=50)
label_seq = tk.Label(text="Sequence:", font=("arial", 15, "bold")).place(x=10, y=110)
label_PI = tk.Label(text="Instance:", font=("arial", 15, "bold")).place(x=450, y=50)
label_qty = tk.Label(text="Qty", font=("arial", 15, "bold")).place(x=500, y=110)
label_cname = tk.Label(text="Customer", font=("arial", 15, "bold")).place(x=450, y=170)
label_cname = tk.Label(text="Batch name", font=("arial", 15, "bold")).place(x=450, y=230)

pV_var = tk.StringVar()
seq_var = tk.StringVar()
pI_var = tk.StringVar()
qty_var = tk.StringVar()
cname_var = tk.StringVar()
nbatch_var = tk.StringVar()

# get user details to store in database
pV_entry = tk.Entry(bd=5, textvariable=pV_var, bg="yellow")
pV_entry.place(x=180, y=45, width=220, height=45)

seq_entry = tk.Entry(bd=5, textvariable=seq_var, bg="yellow")
seq_entry.place(x=180, y=105, width=220, height=45)

# pI_entry = tk.Entry(bd=5,textvariable=pI_var,bg="yellow")
# pI_entry.place(x=580,y=45,width=220,height=45)

pQty_entry = tk.Entry(bd=5, textvariable=qty_var, bg="yellow")
pQty_entry.place(x=580, y=105, width=220, height=45)

cName_entry = tk.Entry(bd=5, textvariable=cname_var, bg="yellow")
cName_entry.place(x=580, y=165, width=220, height=45)

nbatch_entry = tk.Entry(bd=5, textvariable=nbatch_var, bg="yellow")
nbatch_entry.place(x=580, y=225, width=220, height=45)

# create two buttons for insertion and deletetion operation
insert_btn = tk.Button(bd=4, bg="blue", fg="white", command=insert_db, text="Insert order",
                       font=("arial", 15, "bold")).place(x=120, y=200)
delete_btn = tk.Button(bd=4, bg="blue", fg="white", command=delete_db, text="Delete", font=("arial", 15, "bold")).place(
    x=250, y=200)
load_btn = tk.Button(bd=4, bg="blue", fg="white", command=refresh_dropdown, text="Update product list",
                     font=("arial", 11, "bold")).place(x=280, y=300)
cOrder_btn = tk.Button(bd=4, bg="blue", fg="white", command=create_bOrder, text="Create Order",
                       font=("arial", 15, "bold")).place(x=680, y=300)
pSelect_btn = tk.Button(root, text="Load the Instance", command=show).place(x=720, y=10)

# datatype of menu text
clicked = StringVar(root)
# initial menu text
clicked.set(None)

# Create Dropdown menu
drop = tk.OptionMenu(root, clicked, *dummylist)
drop.place(x=700, y=60)

# Create Label
label_pSelected = Label(root, text=" ")
label_pSelected.place(x=600, y=50)

# label = Label(text=" ", font=("arial", 15, "bold")).place(x=700, y=50)
# label.pack()

label2 = Label(root, text=" ")
label2.place(relx=0.0, rely=1.0, anchor='sw')
label2.pack()

root.mainloop()

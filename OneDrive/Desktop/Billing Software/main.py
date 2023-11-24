from datetime import date , datetime
import os , re
import sqlite3
from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk #pip install pillow
import random
from tkinter import messagebox
import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD
import win32print
import win32api
from tkinter import filedialog
# import pandas as pd
# import tensorflow as tf
# import numpy as np
# import sklearn
# from sklearn.decomposition import TruncatedSVD

class Database :
      
      def __init__(self , conn , crsr ):
            self.conn = conn
            self.crsr = crsr
      
      def customer(self):
            customer_table = '''
                  CREATE TABLE IF NOT EXISTS customers (
                        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_name VARCHAR(255),
                        customer_mobile VARCHAR(255),
                        customer_email VARCHAR(255)
                        )'''
            self.crsr.execute(customer_table)   
            self.conn.commit()
            
      def customer_values(self , name , email , mobile ):
            query = f'''INSERT INTO customers (customer_name , customer_email ,customer_mobile)
                        VALUES('{name}' ,'{email}' , '{mobile}' )'''
            self.crsr.execute(query)
            self.conn.commit()
            
            return self.crsr.lastrowid
      
      def product(self):
            product_table = '''
                  CREATE TABLE IF NOT EXISTS products (
                        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        category VARCHAR(255),
                        sub_category VARCHAR(255),
                        product_name VARCHAR(255),
                        price DECIMAL(10, 2),
                        quantity INTEGER
                        )
                        '''
            self.crsr.execute(product_table)
            self.conn.commit() 
      
      def product_values(self,category, sub_cat , product , price , qty):
            query = '''
            INSERT INTO products (category, sub_category, product_name, price, quantity)
            VALUES (?, ?, ?, ?, ?)
            '''
            values = (category, sub_cat, product, price, qty)
            
            try:
                  self.crsr.execute(query, values)
                  self.conn.commit()
                  messagebox.showinfo("Success", "Product Added Successfully")
            except sqlite3.Error as e:
                  messagebox.showerror("Error", f"Error adding product: {str(e)}") 
      
      def billtable(self):
            bill_table = '''
                  CREATE TABLE IF NOT EXISTS bills (
                        bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_id INTEGER,
                        bill_date DATE,
                        total_amount DECIMAL(10, 2),
                        invoice_number varchar(20) UNIQUE,
                        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                        )'''
            self.crsr.execute(bill_table)
            self.conn.commit()
      
      def bill_values(self, invoice_number, c_id , bill_date,  total_bill ):
            query = "INSERT INTO bills (invoice_number, customer_id, bill_date, total_amount) VALUES (? , ? , ? , ?)"
            bill_data = (invoice_number, c_id, bill_date, total_bill)

            self.crsr.execute(query, bill_data)
            self.conn.commit() 
            return self.crsr.lastrowid
      
      def billitems(self):
            bill_items = '''
                  CREATE TABLE IF NOT EXISTS bill_items (
                        bill_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        bill_id INTEGER,
                        product_id INTEGER,
                        quantity INTEGER,
                        FOREIGN KEY (bill_id) REFERENCES bills(bill_id),
                        FOREIGN KEY (product_id) REFERENCES products(product_id)
                        )'''
            self.crsr.execute(bill_items)
            self.conn.commit()
            
      def bill_items_entry(self , bill_id , p_id , qty):
            query = f"INSERT INTO bill_items (bill_id, product_id, quantity) VALUES ({bill_id}, {p_id}, {qty})" 
            self.crsr.execute(query)
            self.conn.commit()
            
      
      def earasedata(self):
            q = 'DELETE FROM customers'
            self.crsr.execute(q)
            q = 'DELETE FROM bills'
            self.crsr.execute(q)
            self.conn.commit()
      
      def print_customer(self):
            sql = '''
            SELECT * FROM customers'''
            self.crsr.execute(sql)
            result = self.crsr.fetchall()
            print(result)
      
      def printbill(self):
            sql = "select * from bills"
            self.crsr.execute(sql)
            print(self.crsr.fetchall())
      
      def printbillitmes(self):
            sql = "select * from bill_items"
            self.crsr.execute(sql)
            print(self.crsr.fetchall())
            
      def purchaseHistory(self , customer_id=0):
            query = f'''
            SELECT
                  b.invoice_number,
                  b.bill_id,
                  b.bill_date,
                  p.product_name,
                  bi.quantity,
                  p.price,
                  b.total_amount
            FROM
                  bills AS b
            JOIN
                  bill_items AS bi ON b.bill_id = bi.bill_id
            JOIN
                  products AS p ON bi.product_id = p.product_id
            WHERE
                  b.customer_id = {customer_id}
            '''

            # Execute the query
            self.crsr.execute(query)

            # Fetch the results
            purchase_history = self.crsr.fetchall()
            

            # # Print or process the purchase history data as needed
            # for row in purchase_history:
            #       bill_id , bill_date, product_name, quantity, price , total = row
            #       print(f"Bill Id: {bill_id} , Date: {bill_date}, Product: {product_name}, Quantity: {quantity}, Price: {price}")
            
            return purchase_history
                  

            # query = f'''
            #             SELECT COUNT(*) as count_value 
            #             FROM customers
            #             WHERE customer_email = 'shaikjavid8640@gmail.com';
            #             '''
                  
                  
      def get_customer_product_purchase_data(self):
            query = '''
                  SELECT
                        c.customer_id AS customer_id,
                        p.product_id AS product_id,
                        bi.quantity AS quantity
                  FROM
                        customers AS c
                  JOIN
                        bills AS b ON c.customer_id = b.customer_id
                  JOIN
                        bill_items AS bi ON b.bill_id = bi.bill_id
                  JOIN
                        products AS p ON bi.product_id = p.product_id
            '''

            self.crsr.execute(query)
            result = self.crsr.fetchall()

            # Print or process the retrieved data as needed
            for row in result:
                  customer_id, product_id, quantity = row
                  print(f"Customer ID: {customer_id}, Product ID: {product_id}, Quantity: {quantity}")
            return result
      
      def getProduct(self , id):
            query = f'''SELECT product_name from products where product_id={id};'''
            self.crsr.execute(query)
            return self.crsr.fetchall()
      
      def products(self):
            query = f'''SELECT * from products'''
            self.crsr.execute(query)
            return self.crsr.fetchall()
      
      def search_product(self , search_query ):
            query = f'''
                  SELECT * FROM products
                  WHERE product_id = ? OR LOWER(category) LIKE LOWER(?) OR LOWER(sub_category) LIKE LOWER(?) OR LOWER(product_name) LIKE LOWER(?)
            '''
            search_query = '%' + search_query.lower() + '%'  # Adding wildcards for partial matching in lowercase
            self.crsr.execute(query, (search_query,search_query, search_query, search_query))
            product = self.crsr.fetchall()
            return product
      
      def update_product_details(self, pid , new_category, new_subcategory, new_product_name, new_price, new_quantity):
            query = f'''
            UPDATE products
            SET category = ?,
                  sub_category = ?,
                  product_name = ?,
                  price = ?,
                  quantity = ?
            WHERE product_id = ?
            '''
            self.crsr.execute( query , (new_category, new_subcategory, new_product_name, new_price, new_quantity, pid))
            self.conn.commit()
            return None
      
      def delete_product(self , pid):
            query = f'''DELETE FROM products WHERE product_id = ? ;'''
            try:
                  self.crsr.execute(query , (pid,))
                  self.conn.commit()
                  messagebox.showinfo("Success", "Product deleted Successfully")
            except sqlite3.Error as e:
                  messagebox.showerror("Error", f"Error deleting product: {str(e)}") 
                  
                  
      # user management           
      def users(self):
            query = f'''SELECT * FROM customers'''
            self.crsr.execute(query)
            return self.crsr.fetchall()
      
      def delete_user(self , uid):
            query = f'''DELETE FROM customers WHERE customer_id = ? ;'''
            try :
                  self.crsr.execute(query, (uid, ))
                  self.conn.commit()
                  messagebox.showinfo("Success", "User deleted Successfully")
            except sqlite3.Error as e:
                  messagebox.showerror("Error", f"Error deleting user: {str(e)}")
                  
      def search_user(self, search_query):
            cid = ''
            if search_query.isdigit():
                  cid = int(search_query)
            query = f'''
                  SELECT * FROM customers
                  WHERE customer_id = ? OR LOWER(customer_name) LIKE LOWER(?) OR LOWER(customer_email) LIKE LOWER(?) OR LOWER(customer_mobile) LIKE LOWER(?)
            '''
            search_query = '%' + search_query.lower() + '%'
            self.crsr.execute(query , (cid, search_query , search_query, search_query))
            return self.crsr.fetchall()

class LoginApp(Database):
      
      def __init__(self, login_app):
            self.db = Database(Bill_App.conn , Bill_App.crsr)
            
            self.login_app = login_app
            self.login_app.title("Login")
            
            screen_width = self.login_app.winfo_screenwidth()
            screen_height = self.login_app.winfo_screenheight()
            
            self.canvas = Canvas(self.login_app, width=screen_width, height=screen_height)
            self.canvas.pack()

            
            header = Label(self.canvas , text="Welcome to Billing Software" ,font=("times new roman",35,"bold"),fg="white",bg="orangered" , highlightthickness=0)
            self.canvas.create_window(480 ,20 , anchor="nw", window=header)
            
            img1 = Image.open("Images/loginBg.jpg").resize((screen_width, screen_height))
            self.photoimg = ImageTk.PhotoImage(img1)
            
            # Display the background image on the self.canvas
            self.canvas.create_image(0, 0, image=self.photoimg, anchor="nw")
            self.Login_Frame=Frame(self.login_app,bd=5,relief=GROOVE,bg="orangered")   #bd=Border,relief=border style
            self.Login_Frame.place(x=635,y=100,width=250,height=150)

            #User label
            self.userlabel = Label(self.Login_Frame, text="Enter Username : " , font=("arial sans-serif",8),fg="black",bg="orangered")
            self.userlabel.grid(row=0, column=0, sticky="w", pady=10)

            # user Entry
            self.entry_username = Entry(self.Login_Frame)
            self.entry_username.grid(row=0, column=1, pady=10)

            self.passwdlabel = Label(self.Login_Frame, text="Enter Password:", font=("arial sans-serif", 8), fg="black", bg="orangered")
            self.passwdlabel.grid(row=1, column=0, sticky="w", pady=10)

            self.entry_password = Entry(self.Login_Frame, show="*")
            self.entry_password.grid(row=1, column=1, pady=10)

            self.btn_login = Button(self.Login_Frame, text="Login", command=self.replace_frame, cursor="hand2")
            self.btn_login.grid(row=2, columnspan=2, pady=10)


      def login(self):
            username = self.entry_username.get()
            password = self.entry_password.get()

            # Perform login verification here
            if username == "admin" and password == "admin":
                  self.Login_Frame.place_forget()
                  self.admin_frame()
            else:
                  messagebox.showerror("Login Failed", "Invalid username or password. Please try again!")

      def open_billing_app(self):
            self.login_app.destroy()  # Close the login window
            root = Tk()
            billing_app = Bill_App(root)
            billing_app.run()
            
      def admin_login(self):
            Bill_App.exit_screen(self)
            root = Tk()
            LoginApp(root)
            
      def admin_frame(self):
            self.Main_Frame=Frame(self.login_app,bd=5,relief=GROOVE,bg="skyblue")   #bd=Border,relief=border style
            self.Main_Frame.place(x=10,y=100,width=self.login_app.winfo_screenwidth())
            
            admin_frame = Frame(self.Main_Frame)
            admin_frame.pack()

            # Function to display content for different sections
            def display_section_content(section_name):
                  # print(section_name)
                  # Clear previous content (if any)
                  for widget in admin_frame.winfo_children():
                        widget.destroy() 
                        
                  self.login_app.destroy()
                  root = Tk()
                  if section_name == 'Product Management':
                        ProductManagementApp(root).run()
                  elif "User Management":
                        pass
                  elif section_name == "Pricing and Taxation" :
                        pass
                  elif section_name == "Transaction Monitoring" :
                        pass
                  elif section_name == "Customer Management" :
                        pass
                  elif section_name == "Inventory Management" :
                        pass
                  elif section_name == "Reports and Analytics" :
                        pass
                  elif section_name == "Settings and Configuration" :
                        pass
                  elif section_name == "Security and User Access" :
                        pass
                  elif section_name == "Backup and Restore" :
                        pass
                  elif section_name == "Notifications and Alerts" :
                        pass
                  elif section_name == "Help and Support" :
                        pass
                  elif section_name == "Log and Audit Trails" :
                        pass
                  elif section_name == "Multi-Store Management":
                        pass
                  

            # Create buttons for each admin feature
            admin_features = [
                  "User Management",
                  "Product Management",
                  "Pricing and Taxation",
                  "Transaction Monitoring",
                  "Customer Management",
                  "Inventory Management",
                  "Reports and Analytics",
                  "Settings and Configuration",
                  "Security and User Access",
                  "Backup and Restore",
                  "Notifications and Alerts",
                  "Help and Support",
                  "Log and Audit Trails",
                  "Multi-Store Management"
            ]

            for feature in admin_features:
                  button = Button(admin_frame, text=feature, command=lambda f=feature: display_section_content(f) , cursor='hand2')
                  button.pack(side="left", padx=10 )
               
      def show_option1(self):
            print("Option")
            pass

            
      def replace_frame(self): 
            self.login()
            # self.Login_Frame.place_forget()
      
      def cancel(self):
            self.entry_category.delete(0,END) 
            self.entry_sub_category.delete(0,END)
            self.entry_product.delete(0,END)
            self.entry_price.delete(0,END)
            self.entry_qty.delete(0,END)
            
            
      def save_products(self):
            conn = Bill_App.conn
            crsr = Bill_App.crsr
            
            cat = self.entry_category.get().lower()
            sub_cat = self.entry_sub_category.get().lower()
            pro = self.entry_product.get().lower()
            pri = self.entry_price.get() 
            qty =  self.entry_qty.get()
            
            if cat!="" and sub_cat!="" and pro !="" and pri != "" and int(qty)>=1 :
                  query = '''INSERT INTO products(category ,sub_category , product_name, price ,quantity)
                        VALUES(? , ? , ? , ? ,?)
                        '''
                  values = (cat,sub_cat,pro,pri,qty)
                  crsr.execute(query , values)
                  conn.commit()
                  status = crsr.rowcount
                  if status >0 :
                        messagebox.showinfo("Add Product", "Product has been added sucessfully.")
                  else :
                        messagebox.showerror("Error" , "Failed insert the product.")
            else :
                  messagebox.showerror("No Data","Plese enter the data.")
                  
          
class Bill_App(LoginApp, Database):
      conn = sqlite3.connect('Billing_App.db')
      crsr = conn.cursor()
      db = Database(conn, crsr )
      db.product()
      db.customer()
      db.billitems()
      db.billtable()
      # db.earasedata()
      # db.purschseHistory()
      # db.get_customer_product_purchase_data()
      # db.print_customer()
      # db.printbill()
      # db.printbillitmes()
      db.products()
      # db.product_values('Clothing', 'Shirt','Denim',2000 ,2)
      # db.product_values('Mobiles' , 'OnePlus', 'Nord', 30000 , 1)
      # db.product_values('Mobiles', 'OnePlus', 'One10T' , 90000 , 3)
      #db.product_values('Clothing', 'T-Shirt','polo',1500,2)
      def __init__(self,root) :
            self.root=root
            self.root.geometry("1530x800+0+0")
            self.root.title("Billing Software")
            #...........................Variables..................................
            self.db = Bill_App.db
            
            self.Cust_Name=StringVar()
            self.Cust_Phone=StringVar()
            self.Bill_NO=StringVar()
            z=random.randint(1000,9999)
            self.Bill_NO.set(z)
            self.Cust_Email=StringVar()
            self.Search_Bill=StringVar()
            self.Product=StringVar()
            self.Price=IntVar()
            self.Quantity=IntVar()
            self.Sub_Total=StringVar()
            self.Tax=IntVar()
            self.Total=StringVar()
            self.flag = 0 
            self.total_qty = 0
            self.idx = 16.0
            #Product Catagerory List
            query = 'SELECT DISTINCT category FROM products'
            self.crsr.execute(query)
            rows =  self.crsr.fetchall()

            self.Category=["Select Option"]+ [row[0] for row in rows]
            
            
            # Validation functions
            phone_validation = root.register(self.validate_phone)
            email_validation = root.register(self.validate_email)

#..........................................................................................................................................




#image 1
            img=Image.open("Images/image1.jpg")
            img=img.resize((500,130)) #it convert low level img to high level img
            self.photoimg=ImageTk.PhotoImage(img)

            lb1_img=Label(self.root,image=self.photoimg)
            lb1_img.place(x=500,y=0,width=500,height=130)

#image 2    
            img2=Image.open("Images/Billing2.png")
            img2=img2.resize((500,130), ) #it convert low level img to high level img
            self.photoimg2=ImageTk.PhotoImage(img2)

            lb1_img2=Label(self.root,image=self.photoimg2)
            lb1_img2.place(x=0,y=0,width=500,height=130)
#image 3    
            img3=Image.open("Images/Billing1.png")
            img3=img3.resize((600,130), ) #it convert low level img to high level img
            self.photoimg3=ImageTk.PhotoImage(img3)

            lb1_img3=Label(self.root,image=self.photoimg3)
            lb1_img3.place(x=1000,y=10,width=600,height=130)

            lbl_title=Label(self.root,text="BILLING SOFTWARE",font=("times new roman",38,"bold"),bg="white",fg="red") #where we want to make label we use = root
            lbl_title.place(x=0,y=130,width=1530,height=45)
            
            self.adminLogin=Button(self.root,command=self.admin_login,text="Admin Login",font=("arial",10,"bold"),bg="lightgrey",fg="black",width=13,cursor="hand2")
            self.adminLogin.place(x=1220,y=130,width=130,height=45)
            
            Main_Frame=Frame(self.root,bd=5,relief=GROOVE,bg="white")   #bd=Border,relief=border style
            Main_Frame.place(x=0,y=175,width=1530,height=630)           #to underline text
            
            #Customer label frame
            Cust_Frame=LabelFrame(Main_Frame,text="Customer",font=("times new roman",12,"bold"),bg="white",fg="red")
            Cust_Frame.place(x=10,y=5,width=350,height=150)

            #Name
            self.lblCustName=Label(Cust_Frame,font=("arial",12,"bold"),bg="white",text="Customer Name",bd=4)
            self.lblCustName.grid(row=0,column=0,sticky=W,padx=5,pady=2)

            self.txtCusName=ttk.Entry(Cust_Frame,textvariable=self.Cust_Name,font=("arial",10,"bold"),width=24)
            self.txtCusName.grid(row=0,column=1,sticky=W,padx=5,pady=2)
            
            
            #Mobile Number
            self.lbl_mob=Label(Cust_Frame,text="Mobile Number",font=("times new roman",12,"bold"),bg="white")
            self.lbl_mob.grid(row=1,column=0,sticky=W,padx=5,pady=2) #west

            self.entry_mob=ttk.Entry(Cust_Frame,textvariable=self.Cust_Phone,font=("times new roman",10,"bold"),width=24, validate="key", validatecommand=(phone_validation, '%P'))                                                  #if we want to use any variable we use self
            self.entry_mob.grid(row=1,column=1)

            #Email 
            self.lblEmail=Label(Cust_Frame,font=("arial",12,"bold"),bg="white",text="Email",bd=4)
            self.lblEmail.grid(row=2,column=0,sticky=W,padx=5,pady=2)

            self.txtEmail=ttk.Entry(Cust_Frame,textvariable=self.Cust_Email,font=('arial',10,'bold'),width=24, validate="key", validatecommand=(email_validation, '%P'))
            self.txtEmail.grid(row=2,column=1,sticky=W,padx=5,pady=2)
            
            # Bind callback functions to the entry fields
            self.txtCusName.bind('<KeyRelease>', self.update_textarea)
            self.entry_mob.bind('<KeyRelease>', self.update_textarea)
            self.txtEmail.bind('<KeyRelease>', self.update_textarea)
            
            #Product label frame
            Product_Frame=LabelFrame(Main_Frame,text="Product",font=("times new roman",12,"bold"),bg="white",fg="red")
            Product_Frame.place(x=370,y=5,width=640,height=150)

            #SelectCategory
            self.lblCategory=Label(Product_Frame,font=("arial",12,"bold"),bg="white",text="Select Catageory",bd=4)
            self.lblCategory.grid(row=0,column=0,sticky=W,padx=5,pady=2)
                                                            #To call productCatageory

            self.Combox_Category=ttk.Combobox(Product_Frame,values=self.Category ,font=("arial",10,"bold"),width=24,state="readonly") #Combobox will be in our ttk
            self.Combox_Category.current(0)
            self.Combox_Category.grid(row=0,column=1,sticky=W,padx=5,pady=2)
            self.Combox_Category.bind("<<ComboboxSelected>>",self.Categories)
            #SubCategory
            self.lblSubCategory=Label(Product_Frame,font=("arial",14,"bold"),bg="white",text="Subcatageory",bd=4)
            self.lblSubCategory.grid(row=1,column=0,sticky=W,padx=5,pady=2)

            self.ComboxSubCategory=ttk.Combobox(Product_Frame,value=[""],state="readonly",font=("arial",10,"bold"),width=24)
            self.ComboxSubCategory.grid(row=1,column=1,sticky=W,padx=5,pady=2)
            self.ComboxSubCategory.bind("<<ComboboxSelected>>",self.Product_add)

        #Product Name
            self.lblproduct=Label(Product_Frame,font=("arial",12,"bold"),bg="white",text="Product Name",bd=4)
            self.lblproduct.grid(row=2,column=0,sticky=W,padx=5,pady=2)

            self.ComboxProduct=ttk.Combobox(Product_Frame,textvariable=self.Product,state="readonly",font=("arial",10,"bold"),width=24)
            self.ComboxProduct.grid(row=2,column=1,sticky=W,padx=5,pady=2)
            self.ComboxProduct.bind("<<ComboboxSelected>>",self.price)


            #Price
            self.lblPrice=Label(Product_Frame,font=("arial",12,"bold"),bg="white",text="Prices",bd=4)
            self.lblPrice.grid(row=0,column=2,sticky=W,padx=5,pady=2)

            self.ComboxPrice=ttk.Combobox(Product_Frame,textvariable="hello",state="readonly",font=("arial",10,"bold"),width=24)
            self.ComboxPrice.grid(row=0,column=3,sticky=W,padx=5,pady=2)


            #Quantity
            self.lblQty=Label(Product_Frame,font=("arial",12,"bold"),bg="white",text="Qty",bd=4)
            self.lblQty.grid(row=1,column=2,sticky=W,padx=5,pady=2)

            self.ComboxQty=ttk.Entry(Product_Frame,textvariable=self.Quantity,font=("arial",10,"bold"),width=26)
            self.ComboxQty.grid(row=1,column=3,sticky=W,padx=5,pady=2)

            #Middle Frame
            MiddleFrame=Frame(Main_Frame,bd=10)
            MiddleFrame.place(x=10,y=160,width=990,height=300)

        #image 1
            img12=Image.open("Images/image2.jpg")
            img12=img12.resize((540,380) ) #it convert low level img to high level img
            self.photoimg12=ImageTk.PhotoImage(img12)

            lb1_img12=Label(MiddleFrame,image=self.photoimg12)
            lb1_img12.place(x=0,y=0,width=500,height=340)

#image 2    
            img_13=Image.open("Images/image3.jpg")
            img_13=img_13.resize((540,380)) #it convert low level img to high level img
            self.photoimg_13=ImageTk.PhotoImage(img_13)

            lb1_img_13=Label(MiddleFrame,image=self.photoimg_13)
            lb1_img_13.place(x=490,y=0,width=500,height=340)



        #Search
            Search_Frame=Frame(Main_Frame,bd=2,bg="white")
            Search_Frame.place(x=1010,y=10,width=500,height=40)

            self.lblBill=Label(Search_Frame,font=("arial",12,"bold"),bg="yellow",text="Bill Number",fg="Black")
            self.lblBill.grid(row=0,column=0,sticky=W,padx=1)

            #Entry Click
            self.bill_Entry_Search=ttk.Entry(Search_Frame,textvariable=self.Search_Bill,font=("arial",10,"bold"),width=18)
            self.bill_Entry_Search.grid(row=0,column=1,sticky=W,padx=2)

            #Search Button
            self.BtnSearch=Button(Search_Frame,command=self.find_bill,text="Search",font=("arial",10,"bold"),bg="orangered",fg="white",width=13,cursor="hand2")
            self.BtnSearch.grid(row=0,column=2)

        
        
        #RightFrame Bill Area
            RightLabelFrame=LabelFrame(Main_Frame,text="Bill Area",font=("times new roman",12,"bold"),bg="white",fg="red")
            RightLabelFrame.place(x=1015,y=45,width=350,height=350)

            #scrollBar
            scroll_y=Scrollbar(RightLabelFrame,orient=VERTICAL)
            self.textarea=Text(RightLabelFrame,yscrollcommand=scroll_y.set,bg="white",fg="blue",font=("times new roman",12,"bold"))
            scroll_y.pack(side=RIGHT,fill=Y)
            scroll_y.config(command=self.textarea.yview )
            self.textarea.pack(fill=BOTH,expand=1)
            

        #Bill Counter label frame
            Bottom_Frame=LabelFrame(Main_Frame,text="Bill Counter",font=("times new roman",12,"bold"),bg="white",fg="red")
            Bottom_Frame.place(x=0,y=400,width=1520,height=300)
            
            #SubTotal
            self.lblSubTotal=Label(Bottom_Frame,font=("arial",12,"bold"),bg="white",text="Sub Amount",bd=4)
            self.lblSubTotal.grid(row=0,column=0,sticky=W,padx=5,pady=2)

            self.EntrySubTotal=ttk.Entry(Bottom_Frame,font=("arial",10,"bold"),width=31)
            self.EntrySubTotal.grid(row=0,column=1,sticky=W,padx=5,pady=2)

            #Tax
            self.lbl_tax=Label(Bottom_Frame,font=("arial",12,"bold"),bg="white",text="Gov Tax",bd=4)
            self.lbl_tax.grid(row=1,column=0,sticky=W,padx=5,pady=2)

            self.tax_entry=ttk.Entry(Bottom_Frame,font=("arial",12,"bold"),width=24)
            self.tax_entry.grid(row=1,column=1,sticky=W,padx=5,pady=2)


        #Total
            self.lblAmountTotal=Label(Bottom_Frame,font=("arial",12,"bold"),bg="white",text="Total",bd=4)
            self.lblAmountTotal.grid(row=2,column=0,sticky=W,padx=5,pady=2)

            self.txtAmountTotal=ttk.Entry(Bottom_Frame,font=("arial",12,"bold"),width=24)
            self.txtAmountTotal.grid(row=2,column=1,sticky=W,padx=5,pady=2)
                        
            #Button Frame
            Btn_Frame=Frame(Bottom_Frame,bd=20,bg="white")
            Btn_Frame.place(x=560,y=0)

            self.BtnAddToCart=Button(Btn_Frame,command=self.AddItem,height=2,text="Add To Cart",font=("arial",12,"bold"),bg="orangered",fg="white",width=15,cursor="hand2")
            self.BtnAddToCart.grid(row=0,column=0)

        
            self.Btngenerate_bill=Button(Btn_Frame,command=self.gen_bill,height=2,text="Generate Bill",font=("arial",12,"bold"),bg="orangered",fg="white",width=15,cursor="hand2")
            self.Btngenerate_bill.grid(row=0,column=1)



            self.BtnPrint=Button(Btn_Frame,command=self.iprint,height=2,text="Print",font=("arial",12,"bold"),bg="orangered",fg="white",width=15,cursor="hand2")
            self.BtnPrint.grid(row=0,column=3)


            self.BtnClear=Button(Btn_Frame, command=self.clear ,height=2,text="Clear",font=("arial",12,"bold"),bg="orangered",fg="white",width=15,cursor="hand2")
            self.BtnClear.grid(row=0,column=4)


            self.BtnExit=Button(Btn_Frame,command=self.exit_screen , height=2,text="Exit",font=("arial",12,"bold"),bg="orangered",fg="white",width=15,cursor="hand2")
            self.BtnExit.grid(row=0,column=5)
#...........................................................................................................................................
            self.welcome(self.Bill_NO.get() ,self.Cust_Name.get() , self.Cust_Phone.get() , self.Cust_Email.get() ) # for welcome fun (page) 
            self.total_price = 0 #To add items
            self.products = {}  #To add prducts into the cart
            
      def welcome(self , bill_no , cust_num , phone_num , email):
            self.textarea.delete(1.0,END) #textarea is a variable name
            self.textarea.insert(END,"\t Welcome To Our Store")
            self.textarea.insert(END,f"\n Bill Number: {bill_no}")
            self.textarea.insert(END,f"\n Customer Name: {cust_num}")
            self.textarea.insert(END,f"\n Phone Number: {phone_num}")
            self.textarea.insert(END,f"\n Email: {email}")
            self.textarea.insert(END,"\n===================================")
            self.textarea.insert(END,f"\n Products\t\tQTY\t\tPrice")
            self.textarea.insert(END,"\n===================================\n")        
            self.textarea.config(state=DISABLED)
      
      # Product window 
      def update_textarea(self, event):
            # Clear the existing content in the Textarea
            self.textarea.config(state=NORMAL)
            self.textarea.delete(1.0, END)

            # Retrieve values from entry fields
            bill_no = self.Bill_NO.get()
            cust_name = self.Cust_Name.get()
            phone_num = self.Cust_Phone.get()
            email = self.Cust_Email.get()
            
            # Update the Textarea with the new values
            self.textarea.insert(END, f"\t Welcome To Our Store")
            self.textarea.insert(END,f"\n Bill Number: {bill_no}")
            self.textarea.insert(END, f"\n Customer Name: {cust_name}")
            self.textarea.insert(END, f"\n Phone Number: {phone_num}")
            self.textarea.insert(END, f"\n Email: {email}")
            self.textarea.insert(END, "\n===================================")
            self.textarea.insert(END, f"\n Products\t\tQTY\t\tPrice")
            self.textarea.insert(END, "\n===================================\n")
            self.textarea.config(state=DISABLED)
      
      def replace_row(self , search_text):
      # Find the index of the search_text in the Text widget
            start_index = self.textarea.search(search_text, "1.0", "end", nocase=True)

            if start_index:
                  # Get the line number of the found index
                  line_number, _ = start_index.split(".")

                  # Calculate the start and end indices of the entire row
                  start_row_index = f"{line_number}.0"
                  end_row_index = f"{line_number}.end"

                  # Delete the entire row
                  self.textarea.delete(start_row_index , end_row_index)

                  # Insert the replacement_text at the start of the row
                  return start_row_index
            
      #Validation functions
            
      def validate_phone(self, new_value):
            return new_value.isdigit() or new_value == ""


            


      def validate_email(self, new_value):
            # A simple email validation check
            return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', new_value) is not None or new_value == ""


            
      def AddItem(self):
            self.tax_input=StringVar()
            Tax=1
            if self.Cust_Name.get() == "" or self.Cust_Phone.get() == "":
                  messagebox.showerror("Error" , "Please Enter Customer Details")
            elif self.ComboxProduct.get()=="" or self.ComboxPrice.get()=="" :
                  messagebox.showerror("Error","Please Select A Product")
            else:
                  self.textarea.config(state=NORMAL)
                  self.price = float(self.ComboxPrice.get())
                  self.qty = int(self.ComboxQty.get())
                  self.total_qty += self.qty
                  product = self.Product.get()
                  flag = 0
                  if product in self.products:
                        self.total_price -= self.price*self.products[product]
                        self.products[product]+= self.qty 
                        
                        flag = 1
                  else :
                        self.products[product] = self.qty
                  
                  
                  qty = self.products[product]
                  self.total = self.price*qty
                  self.total_price += self.total
                  
                  if flag :
                        idx = self.replace_row(product)
                        self.textarea.insert(idx, f" {self.Product.get()}\t\t{qty}\t\t{self.total}")
                  else :
                        self.textarea.insert(END, f"\n {self.Product.get()}\t\t{qty}\t\t{self.total}")
                  
                  
                  self.EntrySubTotal.delete(0, END)
                  self.EntrySubTotal.insert(END, str('RS.%.2f'%((self.total_price))))
                  
                  self.tax_entry.delete(0, END)
                  self.tax_entry.insert(END, str('RS.%.2f'%(((((self.total_price)) - (self.Price.get()))*Tax)/100)))
                  
                  self.txtAmountTotal.delete(0,END)
                  self.txtAmountTotal.insert(END, str('RS.%.2f'%((((self.total_price)) + (((((self.total_price)) - (self.Price.get()))*Tax)/100)))))
                  
            
            self.textarea.config(state=DISABLED)
            self.idx = self.textarea.index("end-1c linestart")
            #print(self.idx)
            
            
      def check_printer_connection():
            printer_name = win32print.GetDefaultPrinter()
            printer_info = win32print.GetPrinter(printer_name, 2)
            status = printer_info['Status']
            return status == win32print.PRINTER_STATUS_READY
      
            
      def gen_bill(self):
            
            def generate_invoice_number():
            # Get the current date in the format YYYYMMDD
                  current_date = datetime.now().strftime("%Y%m%d")
                  
                  # Generate a unique identifier (you can use a random number generator or any other method)
                  unique_identifier = random.randint(100000, 999999)  # Generates a random 6-digit number
                  
                  # Combine the prefix, date, and unique identifier
                  invoice_number = f"INV-{current_date}-{unique_identifier}"
                  
                  return invoice_number
      
            if self.Cust_Name.get() != "" and self.Cust_Phone.get() != "":
                  self.textarea.config(state=NORMAL)
                  if self.Product.get()=="" or self.Cust_Name.get() == "" or self.Cust_Phone.get() == "" :
                        messagebox.showerror("Error","Please Add To Cart Product")
                  else:
                        
                        self.textarea.insert(END,f"\n=================================")
                        self.textarea.insert(END,f"\n Sub Amount:\t\t\t{self.EntrySubTotal.get()}")
                        self.textarea.insert(END,f"\n Tax Amount:\t\t\t{self.tax_entry.get()}")
                        self.textarea.insert(END,f"\n Total Amount:\t\t\t{self.txtAmountTotal.get()}")
                        self.textarea.insert(END,f"\n================================")
                        
                        total_bill = self.txtAmountTotal.get()
                        customer_mobile = self.entry_mob.get()
                        
                        query = '''
                              SELECT product_id FROM products WHERE product_name = ?
                              '''
                        p_id_list = []
                        for product in self.products:
                              self.crsr.execute(query, (product,))
                              result = self.crsr.fetchall()
                              if result:
                                    p_id = result[0][0]
                                    p_id_list.append(p_id)
                                    
                        customer_name = self.txtCusName.get()
                        customer_email = self.txtEmail.get()
                        
                        query = f'''
                        SELECT COUNT(*) as count_value 
                        FROM customers
                        WHERE customer_email = '{customer_email}' OR customer_mobile = '{customer_mobile}';
                        '''
                        
                        self.crsr.execute(query)
                        
                        invoice_number = generate_invoice_number()
                        if self.crsr.fetchone()[0]:
                              query = f'''
                              SELECT customer_id FROM customers  
                              WHERE customer_email = '{customer_email}' OR customer_mobile = '{customer_mobile}';
                              '''
                              
                              self.crsr.execute(query)
                              c_id = self.crsr.fetchone()[0]
                              
                              bill_id = self.db.bill_values(invoice_number, c_id , date.today() , total_bill)
                              
                        else :
                              c_id = self.db.customer_values(customer_name ,customer_email, customer_mobile)
                              
                              bill_id = self.db.bill_values(invoice_number,  c_id , date.today() , total_bill)
                        
                        for p_id in p_id_list:
                              self.db.bill_items_entry(bill_id ,p_id , self.qty)
                        
                        
                  self.textarea.config(state=DISABLED)
            else :
                  messagebox.showerror("Error","Please Enter Customer Details")
            
            
      def iprint(self):
            result = messagebox.askquestion("Print Bill", "Do you want to print the bill?")
            if result=='yes':
                  bill_content = self.textarea.get("1.0",END)
                  
                  file_name = "bill.txt"
                  with open(file_name, "w") as f:
                        f.write(bill_content)
                  
                  # Open the PDF bill with the default application
                  if file_name :
                        win32api.ShellExecute(0, "print",file_name , None , "." , 0)
                        messagebox.showinfo("Print Bill", "Bill printed successfully.")
                  else :
                        messagebox.showinfo("Print bill" , "Bill not printed")

            else :
                  messagebox.showinfo("Print bill" , "Bill not printed")

      def find_bill(self):
            bill_no = self.bill_Entry_Search.get()
            if bill_no == "" :
                  messagebox.showerror("Bill id", "Enter bill number")
            else:
                  bill_no = int(bill_no)
                  select_query = '''
                        SELECT c.customer_name, c.customer_mobile,
                              p.product_name, bi.quantity , p.price, b.total_amount 
                              FROM customers c
                              JOIN bills b ON b.customer_id = c.customer_id
                              JOIN bill_items bi ON bi.bill_id = b.bill_id
                              JOIN products p ON p.product_id = bi.product_id
                              WHERE b.bill_id = ?
                        '''
                  self.crsr.execute(select_query, (bill_no,))
                  result = self.crsr.fetchall()

            # Print the customer details
            if result:
                  self.textarea.config(state=NORMAL)
                  self.textarea.delete("1.0", END)
                  self.textarea.insert(END," \tBill Fetched Successfully")
                  self.textarea.insert(END,f"\n Customer Name: {result[0][0]}")
                  self.textarea.insert(END, f"\n Customer Mobile : {result[0][1]}")
                  self.textarea.insert(END,f"\n===================================\n Products\t\tQTY\t\tPrice")
                  self.textarea.insert(END,"\n===================================")
                  for i in range(len(result)):
                        self.textarea.insert(END, f"\n {result[i][2]}\t\t{result[i][3]}\t\t{result[i][4]}")
                  self.textarea.insert(END , f"\n==================================\n Total Price : {result[i][5]}")
            else :
                  messagebox.showwarning("Not Found","Bill not found.")
            
            self.textarea.config(state=DISABLED)
            
            
            
#.........................Categories Fun..................................................

      def Categories(self,event=""):
            selected_category = self.Combox_Category.get()
    
            if selected_category == "Select Option":
                  self.ComboxSubCategory.config(values=['Select option'])
            else:
                  # Retrieve subcategories from the database based on the selected category
                  query = "SELECT DISTINCT sub_category FROM products WHERE category = ?"
                  self.crsr.execute(query, (selected_category,))
                  rows = self.crsr.fetchall()
                  subcategories = [row[0] for row in rows]
                  self.ComboxSubCategory.config(values=subcategories)
                  self.ComboxSubCategory.current(0)


#...........................Product Fun.............................................                

      def Product_add(self,event=""):
            selected_sub_category = self.ComboxSubCategory.get()
            if selected_sub_category == "Select option":
                  self.ComboxProduct.config(values=[])
            else:
                  # Retrieve subcategories from the database based on the selected category
                  query = "SELECT DISTINCT product_name FROM products WHERE sub_category = ?"
                  self.crsr.execute(query, (selected_sub_category,))
                  rows = self.crsr.fetchall()
                  products = [row[0] for row in rows]
                  self.ComboxProduct.config(values=products)
                  self.ComboxProduct.current(0)
            
            
#...........................Price Fun..................................................................

      def price(self,event=""):
            selected_product = self.ComboxProduct.get()
            query = 'SELECT price from products WHERE product_name = ?'
            self.crsr.execute(query,(selected_product,))
            product_price = self.crsr.fetchall()
            price = product_price[0]
            self.ComboxPrice.config(value=price)
            self.ComboxPrice.current(0)
            self.Quantity.set(1)
      
      def clear(self,event=""):
            self.textarea.config(state=NORMAL)
            self.textarea.delete(1.0,END)
            self.welcome(self.Bill_NO.get() ,self.Cust_Name.get() , self.Cust_Phone.get() , self.Cust_Email.get() )
            # self.textarea.delete(2.0,3.0)
            # self.Bill_NO.set(random.randint(1,1000))
            # self.textarea.insert(2.0,f" Bill Number: {self.Bill_NO.get()}\n")
            self.textarea.config(state=DISABLED)
            self.tax_entry.delete(0, END)
            self.EntrySubTotal.delete(0,END)
            self.txtAmountTotal.delete(0,END)
            
            self.total_price = 0
            self.products.clear()
      
      def clear_from_subtotal(self):
            print(eval(f'{self.idx}-5.0'))
            self.textarea.delete(eval(f'{self.idx}-5.0'), END)
      
      def exit_screen(self , event=""):
            self.root.destroy()
            
      def run(self):
            self.root.mainloop()
            
#........................................................................................................................................

class ProductRecommendation(Bill_App):
      """Product recommendation based on purchasing behavior"""
      def __init__(self):
            db = Bill_App.db 
            purchase_history = db.get_customer_product_purchase_data()

            # Create a DataFrame from the purchase history data
            df = pd.DataFrame(purchase_history, columns=['customer_id', 'product_id', 'quantity'])
            
            df.dropna()
            # print("Head --->\n" ,df.head())
            
            # print(df.shape)
            # Create a user-item matrix using Pandas pivot_table
            user_item_matrix = df.pivot_table(index='customer_id', columns='product_id', values='quantity', fill_value=0)
            
            # print(user_item_matrix.head())
            
            X = user_item_matrix.T
            # print(X.head())
            
            SVD = TruncatedSVD(n_components=5)
            decomposed_matrix = SVD.fit_transform(X)
            # print(decomposed_matrix.shape)
            
            correlation_matrix = np.corrcoef(decomposed_matrix)
            # print(correlation_matrix.shape)
            # Reset the index to ensure the user_id becomes a column
            i = X.index[0]

            product_names = list(X.index)
            product_ID = product_names.index(i)
            print(product_ID)
            
            correlation_product_ID = correlation_matrix[product_ID]
            print(correlation_product_ID.shape)
            

            Recommend = list(X.index[correlation_product_ID > 0.90])

            # Removes the item already bought by the customer
            Recommend.remove(i) 

            print(Recommend[0:])
            for id in Recommend:
                  results = db.getProduct(id)
                  print(results)

      # Print the TensorFlow user-item matrix
      # print(user_item_matrix_tf)
      
      
class ProductManagementApp(Bill_App):
    
    def __init__(self, root):
        self.db = Bill_App.db
        self.root = root
        self.root.title("Product Management")
        self.root.geometry("1530x800+0+0")

        # Product List
        self.product_list = ttk.Treeview(self.root, columns=("Category", "Subcategory", "Name", "Price", "Quantity"))
        self.product_list.heading("#1", text="Category")
        self.product_list.heading("#2", text="Subcategory")
        self.product_list.heading("#3", text="Name")
        self.product_list.heading("#4", text="Price")
        self.product_list.heading("#5", text="Quantity")
        
        # Add a scrollbar for the Treeview
        tree_scroll = ttk.Scrollbar(self.root, orient="vertical", command=self.product_list.yview)
        tree_scroll.pack(side="right", fill="y")
        self.product_list.configure(yscrollcommand=tree_scroll.set)
        
        self.insert_sample_products()
        
        self.product_list.pack(pady=20)

        # Search and Filter
        self.filter_frame = ttk.LabelFrame(self.root, text="Search and Filter")
        self.filter_frame.pack(pady=10)

        self.search_label = ttk.Label(self.filter_frame, text="Search:")
        self.search_label.grid(row=0, column=0)

        self.search_entry = ttk.Entry(self.filter_frame)
        self.search_entry.grid(row=0, column=1)

        self.filter_button = ttk.Button(self.filter_frame, text="Filter", command=self.filter_products)
        self.filter_button.grid(row=0, column=2)

        # Add New Product
        self.add_product_frame = ttk.LabelFrame(self.root, text="Add New Product")
        self.add_product_frame.pack(pady=10)

        self.category_label = ttk.Label(self.add_product_frame, text="Category:")
        self.category_label.grid(row=0, column=0)

        self.category_entry = ttk.Entry(self.add_product_frame)
        self.category_entry.grid(row=0, column=1)

        self.subcategory_label = ttk.Label(self.add_product_frame, text="Subcategory:")
        self.subcategory_label.grid(row=1, column=0)

        self.subcategory_entry = ttk.Entry(self.add_product_frame)
        self.subcategory_entry.grid(row=1, column=1)

        self.name_label = ttk.Label(self.add_product_frame, text="Name:")
        self.name_label.grid(row=2, column=0)

        self.name_entry = ttk.Entry(self.add_product_frame)
        self.name_entry.grid(row=2, column=1)

        self.price_label = ttk.Label(self.add_product_frame, text="Price:")
        self.price_label.grid(row=3, column=0)

        self.price_entry = ttk.Entry(self.add_product_frame)
        self.price_entry.grid(row=3, column=1)

        self.quantity_label = ttk.Label(self.add_product_frame, text="Quantity:")
        self.quantity_label.grid(row=4, column=0)

        self.quantity_entry = ttk.Entry(self.add_product_frame)
        self.quantity_entry.grid(row=4, column=1)

        self.add_product_button = ttk.Button(self.add_product_frame, text="Add Product", command=self.add_product)
        self.add_product_button.grid(row=5, columnspan=2)

        # Edit and Delete Product
        self.edit_delete_frame = ttk.LabelFrame(self.root, text="Edit and Delete Product")
        self.edit_delete_frame.pack(pady=10)

        self.edit_button = ttk.Button(self.edit_delete_frame, text="Edit Product", command=self.edit_product)
        self.edit_button.grid(row=0, column=0)

        self.delete_button = ttk.Button(self.edit_delete_frame, text="Delete Product", command=self.delete_product)
        self.delete_button.grid(row=0, column=1)
        
    def insert_sample_products(self):
        products = self.db.products()

        for i, product in enumerate(products, start=1):
            self.product_list.insert("", "end", iid=i, values=product[1:])


    def filter_products(self):
        # Get the user's search query
        search_query = self.search_entry.get().strip().lower()
        
        # Clear the current product list
        for item in self.product_list.get_children():
            self.product_list.delete(item)

        # Fetch products from your database or data source
        products = self.db.search_product(search_query)  # Implement this method

        # Filter and display products that match the search query
        for product in products:
            category, subcategory, name, price, quantity = product[1:]

            if search_query in name.lower() or search_query in category.lower() or search_query in subcategory.lower():
                self.product_list.insert("", "end", values=(category, subcategory, name, price, quantity))
    
    def add_product(self):
        category = self.category_entry.get().strip().capitalize()
        sub_category = self.subcategory_entry.get().strip().capitalize()
        product = self.name_entry.get().strip().capitalize()
        price = self.price_entry.get()
        qty = self.quantity_entry.get()
        if not all([category, sub_category, product]):
            messagebox.showerror('Error', 'All fields are required')
        elif price =="" or qty == "":
            messagebox.showerror("Error","Please Enter price or qty")
        
        self.db.product_values(category , sub_category, product , price , qty)
        messagebox.showinfo("Success", "Product Added Successfully")
        

    def edit_product(self):
        # Implement editing a product
        selected_item = self.product_list.focus()
        if selected_item:
            # Retrieve data from the selected row
            data = self.product_list.item(selected_item, 'values')
            print(data)

    def delete_product(self):
        # Implement deleting a product
        pass
    
    def run(self):
        self.root.mainloop()
        
    def close(self):
        self.root.destroy()

if __name__=='__main__':
      root  = Tk()
      Bill_App(root)
      Bill_App.clear()
      # root.mainloop()
      # LoginApp(login_app)
       
                

 
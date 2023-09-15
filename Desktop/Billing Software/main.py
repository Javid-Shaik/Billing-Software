from datetime import date
import os
import sqlite3
from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk #pip install pillow
import random
from tkinter import messagebox
import win32print
import win32api
from tkinter import filedialog

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
            query = f'''
            INSERT INTO products(category , sub_category , product, price , quantity ) 
            VALUES('{category}' , '{sub_cat}' ,'{product}' , {price}, {qty})'''
            self.crsr.execute(query)
            self.conn.commit()  
      
      def billtable(self):
            bill_table = '''
                  CREATE TABLE IF NOT EXISTS bills (
                        bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_id INTEGER,
                        bill_date DATE,
                        total_amount DECIMAL(10, 2),
                        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                        )'''
            self.crsr.execute(bill_table)
            self.conn.commit()
      
      def bill_values(self, c_id , bill_date,  total_bill ):
            query = "INSERT INTO bills (customer_id, bill_date, total_amount) VALUES (? , ? , ?)"
            bill_data = (c_id, bill_date, total_bill)

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
            
class Bill_App(Database):
      conn = sqlite3.connect('Billing_App.db')
      crsr = conn.cursor()
      db = Database(conn, crsr )
      db.product()
      db.customer()
      
      db.billitems()
      db.billtable()
      db.earasedata()
      # db.print_customer()
      # db.printbill()
      # db.printbillitmes()
      
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
            self.Prices=IntVar()
            self.Quantity=IntVar()
            self.Sub_Total=StringVar()
            self.Tax=StringVar()
            self.Total=StringVar()
            self.flag = 0 
            self.total_qty = 0
            self.idx = 16.0
            #Product Catagerory List
            query = 'SELECT DISTINCT category FROM products'
            self.crsr.execute(query)
            rows =  self.crsr.fetchall()

            self.Category=["Select Option"]+ [row[0] for row in rows]

#             self.SubCatClothing=["Pant","T-Shirt","Shirt"]
#             self.pant=["Levis","Mufti","Denim"]
#             self.price_levis=4000
#             self.price_Mufti=6000
#             self.price_Denim=8000

#             self.T_Shirt=["Polo","Roadster","Cargo"]
#             self.price_polo=2000
#             self.price_Roadster=1800
#             self.price_Cargo=2500

#             self.Shirt=["Peter England","Louis Phillipe","Lee Cooper"]
#             self.price_Peter=3000
#             self.price_Louis=5000
#             self.price_Lee=7000

#             #SubCatLifeStyle
#             self.SubCatLifeStyle=["Bath Soap","Face Wash","Hair Oil"]
#             self.Bath_soap=["Mysore Sandal","Lux","Dove","Pears"]
#             self.price_Mysore=20
#             self.price_Lux=float(25)
#             self.price_Dove=40
#             self.price_pears=35

#             #Face Cream
#             self.Face_Cream=["Ponds","Patanjali","Olay","Garnier"]
#             self.price_Ponds=50
#             self.price_Patanjali=30
#             self.price_Olay=70
#             self.price_Garnier=75

#             #Hair Oil
#             self.Hair_oil=["Parachute","Almond","Jasmin"]
#             self.price_parachute=30
#             self.price_almond=60
#             self.price_jasmin=25

# #Mobiles..................................................................................................................................
#             self.SubCatMobiles=["OnePlus","IPhone","Samsung","Xiome"]

#             self.OnePlus=["Nord","NordCE","One8","One10T"]
#             self.price_Nord=30000
#             self.price_NordCE=25000
#             self.price_One8=80000
#             self.price_One10T=90000

#             self.IPhone=["I11","I12","I10"]
#             self.price_I11=45000
#             self.price_I12=90000
#             self.price_I10=80000

        
#             self.Samsung=["Samsung Galaxy","Samsung M12","Samsung M21"]
#             self.price_Galaxy=15000
#             self.price_M12=22000
#             self.price_M21=25000

#             self.Xiome=["Redmi_11","Redmi_12","RedmiPro"]
#             self.price_r11=17000
#             self.price_r12=23000
#             self.price_rpro=32000

#..........................................................................................................................................




#image 1
            self.products = []
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
            
            self.BtnSearch=Button(self.root,command=self.find_bill,text="Admin Login",font=("arial",10,"bold"),bg="lightgrey",fg="black",width=13,cursor="hand2")
            self.BtnSearch.place(x=1220,y=130,width=130,height=45)
            
            Main_Frame=Frame(self.root,bd=5,relief=GROOVE,bg="white")   #bd=Border,relief=border style
            Main_Frame.place(x=0,y=175,width=1530,height=630)           #to underline text
            
        #Customer label frame
            Cust_Frame=LabelFrame(Main_Frame,text="Customer",font=("times new roman",12,"bold"),bg="white",fg="red")
            Cust_Frame.place(x=10,y=5,width=350,height=150)

            #Mobile Number

            self.lblCustName=Label(Cust_Frame,font=("arial",12,"bold"),bg="white",text="Customer Name",bd=4)
            self.lblCustName.grid(row=0,column=0,sticky=W,padx=5,pady=2)

            self.txtCusName=ttk.Entry(Cust_Frame,textvariable=self.Cust_Name,font=("arial",10,"bold"),width=24)
            self.txtCusName.grid(row=0,column=1,sticky=W,padx=5,pady=2)
            
            self.lbl_mob=Label(Cust_Frame,text="Mobile Number",font=("times new roman",12,"bold"),bg="white")
            self.lbl_mob.grid(row=1,column=0,sticky=W,padx=5,pady=2) #west

            self.entry_mob=ttk.Entry(Cust_Frame,textvariable=self.Cust_Phone,font=("times new roman",10,"bold"),width=24)                                                  #if we want to use any variable we use self
            self.entry_mob.grid(row=1,column=1)

            self.lblEmail=Label(Cust_Frame,font=("arial",12,"bold"),bg="white",text="Email",bd=4)
            self.lblEmail.grid(row=2,column=0,sticky=W,padx=5,pady=2)

            self.txtEmail=ttk.Entry(Cust_Frame,textvariable=self.Cust_Email,font=('arial',10,'bold'),width=24)
            self.txtEmail.grid(row=2,column=1,sticky=W,padx=5,pady=2)
            
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
            self.tax_Entry_Search=ttk.Entry(Search_Frame,textvariable=self.Search_Bill,font=("arial",10,"bold"),width=18)
            self.tax_Entry_Search.grid(row=0,column=1,sticky=W,padx=2)

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

            self.txt_tax=ttk.Entry(Bottom_Frame,font=("arial",12,"bold"),width=24)
            self.txt_tax.grid(row=1,column=1,sticky=W,padx=5,pady=2)


        #Total
            self.lblAmountTotal=Label(Bottom_Frame,font=("arial",12,"bold"),bg="white",text="Total",bd=4)
            self.lblAmountTotal.grid(row=2,column=0,sticky=W,padx=5,pady=2)

            self.txtAmountTotal=ttk.Entry(Bottom_Frame,font=("arial",12,"bold"),width=24)
            self.txtAmountTotal.grid(row=2,column=1,sticky=W,padx=5,pady=2)

            Btn_Frame = Frame(Bottom_Frame, bd=20, bg="white")
            Btn_Frame.place(x=620, y=0)
                        
            #Button Frame
            Btn_Frame=Frame(Bottom_Frame,bd=20,bg="white")
            Btn_Frame.place(x=620,y=0)

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
            self.prices =[] #To add items
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
                        self.products[product]+= self.qty 
                        flag = 1
                  else :
                        self.products[product] = self.qty
                  
                  
                  self.qty = self.products[product]
                  self.total = self.price*self.qty
                  self.prices.append(self.total)
                  
                  if flag :
                        idx = self.replace_row(product)
                        self.textarea.insert(idx, f" {self.Product.get()}\t\t{self.qty}\t\t{self.total}")
                  else :
                        self.textarea.insert(END, f"\n {self.Product.get()}\t\t{self.qty}\t\t{self.total}")
                  
                  
                  self.EntrySubTotal.delete(0, END)
                  self.EntrySubTotal.insert(END, str('RS.%.2f'%(sum(self.prices))))
                  
                  self.txt_tax.delete(0, END)
                  self.txt_tax.insert(END, str('RS.%.2f'%((((sum(self.prices)) - (self.Prices.get()))*Tax)/100)))
                  
                  self.txtAmountTotal.delete(0,END)
                  self.txtAmountTotal.insert(END, str('RS.%.2f'%(((sum(self.prices)) + ((((sum(self.prices)) - (self.Prices.get()))*Tax)/100)))))
                  
            
            self.textarea.config(state=DISABLED)
            self.idx = self.textarea.index("end-1c linestart")
            #print(self.idx)
      def check_printer_connection():
            printer_name = win32print.GetDefaultPrinter()
            printer_info = win32print.GetPrinter(printer_name, 2)
            status = printer_info['Status']
            return status == win32print.PRINTER_STATUS_READY
            
      def gen_bill(self):
            if self.Cust_Name.get() != "" and self.Cust_Phone.get() != "":
                  self.textarea.config(state=NORMAL)
                  if self.Product.get()=="" or self.Cust_Name.get() == "" or self.Cust_Phone.get() == "" :
                        messagebox.showerror("Error","Please Add To Cart Product")
                  else:
                        
                        self.textarea.insert(END,f"\n=================================")
                        self.textarea.insert(END,f"\n Sub Amount:\t\t\t{self.EntrySubTotal.get()}")
                        self.textarea.insert(END,f"\n Tax Amount:\t\t\t{self.txt_tax.get()}")
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
            
                        c_id = self.db.customer_values(self.txtCusName.get() ,self.txtEmail.get(), customer_mobile)
                        
                        bill_id = self.db.bill_values(c_id , date.today() , total_bill)
                        
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
            bill_no = int(self.tax_Entry_Search.get())
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
            self.textarea.delete(2.0,3.0)
            self.Bill_NO.set(random.randint(1,1000))
            self.textarea.insert(2.0,f" Bill Number: {self.Bill_NO.get()}\n")
            self.textarea.config(state=DISABLED)
            self.txt_tax.delete(0, END)
            self.EntrySubTotal.delete(0,END)
            self.txtAmountTotal.delete(0,END)
            
            self.prices.clear()
            self.products.clear()
      
      def clear_from_subtotal(self):
            print(eval(f'{self.idx}-5.0'))
            self.textarea.delete(eval(f'{self.idx}-5.0'), END)
      
      def exit_screen(self , event=""):
            self.root.destroy()
            
      def run(self):
            self.root.mainloop()
#........................................................................................................................................

class LoginApp(Database):
      
      def __init__(self, login_app):
            self.db = Database(Bill_App.conn , Bill_App.crsr)
            
            self.login_app = login_app
            self.login_app.title("Login")
            
            screen_width = self.login_app.winfo_screenwidth()
            screen_height = self.login_app.winfo_screenheight()
            
            self.canvas = Canvas(self.login_app, width=screen_width, height=screen_height)
            self.canvas.pack()

            
            header = Label(self.canvas , text="Welcome to Billing Software" ,font=("times new roman",35,"bold"),fg="#677cb6",bg="#b4e2f5" , highlightthickness=0)
            self.canvas.create_window(480 ,20 , anchor="nw", window=header)
            
            img1 = Image.open("Images/background.jpg").resize((screen_width, screen_height))
            self.photoimg = ImageTk.PhotoImage(img1)
            
            # Display the background image on the self.canvas
            self.canvas.create_image(0, 0, image=self.photoimg, anchor="nw")
            self.Main_Frame=Frame(self.login_app,bd=5,relief=GROOVE,bg="skyblue")   #bd=Border,relief=border style
            self.Main_Frame.place(x=635,y=100,width=250,height=150)

            #User label
            self.userlabel = Label(text="Enter Username : " , font=("arial sans-serif",8),fg="black",bg="skyblue")
            self.canvas.create_window(640,111,anchor="nw",window=self.userlabel,height=20)

            # user Entry
            self.entry_username = Entry(self.login_app)
            self.canvas.create_window(730,111,anchor="nw",window=self.entry_username,height=20)

            #password label
            self.passwdlabel = Label(text="Enter Password : " , font=("arial sans-serif",8),fg="black" ,bg="skyblue")
            self.canvas.create_window(640,150,anchor="nw",window=self.passwdlabel , height=20)

            #password Entry
            self.entry_password = Entry(self.login_app, show="*" )
            self.canvas.create_window(730,150,anchor="nw",window=self.entry_password , height=20)
            
            #login button
            self.btn_login = Button(self.login_app, text="Login", command=self.replace_frame,cursor="hand2")
            self.canvas.create_window(730,200,anchor="nw",window=self.btn_login,width=70)


      def login(self):
            username = self.entry_username.get()
            password = self.entry_password.get()

            # Perform login verification here
            if username == "admin" and password == "admin":
                  self.open_billing_app()
            else:
                  messagebox.showerror("Login Failed", "Invalid username or password")

      def open_billing_app(self):
            self.login_app.destroy()  # Close the login window
            root = Tk()
            billing_app = Bill_App(root)
            billing_app.run()
      
      def admin_frame(self):
            self.Main_Frame=Frame(self.login_app,bd=5,relief=GROOVE,bg="skyblue")   #bd=Border,relief=border style
            self.Main_Frame.place(x=635,y=100,width=250,height=300)

            #Category Label
            self.category_label = Label(text="Enter Category : " , font=("arial sans-serif",8),fg="black",bg="skyblue")
            self.canvas.create_window(640,110,anchor="nw",window=self.category_label ,height=20)

            # Category Entry
            self.entry_category = Entry(self.login_app )
            self.canvas.create_window(750,110,anchor="nw",window=self.entry_category,height=20)
            
            # Sub category Label
            self.sub_category_label = Label(text="Enter Sub Category : " , font=("arial sans-serif",8),fg="black",bg="skyblue")
            self.canvas.create_window(640,150,anchor="nw",window=self.sub_category_label ,height=20)

            # Sub category Entry
            self.entry_sub_category = Entry(self.login_app )
            self.canvas.create_window(750,150,anchor="nw",window=self.entry_sub_category,height=20)
            
            #Product Label
            self.product_label = Label(text="Enter Product Name : " , font=("arial sans-serif",8),fg="black",bg="skyblue")
            self.canvas.create_window(640,190,anchor="nw",window=self.product_label,height=20)

            # Product Entry
            self.entry_product = Entry(self.login_app)
            self.canvas.create_window(750,190,anchor="nw",window=self.entry_product , height=20)

            # Price label
            self.price_label = Label(text="Enter Price : " , font=("arial sans-serif",8),fg="black" ,bg="skyblue")
            self.canvas.create_window(640,230,anchor="nw",window=self.price_label , height=20)

            #Price Entry
            self.entry_price = Entry(self.login_app)
            self.canvas.create_window(750,230,anchor="nw",window=self.entry_price , height=20)
            
            #Quntity Label
            self.qty_label = Label(text="Enter Quantity : " ,font=("arial sans-serif",8),fg="black" ,bg="skyblue")
            self.canvas.create_window(640,270,anchor="nw",window=self.qty_label , height=20)

            # Quantity Entry
            self.entry_qty = Entry(self.login_app)
            self.canvas.create_window(750,270,anchor="nw",window=self.entry_qty , height=20)
            
            
            # Cancel Button 
            self.cancel_btn = Button(self.login_app, text="Cancel", command=self.cancel,cursor="hand2")
            self.canvas.create_window(650,320,anchor="nw",window=self.cancel_btn,width=70)
            
            #Save button
            self.save_product = Button(self.login_app, text="Add Product", command=self.save_products,cursor="hand2")
            self.canvas.create_window(800,320,anchor="nw",window=self.save_product,width=70)
            
            self.btn_login = Button(self.login_app, text="Login", command=self.login,cursor="hand2")
            self.canvas.create_window(800,350,anchor="nw",window=self.btn_login,width=70)

            
      def replace_frame(self):
            self.Main_Frame.place_forget()
            self.admin_frame()  
      
      def cancel(self):
            self.entry_category.delete(0,END) 
            self.entry_sub_category.delete(0,END)
            self.entry_product.delete(0,END)
            self.entry_price.delete(0,END)
            self.entry_qty.delete(0,END)
            self.textarea.delete()
            
            
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
                  
if __name__=='__main__':
      root  = Tk()
      Bill_App(root)
      root.mainloop()
      # LoginApp(login_app)
       
                

 
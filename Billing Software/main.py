import os
from tkinter import *
from tkinter import ttk
import tkinter
from PIL import Image,ImageTk #pip install pillow
import random
from tkinter import messagebox
import tempfile



class Bill_App:
    def __init__(self,root) :
        self.root=root
        self.root.geometry("1530x800+0+0")
        self.root.title("Billing Software")
        #...........................Variables..................................
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


        #Product Catagerory List
        self.Category=("Select Option","Clothing","LifeStyle","Mobiles")

        self.SubCatClothing=["Pant","T-Shirt","Shirt"]
        self.pant=["Levis","Mufti","Denim"]
        self.price_levis=4000
        self.price_Mufti=6000
        self.price_Denim=8000

        self.T_Shirt=["Polo","Roadster","Cargo"]
        self.price_polo=2000
        self.price_Roadster=1800
        self.price_Cargo=2500

        self.Shirt=["Peter England","Louis Phillipe","Lee Cooper"]
        self.price_Peter=3000
        self.price_Louis=5000
        self.price_Lee=7000

        #SubCatLifeStyle
        self.SubCatLifeStyle=["Bath Soap","Face Wash","Hair Oil"]
        self.Bath_soap=["Mysore Sandal","Lux","Dove","Pears"]
        self.price_Mysore=20
        self.price_Lux=float(25)
        self.price_Dove=40
        self.price_pears=35

        #Face Cream
        self.Face_Cream=["Ponds","Patanjali","Olay","Garnier"]
        self.price_Ponds=50
        self.price_Patanjali=30
        self.price_Olay=70
        self.price_Garnier=75

        #Hair Oil
        self.Hair_oil=["Parachute","Almond","Jasmin"]
        self.price_parachute=30
        self.price_almond=60
        self.price_jasmin=25

#Mobiles..................................................................................................................................
        self.SubCatMobiles=["OnePlus","IPhone","Samsung","Xiome"]

        self.OnePlus=["Nord","NordCE","One8","One10T"]
        self.price_Nord=30000
        self.price_NordCE=25000
        self.price_One8=80000
        self.price_One10T=90000

        self.IPhone=["I11","I12","I10"]
        self.price_I11=45000
        self.price_I12=90000
        self.price_I10=80000

        
        self.Samsung=["Samsung Galaxy","Samsung M12","Samsung M21"]
        self.price_Galaxy=15000
        self.price_M12=22000
        self.price_M21=25000
        
        self.Xiome=["Redmi_11","Redmi_12","RedmiPro"]
        self.price_r11=17000
        self.price_r12=23000
        self.price_rpro=32000

#..........................................................................................................................................




#image 1
        img=Image.open("Images/Billing1.png")
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
        img3=Image.open("Images/Billing3.png")
        img3=img3.resize((520,130), ) #it convert low level img to high level img
        self.photoimg3=ImageTk.PhotoImage(img3)

        lb1_img3=Label(self.root,image=self.photoimg3)
        lb1_img3.place(x=1000,y=10,width=600,height=130)

        lbl_title=Label(self.root,text="BILLING SOFTWARE",font=("times new roman",38,"bold"),bg="white",fg="red") #where we want to make label we use = root
        lbl_title.place(x=0,y=130,width=1530,height=45)

        Main_Frame=Frame(self.root,bd=5,relief=GROOVE,bg="white")   #bd=Border,relief=border style
        Main_Frame.place(x=0,y=175,width=1530,height=630)           #to underline text

        #Customer label frame
        Cust_Frame=LabelFrame(Main_Frame,text="Customer",font=("times new roman",12,"bold"),bg="white",fg="red")
        Cust_Frame.place(x=10,y=5,width=350,height=150)

        #Mobile Number
        self.lbl_mob=Label(Cust_Frame,text="Mobile Number",font=("times new roman",12,"bold"),bg="white")
        self.lbl_mob.grid(row=0,column=0,sticky=W,padx=5,pady=2) #west

        self.entry_mob=ttk.Entry(Cust_Frame,textvariable=self.Cust_Phone,font=("times new roman",10,"bold"),width=24)                                                  #if we want to use any variable we use self
        self.entry_mob.grid(row=0,column=1)

        self.lblCustName=Label(Cust_Frame,font=("arial",12,"bold"),bg="white",text="Customer Name",bd=4)
        self.lblCustName.grid(row=1,column=0,sticky=W,padx=5,pady=2)

        self.txtCusName=ttk.Entry(Cust_Frame,textvariable=self.Cust_Name,font=("arial",10,"bold"),width=24)
        self.txtCusName.grid(row=1,column=1,sticky=W,padx=5,pady=2)
        
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
        
        self.Combox_Category=ttk.Combobox(Product_Frame,value=self.Category ,font=("arial",10,"bold"),width=24,state="readonly") #Combobox will be in our ttk
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

        self.ComboxPrice=ttk.Combobox(Product_Frame,textvariable=self.Prices,state="readonly",font=("arial",10,"bold"),width=24)
        self.ComboxPrice.grid(row=0,column=3,sticky=W,padx=5,pady=2)
        

        #Quantity
        self.lblQty=Label(Product_Frame,font=("arial",12,"bold"),bg="white",text="Qty",bd=4)
        self.lblQty.grid(row=1,column=2,sticky=W,padx=5,pady=2)

        self.ComboxQty=ttk.Entry(Product_Frame,textvariable=self.Quantity,font=("arial",10,"bold"),width=26)
        self.ComboxQty.grid(row=1,column=3,sticky=W,padx=5,pady=2)

        #Middle Frame
        MiddleFrame=Frame(Main_Frame,bd=10)
        MiddleFrame.place(x=10,y=160,width=990,height=540)

        #image 4
        img12=Image.open("Images/Billing1.png")
        img12=img12.resize((500,130) ) #it convert low level img to high level img
        self.photoimg12=ImageTk.PhotoImage(img12)
        lb1_img12=Label(MiddleFrame,image=self.photoimg12)
        lb1_img12.place(x=0,y=0,width=500,height=340)

#image 5
        img_13=Image.open("Images/Billing2.png")
        img_13=img_13.resize((490,340)) #it convert low level img to high level img
        self.photoimg_13=ImageTk.PhotoImage(img_13)

        lb1_img_13=Label(MiddleFrame,image=self.photoimg_13)
        lb1_img_13.place(x=490,y=0,width=500,height=340)



        #Search
        Search_Frame=Frame(Main_Frame,bd=2,bg="white")
        Search_Frame.place(x=1020,y=15,width=500,height=40)

        self.lblBill=Label(Search_Frame,font=("arial",12,"bold"),bg="yellow",text="Bill Number",fg="Black")
        self.lblBill.grid(row=0,column=0,sticky=W,padx=1)

        #Entry Click
        self.tax_Entry_Search=ttk.Entry(Search_Frame,textvariable=self.Search_Bill,font=("arial",10,"bold"),width=24)
        self.tax_Entry_Search.grid(row=0,column=1,sticky=W,padx=2)

        #Search Button
        self.BtnSearch=Button(Search_Frame,command=self.find_bill,text="Search",font=("arial",10,"bold"),bg="orangered",fg="white",width=15,cursor="hand2")
        self.BtnSearch.grid(row=0,column=2)

        
        
        #RightFrame Bill Area
        RightLabelFrame=LabelFrame(Main_Frame,text="Bill Area",font=("times new roman",12,"bold"),bg="white",fg="red")
        RightLabelFrame.place(x=1015,y=45,width=460,height=440)

        #scrollBar
        scroll_y=Scrollbar(RightLabelFrame,orient=VERTICAL)
        self.textarea=Text(RightLabelFrame,yscrollcommand=scroll_y.set,bg="white",fg="blue",font=("times new roman",12,"bold"))
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_y.config(command=self.textarea.yview)
        self.textarea.pack(fill=BOTH,expand=1)

        #Bill Counter label frame
        Bottom_Frame=LabelFrame(Main_Frame,text="Bill Counter",font=("times new roman",12,"bold"),bg="white",fg="red")
        Bottom_Frame.place(x=0,y=485,width=1520,height=130)

        #SubTotal
        self.lblSubTotal=Label(Bottom_Frame,font=("arial",12,"bold"),bg="white",text="SubTotal",bd=4)
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

        #Button Frame
        Btn_Frame=Frame(Bottom_Frame,bd=20,bg="white")
        Btn_Frame.place(x=620,y=0)

        self.BtnAddToCart=Button(Btn_Frame,command=self.AddItem,height=2,text="Add To Cart",font=("arial",12,"bold"),bg="orangered",fg="white",width=15,cursor="hand2")
        self.BtnAddToCart.grid(row=0,column=0)

        
        self.Btngenerate_bill=Button(Btn_Frame,command=self.gen_bill,height=2,text="Generate Bill",font=("arial",12,"bold"),bg="orangered",fg="white",width=15,cursor="hand2")
        self.Btngenerate_bill.grid(row=0,column=1)


        
        self.BtnPrint=Button(Btn_Frame,command=self.iprint,height=2,text="Print",font=("arial",12,"bold"),bg="orangered",fg="white",width=15,cursor="hand2")
        self.BtnPrint.grid(row=0,column=3)

        
        self.BtnClear=Button(Btn_Frame,height=2,text="Clear",font=("arial",12,"bold"),bg="orangered",fg="white",width=15,cursor="hand2")
        self.BtnClear.grid(row=0,column=4)

        
        self.BtnExit=Button(Btn_Frame,height=2,text="Exit",font=("arial",12,"bold"),bg="orangered",fg="white",width=15,cursor="hand2")
        self.BtnExit.grid(row=0,column=5)
#...........................................................................................................................................
        self.welcome() # for welcome fun (page) 
        self.l=[] #To add items
    def welcome(self):
          self.textarea.delete(1.0,END) #textarea is a variable name
          self.textarea.insert(END,"\t Welcome To Our Store")
          self.textarea.insert(END,f"\n Bill Number:{self.Bill_NO.get()}")
          self.textarea.insert(END,f"\n Customer Name:{self.Cust_Name.get()}")
          self.textarea.insert(END,f"\n Phone Number:{self.Cust_Phone.get()}")
          self.textarea.insert(END,f"\n Email:{self.Cust_Email.get()}")

          self.textarea.insert(END,"\n===============================================")
          self.textarea.insert(END,f"\n Products\t\t\tQTY\tPrice")
          self.textarea.insert(END,"\n===============================================\n")        

    def AddItem(self):
          self.tax_input=tkinter.StringVar()
          Tax=1
          self.n=self.Prices.get()
          self.m=self.Quantity.get()*self.n #5*5000=25000
          self.l.append(self.m)
          if self.Product.get()=="":
                messagebox.showerror("Error","Please Select A Product Name")
          else:
               self.textarea.insert(END, f"\n {self.Product.get()}\t\t{self.Quantity.get()}\t\t{self.m}")

               self.Sub_Total.set(str('RS.%.2f'%(sum(self.l))))
               self.tax_input.set(str('RS.%.2f'%((((sum(self.l)) - (self.Prices.get()))*Tax)/100)))
               self.Total.set(str('RS.%.2f'%(((sum(self.l)) + ((((sum(self.l)) - (self.Prices.get()))*Tax)/100)))))

            #    Sub_Total = sum(self.l)
            #    Tax = (Sub_Total - self.Prices.get()) * Tax / 100
            #    total_amount = Sub_Total + Tax

            #    self.Sub_Total.set(f"Rs. {Sub_Total:.2f}")
            #    self.Tax.set(f"Rs. {Tax:.2f}")
            #    self.Total.set(f"Rs. {total_amount:.2f}")

    def gen_bill(self):
          if self.Product.get()=="":
            messagebox.showerror("Error","Please Add To Cart Product")
          else:
                text=self.textarea.get(10.0,(10.0+float(len(self.l))))
                self.welcome()
                self.textarea.insert(END,text)
                self.textarea.insert(END,f"\n==========================================")
                self.textarea.insert(END,f"\n Sub Amount:\t\t\t{self.Sub_Total.get()}")
                self.textarea.insert(END,f"\n Tax Amount:\t\t\t{self.tax_input.get()}")
                self.textarea.insert(END,f"\n Total Amount:\t\t\t{self.Total.get()}")
                self.textarea.insert(END,f"\n==========================================")


    def iprint(self):
          q=self.textarea.get(1.0,"end-1c")
          filename=tempfile.mktemp('.txt')
          open(filename,'w').write(q)
          os.stsrtfile(filename,"print")

    def find_bill(self):
          found="no"
          for i in os.listdir("bills/"):
                if i.split('.')[0]==self.Search_Bill.get():
                   f1=open(f'bills/{i}','r')
                   self.textarea.delete(1.0,END)
                   for d in f1:
                         self.textarea.insert(END,d)
                         f1.close()
                         found="yes"

                if found=='no':
                      messagebox.showerror("Error","invalid Bill Number")

#.........................Categories Fun..................................................

    def Categories(self,event=""):
        if self.Combox_Category.get()=="Clothing":
                self.ComboxSubCategory.config(value=self.SubCatClothing)
                self.ComboxSubCategory.current(0)
        if self.Combox_Category.get()=="LifeStyle":
                self.ComboxSubCategory.config(value=self.SubCatLifeStyle)
                self.ComboxSubCategory.current(0)
        if self.Combox_Category.get()=="Mobiles":
                self.ComboxSubCategory.config(value=self.SubCatMobiles)
                self.ComboxSubCategory.current(0)


#...........................Product Fun.............................................                

    def Product_add(self,event=""):
          if self.ComboxSubCategory.get()=="Pant":
                self.ComboxProduct.config(value=self.pant)
                self.ComboxProduct.current(0)
                #T-Shirt,Shirt
          if self.ComboxSubCategory.get()=="T-Shirt":
                self.ComboxProduct.config(value=self.T_Shirt)
                self.ComboxProduct.current(0) 
          if self.ComboxSubCategory.get()=="Shirt":
                self.ComboxProduct.config(value=self.Shirt)
                self.ComboxProduct.current(0)

        #LifeStyle
          if self.ComboxSubCategory.get()=="Bath Soap":
                self.ComboxProduct.config(value=self.Bath_soap)
                self.ComboxProduct.current(0)

          if self.ComboxSubCategory.get()=="Face Wash":
                self.ComboxProduct.config(value=self.Face_Cream) 
                self.ComboxProduct.current(0)

          if self.ComboxSubCategory.get()=="Hair Oil":
                self.ComboxProduct.config(value=self.Hair_oil) 
                self.ComboxProduct.current(0) 

        # Mobile
        
          if self.ComboxSubCategory.get()=="OnePlus":
                self.ComboxProduct.config(value=self.OnePlus) 
                self.ComboxProduct.current(0) 

          if self.ComboxSubCategory.get()=="IPhone":
                self.ComboxProduct.config(value=self.IPhone) 
                self.ComboxProduct.current(0) 

          if self.ComboxSubCategory.get()=="Samsung":
                self.ComboxProduct.config(value=self.Samsung) 
                self.ComboxProduct.current(0)  

          if self.ComboxSubCategory.get()=="Xiome":
                self.ComboxProduct.config(value=self.Xiome) 
                self.ComboxProduct.current(0)  

#...........................Price Fun..................................................................

    def price(self,event=""):
          #Pant
          if self.ComboxProduct.get()=="Levis":
                self.ComboxPrice.config(value=self.price_levis)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

        # self.price_levis=4000
        # self.price_Mufti=6000
        # self.price_Denim=8000
         
          if self.ComboxProduct.get()=="Mufti":
                self.ComboxPrice.config(value=self.price_Mufti)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)
        
          if self.ComboxProduct.get()=="Denim":
                self.ComboxPrice.config(value=self.price_Denim)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)


          #T-Shirt

        # self.price_polo=2000
        # self.price_Roadster=1800
        # self.price_Cargo=2500
    
          if self.ComboxProduct.get()=="Polo":
                self.ComboxPrice.config(value=self.price_polo)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)
        
          if self.ComboxProduct.get()=="Roadster":
                self.ComboxPrice.config(value=self.price_Roadster)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

          if self.ComboxProduct.get()=="Cargo":
                self.ComboxPrice.config(value=self.price_Cargo)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

        #Shirt

        # self.Shirt=["Peter England","Louis Phillipe","Lee Cooper"]
        # self.price_Peter=3000
        # self.price_Louis=5000
        # self.price_Lee=7000

          if self.ComboxProduct.get()=="Peter England":
                self.ComboxPrice.config(value=self.price_Peter)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

          if self.ComboxProduct.get()=="Louis Phillipe":
                self.ComboxPrice.config(value=self.price_Louis)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

          if self.ComboxProduct.get()=="Lee Copper":
                self.ComboxPrice.config(value=self.price_Lee)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

                #Soaps
        # self.Bath_soap=["Mysore Sandal","Lux","Dove","Pears"]
        # self.price_Mysore=20
        # self.price_Lux=float(25)
        # self.price_Dove=40
        # self.price_pears=35

          if self.ComboxProduct.get()=="Mysore Sandal":
                self.ComboxPrice.config(value=self.price_Mysore)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

          if self.ComboxProduct.get()=="Lux":
                self.ComboxPrice.config(value=self.price_Lux)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

          if self.ComboxProduct.get()=="Dove":
                self.ComboxPrice.config(value=self.price_Dove)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

          if self.ComboxProduct.get()=="Pears":
                self.ComboxPrice.config(value=self.price_pears)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

        #Face Cream

        # self.Face_Cream=["Ponds","Patanjali","Olay","Garnier"]
        # self.price_Ponds=50
        # self.price_Patanjali=30
        # self.price_Olay=70
        # self.price_Garnier=75

          if self.ComboxProduct.get()=="Ponds":
                self.ComboxPrice.config(value=self.price_Ponds)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

          if self.ComboxProduct.get()=="Patanjali":
                self.ComboxPrice.config(value=self.price_Patanjali)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)
        
          if self.ComboxProduct.get()=="Olay":
                self.ComboxPrice.config(value=self.price_Olay)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

          if self.ComboxProduct.get()=="Garnier":
                self.ComboxPrice.config(value=self.price_Garnier)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

        #Hair_Oil

        # self.Hair_oil=["Parachute","Almond","Jasmin"]
        # self.price_parachute=30
        # self.price_almond=60
        # self.price_jasmin=25

          if self.ComboxProduct.get()=="Parachute":
                self.ComboxPrice.config(value=self.price_parachute)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)
        
          if self.ComboxProduct.get()=="Almond":
                self.ComboxPrice.config(value=self.price_almond)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

          if self.ComboxProduct.get()=="Jasmin":
                self.ComboxPrice.config(value=self.price_jasmin)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)
        
        #OnePlus
        # self.OnePlus=["Nord","NordCE","One8","One10T"]
        # self.price_Nord=30000
        # self.price_NordCE=25000
        # self.price_One8=80000
        # self.price_One10T=90000

          if self.ComboxProduct.get()=="Nord":
                self.ComboxPrice.config(value=self.price_Nord)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

          if self.ComboxProduct.get()=="NordCE":
                self.ComboxPrice.config(value=self.price_NordCE)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

          if self.ComboxProduct.get()=="One8":
                self.ComboxPrice.config(value=self.price_One8)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

          if self.ComboxProduct.get()=="One10T":
                self.ComboxPrice.config(value=self.price_One10T)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

        #IPhone
        # self.IPhone=["I11","I12","I10"]
        # self.price_I11=45000
        # self.price_I12=90000
        # self.price_I10=80000

          if self.ComboxProduct.get()=="I11":
                self.ComboxPrice.config(value=self.price_I11)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

          if self.ComboxProduct.get()=="I12":
                self.ComboxPrice.config(value=self.price_I12)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

          if self.ComboxProduct.get()=="I10":
                self.ComboxPrice.config(value=self.price_I10)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

        #Samsung
        # self.Samsung=["Samsung Galaxy","Samsung M12","Samsung M21"]
        # self.price_Galaxy=15000
        # self.price_M12=22000
        # self.price_M21=25000

          if self.ComboxProduct.get()=="Samsung Galaxy":
                self.ComboxPrice.config(value=self.price_Galaxy)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

          if self.ComboxProduct.get()=="Samsung M12":
                self.ComboxPrice.config(value=self.price_M12)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)
        
          if self.ComboxProduct.get()=="Samsung M21":
                self.ComboxPrice.config(value=self.price_M21)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

        #Xiome
        # self.Xiome=["Redm_11","Redmi_12","RedmiPro"]
        # self.price_r11=17000
        # self.price_1r2=23000
        # self.price_rpro=32000

          if self.ComboxProduct.get()=="Redmi_11":
                self.ComboxPrice.config(value=self.r11)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)
        
          if self.ComboxProduct.get()=="Redmi_12":
                self.ComboxPrice.config(value=self.price_r12)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)

          if self.ComboxProduct.get()=="RedmiPro":
                self.ComboxPrice.config(value=self.price_rpro)
                self.ComboxPrice.current(0)
                self.Quantity.set(1)
#........................................................................................................................................
               
                

if __name__=='__main__':
    root=Tk()
    obj=Bill_App(root)
    root.mainloop()
 
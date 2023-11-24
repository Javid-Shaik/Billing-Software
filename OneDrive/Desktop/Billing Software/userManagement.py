import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
from main import Bill_App
from PIL import Image , ImageTk


class UserManagementApp:
    def __init__(self , root) -> None:
        self.db = Bill_App.db
        self.root = root
        self.root.title("User Management")
        self.root.geometry("1530x800+0+0")

        # User List
        self.user_list = ttk.Treeview(self.root, columns=("Customer ID", "Name", "Mobile", "Email"))
        self.user_list.heading("#1", text="Customer ID     ↑",  anchor="w", command=lambda: self.sort_by(self.user_list, "Customer ID" , False ))
        self.user_list.heading("#2", text="Name     ↑", anchor="w", command=lambda: self.sort_by(self.user_list, "Name" , False ))
        self.user_list.heading("#3", text="Mobile     ↑", anchor="w", command=lambda: self.sort_by(self.user_list, "Mobile" , False ))
        self.user_list.heading("#4", text="Email     ↑", anchor="w", command=lambda: self.sort_by(self.user_list, "Email" , False ))
        
        tree_scroll = ttk.Scrollbar(self.root, orient="vertical", command=self.user_list.yview)
        tree_scroll.pack(side="right", fill="y")
        self.user_list.configure(yscrollcommand=tree_scroll.set )
        
        self.insert_sample_users()
        
        self.user_list.pack(pady=20)

        # Search and Filter
        self.filter_frame = ttk.LabelFrame(self.root, text="Search and Filter")
        self.filter_frame.pack(pady=10)

        self.search_label = ttk.Label(self.filter_frame, text="Search:")
        self.search_label.grid(row=0, column=0)

        self.search_entry = ttk.Entry(self.filter_frame)
        self.search_entry.grid(row=0, column=1)

        self.filter_button = ttk.Button(self.filter_frame, text="Filter", command=self.filter_users , cursor='hand2')
        self.filter_button.grid(row=0, column=2)
        
        self.edit_delete_frame = ttk.LabelFrame(self.root, text="See and Delete User")
        self.edit_delete_frame.pack(pady=10)

        self.edit_button = ttk.Button(self.edit_delete_frame, text="User Details", command=self.user_details , cursor='hand2')
        self.edit_button.grid(row=0, column=0)

        self.delete_button = ttk.Button(self.edit_delete_frame, text="Delete User", command=self.delete_user , cursor='hand2')
        self.delete_button.grid(row=0, column=1)
        
        # Load the refresh icon image
        refresh_img = Image.open("Images/refresh-button.png")  # Replace "refresh.png" with your image file path
        refresh_img = refresh_img.resize((20, 20))  # Resize the image as needed
        self.refresh_icon = ImageTk.PhotoImage(refresh_img)
        
        screen_width = self.root.winfo_screenwidth()
        top_right_x = screen_width - 180  # Adjust the position as needed
        top_right_y = 20

        # Create a refresh button using a Label widget with the image
        self.refresh_button = ttk.Label(self.root, image=self.refresh_icon, cursor='hand2')
        self.refresh_button.bind("<Button-1>", lambda event: self.refresh_data())  # Bind the refresh function
        self.refresh_button.place(x=top_right_x, y=top_right_y)
        
        
    def refresh_data(self):
        # Clear the existing data
        self.user_list.delete(*self.user_list.get_children())

        # Repopulate the Treeview with updated data
        self.insert_sample_users()
        print("Users updated")
        
    
    def insert_sample_users(self):
        users = self.db.users()

        for i, user in enumerate(users, start=1):
            self.user_list.insert("", "end", iid=i, values=user)
            
    def filter_users(self):
        # Get the user's search query
        search_query = self.search_entry.get().strip().lower()

        # Fetch products from your database or data source
        users = self.db.search_user(search_query)  # Implement this method

        if users:
            # Clear the current product list
            for item in self.user_list.get_children():
                self.user_list.delete(item)
            
            for user in users:
                cid, name, mobile, email = user
                
                 # Filter and display products that match the search query
                if search_query in name.lower() or search_query in email.lower() or search_query in mobile.lower():
                    self.user_list.insert("", "end", values=(cid , name, mobile, email))
        else :
            messagebox.showerror("Error","User not present")
    
    def sort_by(self, tree, col, descending):
        
        data = [(tree.set(child, col), child) for child in tree.get_children('')]

        # Sort the data based on the column values
        data.sort(reverse=descending)

        for index, item in enumerate(data):
            tree.move(item[1], '', index)

        # Switch the direction for the next click
        heading_text = f"{col} {'    ↓' if descending else '    ↑'}"
        tree.heading(col, text=heading_text,  command=lambda: self.sort_by(tree, col, not descending))
        
    def user_details(self):
        selected_item = self.user_list.selection()
        if selected_item:
            product_data = self.user_list.item(selected_item)
            existing_values = product_data["values"]

            # Create an edit window
            user_window = tk.Toplevel(self.root)
            user_window.title("User Data")
            # user_window.geometry("480x480")
            
            # self.db.printbill()
            
            user_data = self.db.purchaseHistory(existing_values[0])
            
            

            tree = ttk.Treeview(user_window, columns=("Invoice" , "Bill ID", "Date", "Product", "Quantity", "Price"), show="headings")

            # Define column headings
            tree.heading("Invoice", text="Invoice")
            tree.heading("Bill ID", text="Bill ID")
            tree.heading("Date", text="Date")
            tree.heading("Product", text="Product")
            tree.heading("Quantity", text="Quantity")
            tree.heading("Price", text="Price")

            # Add data to the Treeview
            for item in user_data:
                tree.insert("", "end", values=item)

            # Style the Treeview
            style = ttk.Style()
            style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

            # Set column widths
            tree.column("Invoice", width=200)
            tree.column("Bill ID", width=100)
            tree.column("Date", width=150)
            tree.column("Product", width=200)
            tree.column("Quantity", width=100)
            tree.column("Price", width=100)

            # Pack the Treeview
            tree.pack()
                
    # delete the user
    def delete_user(self):
        selected_item = self.user_list.selection()
        
        if selected_item:
            result = messagebox.askquestion("Delete User?", "Are you sure?")
            if result=='yes':
                
                product_data = self.user_list.item(selected_item)
                existing_values = product_data["values"]
                uid = existing_values[0]
                # Delete the selected user from the Treeview widget
                self.db.delete_user(uid)
                self.user_list.delete(selected_item)
            else :
                  messagebox.showinfo("Delete User?" , "User is not deleted")
        
    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    app = UserManagementApp(root)
    root.mainloop()
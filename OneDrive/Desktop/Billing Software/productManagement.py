import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from main import Bill_App

class ProductManagementApp:
    
    def __init__(self, root):
        self.db = Bill_App.db
        self.root = root
        self.root.title("Product Management")
        self.root.geometry("1530x800+0+0")
        
        # Product List
        self.product_list = ttk.Treeview(self.root, columns=("Product Id" ,"Category", "Subcategory", "Name", "Price", "Quantity"))
        self.product_list.heading("#1", text="Product ID     ↑" , command=lambda: self.sort_by(self.product_list ,"Product Id" , False ))
        self.product_list.heading("#2", text="Category     ↑", command=lambda: self.sort_by(self.product_list ,"Category" , False ))
        self.product_list.heading("#3", text="Subcategory     ↑", command=lambda: self.sort_by(self.product_list ,"Subcategory" , False ))
        self.product_list.heading("#4", text="Name     ↑", command=lambda: self.sort_by(self.product_list ,"Name" , False ))
        self.product_list.heading("#5", text="Price     ↑", command=lambda: self.sort_by(self.product_list ,"Price" , False ))
        self.product_list.heading("#6", text="Quantity     ↑", command=lambda: self.sort_by(self.product_list ,"Quantity" , False ))
        
        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
            
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

        self.filter_button = ttk.Button(self.filter_frame, text="Filter", command=self.filter_products , cursor='hand2')
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

        self.add_product_button = ttk.Button(self.add_product_frame, text="Add Product", command=self.add_product , cursor='hand2')
        self.add_product_button.grid(row=5, columnspan=2)

        # Edit and Delete Product
        self.edit_delete_frame = ttk.LabelFrame(self.root, text="Edit and Delete Product")
        self.edit_delete_frame.pack(pady=10)

        self.edit_button = ttk.Button(self.edit_delete_frame, text="Edit Product", command=self.edit_product , cursor='hand2')
        self.edit_button.grid(row=0, column=0)

        self.delete_button = ttk.Button(self.edit_delete_frame, text="Delete Product", command=self.delete_product , cursor='hand2')
        self.delete_button.grid(row=0, column=1)
        
        
    def sort_by(self, tree, col, descending):
        
        data = [(tree.set(child, col), child) for child in tree.get_children('')]

        # Sort the data based on the column values
        data.sort(reverse=descending)

        for index, item in enumerate(data):
            tree.move(item[1], '', index)

        # Switch the direction for the next click
        heading_text = f"{col} {'    ↓' if descending else '    ↑'}"
        tree.heading(col, text=heading_text,  command=lambda: self.sort_by(tree, col, not descending))
        
        
        
    def edit_product(self):
        selected_item = self.product_list.selection()
        if selected_item:
            product_data = self.product_list.item(selected_item)
            existing_values = product_data["values"]

            # Create an edit window
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Product")

            # Add input boxes for editing
            input_entries = []
            for i, label_text in enumerate(["Product Id", "Category", "Subcategory", "Name", "Price", "Quantity"]):
                label = tk.Label(edit_window, text=label_text)
                label.grid(row=i, column=0)

                input_var = tk.StringVar()
                input_entry = tk.Entry(edit_window, textvariable=input_var)
                if i == 0:  # Disable the "Product Id" entry
                    input_entry.config(state="disabled")
                input_var.set(existing_values[i])  # Display existing values
                input_entry.grid(row=i, column=1)
                input_entries.append(input_var)

            # Add a "Save" button to save the edited product
            save_button = tk.Button(edit_window, text="Save", command=lambda: self.save_product(selected_item, input_entries, edit_window))
            save_button.grid(row=len(input_entries), columnspan=2)

    def save_product(self, selected_item, input_entries, edit_window):
        # Retrieve the edited values from input_entries
        edited_values = [entry.get() for entry in input_entries]
        # print(*edited_values)
        self.db.update_product_details(*edited_values)
        

        # Update the selected product with edited values
        self.product_list.item(selected_item, values=edited_values)

        # Close the edit window
        edit_window.destroy()
        
    def insert_sample_products(self):
        products = self.db.products()

        for i, product in enumerate(products, start=1):
            self.product_list.insert("", "end", iid=i, values=product)


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
            pid, category, subcategory, name, price, quantity = product

            if search_query in name.lower() or search_query in category.lower() or search_query in subcategory.lower():
                self.product_list.insert("", "end", values=(pid , category, subcategory, name, price, quantity))
    
    def add_product(self):
        category = self.category_entry.get().strip().capitalize()
        sub_category = self.subcategory_entry.get().strip().capitalize()
        product = self.name_entry.get().strip().capitalize()
        price = self.price_entry.get()
        qty = self.quantity_entry.get()
        
        if category == "" or sub_category == "" or product == "" or price =="" or qty == "" :
            messagebox.showerror("Error","All fileds are required")
        else :
            self.db.product_values(category , sub_category, product , price , qty)
            self.refresh_product_list()

    def delete_product(self):
        selected_item = self.product_list.selection()
        
        if selected_item:
            result = messagebox.askquestion("Delete Product!", "Are you sure?")
            if result=='yes':
                
                product_data = self.product_list.item(selected_item)
                existing_values = product_data["values"]
                pid = existing_values[0]
                # Delete the selected product from the Treeview widget
                self.db.delete_product(pid)
                self.product_list.delete(selected_item)
            else :
                  messagebox.showinfo("Delete Product!" , "Product is not deleted")
                  
    def refresh_product_list(self):
    # Clear the current items in the product list
        for item in self.product_list.get_children():
            self.product_list.delete(item)

        # Retrieve the updated product data from your database
        updated_product_data = self.db.products()

        # Populate the product list with the updated data
        for product in updated_product_data:
            self.product_list.insert("", "end", values=product)
            
    

    
    def run(self):
        self.root.mainloop()
        
    def close(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ProductManagementApp(root)
    root.mainloop()

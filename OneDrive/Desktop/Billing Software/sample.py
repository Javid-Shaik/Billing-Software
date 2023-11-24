import tkinter as tk
from tkinter import ttk

class UserManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Management")
        self.root.geometry("600x400")

        self.user_list = ttk.Treeview(self.root, columns=("Customer ID", "Name", "Mobile", "Email", "Select"))
        self.user_list.heading("#1", text="Customer ID")
        self.user_list.heading("#2", text="Name")
        self.user_list.heading("#3", text="Mobile")
        self.user_list.heading("#4", text="Email")
        self.user_list.heading("#5", text="Select")

        self.user_list.pack(pady=20)

        # Add sample users with checkboxes
        for i in range(1, 6):
            item_id = f"I00{i}"  # Use strings as item IDs
            item = self.user_list.insert("", "end", iid=item_id, values=(i, f"User {i}", f"12345{i}", f"user{i}@example.com", False))

        # Add checkboxes using tags
        self.user_list.tag_configure("checked", background="green")  # You can customize the background color
        self.user_list.tag_configure("unchecked", background="red")  # You can customize the background color

        # Create a set to store the selected item IDs
        self.selected_items = set()

        # Add buttons for actions
        select_all_button = tk.Button(self.root, text="Select All", command=self.select_all)
        select_all_button.pack(side="left")
        deselect_all_button = tk.Button(self.root, text="Deselect All", command=self.deselect_all)
        deselect_all_button.pack(side="left")
        delete_selected_button = tk.Button(self.root, text="Delete Selected", command=self.delete_selected)
        delete_selected_button.pack(side="left")

    def toggle_select(self, item_id):
        if item_id in self.selected_items:
            self.selected_items.remove(item_id)
            self.user_list.item(item_id, tags=("unchecked",))
        else:
            self.selected_items.add(item_id)
            self.user_list.item(item_id, tags=("checked",))

    def select_all(self):
        for item_id in self.user_list.get_children():
            self.selected_items.add(item_id)
            self.user_list.item(item_id, tags=("checked",))

    def deselect_all(self):
        for item_id in self.user_list.get_children():
            self.selected_items.remove(item_id)
            self.user_list.item(item_id, tags=("unchecked",))
            
    def select_each(self):
        selected_item = self.user_list.selection()
        if selected_item:
            self.selected_items.add(selected_item)
            self.user_list.item(selected_item ,tags=('checked',))

    def delete_selected(self):
        for item_id in self.selected_items:
            self.user_list.delete(item_id)
        self.selected_items.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = UserManagementApp(root)
    root.mainloop()

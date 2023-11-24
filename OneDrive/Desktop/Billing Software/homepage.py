import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from main import LoginApp 
 
class HomePage:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Home Page")
        
        # Load your background image and resize it to fit the screen dimensions
        self.background_image = Image.open("Images/b1.jpg")
        self.background_image = self.background_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        # Create a Canvas widget for the background image, set its size to screen dimensions
        self.canvas = tk.Canvas(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.pack()

        # Place the background image on the canvas
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        # Create buttons with different colors on the canvas
        button_styles = {
            "About": {"text": "About", "background": "green"},
            "Admin": {"text": "Admin", "bg": "blue"},
            "Login": {"text": "Login", "bg": "blue"}
        }

        # Y-coordinate to position buttons
        for page_name, style_info in button_styles.items():
            if page_name == "About":
                x_coordinate = 1270  # Move the "About" button to the left side
                y_coordinate = 60
            elif page_name == "Admin":
                x_coordinate = self.root.winfo_screenwidth() - 200  # Move the "Login" button to the right side
                y_coordinate = 60
            elif page_name == "Login":
                x_coordinate = self.root.winfo_screenwidth() - 945  # Move the "Admin" button to the right side
                y_coordinate = 390
            else:
                x_coordinate = 20

            button = ttk.Button(
                self.root,
                text=style_info["text"],
                style="Content.TButton",
                command=lambda name=page_name: self.open_page(name),
                cursor="hand2"  # Set the cursor to "hand2" for pointer effect
            )
            self.canvas.create_window(x_coordinate, y_coordinate, anchor="nw", window=button, width=100, height=40)
            y_coordinate += 50  # Increase the y-coordinate for the next button

        # Create a transparent label to display the text in 1 line and move it to the right-center
        text_line = "Billing software simplifies product management by enabling users to add and remove items from their inventory effortlessly. It streamlines the billing process, automates invoicing, and manages product catalogs efficiently, making it essential for businesses."

        # Create a transparent image (1x1 pixel)
        transparent_image = Image.new("RGBA", (1, 1), (255, 255, 255, 0))
        transparent_photo = ImageTk.PhotoImage(transparent_image)

        # Use the transparent image as the label's background
        text_label = tk.Label(self.canvas, text=text_line, font=("Helvetica", 16), fg="black", image=transparent_photo,
                            compound="center", justify="left", wraplength=500)
        text_label.place(relx=0.7, rely=0.4, anchor="center")

    def open_page(self, name):
        home.exit_home_screen()
        root = tk.Tk()
        if name == "Admin":
            LoginApp(root)
        elif name == "Login":
            LoginApp(root).open_billing_app()
            pass
            
    def run(self):
        self.root.mainloop()
    
    def exit_home_screen(self):
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    home = HomePage(root)
    home.run()
    

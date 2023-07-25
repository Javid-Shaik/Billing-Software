# from tkinter import Tk, Label
# from PIL import Image, ImageTk

# root = Tk()

# # Load the GIF animation
# animation = Image.open("Images/homepage.gif")
# frames = []
# for frame in range(animation.n_frames):
#     animation.seek(frame)
#     frames.append(ImageTk.PhotoImage(animation))

# # Create a Label widget to display the animation
# label = Label(root)
# label.pack()

# # Function to update the animation frame
# def update_frame(frame=0):
#     label.config(image=frames[frame])
#     frame = (frame + 1) % len(frames)
#     root.after(100, update_frame, frame)

# # Start the animation
# update_frame()

# root.mainloop()

import win32print
import win32con

def print_bill(bill_data):
    printer_name = win32print.GetDefaultPrinter()

    # Create a printer handle
    handle = win32print.OpenPrinter(printer_name)

    # Set the print properties
    properties = win32print.GetPrinter(handle, 2)
    properties['pDevMode'].Orientation = win32con.DMORIENT_LANDSCAPE
    properties['pDevMode'].PaperSize = win32con.DMPAPER_A4
    win32print.SetPrinter(handle, 2, properties, 0)

    # Print the bill
    win32print.StartDocPrinter(handle, 1, ("Bill", None, "RAW"))
    win32print.StartPagePrinter(handle)
    
    for item in bill_data:
        line = f"{item['name']}: {item['price']}\n"
        win32print.WritePrinter(handle, line.encode('utf-8'))

    win32print.EndPagePrinter(handle)
    win32print.EndDocPrinter(handle)
    win32print.ClosePrinter(handle)

# Example bill data
bill = [
    {'name': 'Item 1', 'price': 10.99},
    {'name': 'Item 2', 'price': 5.99},
    {'name': 'Item 3', 'price': 7.99}
]

# Print the bill
print_bill(bill)

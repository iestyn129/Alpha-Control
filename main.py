from PIL import Image
import threading
import customtkinter as ctk
import tkinter as tk
import os
import time
import packaging
from tkinter import filedialog


class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.check_var = None
        self.checkbox = None
        self.do = None
        ctk.set_appearance_mode("dark")
        self.prgbar = None
        self.file_input = None
        self.root = None
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = ctk.CTk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.title("Alpha Control")
        self.root.geometry("480x300")
        self.root.resizable(False, False)

        border = ctk.CTkFrame(master=self.root)  # frame = clean
        border.pack(pady=10, padx=10, fill="both", expand=True)

        frame = ctk.CTkFrame(master=border)  # frame = clean
        frame.pack(pady=10, padx=10)

        frame2 = ctk.CTkFrame(master=border)  # frame = clean
        frame2.pack(pady=10, padx=10)

        title = ctk.CTkLabel(master=frame, text="Input File: ", font=("Nunito", 14))
        title.grid(row=0, column=0, padx=10, pady=20)

        self.file_input = ctk.CTkEntry(master=frame, width=180, placeholder_text="Input File", font=("Nunito", 14))
        self.file_input.grid(row=0, column=1, padx=10, pady=20)

        button = ctk.CTkButton(master=frame, text="Browse", width=80, command=input_file, fg_color="#c51b1b",
                               hover_color="#7f0000", font=("Nunito", 14))
        button.grid(row=0, column=2, padx=10, pady=20)
        
        self.check_var = ctk.StringVar(value="off")
        self.checkbox = ctk.CTkCheckBox(master=frame2, text="Premultiply?", variable=self.check_var, onvalue="on", offvalue="off", font=("Nunito", 14), command=checkbox_event)
        self.checkbox.pack(pady=15, padx=20)

        self.do = ctk.CTkButton(master=frame2, anchor="center", text="Unpremultiply Alpha", command=start, fg_color="#c51b1b",
                           hover_color="#7f0000", font=("Nunito", 17))
        self.do.pack(pady=15, padx=20)

        self.prgbar = ctk.CTkProgressBar(master=border, orientation="horizontal", mode="indeterminate")
        self.prgbar.pack(padx=20, pady=20)

        self.root.mainloop()

    # Add a method to get file_input value from outside the class
    def get_file_input(self):
        return self.file_input.get()

    def set_file_input_value(self, value):
        self.file_input.delete(0, tk.END)
        self.file_input.insert(0, value)

    def prgbar_start(self):
        self.prgbar.start()

    def prgbar_stop(self):
        self.prgbar.stop()

    def doBtnPMA(self, config):
        return self.do.configure(text=config)

    def doBtnGet(self):
        return self.do.cget("text")

    def fuck_you(self):
        return self.check_var.get()


app = App()


def checkbox_event():
    if app.doBtnGet() == "Premultiply Alpha":
        app.doBtnPMA("Unpremultiply Alpha")
    else:
        app.doBtnPMA("Premultiply Alpha")


def input_file():
    global filepath
    filepath = filedialog.askopenfilename(filetypes=[(".PNGs", ["*.png"])])
    filepath = os.path.normpath(filepath)
    app.set_file_input_value(filepath)
    return filepath


def perform_file_operations():
    app.prgbar_start()

    print(app.fuck_you())
    if app.fuck_you() == "off":
        unpremultiply(filepath)
    else:
        premultiply(filepath)


def start():
    threading.Thread(target=perform_file_operations).start()


def unpremultiply(image_path):
    img = Image.open(image_path)
    img_data = img.load()
    width, height = img.size

    for y in range(height):
        for x in range(width):
            r, g, b, a = img_data[x, y]

            if a != 0:
                r = int((255 * r) / a)
                g = int((255 * g) / a)
                b = int((255 * b) / a)

            img_data[x, y] = (r, g, b, a)

    img.save(f"{os.path.splitext(image_path)[0]}_unpremultiplied.png")
    app.prgbar_stop()


def premultiply(image_path):
    img = Image.open(image_path)
    img_data = img.load()
    width, height = img.size

    for y in range(height):
        for x in range(width):
            r, g, b, a = img_data[x, y]

            r = int((r * a) / 255)
            g = int((g * a) / 255)
            b = int((b * a) / 255)

            img_data[x, y] = (r, g, b, a)

    img.save(f"{os.path.splitext(image_path)[0]}_premultiplied.png")
    app.prgbar_stop()


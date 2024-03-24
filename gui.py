import tkinter as tk


class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Hello World")
        self.window.geometry("300x200")
        self.label = tk.Label(self.window, text="Hello World!")
        self.label.pack()
        self.window.mainloop()
        
        
        

if __name__ == "__main__":
    gui = GUI()

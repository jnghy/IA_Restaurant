import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import menu as m

class App(tk.Tk):
    def __init__(self):
        # Create the window
        super().__init__()
        self.title("Restaurant Management System")
        self.geometry("%dx%d+0+0" % (self.winfo_screenwidth(),self.winfo_screenheight()))
        self.protocol("WM_DELETE_WINDOW", self.callback)

        m.menu()

    def callback(self):
        if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            self.destroy()

if __name__ == "__main__":
    app = App()         # Run our window, called AppWindow
    app.mainloop()         # Start the program loop until all windows exit


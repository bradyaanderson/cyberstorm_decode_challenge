###########################################################
# Names: Brady, Zach, and Sam
# Date: 4/30/17
# This is a test for the GUI for Constellation Crack.
###########################################################
from Tkinter import *

class Window:
    def __init__(self, master):
        self.master = master
        master.title("Constellation Crack")

        self.set_up_gui()

    # sets up GUI for application
    def set_up_gui(self):
        self.widget_w = int(WIDTH/16)
        self.widget_h = int(HEIGHT/27)

        self.set_up_code_box(0, 0)
        self.set_up_timer_box(1, 0)
        self.set_up_image_box(0, 1)
        self.set_up_hints_box(1, 1)

    # set up code box
    def set_up_code_box(self, r, c):
        self.code = Label(self.master, text="This is where the code will be", bg="green",
                            width=self.widget_w, height=self.widget_h)
        self.code.grid(row=r, column=c)

    # set up timer box
    def set_up_timer_box(self, r, c):
        self.timer = Label(self.master, text="This is where the timer will be", bg="red",
                            width=self.widget_w, height=self.widget_h)
        self.timer.grid(row=r, column=c)

    # set up image box
    def set_up_image_box(self, r, c):
        self.image = Label(self.master, text="This is where the image will be", bg="blue",
                            width=self.widget_w, height=self.widget_h)
        self.image.grid(row=r, column=c)

    # set up hints box
    def set_up_hints_box(self, r, c):
        self.hints = Label(self.master, text="This is where the hints will be", bg="orange",
                            width=self.widget_w, height=self.widget_h)
        self.hints.grid(row=r, column=c)




WIDTH = 1280
HEIGHT = 720

app = Tk()
window = Window(app)
app.geometry('{}x{}'.format(WIDTH, HEIGHT))
app.mainloop()

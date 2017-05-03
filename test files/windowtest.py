###########################################################
# Names: Brady, Zach, and Sam
# Date: 4/30/17
# This is a test for the GUI for Constellation Crack.
###########################################################
from Tkinter import *
from time import time
from datetime import timedelta

class Timer(object):
    def __init__(self, total_time):
        self.total_time = total_time
        self.start_time = time()

    def get_time_left(self):
        current_time_left = self.total_time - time() + self.start_time
        if current_time_left > 0:
            return str(timedelta(seconds=current_time_left+1))[3:7]
        return '0:00'

class Window:
    def __init__(self):
        self.root = Tk()
        self.root.title("Constellation Crack")
        self.root.configure(bg="black")
        self.game_time = Timer(300)
        self.set_up_gui()

        self.update_timer()
        self.root.mainloop()

    def update_timer(self):
        self.timer.configure(text=self.game_time.get_time_left())
        self.root.after(100, self.update_timer)



    # sets up GUI for application
    def set_up_gui(self):
        self.widget_w = int(WIDTH/90)
        self.widget_h = int(HEIGHT/130)

        self.set_up_code_box(0, 0)
        self.set_up_timer_box(1, 0)
        self.set_up_image_box(0, 1)
        self.set_up_hints_box(1, 1)

    # set up code box
    def set_up_code_box(self, r, c):
        self.code = Label(self.root, text="DF%$JD!WEK]", bg="green",
                            width=self.widget_w, height=self.widget_h, font=("Courier", 50))
        self.code.grid(row=r, column=c)

    # set up timer box
    def set_up_timer_box(self, r, c):
        self.timer = Label(self.root, text="This is where the timer will be", bg="red",
                            width=self.widget_w, height=self.widget_h, font=("Courier", 50))
        self.timer.grid(row=r, column=c)

    # set up image box
    def set_up_image_box(self, r, c):
        photo = PhotoImage(file="test.gif")

        self.image = Label(self.root, image=photo,
                            width=500, height=370, bg="black")
        self.image.image = photo
        self.image.grid(row=r, column=c)

    # set up hints box
    def set_up_hints_box(self, r, c):
        self.hints = Label(self.root, text="This is where the hints will be", bg="orange",
                            width=int(self.widget_w * (5/2.)), height=int(self.widget_h * (5/2.)), font=("Courier", 20))
        self.hints.grid(row=r, column=c)

WIDTH = 1280
HEIGHT = 720

app = Window()

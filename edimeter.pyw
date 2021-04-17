import time
import datetime as dt

import tkinter as tk
from tkinter import messagebox

t_now = dt.datetime.now()
t_pom = 1*60
t_delta = dt.timedelta(0, t_pom)
t_fut = t_now +t_delta
delta_sec = 5*60
t_fin = t_now+dt.timedelta(0,t_pom+delta_sec)

root = tk.Tk()
root.withdraw()

root = tk.Tk()
root.withdraw()

messagebox.showinfo("Pomodoro started", "\n it is now"+t_now.strftime("%H:%M")+"hrs.\nTimer set up for 25 mins")

while True:
    if t_now < t_fut:
        #print('pomodoro')
    elif t_fut <= t_now <=t_fin:
        print('in break')
        if breaks == 0:
            print('if break')
            
        print('Break time!')
        breaks += 1
    else:
        print('finished')
        breaks = 0
        
        usr_ans = messagebox.askyesno("Pomodoro Finished", "would you like to start another pomodoro?")
        total_pomodoros +=1
        if usr_ans == True:
            t_now = dt.datetime.now()
            t_fut = t_now +dt.timedelta(0,t_pom)
            t_fin = t_now +dt.timedelta(0,t_pom+delta_sec)
            continue
        elif usr_ans == False:
            messagebox.showinfo("Pomodoro Finished", "\n You completed "+str(total_pomodoros)+" pomodoros today!")
            
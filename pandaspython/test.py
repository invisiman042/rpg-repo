from distutils import command
from tkinter import *
import time
from turtle import width

nb_cookie = 0
multiplicator = 1
cookie_per_second = 0
rate = 0

fenetre = Tk()
# fenetre.geometry('200x200')

def add_cookie():
    global nb_cookie
    global multiplicator
    nb_cookie += multiplicator
    cookie_count.config(text=f'{nb_cookie} cookies')

def enable_button():
    if str(bouton_clic['state']) == DISABLED:
        bouton_clic.config(state=NORMAL)
    else:
        bouton_clic.config(state=DISABLED)

def autoclic():
    global nb_cookie
    global fenetre
    nb_cookie += 1
    cookie_count.config(text=f'{nb_cookie} cookies')
    fenetre.after(1000, autoclic)

# def calculate_rate():
#     global cookie_per_second
#     print(cookie_per_second)
#     return int(cookie_per_second)

# def update_rate():
#     firt_value = calculate_rate
#     second_value = fenetre.after(100, calculate_rate)
#     rate = second_value - firt_value
#     cookie_rate.config(text=f'{rate} cookies')

photo = PhotoImage(file = 'cookie.png')
photo = photo.subsample(10, 10)

cookie_count = Label(fenetre, text=f'{nb_cookie} cookies', bg='white')
cookie_count.pack()

# cookie_rate = Label(fenetre, text=f'{cookie_per_second} /s', bg='white')
# cookie_rate.pack()

bouton_clic = Button(fenetre, text='Cookie', command=add_cookie, height=100, width=100, image=photo, bg='white')
bouton_clic.pack()

bouton_enable = Button(fenetre, text='disable / enable cookie', command=enable_button)
bouton_enable.pack()

bouton_autoclic = Button(fenetre, text='purchase autoclic', command=autoclic)
bouton_autoclic.pack()

# bouton_update = Button(fenetre, text='update rate', command=update_rate)
# bouton_update.pack()

mainloop()
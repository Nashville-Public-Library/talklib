import sqlite3
from tkinter import *
from tkinter import ttk


connection = sqlite3.connect('D:/wireready/test.db')
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS tlshow (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                show TEXT, 
                show_filename TEXT, 
                url TEXT DEFAULT NULL,
                is_permalink INTEGER DEFAULT 0,
                include_date INTEGER DEFAULT 0,
                remove_yesterday INTEGER DEFAULT 0,
                is_local INTEGER DEFAULT 0,
                local_file TEXT DEFAULT NULL,
                remove_source INTEGER DEFAULT 0,
                check_if_above INTEGER DEFAULT 0,
                check_if_below INTEGER DEFAULT 0
                )''')

rows = cursor.execute("SELECT * FROM tlshow")
for row in rows:
    print(row)

cursor.close()
connection.close()



root = Tk()
root.title("talklib GUI")
root.geometry("1024x600")
main_window = ttk.Frame(root)
main_window.pack()



root.mainloop()
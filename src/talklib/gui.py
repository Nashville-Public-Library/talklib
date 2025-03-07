import sqlite3
from tkinter import *
from tkinter import ttk

def sql_new_RSS_show(show, show_filename, url, include_date=0, remove_yesterday=0, check_if_above=0, check_if_below=0):
    connection = sqlite3.connect('D:/wireready/test.db')
    cursor = connection.cursor()

    cursor.execute(f'''INSERT INTO tlshow (
                   show,
                   show_filename,
                   url,
                   include_date,
                   remove_yesterday,
                   check_if_above,
                   check_if_below
                   )
                   VALUES (?, ?, ?, ?, ?, ?, ?);''', 
                   (show, show_filename, url, include_date, remove_yesterday, check_if_above, check_if_below))
    connection.commit()
    
def sql_read_table():

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

    return rows

root = Tk()
root.title("talklib GUI")
root.geometry("1024x600")
main_window = ttk.Frame(root)
main_window.grid()

rows = sql_read_table()
row_num = 0
for row in rows:
    pod_window = ttk.Frame(main_window, padding=20)
    pod_window.pack()
    label = ttk.Label(master=pod_window, text=str(row[1]))
    label.grid()
    ttk.Button(master=pod_window, text="EDIT").grid()
    for r in row:
        ttk.Label(master=pod_window, text=str(r)).grid()    
    row_num = row_num +1


root.mainloop()

# sql_new_RSS_show(show='New York Times', show_filename='NYT', url='http://wireready.org/tic/nytimes.rss', remove_yesterday=1, include_date=1, check_if_above=59, check_if_below=55)

rows = sql_read_table()
for row in rows:
    print(row)
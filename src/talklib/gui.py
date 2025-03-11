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

def sql_column_names():
    connection = sqlite3.connect('D:/wireready/test.db')
    cursor = connection.cursor()
    cursor.execute(f"PRAGMA table_info(tlshow);")
    columns = cursor.fetchall()
    return columns

def sql_delete_row(id: int):
    connection = sqlite3.connect('D:/wireready/test.db')
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM tlshow WHERE id = {id};")
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
root.geometry("1400x600")
main_window = ttk.Frame(root)
main_window.grid()

names = ttk.Frame(main_window).grid()
name_column_num = 1
columns = sql_column_names()
for column in columns:
    label = ttk.Label(master=names, text=column[1]).grid(row=0, column=name_column_num, sticky="w")
    name_column_num +=1
rows = sql_read_table()
row_num = 1
for row in rows:
    pod_window = ttk.Frame(main_window).grid()
    # pod_window.pack()
    label = ttk.Label(master=pod_window).grid(row=row_num, column=0)
    ttk.Button(master=label, text="EDIT").grid(row=row_num, pady=5, padx=5)
    column_num = 1
    for index, value in enumerate(row):
        # set 0 & 1 to False & True EXCEPT for the first item (the primary key, the first of which is labelled 1)
        if index != 0:
            if value == 0:
                value = False
            if value == 1:
                value = True
        ttk.Label(master=label, text=str(value)).grid(column=column_num, row=row_num, sticky="w")    
        column_num = column_num +1
    row_num += 1


root.mainloop()

# sql_new_RSS_show(show='Washington Post', show_filename='WP', url='https://wireready.org/tic/wash.rss', remove_yesterday=1, include_date=1, check_if_above=59, check_if_below=55)

# sql_column_names()
# rows = sql_read_table()
# for row in rows:
#     print(row)
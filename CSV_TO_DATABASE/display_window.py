


import tkinter as tk
from tkinter import messagebox
import data_ui as du







class Database_ui:

    def get_values(self):

        password = entry.get()
        database = entry1.get()
        return password, database

    def get_entries(self):

        passw, db_ = self.get_values()
        db = du.Database_connect(passw, db_)
        cursor_check = db.try_connection()

        if cursor_check != None:
            top_1 = tk.Tk()
            canvas_1 = tk.Canvas(
                    top_1, width=400, height=250, background="light blue")

            tk.Label(top_1, text="Select Table to Read Data", font=(
                    "Helvetica", 14), background="light blue").place(x=100, y=50)

            table_name = tk.Entry(top_1)

            tk.Label(top_1, text="Table name", font=("Helvetica", 12),
                         background="light blue").place(x=90, y=120)
            canvas_1.create_window(240, 130, window=table_name)

            def read_data():
                
                table_ = table_name.get()
                tabel_record = db.select_tables(table_)
                if tabel_record != -1:
                    messagebox.showinfo("info", tabel_record)
                else:
                    messagebox.showerror(
                            "error", "table not present or wrong query")

            tk.Button(top_1, text="Read", bg='white',
                          fg='Black', command=read_data).place(x=90, y=170)

            canvas_1.pack()
            canvas_1.mainloop()
        else:
            messagebox.showerror(
                "error", "either password or database name invalid ")

    def csv_data(self):

        passw, db_ = self.get_values()
        db = du.Database_connect(passw, db_)
        cursor_check = db.try_connection()

        if cursor_check != None:

            top_1 = tk.Tk()
            canvas_1 = tk.Canvas(
                    top_1, width=400, height=250, background="light blue")

            tk.Label(top_1, text="Select a CSV file", font=(
                    "Helvetica", 14), background="light blue").place(x=100, y=50)

            file_name = tk.Entry(top_1)

            tk.Label(top_1, text="File name", font=("Helvetica", 12),
                         background="light blue").place(x=90, y=100)

            canvas_1.create_window(240, 110, window=file_name)

            user_table = tk.Entry(top_1)

            tk.Label(top_1, text="table name", font=("Helvetica", 12),
                         background="light blue").place(x=90, y=140)

            canvas_1.create_window(240, 150, window=user_table)

            def write_data():

                file_ = file_name.get()
                table_ = user_table.get()

                tabel_result = db.create_table(file_, table_)

                if tabel_result != -1:

                    messagebox.showinfo(
                            "info", "table create successfully!!!")

                else:

                    messagebox.showerror(
                            "error", "file not found or table already created")

            tk.Button(top_1, text="Create", bg='white',
                          fg='Black', command=write_data).place(x=90, y=170)

            canvas_1.pack()
            canvas_1.mainloop()

        else:

            messagebox.showerror("error","wrong databasename or password")

if __name__ == "__main__":
    
    dui = Database_ui()

    top = tk.Tk()
    canvas = tk.Canvas(top, width=400, height=250, background="light blue")
    tk.Label(top, text="Connect to Database",
             font=("Helvetica", 14), background="light blue").place(x=100, y=50)
    tk.Label(top, text="Password", background="light blue",
             font=("Helvetica", 10)).place(x=100, y=88)
    tk.Label(top, text="DB Name", background="light blue",
             font=("Helvetica", 10)).place(x=100, y=120)

    entry = tk.Entry(top)
    entry1 = tk.Entry(top)

    canvas.create_window(240, 100, window=entry)
    canvas.create_window(240, 130, window=entry1)

    tk.Button(top, text="Read Data", bg='white',
              fg='Black', command=dui.get_entries).place(x=90, y=170)

    tk.Button(top, text="CSV to Database", bg='white',
              fg='Black', command=dui.csv_data).place(x=180, y=170)

    canvas.pack()
    canvas.mainloop()
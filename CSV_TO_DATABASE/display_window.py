import tkinter as tk
from tkinter import messagebox
import data_ui as du  # data_ui contains the Database_connect class

# Class for managing database interactions through GUI
class Database_ui:

    # Method to get password and database name from user input
    def get_values(self):
        password = entry.get()
        database = entry1.get()
        return password, database

    # Method to handle reading data from a table
    def get_entries(self):
        passw, db_ = self.get_values()
        db = du.Database_connect(passw, db_)  # Connect to the database
        cursor_check = db.try_connection()  # Check if connection is successful

        if cursor_check != None:  # If connection is successful
            # Create a new window for selecting table and displaying data
            top_1 = tk.Tk()
            canvas_1 = tk.Canvas(top_1, width=400, height=250, background="light blue")

            # Label and entry for entering table name
            tk.Label(top_1, text="Select Table to Read Data", font=("Helvetica", 14), background="light blue").place(x=100, y=50)
            table_name = tk.Entry(top_1)
            tk.Label(top_1, text="Table name", font=("Helvetica", 12), background="light blue").place(x=90, y=120)
            canvas_1.create_window(240, 130, window=table_name)

            # Function to read data from selected table
            def read_data():
                table_ = table_name.get()
                table_record = db.select_tables(table_)  # Retrieve data from the table
                if table_record != -1:
                    messagebox.showinfo("info", table_record)  # Display data in a messagebox
                else:
                    messagebox.showerror("error", "Table not present or wrong query")

            tk.Button(top_1, text="Read", bg='white', fg='Black', command=read_data).place(x=90, y=170)

            canvas_1.pack()
            canvas_1.mainloop()
        else:
            messagebox.showerror("error", "Either password or database name is invalid ")

    # Method to handle importing data from a CSV file
    def csv_data(self):
        passw, db_ = self.get_values()
        db = du.Database_connect(passw, db_)
        cursor_check = db.try_connection()

        if cursor_check != None:
            top_1 = tk.Tk()
            canvas_1 = tk.Canvas(top_1, width=400, height=250, background="light blue")

            tk.Label(top_1, text="Select a CSV file", font=("Helvetica", 14), background="light blue").place(x=100, y=50)
            file_name = tk.Entry(top_1)
            tk.Label(top_1, text="File name", font=("Helvetica", 12), background="light blue").place(x=90, y=100)
            canvas_1.create_window(240, 110, window=file_name)

            user_table = tk.Entry(top_1)
            tk.Label(top_1, text="table name", font=("Helvetica", 12), background="light blue").place(x=90, y=140)
            canvas_1.create_window(240, 150, window=user_table)

            def write_data():
                file_ = file_name.get()
                table_ = user_table.get()

                table_result = db.create_table(file_, table_)  # Create table from CSV file
                if table_result != -1:
                    messagebox.showinfo("info", "Table created successfully!!!")
                else:
                    messagebox.showerror("error", "File not found or table already created")

            tk.Button(top_1, text="Create", bg='white', fg='Black', command=write_data).place(x=90, y=170)

            canvas_1.pack()
            canvas_1.mainloop()
        else:
            messagebox.showerror("error", "Wrong database name or password")

if __name__ == "__main__":
    dui = Database_ui()  # Create an instance of Database_ui class

    # Create the main window for database connection
    top = tk.Tk()
    canvas = tk.Canvas(top, width=400, height=250, background="light blue")
    tk.Label(top, text="Connect to Database", font=("Helvetica", 14), background="light blue").place(x=100, y=50)
    tk.Label(top, text="Password", background="light blue", font=("Helvetica", 10)).place(x=100, y=88)
    tk.Label(top, text="DB Name", background="light blue", font=("Helvetica", 10)).place(x=100, y=120)

    # Entry fields for password and database name
    entry = tk.Entry(top)
    entry1 = tk.Entry(top)
    canvas.create_window(240, 100, window=entry)
   

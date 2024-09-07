import pandas as pd
import pyodbc


class ConnectionString:

    def __init__(self) -> None:
        self.conn_str = (
                'DRIVER={SQL Server};'
                'SERVER=looqupsqlserver.database.windows.net;'
                'DATABASE=consumerDB;'
                'UID=looqupadmin;'
                'PWD=L00uqup$dmin;')
    
class MakeConnection(ConnectionString):

    def __init__(self) -> None:
        super().__init__()

    def cursor_connection(self):

        try:
            connection = pyodbc.connect(self.conn_str,timeout=10)
            return connection
        except Exception as e:
            return e

class DatabaseOperations(MakeConnection):

    def __init__(self) -> None:
        super().__init__()
        self.cursor = self.cursor_connection().cursor()
    

    def read_from_table(self,table_name):

        try:
            sql_query = self.cursor.execute(f"SELECT * FROM {table_name};")
            # Fetch the data and column names
            rows = self.cursor.fetchall()
            print(rows)
            data = sql_query.fetchall()
            df = pd.DataFrame([list(data) for data in data], columns=[columns[0] for columns in sql_query.description])
            return df
        except Exception as e:
            return e



class WriteToTable(ConnectionString):
    
    def __init__(self):
        super().__init__()

    def append_dataframe_to_mysql(self,df=None, table_name=None):
        """
            Appends data from a DataFrame into an existing MySQL table.

            Parameters:
            df (pd.DataFrame): The DataFrame containing data to be appended.
            table_name (str): The name of the table where data will be appended.
           
            """
        try:
            # Connect to the MySQL server
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()
            # Generate the SQL query dynamically based on DataFrame columns
            columns = ', '.join(df.columns)  # Column names for the SQL query
            placeholders = ', '.join(['?'] * len(df.columns))  # Placeholders for values
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            # Convert DataFrame rows to list of tuples for executemany()
            data = [tuple(row) for row in df.to_numpy()]
            # Use executemany to append all rows at once
            cursor.executemany(sql, data)
            # Commit the transaction
            conn.commit()
            print(f"Data appended successfully to '{table_name}'.")
        except pyodbc.Error as e:
            print(f"Error appending data: {e}")
            

if __name__ == '__main__':
    d = DatabaseOperations()
    data = d.read_from_table(table_name='db0.fnbsynthdata')
    print(data)
    print(type(data))

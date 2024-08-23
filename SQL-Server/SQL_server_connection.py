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
            data = sql_query.fetchall()
            df = pd.DataFrame([list(data) for data in data], columns=[columns[0] for columns in sql_query.description])
            return df
        except Exception as e:
            return e


if __name__ == '__main__':
    d = DatabaseOperations()
    data = d.read_from_table(table_name='demand_predictions_table')
    print(data)
    print(type(data))

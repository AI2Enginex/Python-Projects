from sqlalchemy import create_engine
import urllib
import pyodbc
import pandas as pd

class ConnectionString:

    def __init__(self):
        self.conn_str = (
                    'DRIVER=################'
                    'SERVER=############'
                    'DATABASE=consumerDB;'
                    'UID=############'
                    'PWD=############')

class CreateEngine(ConnectionString):

    def __init__(self):
        super().__init__()

    def create_engine(self):
        try:
            quoted = urllib.parse.quote_plus(self.conn_str)
            return create_engine(f'mssql+pyodbc:///?odbc_connect={quoted}')
        except Exception as e:
            return e

class DatabaseOperations(CreateEngine):

    def __init__(self):
        super().__init__()

    def read_from_table(self,table_name):

        try:
            query = f"SELECT * FROM {table_name}"
            return pd.read_sql_query(query, con=self.create_engine())
        except Exception as e:
            return e
        
if __name__ == '__main__':

    d = DatabaseOperations()
    df = d.read_from_table(table_name='demand_predictions_table')
    print(df)

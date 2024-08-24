from sqlalchemy import create_engine  # Import SQLAlchemy for creating database engines
import urllib  # Import urllib for URL encoding the connection string
import pyodbc  # Import pyodbc for ODBC connections (used implicitly through SQLAlchemy)
import pandas as pd  # Import pandas for data manipulation and SQL operations

# class for connection parameters
class ConnectionString:

    def __init__(self):
        self.conn_str = (
                    'DRIVER={SQL Server};'
                    'SERVER=looqupsqlserver.database.windows.net;'
                    'DATABASE=consumerDB;'
                    'UID=looqupadmin;'
                    'PWD=L00uqup$dmin;')

# Class to create a SQLAlchemy engine, inherits from ConnectionString
class CreateEngine(ConnectionString):

    def __init__(self):
        # Call the constructor of the parent class (ConnectionString) to initialize the connection string
        super().__init__()

    def create_engine(self):
        # Method to create and return a SQLAlchemy engine
        try:
            # Encode the connection string to make it URL safe
            quoted = urllib.parse.quote_plus(self.conn_str)
            # Create the SQLAlchemy engine using the encoded connection string
            return create_engine(f'mssql+pyodbc:///?odbc_connect={quoted}')
        except Exception as e:
            # Return the exception if something goes wrong
            return e

# Class to handle database operations, inherits from CreateEngine
class DatabaseOperations(CreateEngine):

    def __init__(self):
        # Call the constructor of the parent class (CreateEngine) to initialize the engine creation process
        super().__init__()
    
    # Method to read list of tables from the database
    def list_tables(self):
        try:
            # SQL query to retrieve the list of tables in the current database
            query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';"
            # Execute the query and return the result as a DataFrame
            return pd.read_sql_query(query, con=self.create_engine())
        except Exception as e:
            return e
        
    
    # Method to read data from a specified table
    def read_from_table(self, table_name=None):
        try:
            # Define the SQL query to select all records from the specified table
            query = f"SELECT * FROM {table_name}"
            # Execute the query using pandas and return the result as a DataFrame
            return pd.read_sql_query(query, con=self.create_engine())
        except Exception as e:
            # Return the exception if something goes wrong
            return e
        
    # Method to read data using limit 
    def read_from_table_with_limit(self, table_name=None, limit=None):
        try:
            # SQL query to select top 'limit' rows from the specified table
            query = f"SELECT TOP {limit} * FROM {table_name}"
            # Execute the query and return the result as a DataFrame
            return pd.read_sql_query(query, con=self.create_engine())
        except Exception as e:
            return e
    # Method to write a DataFrame into a specified table (replacing the table if it exists)
    def write_into_table(self, dataframe=None, table=None):
        try:
            # Write the DataFrame to the SQL table, replacing the table if it already exists
            dataframe.to_sql(table, con=self.create_engine(), if_exists='replace', index=False)
        except Exception as e:
            # Return the exception if something goes wrong
            return e
        
    # Method to write a DataFrame into a specified table (appending data if the table exists)
    def write_to_table_if_exists(self, dataframe=None, table_name=None):
        try:
            # Write the DataFrame to the SQL table, appending the data if the table already exists
            dataframe.to_sql(table_name, con=self.create_engine(), if_exists='append', index=False)
        except Exception as e:
            # Return the exception if something goes wrong
            return e

# Main block to execute when the script runs
if __name__ == '__main__':
    # Instantiate the DatabaseOperations class
    d = DatabaseOperations()

    # Read data from the 'demand_predictions_table' SQL table and store it in a DataFrame
    df = d.read_from_table(table_name='demand_predictions_table')

    # Print the DataFrame to the console
    print(df)
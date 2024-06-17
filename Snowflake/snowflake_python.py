import snowflake.connector
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas



class Connector:
    def __init__(self, username=None, password=None, account_identifier=None, database=None, schema=None):
        # Initialize and establish a connection to Snowflake
        self.ctx = snowflake.connector.connect(
            user=username,
            password=password,
            account=account_identifier,
            database=database,
            schema=schema
        )
        # Create a cursor object to interact with Snowflake
        self.cs = self.ctx.cursor()

class DataBaseTableFunctions(Connector):
    def __init__(self, username=None, password=None, account_identifier=None, database=None, schema=None):
        # Initialize the parent Connector class with the provided parameters
        super().__init__(username, password, account_identifier, database, schema)

    def get_all_tables(self):
        try:
            # Execute a SQL query to retrieve all table names in the schema
            query = "SHOW tables"
            self.cs.execute(query)

            # Fetch all rows from the executed query and return table names as a list
            return [tup[1] for tup in self.cs.fetchall()]
        except Exception as e:
            # Return the exception if any occurs
            return e

    def read_table_data(self, table=None):
        try:
            # Execute a SQL query to select all data from the specified table
            query = f"SELECT * FROM {table}"
            self.cs.execute(query)

            # Fetch all rows from the executed query into a DataFrame
            df = pd.DataFrame(self.cs.fetchall(), columns=[desc[0] for desc in self.cs.description])

            # Return the DataFrame
            return df
        except Exception as e:
            # Return the exception if any occurs
            return e

    def create_table_schema(self, table_name=None, data=None):
        try:
            # Create an initial table with a dummy column 'name'
            self.cs.execute(f"CREATE TABLE {table_name}(name VARCHAR(30))")

            # Iterate over columns in the DataFrame to add them to the table
            for cols in data.columns:
                if data[cols].dtypes != 'object':
                    # If column type is not object (i.e., numerical), add it as INT
                    self.cs.execute(f"ALTER TABLE {table_name} ADD({cols} INT)")
                else:
                    # If column type is object (i.e., string), add it as VARCHAR(100)
                    self.cs.execute(f"ALTER TABLE {table_name} ADD({cols} VARCHAR(100))")

            # Drop the initial dummy column 'name' from the table
            self.cs.execute(f"ALTER TABLE {table_name} DROP name")
            print(f"Table {table_name} created successfully")
        except Exception as e:
            # Return the exception if any occurs
            return e

    def update_table(self, df=None, table=None):
        try:
            # transform the data using python and store it into a new table
            # Insert the DataFrame into the specified Snowflake table
            # If create_auto is True, automatically create the table if it does not exist
            write_pandas(self.ctx, df, table, auto_create_table=True)
            print(f"Successfully inserted rows into {table}.")
        except Exception as e:
            # Print the exception if any occurs
            print(f"An error occurred: {e}")

    def close_connection(self):
        try:
            # Close the cursor and the Snowflake connection
            self.cs.close()
            self.ctx.close()
            print('Cursor and connection closed successfully!')
        except Exception as e:
            # Return the exception if any occurs
            return e

if __name__ == '__main__':
    pass
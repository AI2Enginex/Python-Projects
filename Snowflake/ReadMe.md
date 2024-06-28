# Snowpark Python

This repository provides a set of utility functions for interacting with Snowflake using Python and Pandas. The main functionalities include connecting to Snowflake, 
retrieving table data, creating tables based on DataFrame schemas, inserting data into tables, and closing connections.

# Overview

The script contains two main classes:

Connector: Handles the connection to Snowflake.

DataBaseTableFunctions: Inherits from the Connector class and provides various methods to interact with Snowflake tables.

# Classes and Methods

1. Connector Class
   
The Connector class establishes and manages the connection to the Snowflake database.

Parameters:

username: Snowflake username.

password: Snowflake password.

account_identifier: Snowflake account identifier.

database: Default database to connect to.

schema: Default schema to use.

Creates a connection (self.ctx) and a cursor (self.cs) to interact with Snowflake.

2. DataBaseTableFunctions Class
   
The DataBaseTableFunctions class inherits from Connector and provides various database operations.

Inherits from Connector and initializes it with the provided parameters.

# get_all_tables Method:

Retrieves the names of all tables in the current schema.
Returns a list of table names.

# read_table_data Method:

Parameters:

table: The name of the table to read data from.

Executes a SELECT * query on the specified table.

Fetches the data and returns it as a Pandas DataFrame.

# create_table_schema Method:

Parameters:

table_name: The name of the table to be created.

data: A Pandas DataFrame whose schema will be used to create the table.

Creates a new table with the schema based on the DataFrame's columns.

Columns with non-object data types are added as INT.

Columns with object data types are added as VARCHAR(100).

Drops an initially created dummy column name.

# update_table Method:

Parameters:

df: The Pandas DataFrame to be inserted into the table.

table: The name of the table where the data will be inserted.

create_auto: If True, the table is automatically created if it doesn't exist.

Inserts the DataFrame into the specified Snowflake table using the write_pandas function from snowflake.connector.pandas_tools.

# close_connection Method:

Closes the cursor and the Snowflake connection.

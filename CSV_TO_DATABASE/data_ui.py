import os
import pymysql
import sqlalchemy
import pandas as pd


class Database_connect:

    def __init__(self, password, database):

        self.password = password
        self.database_name = database

    def try_connection(self):

        try:
            self.engine = sqlalchemy.create_engine(
                f'mysql+pymysql://root:{self.password}@localhost:3306/{self.database_name}')
            self.conn = pymysql.connect(
                host='localhost',
                user='root',
                password=self.password,
                db=self.database_name,
            )

            return self.conn.cursor()
        except:
            return None

    def select_tables(self, table_name):

        try:
            self.cur = self.try_connection()
            self.cur.execute(f"select * from {table_name}")
            output = self.cur.fetchall()
            self.cur.close()
            return output

        except:

            return -1

    def create_table(self,file,table_name):

        if os.path.isfile(file):
            self.df = pd.read_csv(file)
            try:
                self.cur = self.try_connection()
                self.cur.execute(f"create table {table_name}(name varchar(30))")
                for cols in self.df.columns:
                    if self.df[cols].dtypes != 'object':
                        self.cur.execute(f"alter table {table_name} add({cols} int)")

                    else:
                        self.cur.execute(f"alter table {table_name} add({cols} varchar(100))")
                self.cur.execute(f"alter table {table_name} drop name")

                self.df.to_sql(
                    name = table_name,
                    con = self.engine,
                    index = False,
                    if_exists = 'append')

            except:

                return -1
           
                

        else:
            return -1

if __name__ == "__main__":

    pass

import warnings
from pymongo import MongoClient
warnings.filterwarnings('ignore')


class Mongo_db:

    def __init__(self, db_name, collection_):

        try:
            self.mongoClient = MongoClient('mongodb://localhost:27017/')
            self.mydb = self.mongoClient[db_name]
            self.collection_name = self.mydb[collection_]
        except:
            return None

    def check_existance(self, key):

        result = self.collection_name.find({key: {"$exists": True}})
        return [value for value in result]

    def set_values(self, key, old_value, new_value):

        my_query = {key: old_value}
        new_values = {"$set": {key: new_value}}
        return my_query, new_values

    def fetch_record(self, master_query, field_name, value):

        query_list = list()

        
        if field_name is 'all' and value is None:
            for data in self.collection_name.find({}):
                query_list.append(data)

        elif master_query != None:
            for data in self.collection_name.find({master_query: {field_name: value}}):
                query_list.append(data)

        else:
            for data in self.collection_name.find({field_name: value}):
                query_list.append(data)

        return query_list
        
        

    def conditional_fetch(self, key, condition, some_value):

        con_query = list()

        query_result = self.check_existance(key)
       
        try:
            if len(query_result) > 0:
                for data in self.collection_name.find({key: {condition: some_value}}):
                    con_query.append(data)
                else:
                    return con_query
            return con_query
        except:
            return "Error"
       

    def insert_query(self, master_query, update_scope, my_query, new_values):

        try:

            if update_scope is 'one' and master_query is None:

                self.collection_name.insert_one(my_query, new_values)
                print("Successfiul")

            elif update_scope is 'many' and master_query is None:

                self.collection_name.insert_many(my_query, new_values)
                print("Successfiul")

        except:
            print("unsuccessful")

    def update_query(self, update_scope, key, my_query, new_values):

        query_result = self.check_existance(key)
        queries, values = self.set_values(key, my_query, new_values)

        try:

            if update_scope is 'one' and len(query_result) > 0:

                self.collection_name.update_one(queries, values)
                print("Successfiul")

            elif update_scope is 'many' and len(query_result) > 0:

                self.collection_name.update_many(queries, values)
                print("Successfiul")
        except:

            print("unsuccessful")

    def conditional_update(self, key, condition, some_value, new_key, val):

        query_result = self.check_existance(key)

        try:

            if len(query_result) > 0:
                self.collection_name.update_many(
                    {key: {condition: some_value}}, {"$set": {new_key: val}})
                print("successful")
            else:
                print("not found")
        except:

            print("unsuccessful")

    def delete_query(self, drop_condition, key, my_query):

        query_result = self.check_existance(key)
        result = {key: my_query}

        try:

            if drop_condition is 'one' and len(query_result) > 0:

                self.collection_name.delete_one(result)
                print("Successfiul")

            elif drop_condition is 'many' and len(query_result) > 0:

                self.collection_name.delete_many(result)
                print("Successfiul")
        except:

            print("unsuccessful")

    def delete_single_val(self, key, query):

        query_result = self.check_existance(key)
        try:
            if len(query_result) > 0:
                self.collection_name.update_many({},{"$unset": {key: query}})
                print("Successful")
            else:
                print("not found")
        except:
            print("unsuccessful operation!!!")


class Aggregate_Functions(Mongo_db):

    def __init__(self, db_name, collection_):

        super().__init__(db_name, collection_)

        self.database = db_name
        self.coll_array = self.collection_name
        self.aggregate_result = []

    def agg_func_opr(self, operation, field_name1, field_name2, new_field, agg_operation, val):

        try:

            agg_re = self.coll_array.aggregate([
                {
                    operation: {field_name1: field_name2,
                                new_field: {agg_operation: val}}
                }

            ])
            for data in agg_re:
                self.aggregate_result.append(data)
        except:
            return self.aggregate_result
        return self.aggregate_result

    def get_mul_val(self, operation, field_name1, field_name2, col1, col2, new_field1, new_field2, agg_operation1, agg_operation2):

        try:
            multiple_agg_opr = self.coll_array.aggregate([
                {
                    operation: {
                        field_name1: field_name2,
                        new_field1: {agg_operation1: col1},
                        new_field2: {agg_operation2: col2},

                    }
                }

            ])

            for data in multiple_agg_opr:
                self.aggregate_result.append(data)
        except:
            return self.aggregate_result
        return self.aggregate_result


class Database_records:

    def __init__(self, data_base_name, collection_name):

        self.aggf = Aggregate_Functions(
            db_name=data_base_name, collection_=collection_name)

    def insert_record(self, query, scope, my_query, val):

        self.aggf.insert_query(query, scope, my_query, val)

    def update_record(self, key, scope, queries, values):

        self.aggf.update_query(scope, key, queries, values)

    def conditional_update(self, key, condition, some_value, new_key, val):

        self.aggf.conditional_update(key, condition, some_value, new_key, val)

    def delete_record(self, drop_condition, key, query):

        self.aggf.delete_query(drop_condition, key, query)

    def delete_single_val(self, key, condition):

        self.aggf.delete_single_val(key, condition)

    def read_table_record(self, query, field, val):

        result = self.aggf.fetch_record(
            master_query=query, field_name=field, value=val)

        if len(result) > 0:
            for data in result:
                print(data)
        else:
            print("somethong is wrong!!!!......ivalid arguments passed")

    def read_condition(self, key, condition, some_value):

        try:
            result_con = self.aggf.conditional_fetch(key, condition, some_value)
            print(result_con)
        except:
            print("Error")
       

    def aggr_func1(self, operation, field_name1, field_name2, new_field, agg_operation, val):

        result1 = self.aggf.agg_func_opr(
            operation, field_name1, field_name2, new_field, agg_operation, val)
        if len(result1) > 0:
            for data in result1:
                print(data)
        else:
            print("somethong is wrong!!!!......ivalid arguments passed")

    def agg_func2(self, operation, field_name1, field_name2, col1, col2, new_field1, new_field2, agg_operation1, agg_operation2):

        result2 = self.aggf.get_mul_val(
            operation, field_name1, field_name2, col1, col2, new_field1, new_field2, agg_operation1, agg_operation2)
        if len(result2) > 0:
            for data in result2:
                print(data)
        else:
            print("somethong is wrong!!!!......ivalid arguments passed")


if __name__ == '__main__':

    db_name = input('Enter database name : ')
    collection_name = input('Enter collection name : ')
    dbr = Database_records(db_name, collection_name)

    dbr.read_table_record(query=None, field='all', val=None)
    dbr.read_condition(key="comments", condition="$gte", some_value=30.0)
    dbr.delete_record(drop_condition='one', key='eligible', query='true')
    dbr.delete_single_val(key='eligible',condition=1)
    dbr.update_record(scope='many', key="user", queries='Engineer', values="Vibhor")

    dbr.conditional_update(key="comments",condition="$gt",some_value=15,new_key="eligible",val="true")

    dbr.aggr_func1(operation="$group", field_name1="_id", field_name2="$title",
    new_field="number_of_subs", agg_operation="$sum", val=1)

    dbr.agg_func2(operation="$group", field_name1="_id", field_name2="$title", col1="$comments",
    col2="$comments", new_field1="max", new_field2="total", agg_operation1="$max", agg_operation2="$avg")

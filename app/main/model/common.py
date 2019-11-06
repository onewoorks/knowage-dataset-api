from . import execute_query, insert_ws_data

class Common_Query:
    def register_ws(self,input):
        insert_ws_data(input)

#from services.intent_analyzer import extract_tables_from_question
#d = [{"id":"1", "table_name":"Prices"}, {"id":"2", "table_name":"Income"}]
#print(extract_tables_from_question(tables_names=d, question="What's the average product price last month?"))

#from services.llm_client import get_answer_and_sql_queries
#print(get_answer_and_sql_queries(table_data={"name":"incomes", "data":{"Jun":[20, 50, 80], "Jul":[90, 60, 10]}}, user_question="get me the avarage income in each month"))
#print(get_answer_and_sql_queries(table_data={"name":"incomes", "data":{"Jun":[20, 50, 80], "Jul":[90, 60, 10]}}, user_question="get me the avarage income in this year"))
#print(get_answer_and_sql_queries(table_data={"name":"incomes", "data":{"2025":{"Jun":[20, 50, 80], "Jul":[90, 60, 10]}}}, user_question="Now is Jul. add a buy as much as 63$"))
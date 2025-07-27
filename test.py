from services.intent_analyzer import extract_tables_from_question


print(extract_tables_from_question(tables_names=["Prices", "Incomes"], question="please add 5$ to price of pepsi soda"))
#from services.rag_builder import main_prompt
#d = [{"ID":"1", "name":"Prices"}, {"ID":"2", "name":"Income"}]
#print(main_prompt(table_names=d, user_text="What's the average product price last month?"))

from services.manager import manager

res = manager(user_text="add new employee to employee table. with age 25 and name Alex Dep and ID 1", user_id=1)
print(res)
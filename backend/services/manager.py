from services.llm_client import get_answer
from db.crud.table import get_user_table_names
from core.logger import logger
from services.change_compiler import PromptCompiler

def manager(user_text:str, user_id:int, table:str=None):
    try:
        tbls = [table] if table else get_user_table_names(user_id=user_id)
        res = get_answer(table_names=tbls, user_text=user_text)

        if not res["answer_sentence"]:
            return "Unfortunately, I did not understand your request. Please try again."

        if res["success"] == False:
            return res["answer_sentence"]
        
        if res["queries"] == []:
            return res["answer_sentence"]
        
        op_flag = False

        for q in res["queries"]:
            if not q or not isinstance(q, dict) or not q["table_id"] or not q["queries"] or q["queries"] == []:
                continue
            try:
                tblID = int(q["table_id"])
            except:
                continue
            compiler = PromptCompiler(user_id=user_id, table_id=tblID)
            for sq in q["queries"]:
                com_res = compiler.compile(prompt=sq)
                if com_res["status"] == "success":
                    op_flag = True
        
        if op_flag == False:
            return "Unfortunately, some changes failed. Please try again."
        
        return res["answer_sentence"]

    except Exception as e:
        logger.error(f"error in manager: {e}")
        return "Unfortunately, I did not understand your request. Please try again."

    

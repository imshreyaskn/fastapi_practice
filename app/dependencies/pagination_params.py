from fastapi import Depends

def pagination_params(limit:int = 10,offset : int=0):
    return {"limit":limit,"offset":offset}
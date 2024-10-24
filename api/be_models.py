from pydantic import BaseModel

class registerInfo(BaseModel):
    username : str
    dob : int
    aname : str
    model : str
    persona : str = None
    qa : list
    password : str
    
class loginInfo(BaseModel):
    username : str
    password : str

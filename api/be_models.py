from pydantic import BaseModel

class registerInfo(BaseModel):
    username : str
    dob : int
    qa : list[str]
    aname : str
    persona : str
    model : str
    password : str
    
class loginInfo(BaseModel):
    username : str
    password : str

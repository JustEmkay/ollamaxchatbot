from pydantic import BaseModel

class registerInfo(BaseModel):
    username : str
    dob : int
    password : str
    
class loginInfo(BaseModel):
    username : str
    password : str

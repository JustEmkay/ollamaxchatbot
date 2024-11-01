from pydantic import BaseModel


class fe_RegisterInfo(BaseModel):
    username : str
    dob : int
    aname : str
    model : str
    persona : str = None
    qa : list
    password : str

class fe_logiInfo(BaseModel):
    username : str
    password : str
    
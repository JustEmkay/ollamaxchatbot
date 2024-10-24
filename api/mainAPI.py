from fastapi import FastAPI
import jwt,jwt.exceptions,uuid,bcrypt
from db_manager import *
from be_models import *
from creds import *
from datetime import datetime,timedelta,timezone
from joi import joi




app = FastAPI()

def hash_pass(userPass:str) -> str:
    print("trying to hash:",userPass)
    pswd = userPass.encode('utf-8')
    return bcrypt.hashpw(pswd,bcrypt.gensalt())

def verify_pass(userPass:str, hashedPass:str) -> bool:
    pswd = userPass.encode('utf-8')
    return bcrypt.checkpw(pswd,hashedPass.encode('utf-8'))

def validate_token(token:str) -> str:
    
    try:
        return {
            'status' : True,
            'msg' : 'Token Active',
            'uid':jwt.decode(token,SECRET_KEY,algorithm)['uid']
            }
    
    except jwt.exceptions.ExpiredSignatureError:
        return {
            'status' : False,
            'msg' : 'Token Expired'
        }

def authenticate_token(token:str):
    try: 
        unpack_token = jwt.decode(token,SECRET_KEY,algorithm)
        return {
            'status' : True,
            'username' : unpack_token['username'],
            'uid' : unpack_token['uid']
        }
    
    except jwt.exceptions.DecodeError as e :
        return {
            'status' : False,
            'msg' : e
            
        } 
    except jwt.exceptions.ExpiredSignatureError:
        return {
            'status' : False,
            'msg' : e
            
        }

  
@app.get("/")
def connection():
    
    return {
        "author" : 'emkay',
        "connection" : True,
        "userData" : usersData,
        "tokensData" : tokensData
    }
    
@app.get("/login/{username}/{password}")
def validateUser(username:str, password:str):
    
    if username in usersData:
        
        hashedPass = usersData[username]['password']
        if verify_pass(password,hashedPass):
            
            
            payload_data = {
                'username' : username,
                'uid' : usersData[username]['uid'],
                'iat':datetime.now(timezone.utc),
                'exp' : datetime.now(timezone.utc) + timedelta(hours=1)
            }
            
            token = jwt.encode(
                payload=payload_data,
                key= SECRET_KEY
            )
            
            tokensData.append(token)
                    
            return {
                'status': True,
                'msg' : 'user found',
                'token' : token
            }
            
        return {
            'status': False,
            'msg' : 'Wrong password'
        }
            
    return {
        'status': False,
        'msg' : 'user not found'
    }

@app.post("/verify/")
async def verifyUser(loginInfo : loginInfo):
    
    if loginInfo.username in usersData:
        
        hashedPass = usersData[loginInfo.username]['password']
        if verify_pass(loginInfo.password,hashedPass):
                    
            return {
                'status': True,
                'msg' : 'user found',
                'uid' : usersData[loginInfo.username]['uid']
            }
            
        return {
            'status': False,
            'msg' : 'Wrong password'
        }
            
    return {
        'status': False,
        'msg' : 'user not found'
    }
    
@app.post("/register")
async def registerUser(regData:registerInfo):
    
    # username='emkay' 
    # dob=1729708200 
    # aname='juhi' 
    # model='gemma2:2b' 
    # persona='' 
    # qa=[0, 'doggy'] 
    # password='Vasu@6969'
    
    
    userid : str  = uuid.uuid1()
    print(regData)
    
    regData.password = hash_pass(regData.password)
    
    create_user(regData)
    
    
    return True

@app.post("/chatbot/{token}")
async def chatbot(token:str, userInput:dict):
    print("useInput:",userInput)
    
    result = authenticate_token(token)
    if result['status']:
        response = joi(userInput['role'],userInput['prompt'])
        if response['status']:
            return response
        else:
            return response
    
    return result
        
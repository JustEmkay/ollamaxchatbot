from fastapi import FastAPI
import jwt,jwt.exceptions,uuid,bcrypt
from db_manager import *
from be_models import *
from creds import *
from datetime import datetime,timedelta,timezone
from joi import joi




app = FastAPI()

def hash_pass(userPass:str) -> str:
    pswd = userPass.encode('utf-8')
    return bcrypt.hashpw(pswd,bcrypt.gensalt())

def verify_pass(userPass:str, hashedPass:str) -> bool:
    pswd = userPass.encode('utf-8')
    return bcrypt.checkpw(pswd,hashedPass)

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
    
    check = check_user(username)
    if check['status']:
        if check['exist']:
            og_pass = get_userPass(username)
            
            if verify_pass(password,og_pass):
                
                uad_response = get_userAccessData(username)
                if uad_response['status']:
                
                    payload_data = {
                        'username' : uad_response['data']['username'],
                        'uid' : uad_response['data']['uid'],
                        'assist_id' : uad_response['data']['assist_id'],
                        'iat':datetime.now(timezone.utc),
                        'exp' : datetime.now(timezone.utc) + timedelta(hours=1)
                    }
                    
                    token = jwt.encode(
                        payload=payload_data,
                        key= SECRET_KEY
                    )
                    
                    return {
                            'status': True,
                            'msg' : 'user found',
                            'token' : token
                    }
                return uad_response  
                            
        else:
            return {
                'status': False,
                'msg' : check['msg']
            }
            

 
@app.get("/loginn/{username}/{password}")
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
    
    result = check_user(regData.username)
    if result['status']:
        
        if result['exist']:
            msg = result['msg']
        else:
            msg = result['msg']
        
        return {
            'status' : True,
            'msg' : msg
        }
    else:
        regData.password = hash_pass(regData.password)
        res = create_user(regData)
        if res['status']:
            return res
        return res
            

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
        
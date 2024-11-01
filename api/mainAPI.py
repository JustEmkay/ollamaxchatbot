from fastapi import FastAPI
import jwt,jwt.exceptions,bcrypt
from db_manager import *
from be_models import *
from creds import *
from datetime import datetime,timedelta,timezone
from chatbot import *




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
            'uid' : unpack_token['uid'],
            'assist_id' : unpack_token['assist_id']
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
    
    result = model_status()
    if result['status']:
        models : list = result['models']
    else:
        models : list = []
    
    return {
        "author" : 'emkay',
        "models" : models
        
    }
    
@app.get("/model/status")
def model_status():
       
    result = llm_status()
    if result['status']:
        return {
            'status' : True,
            'models' : result['models']
        }
    return {
            'status' : False,
            'msg' : result['msg']
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
                            'token' : token,
                    }
                return uad_response  
                            
        else:
            return {
                'status': False,
                'msg' : check['msg']
            }
    return {
        'status': False,
        'msg' : 'Wrong credential. Try again with correct one.'
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
    print("result:",result )
    
    if result['status']:
        
        if result['exist']:
            msg = result['msg']
        else:
            msg = result['msg']
            print("User not in db , creating new user")
            regData.password = hash_pass(regData.password)
            res = create_user(regData)
            if res['status']:
                return res
            return res
        
        return {
            'status' : True,
            'msg' : msg
        }
            
@app.post("/chatbot/{token}")
async def chatbot_req(token:str, userInput:dict):
    
    result = authenticate_token(token)
    if result['status']:
        
        assist_data = get_userAssist_data(result['assist_id'])
        
        response = chatbot(assist_data['model'],assist_data['persona'],
                           userInput['role'],userInput['prompt'])
        
        if response['status']:
            
            user = [result['assist_id'],userInput['role'],userInput['prompt']]
            ai = [result['assist_id'],"ai",response['response']]

            history = save_menmory(result['assist_id'],user,ai)
            if history:
                return {
                    
                    'status' : True,
                    'memories' : history
                    }
        else:
            return {
                'status' : False,
                'msg': "Error occured."
            }
    
    return result
        
@app.get("/chats/{assist_id}")
async def getChats(assist_id:str):

    chats = get_Chats(assist_id)
    
    if chats:
        return {
            'status' : True,
            'chats' : chats
        }
    return {
            'status' : False,
            'msg' : 'Failed to fetch chats.'
    }
        
@app.get("/settings/{assist_id}")
async def getSettings(assist_id:str):
    
    data = get_Settings(assist_id)
    
    return {
        'status' : True,
        'data' : data
    }
    
@app.get("/profile/{uid}")
async def getProfile(uid:str):
    result = get_userProfile(uid)
    if result:
        return {
            'status' : True,
            'data' : result
        }
    
@app.put("/profile/update/{uid}")       
async def updateProfile(uid:str, username:str = None, dob:int = None):
    
    if username:
        result = check_user(username)
        print(result)
        if result['status'] and result['exist']:
             return {
                 'status':False,
                 'msg':'Cannont use that username'
             }
        
    
    update = update_userProfile(uid,username=username,dob=dob)
    if update['status']:
        return {
            'status' : True,
            'msg' : update['msg']
        }
        
# @app.post("/verify/")
# async def verifyUser(loginInfo : loginInfo):
    
#     if loginInfo.username in usersData:
        
#         hashedPass = usersData[loginInfo.username]['password']
#         if verify_pass(loginInfo.password,hashedPass):
                    
#             return {
#                 'status': True,
#                 'msg' : 'user found',
#                 'uid' : usersData[loginInfo.username]['uid']
#             }
            
#         return {
#             'status': False,
#             'msg' : 'Wrong password'
#         }
            
#     return {
#         'status': False,
#         'msg' : 'user not found'
#     }
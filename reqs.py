import requests
from api.creds import API_URL
from fe_models import *

def gatherStartupData() -> dict:
    req = requests.get(API_URL)
    res = req.status_code
    if res == 200:
        return req.json()
    
def login_req(username:str, password:str) -> dict:
    req = requests.get(API_URL + f'login/{username}/{password}')
    res = req.status_code
    if res == 200:
        return req.json()

def chatbot_req(uid:str, assist_id:str, role:str, prompt:str)->dict:
    req = requests.post(API_URL + f'chatbot/{uid}/{assist_id}?role={role}&prompt={prompt}')
    res = req.status_code
    if res == 200:
        return req.json()
    
def registration_req(registerInfo : dict) -> dict:
    req = requests.post(API_URL + f'register',json=dict(registerInfo))
    res = req.status_code
    if res == 200:
        return req.json()
    
def getChat(assist_id:str) -> dict:
    req = requests.get(API_URL + f'chats/{assist_id}')
    res = req.status_code
    if res == 200:
        return req.json() 
    
def getProfileData(uid:str) -> dict:
    req = requests.get(API_URL + f'profile/{uid}')
    res = req.status_code
    if res == 200:
        return req.json() 
    
def getSettingsData(assist_id:str) -> dict:
    req = requests.get(API_URL + f'settings/{assist_id}')
    res = req.status_code
    if res == 200:
        return req.json() 
    
def updateProfileUsername(uid:str, username:str) -> dict:    
    req = requests.put(API_URL + f"profile/update/{uid}?username={username}")
    res = req.status_code
    if res == 200:
        return req.json() 
    
def updateProfileDOB(uid:str, dob:str) -> dict:    
    req = requests.put(API_URL + f'profile/update/{uid}?dob={dob}')
    res = req.status_code
    if res == 200:
        return req.json() 

def updateAssistantAname(assist_id:str, aname:str) -> dict:
    req = requests.put(API_URL + f'assistant/update/{assist_id}?aname={aname}')
    res = req.status_code
    if res == 200:
        return req.json() 

def updateAssistantPersona(assist_id:str, persona:str) -> dict:
    req = requests.put(API_URL + f'assistant/update/{assist_id}?persona={persona}')
    res = req.status_code
    if res == 200:
        return req.json() 
    
def updateAssistantModel(assist_id:str, model:str) -> dict:
    req = requests.put(API_URL + f'assistant/update/{assist_id}?model={model}')
    res = req.status_code
    if res == 200:
        return req.json() 
    
def user_verfication(uid:str, assist_id:str, password:str) -> dict:
    req = requests.get(API_URL + f'users/verify/{uid}/{assist_id}?password={password}')
    res = req.status_code
    if res == 200:
        return req.json() 
    
def delete_chat(assist_id:str, user_chat_id:int, memory_id:int) -> dict:
    req = requests.delete(API_URL + f"chats/delete/{assist_id}/{user_chat_id}/{memory_id}")   
    res = req.status_code
    if res == 200:
        return req.json()
        
def delete_account(uid:str, assist_id:str, password:str, answer:str) -> dict:
    
    req = requests.delete(API_URL + f"profile/delete/{uid}/{assist_id}/{password}/{answer}")
    res = req.status_code
    if res == 200:
        return req.json()
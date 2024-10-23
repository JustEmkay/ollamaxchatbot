import requests
from api.creds import API_URL


def login_req(username:str, password:str) -> dict:
    req = requests.get(API_URL + f'login/{username}/{password}')
    res = req.status_code
    if res == 200:
        return req.json()

def chatbot_req(token:str, role:str, prompt:str)->dict:
    req = requests.post(API_URL + f'chatbot/{token}',json={
        'role':role,
        'prompt' : prompt
    })
    res = req.status_code
    if res == 200:
        return req.json()
    
    
    
    
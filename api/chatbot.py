import ollama


def llm_status() -> bool:

    try:
        result = ollama.list()
        print("Ollama server is running.\n")
        models = [r['model'] for r in result['models'] if r['model'] != 'moondream:latest']
        print(models)
        return {
            'status' : True,
            'models' : models,
        }
        
    except Exception as e:
        print("Ollama server is not running or encountered an error:", e)
        return {
            'status' : False,
            'msg' : 'models are dead',
        }
     
def chatbot(model_name:str,persona:str,role:str,prompt:str):
    
    # print("model_name:",model_name)
    # print("persona:",persona)
    # print("role:",role)
    # print("prompt:",prompt)
    
    try:
        
        content = prompt
        
        if persona: 
        
            content = f"""
                Act as {persona}
                
                prompt : {prompt} 
            
            """
        
        print("chat-bot content:",content)

        res = ollama.chat(model=model_name, 
                        messages=[
                            {
                                'role' : role,
                                'content': content
                            }
                        ])
        # print(f"response : {res['message']['content']}")
        return {
            'status': True,
            "response" : res['message']['content']
            }

    except Exception as e:
        print('Error at joi')
        return {
            'status' : False,
            'msg' : e
        }
    
# if __name__ == "__main__":
#     # llm_status()
#     chatbot('user','do you remember what i said last?')
import ollama


def joi(role:str,prompt:str):
    try:
        res = ollama.chat(model='gemma2:2b', 
                        messages=[
                            {
                                'role' : role,
                                'content': prompt
                            }
                        ])
        print(f"response : {res['message']['content']}")
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
    
if __name__ == "__main__":
    joi('say somwthing in malayalam?')
import streamlit as st 
import time,jwt,jwt.exceptions
from reqs import login_req,chatbot_req
from api.creds import SECRET_KEY,algorithm
import streamlit.components.v1 as components
from forms import register_form


if 'auth' not in st.session_state: st.session_state.auth = None
if 'persona' not in st.session_state: st.session_state.persona = ""
if 'model' not in st.session_state: st.session_state.model = "gemma2:2b"
if 'messages' not in st.session_state: st.session_state.messages = [
    {
        'role':'ai' ,
        'response':'How can i help you today!' 
            }
]

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="expanded",
)

def main() -> None:
    
    st.header("JOI",anchor=False,
              help='chat bot powered by ollama 🦙',
              divider=True)
    
    if not st.session_state.auth:
        
        with st.container(border=True):
            username = st.text_input("enter username:",value='emkay')
            password = st.text_input("enter password:",value='123',type='password')
            
            l_blank,signup_bttn,signin_bttn = st.columns([2,1,1])
            if signup_bttn.button('Sign-up',use_container_width=True):
                ...
            if signin_bttn.button('Sign-in',use_container_width=True,
                                  type='primary'):
                if username and password:
                    st.session_state.auth = login_req(username,password)
                    time.sleep(1)
                    st.rerun()
                    
        register_form()
 
    elif st.session_state.auth:
        
        with st.sidebar:
            st.success('login successful',icon='✅')
    
        unpack_token = jwt.decode(st.session_state.auth['token'],SECRET_KEY,algorithm)
        # st.session_state.messages
        
        # with st.container(border=True,height=400):
        for message in st.session_state.messages:
            if message['role'] == 'user':
                with st.chat_message('user'):
                    st.write(message['prompt'])
            if message['role'] == 'ai':
                with st.chat_message('ai'):
                    st.markdown(message['response'])
                    
        

        if prompt := st.chat_input('Sing a song..'):
            result = chatbot_req(st.session_state.auth['token'],"user",prompt)
            if result:
                if result['status']:
                    st.session_state.messages.append({
                        "role" : "user",
                        "prompt" : prompt
                    })
                    st.session_state.messages.append({
                        "role" : "ai",
                        "response" : result['response']
                    })
        
                st.rerun()
        
    
if __name__ == "__main__":
    
    try: 
        main()
    
    except jwt.exceptions.ExpiredSignatureError:
            st.session_state.auth = None
            st.toast(':red-background[Your token expired!]',icon='❌')
            time.sleep(2)
            st.rerun()
    
    except Exception as e:
        st.error(e,icon='⚡')

        
    finally:
        
        components.html("""
        <script>
        window.onbeforeunload = function() {
            return 'Are you sure you want to leave? You might lose unsaved data.';
        };
        </script>
        """, height=0)
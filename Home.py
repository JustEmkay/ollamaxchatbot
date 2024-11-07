import streamlit as st 
import time,jwt,jwt.exceptions,requests
from reqs import login_req,chatbot_req,gatherStartupData,getChat,getSettingsData,getProfileData
import streamlit.components.v1 as components
from forms import register_form,today_timestamp,delete_alert,alert,logout_sessions
from api.creds import SECRET_KEY,algorithm

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="expanded",
)


if 'auth' not in st.session_state: 
    st.session_state.auth = {
        'status': False,
        'token':None,
        'unpackedToken' : False
    }    
    
if 'account_del_alert' not in st.session_state:
    st.session_state.account_del_alert = False

if 'chatbotData' not in st.session_state: 
    st.session_state.chatbotData = {
    'getChat' : False,
    'messages' : [
        {
            'memory_id' : '0',
            'role' : 'ai',
            'chat' : 'How can i help you ?',
            'created' : today_timestamp
        }
    ]
}

if 'profileData' not in st.session_state: 
    st.session_state.profileData = {
        'getProfile' : False,
        'username' : None,
        'dob' : None,
        'created_date' : None
    }

if 'settingsData' not in st.session_state:
    st.session_state.settingsData = {
        'getSettingsData' : False,
        'aname': None,
        'model' : None,
        'persona' : None
    }

def stream_gen(text:str):
    
    """ 
    text stream generator.
    """
    
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.008)
        
    

def main() -> None:
    
    st.title("Convoo",anchor=False)
    st.caption('🚀 chatbot powered by ollama 🦙')
    
    
    if not st.session_state.auth['status']:
        
        if st.session_state.account_del_alert:
            alert()
                
        with st.container(border=True):
            username = st.text_input("enter username:",value='emkay')
            password = st.text_input("enter password:",value='123',type='password')
            
            l_blank,signup_bttn,signin_bttn = st.columns([2,1,1])
            if signup_bttn.button('Sign-up',use_container_width=True):
                register_form()
                
            if signin_bttn.button('Sign-in',use_container_width=True,
                                  type='primary'):
                if username and password:
                    result = login_req(username,password)
                    if result:
                        if result['status']:
                            st.session_state.auth.update(result)        
                            st.success(result['msg'],icon='✅')
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error(result['msg'],icon='⚠')
                            
                            
    elif st.session_state.auth['status']:
        
        if not st.session_state.auth['unpackedToken']: 
            unpack_token = jwt.decode(st.session_state.auth['token'],SECRET_KEY,algorithm)
            st.session_state.auth.update(unpack_token) 
    

        
        with st.sidebar:
            st.success('login successful',icon='✅')
    
        
        
        if not st.session_state.chatbotData['getChat']:
            chats = getChat(st.session_state.auth['assist_id'])
            if chats['status']:
                st.session_state.chatbotData['messages'] = chats['chats']
            st.session_state.chatbotData['getChat'] = True
        
        if not st.session_state.profileData['getProfile']:
            profile = getProfileData(st.session_state.auth['uid'])
            if profile['status']:
                st.session_state.profileData.update({
                    
                        'getProfile' : True,
                        'username' : profile['data']['username'],
                        'dob' : profile['data']['dob'],
                        'created_date' : profile['data']['created_date']
                })
              
        if not st.session_state.settingsData['getSettingsData']:
            settings = getSettingsData(st.session_state.auth['assist_id'])
            if settings['status']:
                st.session_state.settingsData.update({
                    'getSettingsData' : True,
                    'aname' : settings['data']['aname'],
                    'model' : settings['data']['model'],
                    'persona' : settings['data']['persona']
                })
                
        user_chat_id : int = ''       
                
        for indx,message in enumerate(st.session_state.chatbotData['messages'],start=1):
        
                if message['role'] == 'user':
                    with st.chat_message('user'):
                        st.write(f"**{st.session_state.profileData['username']} :** {message['chat']}")
                        user_chat_id = message['memory_id']
                        
                if message['role'] == 'ai':
                    with st.container(border=True):
                        with st.chat_message('ai'):
                            st.markdown(f"**{st.session_state.settingsData['aname']}**")
                            
                            if indx == len(st.session_state.chatbotData['messages']):
                                st.write_stream(stream_gen(message['chat']))
                            else:
                                st.write(message['chat'])
                            blnk, bttn_col = st.columns([3,1])
                            if bttn_col.button('delete',
                                            key=message['memory_id'],
                                            use_container_width=True):
                                delete_alert(st.session_state.auth['assist_id'],user_chat_id,message['memory_id'])
                    
        if prompt := st.chat_input('Sing a song..'):
            result = chatbot_req(uid=st.session_state.auth['uid'],
                                 assist_id=st.session_state.auth['assist_id'],
                                 prompt=prompt,role="user")
            if result:
                if result['status']:
                    st.session_state.chatbotData['messages'] = result['memories']
                    st.rerun()
        
    
if __name__ == "__main__":
    
    try:
        if 'models' not in st.session_state:
                models = gatherStartupData()
                st.session_state.models = models['models']
                
        main()
    
    except jwt.exceptions.ExpiredSignatureError:
            logout_sessions()
            st.toast(':red-background[Your token expired!]',icon='❌')
            time.sleep(2)
            st.rerun()
            
    except requests.exceptions.ConnectionError:
        st.error("Look like API is dead. Try again later.",icon='☠')
        if st.button('rerun'):
            st.reun()
        
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
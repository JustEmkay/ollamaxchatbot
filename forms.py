import streamlit as st 
from datetime import datetime
import re,time,jwt
from fe_models import fe_RegisterInfo
from reqs import *

# if 'auth' not in st.session_state: st.session_state.auth = None

# unpack_token = jwt.decode(st.session_state.auth['token'],SECRET_KEY,algorithm)

today_timestamp : int = int(datetime.now().timestamp())

def timestamp_to_datetimedate(timestamp:int) -> datetime.date:
    
    return datetime.fromtimestamp(timestamp).date()
    
def default_font() -> None:
    with open( "style.css" ) as css:
            st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
        
model_names : list[str] = [None,'gemma2:2b','llama3:7b']

questions : list[str] = (
    "What is the name of your first pet?",
    "What is the name of the town where you were born?",
    "Who was your childhood villian?",
    "Where was your best family vacation as a kid?",
    "What was the first exam you failed?",
    "Who is your favorite artist?"
)

def age_calc(dob : datetime.date ) -> dict:
    today : datetime.date = datetime.today()
    return today.year - dob.year - ((today.month,today.day) < (dob.month,dob.day))

def validate_password(password : str) -> bool:  
    if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password):  
        return True  
    return False

def validate_username(username : str) -> bool:  
    if re.match(r'^(?=[a-zA-Z0-9._]{4,20}$)(?!.*[_.]{2})[^_.].*[^_.]$', username):  
        return True  
    return False

def timestamp_to_date(stamp : int) -> str:
    tdate = datetime.fromtimestamp(stamp).strftime("%B %d, %Y")
    return tdate

@st.dialog("user Registration",width='large')
def register_form()->None:
    
    placeholder = st.empty()
    
    with placeholder.container():
    
        bttn_disable : list = [True,':red-background[fill all inputs]']    
        
        with st.container(border=True):
            username = st.text_input("Enter your username:",value='emkay')
            uname_alert = st.empty()
            if username:
                if not validate_username(username):
                    uname_alert.warning("Not valid username",icon='🤦‍♂️')
            
            dob_col, age_col = st.columns([3,1],vertical_alignment='bottom')
            dob : datetime.date = dob_col.date_input('select you date of birth',min_value=datetime(1940, 1, 1))
            dob_timestamp=datetime(dob.year,dob.month,dob.day,0,0,0).timestamp()
            age_col.info(f"Age: {age_calc(dob)}")
        
        with st.container(border=True):
            aname_col, model_col = st.columns(2)    
            aname = aname_col.text_input("Enter your assistant name:",value='juhi')
            model = model_col.selectbox("Select model:",st.session_state.models)
            model_alert = st.empty()
            if aname:
                    if not validate_username(aname):
                        model_alert.warning("Not valid assistant name",icon='🤦‍♂️')
            persona = st.text_area("Cretae assistant personality:")
                        
                        
        with st.container(border=True):
            qes,ans = st.columns([0.7,0.3])
            question : int = questions.index(qes.selectbox("select a question:",questions))
            answer = ans.text_input("Enter your answer:",value='doggy')
            qa_alert = st.empty()
            qa = [question, answer]
            
            pas,repas = st.columns(2)
            password = pas.text_input("Create new password:",type='password',value='Vasu@6969')
            re_password = repas.text_input("Re-Enter password:",type='password',value='Vasu@6969')
            pass_alert = st.empty()
        
        if password and re_password:
            if password != re_password:
                pass_alert.warning("both password are not equal",icon='⚠')
            else:
                if not validate_password(re_password):
                    pass_alert.warning("Not valid password",icon='🤦‍♂️')
                else:
                    if username and dob and aname and model and qa and password:
                        bttn_disable = [False,':green-background[Good to go✅]']
                    
                                    
        if st.button('cerate account',use_container_width=True,type='primary',
                    disabled=bttn_disable[0],help=bttn_disable[1]):
            try:
                reg = fe_RegisterInfo(username=username,dob=dob_timestamp,
                                    aname=aname,model=model,persona=persona,
                                    qa=qa,password=re_password)
                result = registration_req(reg)
                if result['status']:
                    placeholder.success(result['msg'])
                else:
                    st.error(result['msg'])
                
            
            except Exception as e:
                st.error(f"User input Validation error:,{e}",icon='⚡')

@st.dialog("update user profile")               
def edit_profile() -> None:
    
    input_col, bttn_col = st.columns([0.8,0.2],vertical_alignment='top')
    
    new_username : str = input_col.text_input("Enter username",
                                              label_visibility='collapsed',
                    placeholder=f'Enter new username here')
    
    age_ip, dob_ip = input_col.columns([0.2,0.8],vertical_alignment='center')
    
    new_dob : datetime.date = dob_ip.date_input("update your date of birth",
                            value=timestamp_to_datetimedate(st.session_state.profileData['dob']),
                            label_visibility='collapsed',
                            min_value=datetime(1940, 1, 1))
    age_ip.write(f"Age: {age_calc(new_dob)}")
    
    alert = st.empty()
    
    if new_username:
        if validate_username(new_username):
            alert.info(f"{st.session_state.profileData['username']} >> {new_username}")
        else:
            alert.warning("invalide username.")
    
    if new_dob != timestamp_to_datetimedate(st.session_state.profileData['dob']):
        alert.info(f"{timestamp_to_datetimedate(st.session_state.profileData['dob'])} \
                   >> {new_dob}")
    
    if bttn_col.button("update",key='update_uname'):
        if validate_username(new_username):
            res1 = updateProfileUsername(st.session_state.auth['uid'],
                                  new_username)
            if res1['status']:
                st.session_state.profileData['username'] = new_username
                st.rerun()
        
    if bttn_col.button("update",key="update_age"):
        dob_timestamp=datetime(new_dob.year,new_dob.month,new_dob.day,0,0,0).timestamp()
        res2 = updateProfileDOB(st.session_state.auth['uid'],dob_timestamp)
        if res2['status']:
            st.session_state.profileData['dob'] = dob_timestamp
            st.rerun()
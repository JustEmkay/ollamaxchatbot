
import streamlit as st 
import time
from forms import default_font,model_names



def redirect_to_login() -> None:
    
    st.caption(':red[please login] 🙏')
    alert = st.empty()
    alert.caption('Redirecting to Login page in 5s')
    
    for i in range(5):
        time.sleep(1)
        alert.caption(f'Redirecting to Login page in {5-i}s')
        
    st.switch_page('home.py')
    


def options() -> None:
    
    with st.expander('Active Model',expanded=True):
        with st.form('Select model'):
            st.selectbox('Model list',st.session_state.models,
                         index=st.session_state.models.index(st.session_state.settingsData['model']))
            if st.form_submit_button("update model."):
                ...

    with st.expander('Model Persona',expanded=True):
        with st.form("persona"):
            persona = st.text_area("Assistant's persona:",
                                placeholder="Enter how you want your assistant to act..",
                                value=st.session_state.settingsData['persona'])
            if st.form_submit_button("update personatity."):
                ...
        
        
    with st.expander('Delete Account'):
        ...
    



def settings() -> None:
    st.header('Settings',anchor=False,divider='red')
    
    if st.session_state.auth:    
        
        st.session_state.settingsData
        
        options()
    else:
        redirect_to_login()
        
        
        

if __name__ == "__main__":
    settings()
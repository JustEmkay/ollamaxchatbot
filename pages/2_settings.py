
import streamlit as st 
import time

def redirect_to_login() -> None:
    
    st.caption(':red[please login] 🙏')
    alert = st.empty()
    alert.caption('Redirecting to Login page in 5s')
    
    for i in range(5):
        time.sleep(1)
        alert.caption(f'Redirecting to Login page in {5-i}s')
        
    st.switch_page('home.py')
    


def options() -> None:
    
    model_names : list[str] = ['gemma2:2b','llama3:7b']
    
    with st.expander('Active Model'):
        with st.form('Select model'):
            st.selectbox('Model list',model_names,
                         index=model_names.index(st.session_state.model))
            if st.form_submit_button("update model."):
                ...

    with st.expander('Model Persona'):
        with st.form("persona"):
            persona = st.text_area("Assistant's persona:",
                                placeholder="Enter how you want your assistant to act..",
                                value=st.session_state.persona)
            if st.form_submit_button("update personatity."):
                ...
        
        
    with st.expander('Delete Account'):
        ...
    



def settings() -> None:
    st.header('Settings',anchor=False,divider='red')
    
    if st.session_state.auth:    
        options()
    else:
        redirect_to_login()
        
        
        

if __name__ == "__main__":
    settings()
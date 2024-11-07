import streamlit as st 
import time
from forms import logout_sessions

def redirect_to_login() -> None:
    
    st.caption(':red[please login] 🙏')
    alert = st.empty()
    alert.caption('Redirecting to Login page in 5s')
    
    for i in range(5):
        time.sleep(1)
        alert.caption(f'Redirecting to Login page in {5-i}s')
        
    st.switch_page('home.py')
    


def logout() -> None:
    
    st.session_state
    
    if st.session_state.auth['status']:    
        if st.button('logout'):
            logout_sessions()
            st.toast(":red[loging out...]")
            time.sleep(2)
            st.rerun()
            
    else:
        redirect_to_login()
        
        
        

if __name__ == "__main__":
    logout()
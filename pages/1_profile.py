
import streamlit as st
from datetime import datetime
from forms import timestamp_to_date,age_calc,edit_profile,redirect_to_login


def profile() -> None:
    st.header(f"Profile: {st.session_state.profileData['username']}",divider='blue',anchor=False)
    
    dob_obj=datetime.fromtimestamp(st.session_state.profileData['dob'])
    
    col1, col2 = st.columns([0.4,0.6])
    col1.image("assets/images/placeholder.jpg",width=100,
                use_column_width=True)
    
    with col2.container(border=True,height=250):
        with st.container(border=True):
            st.markdown(f"Age: {age_calc(dob_obj)}")
            st.markdown(f"Birth-date: {timestamp_to_date(st.session_state.profileData['dob'])}") 
        st.markdown(f"created on: {timestamp_to_date(st.session_state.profileData['created_date'])}")
        if st.button('edit',use_container_width=True):
            edit_profile()
        
        
        
    with st.container(border=True):
        st.subheader(f"Assistant: {st.session_state.settingsData['aname']}",
                     divider=True,help='Go to setting to change assistant options')
        st.markdown(f"Assistant model: {st.session_state.settingsData['model']}")
        with st.container(border=True):
            st.markdown(f"Assistant personality: ")
            if st.session_state.settingsData['persona']:
                st.markdown(f''' {st.session_state.settingsData['persona']} ''')
            else:
                st.info("persona not defined")
    
if __name__ == "__main__":
    
    if st.session_state.auth['status']:
        profile()
    else:
        redirect_to_login()


import streamlit as st 
import time
from forms import default_font,account_verification,redirect_to_login
from reqs import updateAssistantAname,updateAssistantModel,updateAssistantPersona




    
def options() -> None:
    
    
    alert = st.empty()
    
    with st.expander('Model name',expanded=True):
        with st.form('model name'):
            new_aname = st.text_input("Your model name:",placeholder='Enter new name for your model',
                                  value=st.session_state.settingsData['aname'])
            if st.form_submit_button("update name."):
                res1 = updateAssistantAname(st.session_state.auth['assist_id'],aname=new_aname)
                if res1['status']:
                    st.session_state.settingsData['aname'] = new_aname
                    st.rerun()
                else:
                    alert.error(res1['msg'])
    
    
    
    with st.expander('Active Model',expanded=True):
        with st.form('Select model'):
            new_model = st.selectbox('Model list',st.session_state.models,
                         index=st.session_state.models.index(st.session_state.settingsData['model']))
            if st.form_submit_button("update model."):
                res2 = updateAssistantModel(st.session_state.auth['assist_id'],model=new_model)
                if res2['status']:
                    st.session_state.settingsData['model'] = new_model
                    st.rerun()
                else:
                    alert.error(res2['msg'])

    with st.expander('Model Persona',expanded=True):
        with st.form("persona"):
            new_persona = st.text_area("Assistant's persona:",
                                placeholder="Enter how you want your assistant to act..",
                                value=st.session_state.settingsData['persona'])
            if st.form_submit_button("update personatity."):
                res3 = updateAssistantPersona(st.session_state.auth['assist_id'],persona=new_persona)
                if res3['status']:
                    st.session_state.settingsData['persona'] = new_persona
                    st.rerun()
                else:
                    alert.error(res3['msg'])
        
        
    with st.expander('Delete Account',expanded=False):
        account_verification(st.session_state.auth['uid'],
                             st.session_state.auth['assist_id'])
    
def settings() -> None:
    st.header('Settings',anchor=False,divider='red')
    
    if st.session_state.auth['status']:    
        
        # st.session_state.settingsData
        
        options()
    else:
        redirect_to_login()
        
        
    
if __name__ == "__main__":
    settings()
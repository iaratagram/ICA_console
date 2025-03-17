import streamlit as st
from irister_utils import ICA_console_login, get_ICA_data, get_all_participants


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "page" not in st.session_state:
    st.session_state["page"] = "participants_database"


ICA_list = get_ICA_data()
ICA_ids = [item["ic_id"] for item in ICA_list]


## login to ICA console
def login_page():
    st.title("ICA Chatbot Console")
    username = st.text_input("Enter your username")
    password = st.text_input("Enter your password", type="password")
    if st.button("Login"):
        if ICA_console_login(username, password):
            st.success("Login successful")
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("Login failed")


def add_participants_page():
    st.title("Add Participants")
    ## add new participants form
    with st.form("add_participants"):
        name = st.text_input("Enter the name of the participant")
        wa_number = st.text_input("Enter the WhatsApp number of the participant")
        ## prefered language
        language = st.selectbox("Select the preferred language", ["English", "Spanish"])
        ## ICA id
        ICA_id = st.selectbox("Select the ICA id", ICA_ids)
        if st.form_submit_button("Add"):
            ## add to database logic here
            st.success("Participant added successfully")


def participants_database_page():
    st.title("Participants Database")
    st.subheader("Participants database")

    ## get all participants
    st.session_state.participants = get_all_participants()

    
    ## if no participants, show a message
    if not st.session_state.participants:
        st.info("No Participants found. Please add participants using the form above.")
    else:
        ## editable table
        for i, participant in enumerate(st.session_state.participants):
            name_col, wa_col, lang_col, ica_col, edit_col, delete_col, send_col = st.columns([3, 6, 2, 3, 2, 3, 6])
            with name_col:
                st.write(participant["name"])
            with wa_col:
                st.write(participant["whatsapp_number"])
            with lang_col:
                st.write(participant["user_language_option"])
            with ica_col:
                st.write(participant["assigned_ica_id"]) 
            with edit_col:
                if st.button("Edit", key=f"edit_{i}"):
                    st.session_state.edit_participant_id = participant["_id"]
                    st.session_state.edit_mode = True
            with delete_col:
                if st.button("Delete", key=f"delete_{i}"):
                    st.session_state.participants.remove(participant)
                    st.rerun()
            with send_col:
                if st.button("Send Template Greeting Message", key=f"send_message_{i}"):
                    st.success("Message sent successfully")
        
        ## edit participant form
        if st.session_state.get("edit_mode", False):
            st.subheader("Edit Participant")
            edit_id = st.session_state.edit_participant_id
            participant_to_edit = next((p for p in st.session_state.participants if p["_id"] == edit_id), None)
            
            if participant_to_edit:
                with st.form("edit_participant_form"):
                    new_name = st.text_input("name", value=participant_to_edit["name"])
                    new_whatsapp = st.text_input("WhatsApp number", value=participant_to_edit["whatsapp_number"])
                    new_language = st.selectbox("Preferred Language", ["en", "es"], 
                                              index=0 if participant_to_edit["user_language_option"] == "en" else 1)
                    new_ICA = st.selectbox("ICA id", ICA_ids, index=ICA_ids.index(participant_to_edit["assigned_ica_id"]))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button("Save"):
                            participant_to_edit["name"] = new_name
                            participant_to_edit["whatsapp_number"] = new_whatsapp
                            participant_to_edit["user_language_option"] = new_language
                            participant_to_edit["assigned_ica_id"] = new_ICA
                            st.session_state.edit_mode = False
                            st.success("Participant information updated")
                            st.rerun()
                    with col2:
                        if st.form_submit_button("Cancel"):
                            st.session_state.edit_mode = False
                            st.rerun()



def ICA_console_page():
    ## sidebar
    with st.sidebar:
        st.title("ICA Console")
        st.write("Welcome to the ICA Console")
        ## navigation to add participants page or participants database page
        if st.button("Add Participants", "add_participants", type="secondary"):
            st.session_state["page"] = "add_participants"
            st.rerun()
        if st.button("Participants Database", "participants_database", type="secondary"):
            st.session_state["page"] = "participants_database"
            st.rerun()


    if st.session_state["page"] == "add_participants":
        add_participants_page()
    elif st.session_state["page"] == "participants_database":
        participants_database_page()

    



    
def main():
    if st.session_state["logged_in"]:
        ICA_console_page()
    else:
        login_page()


if __name__ == "__main__":
    main()

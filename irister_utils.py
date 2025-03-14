import streamlit as st
import requests

irister_key = st.secrets["IRISTER_API_KEY"]

irister_url = "https://iris-server-e5f0bc08552d.herokuapp.com"

## irister api
## body should be a json
# {
#     "messages": [
#         {"role": "user", "content": "Hello, how are you?"}
#     ]
# }
# api key should be in bearer token

def request_irister(messages):
    url = f"{irister_url}/v1/purer"
    headers = {
        "Authorization": f"Bearer {irister_key}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": messages
    }
    response = requests.post(url, headers=headers, json=data)
    return response.text

def irister_start_session(user_input):
    url = f"{irister_url}/ica/startsession"
    headers = {
        "Authorization": f"Bearer {irister_key}",
        "Content-Type": "application/json"
    }
    data = {"problem_behavior": user_input}
    response = requests.post(url, headers=headers, json=data)
    return response.json()["session_id"]


def ICA_console_login(username, password):
    url = f"{irister_url}/ica/login"
    if username == "admin" and password == "admin":
        return True
    else:
        return False
    # headers = {
    #     "Authorization": f"Bearer {irister_key}",
    #     "Content-Type": "application/json"
    # }
    # data = {"usr": username, "pwd": password} 
    # response = requests.post(url, headers=headers, json=data)
    # return (response.json()["is_success"])

def get_ICA_ids():
    return ["Casey_chat"]
    # url = f"{irister_url}/ica/get_ica_ids"
    # headers = {
    #     "Authorization": f"Bearer {irister_key}",
    #     "Content-Type": "application/json"
    # }
    # response = requests.get(url, headers=headers)
    # return response.json()

def get_all_participants_paginated(page=1, page_size=10):
    url = f"{irister_url}/ica/get_all_participants"
    headers = {
        "Authorization": f"Bearer {irister_key}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, params={"page": page, "page_size": page_size})
    return response.json()


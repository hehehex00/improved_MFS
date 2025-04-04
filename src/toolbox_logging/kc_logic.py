import os
from datetime import datetime, timedelta
from urllib.parse import urlencode

import requests
import streamlit as st
from dotenv import load_dotenv
from streamlit_cookies_controller import CookieController

load_dotenv() 

discovery_url = os.environ.get("KEYCLOAK_DISCOVERY_URL", "https://keycloak.funnel.local:8443/realms/dev-funnel/.well-known/openid-configuration")
client_id = os.environ.get("KEYCLOAK_CLIENT_ID", "dev-toolbox")
client_secret = os.environ.get("KEYCLOAK_CLIENT_SECRET", "hoxVTnMBM6l9JGKppu8pVWn5sq35VMLQ")
redirect_uri = os.environ.get("KEYCLOAK_REDIRECT_URI", "https://dev-toolbox.funnel.local/")
scope = os.environ.get("KEYCLOAK_SCOPE", "openid profile email")


active = False
if os.environ.get("kc_logging", "disabled") == "enabled":
    active = True

def get_cookie_controller():
    controller = st.session_state.get("cookie_controller", None)
    if controller:
        return controller
    
    controller = CookieController()
    st.session_state["cookie_controller"] = controller
    return controller

def get_all_cookies():
    cookies = get_cookie_controller().getAll()
    return cookies

def set_cookie(key, value):
    expires = (datetime.utcnow() + timedelta(days=365))
    max_age = 365 * 24 * 60 * 60
    get_cookie_controller().set(key, value, domain=".funnel.local", expires=expires, max_age=max_age) # set to top level domain of your app
    return True


def get_keycloack_endpoints(discovery_url: str):
    keycloak_urls = requests.get(discovery_url, verify=False).json()
    return keycloak_urls

# Step 2: Build authorization URL
def create_auth_url(auth_endpoint: str):
    auth_params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
    }
    return f"{auth_endpoint}?{urlencode(auth_params)}"

# Streamlit UI
def redirect_to_external_url(url: str):
    st.markdown(f'<meta http-equiv="refresh" content="0; url={url}">', unsafe_allow_html=True)

def get_auth_code_through_redirect(auth_endpoint: str):
    auth_url = create_auth_url(auth_endpoint)
    redirect_to_external_url(auth_url)
    return True, {}, "reloading"
    

def create_auth_post_data(auth_code: str):
    return {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }


def handle_auth() -> (bool, dict, str):
    #return authenticate, identity, and error
    if not active:
        return False, {}, "logging not active"
    cookies = get_all_cookies()

    if cookies:
        if "identity" in cookies:
            return True, cookies["identity"], ""
    query_params = st.query_params
    auth_code_present = "code" in query_params

    kc_endpoints = get_keycloack_endpoints(discovery_url)
    auth_endpoint = kc_endpoints["authorization_endpoint"]
    token_endpoint = kc_endpoints["token_endpoint"]
    userinfo_endpoint = kc_endpoints["userinfo_endpoint"]

    if not auth_code_present:
        get_auth_code_through_redirect(auth_endpoint)
        st.stop() # should stop everything until reload
        return False, {}, "reloading"

    if auth_code_present:
        auth_code = query_params["code"]
        auth_exchange_data = create_auth_post_data(auth_code)
        token_response = requests.post(token_endpoint, data=auth_exchange_data, verify=False)  # `verify=False` for SSL self-signed
        tokens = token_response.json()

        if "access_token" in tokens:
            headers = {"Authorization": f"Bearer {tokens['access_token']}"}
            userinfo_response = requests.get(userinfo_endpoint, headers=headers, verify=False)  # `verify=False` for SSL self-signed
            userinfo = userinfo_response.json()
            if "identity" not in get_all_cookies():
                set_cookie("identity", userinfo)
                st.query_params.clear()
            return True, userinfo, ""
        else:
            return False, {}, tokens

def attach_identity_cookie():
    if not active:
        return {"logging enabled": False}
    cookies = get_all_cookies()
    if 'identity' in cookies:
        return cookies['identity']
    auth, identity, tokens = handle_auth()
    return identity

def log_activity(activity_str: str):
    get_cookie_controller()
    if not active:
        return True
    cookies = get_all_cookies()
    identity = None
    if 'identity' not in cookies:
        identity = {
            "sub": "KC_ID Failed",
            "name": "KC_ID Failed",
            "preferred_username": "KC_ID Failed",
            "given_name": "KC_ID Failed",
            "family_name": "KC_ID Failed",
            "email": "KC_ID Failed"
        },
    else:
        identity = cookies["identity"]
    data = {
        "identity": {
            "sub": identity["sub"],
            "name": identity.get("name", ""),
            "preferred_username": identity.get("preferred_username", ""),
            "given_name": identity.get("given_name", ""),
            "family_name": identity.get("family_name", ""),
            "email": identity.get("email", "")
        },
        "activity": activity_str
    }
    
    # Send the POST request to FastAPI
    fastapi_url = "http://backend-logging:8000/log_activity"
    requests.post(fastapi_url, json=data)

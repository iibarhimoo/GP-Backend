import requests
import json

# CONFIGURATION
API_KEY = "AIzaSyDnkjCfaVMgJxEEwocjlKEUbpekkpTEJHM"  # Replace with your Firebase Web API Key
TEST_EMAIL = "test@test.com"
TEST_PASSWORD = "password123"

def get_id_token():
    # 1. Sign up a new user (or sign in if exists)
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
    payload = {"email": TEST_EMAIL, "password": TEST_PASSWORD, "returnSecureToken": True}
    
    response = requests.post(url, json=payload)
    
    if "EMAIL_EXISTS" in response.text:
        # If user exists, sign in instead
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
        response = requests.post(url, json=payload)

    if response.status_code == 200:
        token = response.json()['idToken']
        print("\n✅ SUCCESS! Here is your Firebase ID Token:\n")
        print(token)
        print("\n(Copy this token for Postman)")
    else:
        print("❌ Error:", response.text)

if __name__ == "__main__":
    get_id_token()
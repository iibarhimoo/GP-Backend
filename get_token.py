import requests

# CONFIGURATION
API_KEY = "AIzaSyDnkjCfaVMgJxEEwocjlKEUbpekkpTEJHM"
TEST_EMAIL = "test@gmail.com"
TEST_PASSWORD = "testpassword123"

def get_id_token():
    # 1. Sign up/in to get token
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
    payload = {"email": TEST_EMAIL, "password": TEST_PASSWORD, "returnSecureToken": True}
    
    response = requests.post(url, json=payload)
    
    # If user exists, sign in
    if "EMAIL_EXISTS" in response.text:
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
        response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("\n✅ SUCCESS! Copy this token:\n")
        print(response.json()['idToken'])
    else:
        print("❌ Error:", response.text)

if __name__ == "__main__":
    get_id_token()
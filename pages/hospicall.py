import requests

url = 'https://hospicall.azurewebsites.net/'
# url_dummy = '127.0.0.1:3000/'

username = "testvincent"
password = "password"

def get_token():
    token_response = requests.post(url+'token', data={'username': username, 'password': password})
    if token_response.status_code == 200:
        # Extract the access token from the response JSON
        token = token_response.json().get('access_token')
        return token
    else:
        # Print the error message if the request was not successful
        print(f"Failed to get token. Status code: {token_response.status_code}")
        return None
    
# def call_facility():
#     longitude = 123
#     latitude = 456
#     user_data = {"username": username, "password": password}

#     access_token = get_token()
#     if access_token:
#         call_url = f"{url}/emergency_call"
#         headers = {"Authorization": f"Bearer {access_token}"}
#         call_payload = {"longitude": longitude, "latitude": latitude}

#         response = requests.post(call_url, headers=headers, json=call_payload)
#     if response.status_code == 200:
#         print("Call made successfully.")
#         print(response.json())
#     else:
#         print(f"Failed to make a call. Status code: {response.status_code}")
#         print(response.json())

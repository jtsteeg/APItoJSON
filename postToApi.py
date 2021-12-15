import requests
import os
import json

loginUrl = 'http://127.0.0.1:5000/login'
url = 'http://127.0.0.1:5000/addpowerplants'

# get access token

x = requests.post(
    loginUrl, json={"username": "admin", "password": "password1"})

print(x.text)
x = x.json()
access_token = x["access_token"]
# print(access_token)


jsonFile = open('powerplants.json')
data = json.load(jsonFile)
count = 0

for powerPlant in data['powerPlants']:
    if(count < 3):
        x = requests.post(
            url, headers={'Authorization': 'Bearer ' + access_token}, json=powerPlant)
        print("adding: ", powerPlant['name'])
        print("post message: " + x.text)

        count += 1
    else:
        break

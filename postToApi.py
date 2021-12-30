import requests
import os
import json

loginUrl = 'https://powermapperapi.azurewebsites.net/login'
url = 'https://powermapperapi.azurewebsites.net/addpowerplants'

admin_username = "admin"
admin_password = "password"

# get access token
x = requests.post(
    loginUrl, json={"username": admin_username, "password": admin_password})

print(x.text)
x = x.json()
access_token = x["access_token"]


jsonFile = open('powerplants.json')
data = json.load(jsonFile)
count = 0

for powerPlant in data['powerPlants']:
    x = requests.post(
        url, headers={'Authorization': 'Bearer ' + access_token}, json=powerPlant)
    print("adding: ", powerPlant['name'])
    print("post message: " + x.text)

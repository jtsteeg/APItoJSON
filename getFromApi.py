import json

import requests

powerPlants = {
    "powerPlants": []
}


illinoisPowerPlants = requests.get(

    "https://api.eia.gov/category/?api_key=1d97ccab56e4ea052f94379e9adb787a&category_id=902944").json()


# print(illinoisPowerPlants['category']['childcategories'])


for i in range(len(illinoisPowerPlants['category']['childcategories'])):
    print(i)
    print(illinoisPowerPlants['category']['childcategories'][i]['name'])
    powerPlants["powerPlants"].insert(i, {})
    powerPlants["powerPlants"][i]["category_id"] = illinoisPowerPlants['category']['childcategories'][i]['category_id']
    powerPlants["powerPlants"][i]["name"] = illinoisPowerPlants['category']['childcategories'][i]['name']
    # powerplants[i] =
    # powerplants[i]["name"]
    # print(i['name'])
    # print(i['category_id'])

with open("powerplants.json", "w") as outfile:
    json.dump(powerPlants, outfile)

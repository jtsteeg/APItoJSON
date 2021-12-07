import json

import requests

powerPlants = {
    "powerPlants": []
}


illinoisPowerPlants = requests.get(

    "https://api.eia.gov/category/?api_key=1d97ccab56e4ea052f94379e9adb787a&category_id=902944").json()


# print(illinoisPowerPlants['category']['childcategories'])

# len(illinoisPowerPlants['category']['childcategories']))


for i in range(3):
    print(i)
    print(illinoisPowerPlants['category']['childcategories'][i]['name'])
    plantCategoryID = illinoisPowerPlants['category']['childcategories'][i]['category_id']
    powerPlants["powerPlants"].insert(i, {})
    powerPlants["powerPlants"][i]["category_id"] = illinoisPowerPlants['category']['childcategories'][i]['category_id']
    powerPlants["powerPlants"][i]["name"] = illinoisPowerPlants['category']['childcategories'][i]['name']

    plantNameAndSeries = requests.get(
        "https://api.eia.gov/category/?api_key=1d97ccab56e4ea052f94379e9adb787a&category_id=" + str(plantCategoryID)).json()

    for j in range(len(plantNameAndSeries['category']['childseries'])):
        if(plantNameAndSeries['category']['childseries'][j]['name'].__contains__("Net generation")):
            print(plantNameAndSeries['category']['childseries'][j]['name'])
            plantSeriesID = plantNameAndSeries['category']['childseries'][j]['series_id']
            break

    print(plantSeriesID)
    plantInfo = requests.get(
        "https://api.eia.gov/series/?api_key=1d97ccab56e4ea052f94379e9adb787a&series_id=" + plantSeriesID).json()

    print("coordinates: " + plantInfo['series'][0]['latlon'])
    print("2020 output: " + str(plantInfo['series'][0]['data'][0][1]))


with open("powerplants.json", "w") as outfile:
    json.dump(powerPlants, outfile)

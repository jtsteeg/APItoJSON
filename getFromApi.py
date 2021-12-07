import json

import requests

powerPlants = {
    "totalOutput": 0,
    "powerPlants": []
}


illinoisPowerPlants = requests.get(

    "https://api.eia.gov/category/?api_key=1d97ccab56e4ea052f94379e9adb787a&category_id=902944").json()


# print(illinoisPowerPlants['category']['childcategories'])

# len(illinoisPowerPlants['category']['childcategories']))

print("number of power stations: " +
      str(len(illinoisPowerPlants['category']['childcategories'])))

for i in range(5):
    plantCategoryID = illinoisPowerPlants['category']['childcategories'][i]['category_id']

    plantNameAndSeries = requests.get(
        "https://api.eia.gov/category/?api_key=1d97ccab56e4ea052f94379e9adb787a&category_id=" + str(plantCategoryID)).json()

    for j in range(len(plantNameAndSeries['category']['childseries'])):
        if(plantNameAndSeries['category']['childseries'][j]['name'].__contains__("Net generation")):
            plantSeriesID = plantNameAndSeries['category']['childseries'][j]['series_id']
            break

    # print(plantSeriesID)
    plantInfo = requests.get(
        "https://api.eia.gov/series/?api_key=1d97ccab56e4ea052f94379e9adb787a&series_id=" + plantSeriesID).json()

    for k in range(len(plantNameAndSeries['category']['childseries'])):
        if(plantNameAndSeries['category']['childseries'][k]['name'].__contains__("natural gas")):
            stationType = "petroleum"
            break
        elif(plantNameAndSeries['category']['childseries'][k]['name'].__contains__("coal")):
            stationType = "petroleum"
            break
        elif(plantNameAndSeries['category']['childseries'][k]['name'].__contains__("oil")):
            stationType = "petroleum"
            break
        elif(plantNameAndSeries['category']['childseries'][k]['name'].__contains__("nuclear")):
            stationType = "nuclear"
            break
        elif(plantNameAndSeries['category']['childseries'][k]['name'].__contains__("hydroelectric")):
            stationType = "hydroelectric"
            break
        elif(plantNameAndSeries['category']['childseries'][k]['name'].__contains__("wind")):
            stationType = "wind"
            break
        elif(plantNameAndSeries['category']['childseries'][k]['name'].__contains__("solar")):
            stationType = "solar"
            break
        else:
            stationType = "other"

    # create powerplant entry and populate with info
    powerPlants["powerPlants"].insert(i, {})
    powerPlants["powerPlants"][i]["name"] = illinoisPowerPlants['category']['childcategories'][i]['name']
    powerPlants["powerPlants"][i]["coordinates"] = plantInfo['series'][0]['latlon']
    powerPlants["powerPlants"][i]["2020 MWH output"] = plantInfo['series'][0]['data'][0][1]
    powerPlants["powerPlants"][i]["type"] = stationType
    powerPlants["totalOutput"] = powerPlants["totalOutput"] + \
        plantInfo['series'][0]['data'][0][1]

    print(i)
    print(illinoisPowerPlants['category']['childcategories'][i]['name'])
    print("coordinates: " + plantInfo['series'][0]['latlon'])
    print("2020 output: " + str(plantInfo['series'][0]['data'][0][1]))
    print("fuel type: " + stationType)


with open("powerplants.json", "w") as outfile:
    json.dump(powerPlants, outfile)

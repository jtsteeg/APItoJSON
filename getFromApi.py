import json
import requests
import os

EIA_KEY = os.getenv('EIA_KEY')


powerPlants = {
    "totalOutput": 0,
    "powerPlants": []
}
eiaUri = "https://api.eia.gov/category/?api_key=%s" % EIA_KEY


# 1st endpoint
illinoisPowerPlants = requests.get(eiaUri + "&category_id=902944").json()

currentPlants = 0
for i in range(len(illinoisPowerPlants['category']['childcategories'])):

    plantCategoryID = illinoisPowerPlants['category']['childcategories'][i]['category_id']

    # 2nd endpoint
    plantNameAndSeries = requests.get(
        eiaUri + "&category_id=" + str(plantCategoryID)).json()

    for j in range(len(plantNameAndSeries['category']['childseries'])):
        if(plantNameAndSeries['category']['childseries'][j]['name'].__contains__("Net generation")):
            plantSeriesID = plantNameAndSeries['category']['childseries'][j]['series_id']
            break

    # 3rd endpoint
    plantInfo = requests.get(
        eiaUri + "&series_id=" + plantSeriesID).json()

    for k in range(len(plantNameAndSeries['category']['childseries'])):
        if(plantNameAndSeries['category']['childseries'][k]['name'].__contains__("natural gas")):
            stationType = "natural gas"
            break
        elif(plantNameAndSeries['category']['childseries'][k]['name'].__contains__("coal")):
            stationType = "coal"
            break
        elif(plantNameAndSeries['category']['childseries'][k]['name'].__contains__("oil")):
            stationType = "oil"
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

    # create a new entry in powerPlants and populate it with info from endpoints
    if(plantInfo['series'][0]['data'][0][0] == "2020" and plantInfo['series'][0]['data'][0][1] > 0):
        print(i)
        print(illinoisPowerPlants['category']['childcategories'][i]['name'])
        print("coordinates: " + plantInfo['series'][0]['latlon'])
        print("2020 output: " + str(plantInfo['series'][0]['data'][0][1]))
        print("fuel type: " + stationType)

        powerPlants["powerPlants"].insert(currentPlants, {})
        powerPlants["powerPlants"][currentPlants]["name"] = illinoisPowerPlants['category']['childcategories'][i]['name']
        powerPlants["powerPlants"][currentPlants]["coordinates"] = plantInfo['series'][0]['latlon']
        powerPlants["powerPlants"][currentPlants]["2020 MWH output"] = plantInfo['series'][0]['data'][0][1]
        powerPlants["powerPlants"][currentPlants]["type"] = stationType
        powerPlants["totalOutput"] = powerPlants["totalOutput"] + \
            plantInfo['series'][0]['data'][0][1]
        currentPlants += 1

with open("powerplants.json", "w") as outfile:
    json.dump(powerPlants, outfile)

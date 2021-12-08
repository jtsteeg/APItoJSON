import json
import requests
import os
import re

EIA_KEY = os.getenv('EIA_KEY')


powerPlants = {
    "totalOutput": 0,
    "powerPlants": []
}
eiaUri = "https://api.eia.gov/category/?api_key=%s" % EIA_KEY
eiaSeriesUri = "https://api.eia.gov/series/?api_key=%s" % EIA_KEY

# 1st endpoint
illinoisPowerPlants = requests.get(eiaUri + "&category_id=902944").json()

currentPlants = 0
# len(illinoisPowerPlants['category']['childcategories'])
for i in range(3):

    plantCategoryID = illinoisPowerPlants['category']['childcategories'][i]['category_id']
    plantName = re.sub("[\(\[].*?[\)\]]", "",
                       illinoisPowerPlants['category']['childcategories'][i]['name']).strip()

    print(plantCategoryID)
    # 2nd endpoint
    plantNameAndSeries = requests.get(
        eiaUri + "&category_id=" + str(plantCategoryID)).json()

    for j in range(len(plantNameAndSeries['category']['childseries'])):
        if(plantNameAndSeries['category']['childseries'][j]['name'].__contains__("Net generation")):
            plantSeriesID = plantNameAndSeries['category']['childseries'][j]['series_id']
            break

    print(plantSeriesID)
    # 3rd endpoint
    plantInfo = requests.get(
        eiaSeriesUri + "&series_id=" + plantSeriesID).json()

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

    print(plantInfo['series'][0]['data'][0][1])

    # create a new entry in powerPlants and populate it with info from endpoints
    if(plantInfo['series'][0]['data'][0][0] == "2020" and plantInfo['series'][0]['data'][0][1] > 0):
        print(i)
        # (illinoisPowerPlants['category']['childcategories'][i]['name'])
        print(plantName)
        print("coordinates: " + plantInfo['series'][0]['latlon'])
        print("outputMWH: " + str(plantInfo['series'][0]['data'][0][1]))
        print("fuel type: " + stationType)

        powerPlants["powerPlants"].insert(currentPlants, {})
        # illinoisPowerPlants['category']['childcategories'][i]['name']
        powerPlants["powerPlants"][currentPlants]["name"] = plantName
        #powerPlants["powerPlants"][currentPlants]["coordinates"] = plantInfo['series'][0]['latlon']
        powerPlants["powerPlants"][currentPlants]["coordinates"] = {
            "lat": float(plantInfo['series'][0]['lat']), "lon": float(plantInfo['series'][0]['lon'])}
        powerPlants["powerPlants"][currentPlants]["outputMWH"] = plantInfo['series'][0]['data'][0][1]
        powerPlants["powerPlants"][currentPlants]["type"] = stationType
        powerPlants["totalOutput"] = powerPlants["totalOutput"] + \
            plantInfo['series'][0]['data'][0][1]
        currentPlants += 1

with open("powerplants.json", "w") as outfile:
    json.dump(powerPlants, outfile)

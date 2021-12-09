import json
import requests
import os
import re
import operator

EIA_KEY = os.getenv('EIA_KEY')
eiaUri = "https://api.eia.gov/category/?api_key=%s" % EIA_KEY
eiaSeriesUri = "https://api.eia.gov/series/?api_key=%s" % EIA_KEY

powerPlants = {
    "totalOutput": 0,
    "powerPlants": []
}


# 1st endpoint
illinoisPowerPlants = requests.get(eiaUri + "&category_id=902944").json()

currentPlants = 0
# len(illinoisPowerPlants['category']['childcategories'])
for i in range(3):

    plantCategoryID = illinoisPowerPlants['category']['childcategories'][i]['category_id']
    plantName = re.sub("[\(\[].*?[\)\]]", "",
                       illinoisPowerPlants['category']['childcategories'][i]['name']).strip()

    print("plant in location " + str(i) + " is " + plantName)
    # 2nd endpoint
    plantNameAndSeries = requests.get(
        eiaUri + "&category_id=" + str(plantCategoryID)).json()

    for j in range(len(plantNameAndSeries['category']['childseries'])):
        if(plantNameAndSeries['category']['childseries'][j]['name'].__contains__("Net generation")):
            plantSeriesID = plantNameAndSeries['category']['childseries'][j]['series_id']
            break

    print("plant series in location " + str(i) + " is " + plantSeriesID)
    # 3rd endpoint
    plantInfo = requests.get(
        eiaSeriesUri + "&series_id=" + plantSeriesID).json()

    if(plantInfo['series'][0]['data'][0][0] == "2020" and plantInfo['series'][0]['data'][0][1] > 0):

        print(i)
        # (illinoisPowerPlants['category']['childcategories'][i]['name'])
        print(plantName)
        print("coordinates: " + plantInfo['series'][0]['latlon'])
        print("outputMWH: " + str(plantInfo['series'][0]['data'][0][1]))
        # print("fuel type: " + stationType)

        powerPlants["powerPlants"].insert(currentPlants, {})
        # illinoisPowerPlants['category']['childcategories'][i]['name']
        powerPlants["powerPlants"][currentPlants]["name"] = plantName
        # powerPlants["powerPlants"][currentPlants]["coordinates"] = plantInfo['series'][0]['latlon']
        powerPlants["powerPlants"][currentPlants]["coordinates"] = {
            "lat": float(plantInfo['series'][0]['lat']), "lon": float(plantInfo['series'][0]['lon'])}
        powerPlants["powerPlants"][currentPlants]["outputMWH"] = plantInfo['series'][0]['data'][0][1]
       # powerPlants["powerPlants"][currentPlants]["type"] = stationType
        powerPlants["totalOutput"] = powerPlants["totalOutput"] + \
            plantInfo['series'][0]['data'][0][1]

        powerPlants["powerPlants"][currentPlants]["fuelTypes"] = {}

        for k in range(len(plantNameAndSeries['category']['childseries'])):
            # print(plantNameAndSeries['category']['childseries'][k]['name'])
            if(plantNameAndSeries['category']['childseries'][k]['series_id'].__contains__("GEN")):
                if(plantNameAndSeries['category']['childseries'][k]['series_id'].__contains__("-NG-ALL.A")):
                    stationType = "natural gas"
                    print(plantName + " uses natural gas!")
                    print(plantNameAndSeries['category']
                          ['childseries'][k]['name'])
                    fuelInfo = requests.get(
                        eiaSeriesUri + "&series_id=" + plantNameAndSeries['category']['childseries'][k]['series_id']).json()
                    print("electicity generated by natural gas in MWH is: " +
                          str(fuelInfo['series'][0]['data'][0][1]))
                    powerPlants["powerPlants"][currentPlants]["fuelTypes"]["natural gas"] = fuelInfo['series'][0]['data'][0][1]

            # elif(plantNameAndSeries['category']['childseries'][k]['series_id'].__contains__("GEN")):
                if(plantNameAndSeries['category']['childseries'][k]['series_id'].__contains__("-SUB-ALL.A")):
                    print(plantName + " uses coal!")
                    print(plantNameAndSeries['category']
                          ['childseries'][k]['name'])
                    fuelInfo = requests.get(
                        eiaSeriesUri + "&series_id=" + plantNameAndSeries['category']['childseries'][k]['series_id']).json()
                    print("electicity generated by coal in MWH is: " +
                          str(fuelInfo['series'][0]['data'][0][1]))
                    powerPlants["powerPlants"][currentPlants]["fuelTypes"]["coal"] = fuelInfo['series'][0]['data'][0][1]
           # elif(plantNameAndSeries['category']['childseries'][k]['series_id'].__contains__("GEN")):
                if(plantNameAndSeries['category']['childseries'][k]['series_id'].__contains__("-DFO-ALL.A")):
                    print(plantName + " uses oil!")
                    fuelInfo = requests.get(
                        eiaSeriesUri + "&series_id=" + plantNameAndSeries['category']['childseries'][k]['series_id']).json()
                    print("electicity generated by oil in MWH is: " +
                          str(fuelInfo['series'][0]['data'][0][1]))
                    powerPlants["powerPlants"][currentPlants]["fuelTypes"]["Oil"] = fuelInfo['series'][0]['data'][0][1]
                if(plantNameAndSeries['category']['childseries'][k]['series_id'].__contains__("-NUC-ALL.A")):
                    print(plantName + " uses NUCLEAR!")
                    fuelInfo = requests.get(
                        eiaSeriesUri + "&series_id=" + plantNameAndSeries['category']['childseries'][k]['series_id']).json()
                    print("electicity generated by nuclear in MWH is: " +
                          str(fuelInfo['series'][0]['data'][0][1]))
                    powerPlants["powerPlants"][currentPlants]["fuelTypes"]["nuclear"] = fuelInfo['series'][0]['data'][0][1]
                if(plantNameAndSeries['category']['childseries'][k]['series_id'].__contains__("-WAT-ALL.A")):
                    print(plantName + " uses hydroelectric!")
                    fuelInfo = requests.get(
                        eiaSeriesUri + "&series_id=" + plantNameAndSeries['category']['childseries'][k]['series_id']).json()
                    print("electicity generated by hydroelectric in MWH is: " +
                          str(fuelInfo['series'][0]['data'][0][1]))
                    powerPlants["powerPlants"][currentPlants]["fuelTypes"]["hydroelectric"] = fuelInfo['series'][0]['data'][0][1]
                if(plantNameAndSeries['category']['childseries'][k]['series_id'].__contains__("-WND-ALL.A")):
                    print(plantName + " uses WIND!")
                    fuelInfo = requests.get(
                        eiaSeriesUri + "&series_id=" + plantNameAndSeries['category']['childseries'][k]['series_id']).json()
                    print("electicity generated by wind in MWH is: " +
                          str(fuelInfo['series'][0]['data'][0][1]))
                    powerPlants["powerPlants"][currentPlants]["fuelTypes"]["wind"] = fuelInfo['series'][0]['data'][0][1]
                if(plantNameAndSeries['category']['childseries'][k]['series_id'].__contains__("-SUN-ALL.A")):
                    print(plantName + " uses Solar!")
                    fuelInfo = requests.get(
                        eiaSeriesUri + "&series_id=" + plantNameAndSeries['category']['childseries'][k]['series_id']).json()
                    print("electicity generated by solar in MWH is: " +
                          str(fuelInfo['series'][0]['data'][0][1]))
                    powerPlants["powerPlants"][currentPlants]["fuelTypes"]["solar"] = fuelInfo['series'][0]['data'][0][1]

        if(powerPlants["powerPlants"][currentPlants]["outputMWH"] > sum(powerPlants["powerPlants"][currentPlants]["fuelTypes"].values())):
            powerPlants["powerPlants"][currentPlants]["fuelTypes"]["other"] = powerPlants["powerPlants"][currentPlants]["outputMWH"] - \
                sum(powerPlants["powerPlants"]
                    [currentPlants]["fuelTypes"].values())

        currentPlants += 1


with open("powerplants.json", "w") as outfile:
    json.dump(powerPlants, outfile)

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

plantTypes = {
    "-NG-ALL.A": "natural gas",
    "-SUB-ALL.A": "subbituminous coal",
    "-BIT-ALL.A": "bituminous coal",
    "-RC-ALL.A": "refined coal",
    "-DFO-ALL.A": "oil",
    "-WAT-ALL.A": "hydroelectric",
    "-NUC-ALL.A": "nuclear",
    "-WND-ALL.A": "wind",
    "-SUN-ALL.A": "solar",
    "-OBG-ALL.A": "biomass",
    "-LFG-ALL.A": "landfill gas"
}

# definition for a renewable resource derived from https://www.eia.gov/energyexplained/renewable-sources/
renewableSources = ["hydroelectric", "wind", "solar", "biomass"]


# 1st endpoint
illinoisPowerPlants = requests.get(eiaUri + "&category_id=902944").json()

currentPlants = 0
# len(illinoisPowerPlants['category']['childcategories'])
for i in range(len(illinoisPowerPlants['category']['childcategories'])):

    plantCategoryID = illinoisPowerPlants['category']['childcategories'][i]['category_id']
    plantName = re.sub("[\(\[].*?[\)\]]", "", illinoisPowerPlants['category']
                       ['childcategories'][i]['name']).strip()

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
        print(plantName)
        print("coordinates: " + plantInfo['series'][0]['latlon'])
        print("outputMWH: " + str(plantInfo['series'][0]['data'][0][1]))

        powerPlants["powerPlants"].insert(currentPlants, {})
        # illinoisPowerPlants['category']['childcategories'][i]['name']
        powerPlants["powerPlants"][currentPlants]["name"] = plantName
        # powerPlants["powerPlants"][currentPlants]["coordinates"] = plantInfo['series'][0]['latlon']
        powerPlants["powerPlants"][currentPlants]["coordinates"] = {
            "lat": float(plantInfo['series'][0]['lat']), "lon": float(plantInfo['series'][0]['lon'])}
        powerPlants["powerPlants"][currentPlants]["outputMWH"] = plantInfo['series'][0]['data'][0][1]
        powerPlants["totalOutput"] = powerPlants["totalOutput"] + \
            plantInfo['series'][0]['data'][0][1]

        powerPlants["powerPlants"][currentPlants]["fuelTypes"] = {}

        for k in range(len(plantNameAndSeries['category']['childseries'])):
            if(plantNameAndSeries['category']['childseries'][k]['series_id'].__contains__("GEN")):
                for fuelSuffix in plantTypes.keys():
                    if(plantNameAndSeries['category']['childseries'][k]['series_id'].__contains__(fuelSuffix)):
                        print(plantName + " uses " + plantTypes[fuelSuffix])
                        fuelInfo = requests.get(
                            eiaSeriesUri + "&series_id=" + plantNameAndSeries['category']['childseries'][k]['series_id']).json()
                        if(fuelInfo['series'][0]['data'][0][1] > 0):
                            powerPlants["powerPlants"][currentPlants]["fuelTypes"][plantTypes[fuelSuffix]
                                                                                   ] = fuelInfo['series'][0]['data'][0][1]

        if(powerPlants["powerPlants"][currentPlants]["outputMWH"] > sum(powerPlants["powerPlants"][currentPlants]["fuelTypes"].values())):
            powerPlants["powerPlants"][currentPlants]["fuelTypes"]["other"] = powerPlants["powerPlants"][currentPlants]["outputMWH"] - \
                sum(powerPlants["powerPlants"]
                    [currentPlants]["fuelTypes"].values())

        topFuel = max(powerPlants["powerPlants"][currentPlants]["fuelTypes"],
                      key=powerPlants["powerPlants"][currentPlants]["fuelTypes"].get)
        print("most used fuel for " + plantName + " is " + topFuel)
        if any(element in topFuel for element in renewableSources):
            print('RENEEEEEEEEWABLE')
            powerPlants["powerPlants"][currentPlants]["renewable"] = True
        else:
            print('not renewable')
            powerPlants["powerPlants"][currentPlants]["renewable"] = False

        currentPlants += 1


with open("powerplants.json", "w") as outfile:
    json.dump(powerPlants, outfile)

from azure.cosmos import CosmosClient, PartitionKey, exceptions
import os
import json
import time

# get enviroment variables
url = 'insert cosmosdb uri here'
key = 'insert cosmosdb key here'

# sets admin user and pw for api
admin_username = 'admin'
admin_password = 'password'

# create db client
client = CosmosClient(url, credential=key)

# set db and container names
database_name = 'powerPlantsdb'
container_name = 'powerPlants'
admin_container_name = 'admins'

try:
    database = client.create_database(database_name)
except exceptions.CosmosResourceExistsError:
    database = client.get_database_client(database_name)
time.sleep(30)
try:
    container = database.create_container(id=container_name, partition_key=PartitionKey(
        path="/name"), unique_key_policy={'uniqueKeys': [{'paths': ['/name']}]})
except exceptions.CosmosResourceExistsError:
    container = database.get_container_client(container_name)
except exceptions.CosmosHttpResponseError:
    raise
try:
    container = database.create_container(id=admin_container_name, partition_key=PartitionKey(
        path="/username"), unique_key_policy={'uniqueKeys': [{'paths': ['/username']}]})
except exceptions.CosmosResourceExistsError:
    container = database.get_container_client(admin_container_name)
except exceptions.CosmosHttpResponseError:
    raise


database = client.get_database_client(database_name)
adminContainer = database.get_container_client(admin_container_name)
adminContainer.upsert_item(
    {'username': admin_username, 'password': admin_password})
print('added username ' + admin_username + ' with password ' + admin_password)

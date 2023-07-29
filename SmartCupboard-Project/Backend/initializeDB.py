import json 
import requests
from databaseClass import myDatabase
import time

cupboardDB = myDatabase()

# check if DB exists 
if "cupboardDBtest" in cupboardDB.clientDB.list_database_names():
    print("DB already exists :) ")
    cupboardDB.clientDB.drop_database("cupboardDBtest")
    print("Dropped...")
else:
    print("cupboardDtest is now being created ...")
    f = open('testDB_data.json')
    Initialization_data = json.load(f) # dict

    cupboardsData = Initialization_data["Cupboards"] # list
    userData = Initialization_data["Users"] # list 
    WellKnownItemsData = Initialization_data["Well_known_items"] # list 
    WellKnownThemesData = Initialization_data["Well_known_themes"] # list 

    for cupboard in cupboardsData:
        requests.post("http://127.0.0.1:5001/insert/Cupboard" , json = cupboard)
        time.sleep(1)

    for user in userData: # user is a dict
        requests.post("http://127.0.0.1:5001/insert/User" , json = user )
        time.sleep(1)

    for knownItem in WellKnownItemsData: # user is a dict
        requests.post("http://127.0.0.1:5001/insert/KnownItem" , json = knownItem )
        time.sleep(1)
    
    for knownTheme in WellKnownThemesData: # user is a dict
        requests.post("http://127.0.0.1:5001/insert/KnownTheme" , json = knownTheme )
        time.sleep(1)

    # simulate training ... Insert current Items in cupboard 1
    requests.post("http://127.0.0.1:5001/train/Cupboard" , json = {"cupboard_id" : 1} )
from crypt import methods
from pickle import NONE
from flask import Flask,request,Response,jsonify
import databaseClass
from bson import json_util, ObjectId
import json 
from datetime import datetime
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
CORS(app)

@app.route('/test' , methods = ['GET','POST']) # Testing
def testFunc():
    print("ok request completed")
    return Response(status=200)

@app.route('/set/cupboardTheme' , methods = ['POST'])
def setCupboardTheme():
    data_json = request.get_json(force=True)
    cupboardId = data_json["cupboardId"]
    themeToSet = data_json["theme"]
    cupboardDB.updateCupboardTheme(cupboardId,themeToSet)

    return Response(status=200)

@app.route('/get/CupboardsTheme' , methods = ['GET'])
def getCupboardsTheme():
    
    cupboardsThemes = cupboardDB.getCupboardsThemes() # list 
    return jsonify(cupboardsThemes)



@app.route('/get/Cupboard/AllProducts' , methods = ['GET'])
def getAllItemsOfCupboard():

    cupId = int(request.args.get("cupboardId"))
    cupboardsItems = cupboardDB.getCupboardAllItems(cupId)
    
    return jsonify(json.loads(json_util.dumps(cupboardsItems)))


@app.route('/get/Cupboard/ExpiringProducts' , methods = ['GET'])
def getCupboardExpiringItems():
    cupId = int(request.args.get("cupboardId"))
    
    expiringCupboardItems = [] # init
    
    cupboardItems = cupboardDB.getCupboardAllItems(cupId)

    for item in cupboardItems:
        expDate_str = item["expiring_date"]
        print(expDate_str)

        expDate_datetime = datetime.strptime(expDate_str,date_format)
        delta_days = (expDate_datetime - today).days + 1 
        if delta_days <= expiringThreshold:
            expiringCupboardItems.append(item)    
    
    return  jsonify(json.loads(json_util.dumps(expiringCupboardItems))) 


@app.route('/get/Cupboard/TotalProductQuantity' , methods = ['GET'])
def getCupboardTotalProductQuantity():
    data_json = request.get_json(force= True)
    cupId = data_json["cupboardId"]
    itemToSearch = data_json["item"]
    
    quantityList = cupboardDB.getItemsQuantityOfCupboardByItemName(cupId,itemToSearch)

    sumQuant = 0 # initialize
    for item in quantityList:
        sumQuant += item["quantity"]    

    return jsonify(sumQuant)


@app.route('/get/Cupboard/ShelfItems' , methods = ['GET'])
def getCupboardShelfItems():
    
    cupId = int(request.args.get("cupboardId"))
    verticalOrder = int(request.args.get("verticalOrder"))

    shelfItems = cupboardDB.getCupboardItemsByShelfId(cupId,verticalOrder)

    return jsonify(json.loads(json_util.dumps(shelfItems)))



@app.route('/get/Cupboards/withIngredient' , methods = ['GET'])
def getCupboardsWhichContainIngredient():
    data_json = request.get_json(force= True)
    itemToSearch = data_json["item"]

    cupboardsWithIngredient = cupboardDB.getCupsWithIngredient(itemToSearch)
    print(cupboardsWithIngredient)

    #blink green light at the door of the cupboard
    for cupboardId in cupboardsWithIngredient:
        cupIP = cupboardDB.getControllerIPByCupId(cupboardId)
        requests_body_blinkDoor = {
            "startLed" : "1",
            "endLed" : "22",
            "color" : "green",
            "blinkingDuration" : "800",
            "totalEventDuration" : "8000",
            "ledstripeId" : "0" 
        }
        if cupboardId == 1 :
            # make a HTTP request to the controller of the cupboard to blink green light at door
            requests.post("http://"+cupIP+"/lights/blinkSomeLeds", json=requests_body_blinkDoor)
        else:
            print("sent http request to blink green light at door of cupboard with id: ",cupboardId)

    return jsonify(cupboardsWithIngredient)


@app.route('/get/Inventory/TotalProductQuantity' , methods = ['GET'])
def getInventoryTotalProductQuantity():
    data_json = request.get_json(force= True)
    itemToSearch = data_json["item"]

    quantityList = cupboardDB.getItemsQuantityOfInventoryByItemName(itemToSearch)

    sumQuant = 0 # initialize
    for item in quantityList:
        sumQuant += item["quantity"]    

    return jsonify(sumQuant)

@app.route('/get/Inventory/ExpiringProducts' , methods = ['GET'])
def getInventoryExpiringItems():
    expiringInventoryItems = [] # init

    inventoryItems = cupboardDB.getInventoryAllItems()

    for item in inventoryItems:
        
        expDate_str = item["expiring_date"]
        expDate_datetime = datetime.strptime(expDate_str,date_format)
        delta_days = (expDate_datetime - today).days + 1 
        if delta_days <= expiringThreshold:
            expiringInventoryItems.append(item)    
    
    # sort expiring Inventory items by cupboards
    expiringInventoryItems.sort(key = lambda x: x["cupboard_id"])

    # Light on and off the corresponding cupboard doors     
    # create a list with the keys "cupboard_id" of the list expiringInventoryItems
    cupboardIds = [item["cupboard_id"] for item in expiringInventoryItems]
    for cupboardId in cupboardIds:
        cupIP = cupboardDB.getControllerIPByCupId(cupboardId)
        requests_body_blinkDoor = {
            "startLed" : "1",
            "endLed" : "22",
            "color" : "red",
            "blinkingDuration" : "800",
            "totalEventDuration" : "8000",
            "ledstripeId" : "0" 
        }
        if cupboardId == 1 :
            # make a HTTP request to the controller of the cupboard to blink red light at door
            requests.post("http://"+cupIP+"/lights/blinkSomeLeds", json=requests_body_blinkDoor)
        else:
            print("Sent HTTP request to cupboard controller of cupboardId: ",cupboardId , "to blink door red")
            print("Sent HTTP request to cupboard controller of cupboardId: ",cupboardId , "to light red above expiring products")


    print(cupboardIds)

    return jsonify(json.loads(json_util.dumps(expiringInventoryItems)))


@app.route('/get/Cupboard/LowQuantityProducts' , methods = ['GET'])
def getCupboardLowQuantityProducts():

    cupId = int(request.args.get("cupboardId"))

    cupboardItems = cupboardDB.getCupboardAllItems(cupId)
    lowQuantProducts = []
    
    for item in cupboardItems:
        itemOriginalWeight = cupboardDB.getOriginalWeight(item["Well_known_item_id"])
        
        currentWeight = item["quantity"]
        if (currentWeight < (lowQuantityThreshold * itemOriginalWeight)):
            lowQuantProducts.append(item)

    return jsonify(json.loads(json_util.dumps(lowQuantProducts)))


@app.route('/get/Inventory/LowQuantityProducts' , methods = ['GET'])
def getInventoryLowQuantityProducts():
    inventoryItems = cupboardDB.getInventoryAllItems()
    lowQuantProducts = []

    for item in inventoryItems:
        itemOriginalWeight = cupboardDB.getOriginalWeight(item["Well_known_item_id"])
        
        currentWeight = item["quantity"]
        if (currentWeight < (lowQuantityThreshold * itemOriginalWeight)):
            lowQuantProducts.append(item)

    return jsonify(json.loads(json_util.dumps(lowQuantProducts)))


@app.route('/get/info/ForAnItem/InCupboard' , methods = ['GET'])
def ItemInfoInCupboard():
    cupId = int(request.args.get("cupboardId"))
    item = request.args.get("item")

    ItemInfo = cupboardDB.getItemInfoInCupboard(cupId,item)

    return jsonify(json.loads(json_util.dumps(ItemInfo)))


# get all cupboards with available space
@app.route('/get/Inventory/AvailableCupboards' , methods = ['GET'])
def getAvailableCups():
    #Get available cupboards
    availableCupsList = cupboardDB.getAvailableCupboards()
    print("Marios")
    print(availableCupsList)
    emptySlots_counter = 0

    availCupsInfoList = [] # init
    for cupboard in availableCupsList:
        for shelfData in cupboard["Shelves"]:
            for slotsData in shelfData["Slots"]:
                if slotsData["end"] - slotsData["start"] >= 10:
                    emptySlots_counter += 1
        cupInfo = {
            "cupboard_id": cupboard["id"],
            "empty_slots": emptySlots_counter
        }
        availCupsInfoList.append(cupInfo)
        emptySlots_counter = 0 # reset counter
    
    print()
    print(availCupsInfoList)

    # make a post request to the CupboardManager server to blink yellow light at door
    requests.post("http://localhost:5001/light/Cupboard/blinkDoor", json={"cupId": 1 , "color": "yellow"})

    return jsonify(availCupsInfoList)

# main():

cupboardDB = databaseClass.myDatabase()
date_format = "%d/%m/%y"
expiringThreshold = 4 # days 
lowQuantityThreshold = 0.2 # 20%
today = datetime.today()#.strftime(date_format)

app.run(debug=True,host='0.0.0.0',port=5002) # Run by Marios PC ,use_reloader=False
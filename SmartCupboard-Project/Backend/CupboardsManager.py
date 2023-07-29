from flask import Flask,request,Response
import databaseClass
import requests
from flask_cors import CORS
import netifaces as ni
from playsound import playsound
import gtts

app = Flask(__name__)
CORS(app)

marios_laptop_ip = ni.ifaddresses('wlp3s0')[ni.AF_INET][0]['addr']
print("Marios laptop IP is : ",marios_laptop_ip)

@app.route('/test' , methods = ['GET','POST']) # Testing
def testFunc():
    print("ok request completed")
    # return {'a': 'c'}, 200
    return Response(status=200)

@app.route('/insert/KnownTheme' , methods = ["POST"])
def insertKnownTheme():
    data_json = request.get_json(force=True)
    name = data_json["_id"]
    icon = data_json["icon"]

    cupboardDB.insertKnownTheme(name,icon)

    return Response(status=200)

@app.route('/insert/Cupboard' , methods = ["POST"])
def insertCup():
    data_json = request.get_json(force= True)
    cupId = data_json["_id"]
    doorStatus = data_json["door_status"]
    knownTheme = data_json["known_theme"]
    defaultTime = data_json["default_time"]
    repEvery = data_json["rep_every"]
    lastLearn = data_json["last_learn"]
    shelfData = data_json["Shelves"]
    cupboardControllerData = data_json["Cupboard_controller"]

    cupboardDB.insertCupboard(cupId,doorStatus,knownTheme,defaultTime,repEvery,lastLearn,shelfData,cupboardControllerData)
    
    return Response(status=200)

@app.route('/insert/User' , methods = ["POST"])
def insertUser():
    data_json = request.get_json(force=True)
    username = data_json["_id"]
    name = data_json["name"]
    surname = data_json["surname"]
    age = data_json["age"]
    permissionsData = data_json["permissions"] # list 
    cupboardDB.insertUser(username,name,surname,age,permissionsData)

    return Response(status=200)

@app.route('/insert/KnownItem' , methods = ["POST"])
def insertKnownItem():
    data_json = request.get_json(force= True)
    category = data_json["categ"]
    name = data_json["name"]
    original_weight = data_json["orig_weight"]
    imagePath = data_json["image"]
    expected_expiring_days = data_json["exp_expiring_days"]

    cupboardDB.insertKnownItem(category,name,original_weight,imagePath,expected_expiring_days)

    return Response(status=200)


@app.route('/set/UserAccess' , methods = ["POST"])
def setUserAccess():
    data_json = request.get_json(force=True)
    userId = data_json["_id"]
    cupIdSetAccess = data_json["cupboard_id"]

    cupboardDB.setAccess(userId,cupIdSetAccess)

    return Response(status=200)

@app.route('/remove/UserAccess' , methods = ["POST"])
def removeUserAccess():
    data_json = request.get_json(force=True)
    userId = data_json["_id"]
    cupIdRemoveAccess = data_json["cupboard_id"]

    cupboardDB.removeAccess(userId,cupIdRemoveAccess)
    return Response(status=200)

@app.route('/close/allCupboardDoors' , methods = ['POST'])
def closeAllCups():
    cupboardsIPs_list = cupboardDB.getAllcupboardsIPs()

    for cupboardIP in cupboardsIPs_list:
        print('http://' + cupboardIP["IP"] + '/door/' + 'close')
    
    return Response(status=200)

@app.route('/train/Cupboard', methods = ['POST'])
def trainCupboard():
    data_json = request.get_json(force=True)
    cupboard_id = data_json["cupboard_id"] # which cupboard to train 
    
    # get IP by cupboard_id
    cupboardIP = cupboardDB.getControllerIPByCupId(cupboard_id)

    print(cupboardIP)
    
    import json 
    if cupboard_id == 1:
        filename = '../experiment/products_cup1_phaseA.json'
    elif cupboard_id == 2:
        filename = '../experiment/products_cup2.json'
    else:
        print("Error: cupboard_id is not 1 or 2")
    
    f = open(filename)
    trainResultsJSON = json.load(f) # dict

    cupboardDB.storeItemsAfterTrain(trainResultsJSON)
    
    # send an http request to backend angular to update the items in the cupboard
    print("Now send an http request to backend angular to inform it that the cupboard has been trained")

    ItemsDataSendToAngular = cupboardDB.getCupboardAllItems(cupboard_id)
    print(type(ItemsDataSendToAngular))
    print(ItemsDataSendToAngular)
    
    requests.post('http://'+marios_laptop_ip+':8080/api/getData/broadcast/test', json = ItemsDataSendToAngular)

    return Response(status=200)


@app.route('/light/Cupboard/ConstantDoor', methods = ['POST'])
def lightConstantDoor():
    data_json = request.get_json(force=True)
    color = data_json["color"]
    cupId = data_json["cupId"]
    cupIP = cupboardDB.getControllerIPByCupId(cupId)

    print("Light constant door with color : ", color)

    if cupId == 1 :
        # make a HTTP request to the controller of the cupboard to blink red light at door
        requests.post("http://"+cupIP+"/lights/ConstantDoor", json={"color" : color})
    else:
        print("sent request to another cupboard to light the door with color : ", color)
    
    return Response(status=200)

@app.route('/light/Cupboard/blinkDoor', methods = ['POST'])
def lightblinkDoor():
    data_json = request.get_json(force=True)
    color = data_json["color"]
    cupId = data_json["cupId"]
    cupIP = cupboardDB.getControllerIPByCupId(cupId)

    print("Blink door with color : ", color)
    blink_req_body = {
    "startLed" : "1",
    "endLed" : "23",
    "color" : color,
    "blinkingDuration" : "800",
    "totalEventDuration" : "4000",
    "ledstripeId" : "0" 
    }

    if cupId == 1 :
        # make a HTTP request to the controller of the cupboard to blink red light at door
        requests.post("http://"+cupIP+"/lights/blinkSomeLeds", json=blink_req_body)
    else:
        print("sent request to another cupboard to blink the door with color : ", color)
    
    return Response(status=200)

@app.route('/highlight/available/Cupboards', methods = ['POST'])
def highlightAvailableCupboards():
        
    #Get available cupboards
    availableCupsList = cupboardDB.getAvailableCupboards()

    # # Highlight available cupboards
    for availableCup in availableCupsList:
        cupId = availableCup["id"]
        controllerIP = cupboardDB.getControllerIPByCupId(cupId)
        print('http://' + controllerIP + '/lights/ConstantDoor')
      
        # # Highlight empty slots of available cupboards
        for shelf in availableCup["Shelves"]:
            verticalOrder = shelf["vertical_order"]
            for slot in shelf["Slots"]:
                print('http://' + controllerIP + '/lights/ConstantFromSpaceToSpace')
                # requests.post('http://' + controllerIP + '/lights/ConstantFromSpaceToSpace' , json={"startSpace" : slot["start"] , "endSpace" : slot["end"] , "color" : "yellow" , "shelf" : verticalOrder})

    return Response(status=200)

@app.route('/highlight/Cupboard/emptySlots', methods = ['POST'])
def highlightEmptySlotsOfCupboard():
    data_json = request.get_json(force=True)
    cupboard_id = data_json["cupboard_id"]

    #Get available cupboards
    availableCupsList = cupboardDB.getAvailableCupboards(specificCupId=cupboard_id)

    # Highlight available cupboards
    for availableCup in availableCupsList:
        cupId = availableCup["id"]
        controllerIP = cupboardDB.getControllerIPByCupId(cupId)
      
        # Highlight empty slots of available cupboards
        for shelf in availableCup["Shelves"]:
            verticalOrder = shelf["vertical_order"]
            for slot in shelf["Slots"]:
                print('http://' + controllerIP + '/lights/ConstantFromSpaceToSpace')

    return Response(status=200)

# create an endpoint for controlling cupboards doors   
@app.route('/controlCupboardDoor', methods = ['POST'])
def controlCupboardDoor():
    data_json = request.get_json(force=True)
    cupboard_id = data_json["cupboard_id"]
    action = data_json["action"] # open or close or semiopen

    controllerIP = cupboardDB.getControllerIPByCupId(cupboard_id)

    print('http://' + controllerIP + '/door/' + action)
    requests.post('http://' + controllerIP + '/door/' + action) # make the HTTP POST request to cupboard controller  

    if action == "close" :
        # turn off the lights inside the cupboard
        requests.post('http://' + controllerIP + '/lights/switchoff' , json = {"ledstripeId" : 1})

    return Response(status=200)


# DEMO PURPOSES
#1
@app.route('/train/Demo/Cupboard/fourItems', methods = ['POST'])
def trainCupboardFour():
    data_json = request.get_json(force=True)
    cupboard_id = data_json["cupboard_id"] # which cupboard to train 
    
    # get IP by cupboard_id
    cupboardIP = cupboardDB.getControllerIPByCupId(cupboard_id)

    
    import json 
    f = open('/home/marios/Desktop/smart_git/SmartCupboard_569/SmartCupboard_ThesisProject/Demo_Remote/learningJSON_outputDEMO_fourItems.json')
    trainResultsJSON = json.load(f) # dict

    print(trainResultsJSON)
    cupboardDB.storeItemsAfterTrain(trainResultsJSON)
    
    # send an http request to backend angular to update the items in the cupboard
    print("Now send an http request to backend angular to inform it that the cupboard has been trained")

    ItemsDataSendToAngular = cupboardDB.getCupboardAllItems(cupboard_id)
    requests.post('http://'+marios_laptop_ip+':8080/api/getData/broadcast/test', json = ItemsDataSendToAngular)

    return Response(status=200)

#2
@app.route('/train/Demo/Cupboard/fiveItems', methods = ['POST'])
def trainCupboardFive():
    data_json = request.get_json(force=True)
    cupboard_id = data_json["cupboard_id"] # which cupboard to train 
    
    # get IP by cupboard_id
    cupboardIP = cupboardDB.getControllerIPByCupId(cupboard_id)

    
    import json 
    f = open('/home/marios/Desktop/smart_git/SmartCupboard_569/SmartCupboard_ThesisProject/Demo_Remote/learningJSON_outputDEMO_fiveItems.json')
    trainResultsJSON = json.load(f) # dict

    
    cupboardDB.storeItemsAfterTrain(trainResultsJSON)
    
    # send an http request to backend angular to update the items in the cupboard
    print("Now send an http request to backend angular to inform it that the cupboard has been trained")

    ItemsDataSendToAngular = cupboardDB.getCupboardAllItems(cupboard_id)
    requests.post('http://'+marios_laptop_ip+':8080/api/getData/broadcast/test', json = ItemsDataSendToAngular)

    return Response(status=200)

# EXPERIMENT
@app.route('/train/experiment', methods = ['POST'])
def trainCupboardExperimentCupOne():
    data_json = request.get_json(force=True)
    cupboard_id = data_json["cupboard_id"] # which cupboard to train 
    
    import json 
    f = open('/home/marios/Desktop/smart_git/SmartCupboard_569/SmartCupboard_ThesisProject/experiment/products_cup1_phaseA.json')
    trainResultsJSON = json.load(f) # dict
    
    cupboardDB.storeItemsAfterTrain(trainResultsJSON)
    
    # send an http request to backend angular to update the items in the cupboard
    print("Now send an http request to backend angular to inform it that the cupboard has been trained")

    ItemsDataSendToAngular = cupboardDB.getCupboardAllItems(cupboard_id)
    requests.post('http://'+marios_laptop_ip+':8080/api/getData/broadcast/test', json = ItemsDataSendToAngular)

    return Response(status=200)

# EXPERIMENT
# create an endpoint which will receive a string in its body and play a mp3 file with that name
@app.route('/playAudio', methods = ['POST'])
def playAudio(): # run without sudo
    data_json = request.get_json(force=True)
    audioFileName = data_json["audioFileName"]
    customMode = data_json["customMode"]
    textToSpeech = data_json["textToSpeech"]
    filepath = '/home/marios/Desktop/smart_git/SmartCupboard_569/SmartCupboard_ThesisProject/code_Servers_raised_externally/audio_tasks/'

    if customMode == "no":
        print(audioFileName)
        
        filepath += audioFileName
        
        # play mp3 file
        playsound(filepath) 
    
    elif customMode == "yes" :
        print(textToSpeech)
        tts = gtts.gTTS(textToSpeech, lang='en')

        # save and overwrite the audio file
        tts.save("audio_tasks/customAudio.mp3")

        filepath += "customAudio.mp3"

        # play the audio file
        playsound(filepath) 
    
    else: 
        print("Error in playAudio()")
        print("customMode value was : " ,customMode)

    return Response(status=200)

# main():

cupboardDB = databaseClass.myDatabase()

app.run(debug=True,host='0.0.0.0',port=5001) # Run by Marios PC ,use_reloader=False

from flask import request,jsonify

arduino_leds = None

def executeCommand(command, arduinoBoard):    
    print("command sent to arduino is : " , command) # debug 
    arduinoBoard.write(bytes(str(command), "utf-8"))
    return "Command has been executed" # needed ?? NO 
    
def light_setSerial(serial):
    global arduino_leds 
    arduino_leds = serial
    print("light serial set")

############
## LIGHTS ##
############

lightsLedOn = 21 

def lights_func(suburl=None):
    global lightsLedOn

    if request.method == 'POST':

        data_json = request.get_json(force=True,silent=True) # a multidict containing POST data
        if suburl == "SpecificLed":  # ledId, color , ledStripeId
                  
            ledId = data_json['ledId']
            ledstripeId = data_json['ledstripeId']

            color = data_json['color']
            command = 'lightSpecificLed' + '_' + str(ledId) + '_' + str(ledstripeId)+ '_' + color + ';'

            executeCommand(command, arduino_leds)        
            return "specific led is on"
        
        elif suburl == "lightOneMoreLed":  # ledId, color , ledStripeId

            command = 'lightOneMoreLed_'  + str(lightsLedOn) + ';'
            print('command of lightOneMoreLed is : ' , command) 

            lightsLedOn = lightsLedOn - 1 
            print('I JUST REDUCED LIGHTS_ON BY ONE') 

            executeCommand(command, arduino_leds)        
            return "one more led is on"
        
        elif suburl == "switchoff":
            ledstripeId = data_json['ledstripeId']
            executeCommand("switchoff_" + str(ledstripeId)+ ';', arduino_leds)
            return "switchoff"
        
        elif suburl == "ConstantFromToLedIDs": # startLed,endLed, color , ledStripeId

            startLed = data_json['startLed']
            endLed = data_json['endLed']
            color = data_json['color']
            ledstripeId = data_json['ledstripeId']
            command = 'c1_' + str(startLed)+ '_' + str(endLed) + '_' + color + '_' + str(ledstripeId) + ';'

            print('command of ConstantFromToLedIDs is : ' , command) # debug 

            executeCommand(command, arduino_leds)
            return jsonify("lightConstantFromToLedIDs") # fix SyntaxError: Unexpected token l in JSON at position 0 at JSON.parse (<anonymous>) at XMLHttpRequest.onLoad
        
        elif suburl == "ConstantlyShelf": # bug -- if i light a shelf and then the other one the previous shelf is switched off
            whichShelf = data_json['whichShelf'] # string -- "up" or "down"
            color = data_json['color']
            
            executeCommand("lightConstantlyShelf_" + whichShelf + '_' + color+ ';',arduino_leds)
            return "Shelf has been lighted"

        elif suburl == "ConstantDoor":
            color = data_json['color'] # string
            executeCommand("lightConstantDoor_" + color + ';',arduino_leds)
            
            return "Door is constantly lighted"


        elif suburl == "LedByLed": # only for the DOOR
            reachLed = data_json['reachLed']
            color = data_json['color'] # string
            duration = data_json['duration']
            executeCommand("lightLedByLed_" + str(reachLed) + '_' + color + '_' + str(duration) + ';' ,arduino_leds) # added + '_' check for 3 http requests problem

            return "Led by led ok "
        
        elif suburl == "setlearning": 
            statusLearning = data_json["status"]
            command = "setLearning_"  + statusLearning + ';'
            print("set learning command is : " , command)
            executeCommand(command, arduino_leds)
            return "Learning setted as on "

        elif suburl == "doorLearningInterruption":
            executeCommand("c2;" , arduino_leds)
            return "There is a doorLearning interruption "
        

        elif suburl == "blinkSomeLeds":
            startLed = data_json['startLed']
            endLed = data_json['endLed']
            color = data_json['color']
            totalEventDuration = data_json['totalEventDuration']
            blinkingDuration = data_json['blinkingDuration']
            ledstripeId = data_json['ledstripeId']
        
            blinking_command = "blinkSomeLeds_" + str(startLed)+"_"+str(endLed)+"_"+color+"_"+str(totalEventDuration)+"_"+str(blinkingDuration)+"_"+str(ledstripeId)+";"
            print("blinking command is : ",blinking_command) # debug
            executeCommand(blinking_command , arduino_leds)
            return "Now some leds are blinking "

        else:
            print("some url error maybe here ...")

    elif request.method == 'GET':
        print('i have a GET request')
        return 'GET req'
    else:
        print("some error here ...")
        return "Error"

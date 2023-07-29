from flask import request

arduino_leds = None 

def proximity_setSerial(serial):
    global arduino_leds 
    arduino_leds = serial
    print("proximity serial set")

def executeCommand(command, arduinoBoard):    
    arduinoBoard.write(bytes(str(command), "utf-8"))
    return "Command has been executed" # needed ?? NO 

def proximity_func(suburl=None):
    if request.method == 'POST':

        if suburl == "status": # weight 
            executeCommand("proximityStatus",arduino_leds) # maybe calculateWeight_ instead
        else:
            return 'Wrong suburl in /proximity'

    return "proximity ok"
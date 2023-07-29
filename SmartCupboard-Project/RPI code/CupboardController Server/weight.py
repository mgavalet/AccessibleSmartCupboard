from flask import request

arduino_leds = None 

def weight_setSerial(serial):
    global arduino_leds 
    arduino_leds = serial
    print("weight serial set")

def executeCommand(command, arduinoBoard):    
    arduinoBoard.write(bytes(str(command), "utf-8"))
    return "Command has been executed" # needed ?? NO 

def weight_func(suburl=None):
    if request.method == 'POST':

        if suburl == "calculateWeight": # weight 
            executeCommand("weightStatus",arduino_leds) # maybe weightStatus_ instead
        else:
            return 'Wrong suburl in /weight'

    return "Weight ok"
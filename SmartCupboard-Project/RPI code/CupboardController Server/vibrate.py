from flask import request

arduino_leds = None 

def vibrate_setSerial(serial):
    global arduino_leds 
    arduino_leds = serial
    print("vibrate serial set")

def executeCommand(command, arduinoBoard):    
    arduinoBoard.write(bytes(str(command), "utf-8"))
    return "Command has been executed" # needed ?? NO 

def vibrate_func(suburl=None):
    if request.method == 'POST':
        data_json = request.get_json(force=True , silent = True)

        if suburl == "steady": # vibrate for vibrationDuration milliseconds
            print("Debug . Suburl is steady") # debug 
            print("vibSteady_" + str(data_json['vibrationDuration'])) # debug 
            executeCommand("vibSteady_" + str(data_json['vibrationDuration']),arduino_leds) # msec
        elif suburl == "periodically":
            executeCommand("vibPeriodically_" 
            + str(data_json['vibrationDuration']) + '_' 
            + str(data_json['eventDuration']) , arduino_leds)
        elif suburl == "times":
            executeCommand('vibTimes_' + str(data_json['times']) + '_' + str(data_json['vibrationDuration']),arduino_leds)
        else:
            return 'Wrong suburl in /vibrate'

    return "Vibration ok"

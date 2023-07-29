from flask import request
# import serial
import modulesCupboard
import redis 
from subprocess import *
import configuration_params

def run_cmd(cmd):
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = str(p.communicate()[0])
        output = output[2 :-3]
        return output


arduino_motor = None 

def door_setSerial(serial):
    global arduino_motor 
    arduino_motor = serial
    print("door serial set")

redisIP = configuration_params.rpi_ip
redisPort = 6379

redis_channel_CommandExec = 'CommandExec' # change that maybe

redis_client = redis.Redis(host=redisIP , port= redisPort) 

p = redis_client.pubsub()
p.subscribe(redis_channel_CommandExec) 

def getDoorStatus():
    return modulesCupboard.doorStatus

def executeCommand(command, arduinoBoard):    
    arduinoBoard.write(bytes(str(command), "utf-8"))
    return "Command has been executed" 

def waitCommandExecutionToBeCompleted(command):   
    global p 

    while True:
        message = p.get_message()


        if message and message != None:
                        
            print('Command argument is ...' ,command)
            print('modulesCupboard.executedCommand is ...' , modulesCupboard.executedCommand) 

            if modulesCupboard.executedCommand != command:
                continue
            else:
                print('break') # debug
                break

def door_func(suburl = None):

    if request.method == 'POST':
        # a multidict containing POST data
        data_json = request.get_json(force=True,silent=True) #silent = True :this method will fail silently and return None.

        if suburl == "open" :
            executeCommand("openTotally",arduino_motor)
            return "open"
        elif suburl == "close" :
            executeCommand("closeTotally",arduino_motor)
            return "close"
        elif suburl == "semiopen" :
            executeCommand("semiOpen",arduino_motor)
            return "semi-open"
        elif suburl == "homing" :
            executeCommand("cupboardHoming",arduino_motor) 
            waitCommandExecutionToBeCompleted("cupboardHoming") # wait ...
            print('This line MUST be printed after waiting !! ') # debug           
            return "door-homing"

        elif suburl == "status": # door-status : 1. Moving , 2. Closed , 3. Opened , 4. Semi-opened
            
            print("Door status is : " , getDoorStatus()) # debug
            
            return modulesCupboard.doorStatus    
        
        elif suburl == "moveTo" :
            x_door = data_json['door_x']
            executeCommand("moveCupboardTo_" + str(x_door),arduino_motor)
            return "moveTo ok"
        elif suburl == "moveBy" :
            x_door = data_json['door_x']
            executeCommand("moveCupboardBy_" + str(x_door),arduino_motor)
            return "moveBy ok" 

        elif suburl == "getCurrentPosition" :
            executeCommand("getDoorPosition_random",arduino_motor) # need _ or not ? 
            return "Request getCurrentPosition executed"

        else:
            return "wrong suburl"
    else:
        return "It was a GET request"

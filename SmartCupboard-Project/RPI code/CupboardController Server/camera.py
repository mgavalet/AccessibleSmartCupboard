import requests
from flask import request
import modulesCupboard
import redis
from subprocess import *
import configuration_params

def run_cmd(cmd):
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = str(p.communicate()[0])
        output = output[2 :-3]
        return output

cameraIP = '192.168.4.19' # constant

redisIP = configuration_params.rpi_ip
redisPort = 6379

redis_channel_CommandExec = 'CommandExec' # change that maybe

try:
    print('attempt for ', redisIP , 'and ' , redisPort) 
    redis_client = redis.Redis(host=redisIP , port= redisPort) 
    p = redis_client.pubsub() 
    p.subscribe(redis_channel_CommandExec)

except Exception as e :
    print ('type is:', e.__class__.__name__) # ConnectionError
    print("Check redis server connection !")
    print("Yourrrrr current attempt was to connect to " ,redisIP,":",redisPort)


arduino_motor = None

def camera_setSerial(serial):
    global arduino_motor 
    arduino_motor = serial
    print("camera serial set")

def executeCommand(command, arduinoBoard):    
    arduinoBoard.write(bytes(str(command), "utf-8"))
    return "Command has been executed" 

def waitCommandExecutionToBeCompleted(command):   
    global p 

    while True:
        message = p.get_message()

        if message and message != None:
                        
            print('Command argument is ...' ,command) # debug
            print('modulesCupboard.executedCommand is ...' , modulesCupboard.executedCommand) # debug

            if modulesCupboard.executedCommand != command:
                continue
            else:
                print('break')
                break

def camera_func(suburl=None):
    if request.method == 'POST':
        data_json = request.get_json(force=True , silent= True)

        if suburl == 'capture':
            print('Before capturing a foto') 
            request_capture = requests.get("http://" + cameraIP + "/capture")
            image_bytes = request_capture.content

            return image_bytes # return the bytes of the captured foto

        elif suburl == 'dohoming' : 
            executeCommand("cameraHoming" , arduino_motor)
            waitCommandExecutionToBeCompleted("cameraHoming") # wait ...
            print('This line MUST be printed after waiting !! ') 

            return "Camera homing"

        elif suburl == 'setFramesize':
            requests.get("http://" + cameraIP + "/control?var=framesize&val=" + str(data_json['framesize']))
            return "Framesized setted in " + str(data_json['framesize'])
        
        elif suburl == 'horizontallyBy':
            executeCommand("moveHorBy_" + str(data_json['x']), arduino_motor)
            waitCommandExecutionToBeCompleted("moveHorBy") # wait ...
            print('This line MUST be printed after waiting !! ') 
            
            return 'horizontally moving ok'
        
        elif suburl == 'verticallyBy':
            executeCommand("moveVerBy_" + str(data_json['y']), arduino_motor)
            waitCommandExecutionToBeCompleted("moveVerBy") # wait ...
            print('This line MUST be printed after waiting !! ') 
            
            return 'vertically by moving ok'
       
        elif suburl == 'bothBy':
            executeCommand("moveBothBy_" + str(data_json['x']) + '_' + str(data_json['y']), arduino_motor)
            waitCommandExecutionToBeCompleted("moveBothBy") # wait ...
            print('This line MUST be printed after waiting !! ') 
            return 'move both by was ok'
        
        elif suburl == 'ToPosition':
            executeCommand("moveToPosition_" + str(data_json['x']) + '_' + str(data_json['y']), arduino_motor)
            waitCommandExecutionToBeCompleted("moveToPosition") # wait ...
            print('This line MUST be printed after waiting !! ') 
            
            return 'Move to position was ok'
        
        elif suburl == 'ToHor':
            executeCommand("moveToHor_" + str(data_json['x']), arduino_motor)
            waitCommandExecutionToBeCompleted("moveToHor") # wait ...
            print('This line MUST be printed after waiting !! ') 
            
            return 'move to horizontally was ok'
        
        elif suburl == 'ToVer':
            executeCommand("moveToVer_" + str(data_json['y']), arduino_motor)
            waitCommandExecutionToBeCompleted("moveToVer") # wait ...
            print('This line MUST be printed after waiting !! ') 
            
            return 'Move vertically to was ok'
        
        else:
            return "Wrong sururl in /camera/"

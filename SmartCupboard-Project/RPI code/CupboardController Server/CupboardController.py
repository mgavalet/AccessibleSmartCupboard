from flask import Flask,jsonify,request,abort
import serial
from flask_cors import CORS
import threading
import redis #  Publisher -- CupboardController
import modulesCupboard
import configuration_params

from lights import lights_func,light_setSerial
from camera import camera_func,camera_setSerial
from door import door_func,door_setSerial
from vibrate import vibrate_func,vibrate_setSerial
from touch import touch_func
from weight import weight_func,weight_setSerial
from proximity import proximity_func,proximity_setSerial

app = Flask(__name__)

CORS(app)
    
############
## TESTER ##
############
json_tester = [ 
{
    'Label' : 'Mustard',
    'Location_start' : 40,
    'Location_end' : 50,
    'Quantity' : 194,
    'Cupboard' : 1,
    'Shelf' : 'Up',
    'Expiring' : 3,
    'WhenLastUsed' : 1,
    'UserLastUsed' : 'Asterios'
},
{
    'Label' : 'Tomato',
    'Location_start' : 5,
    'Location_end' : 15,
    'Quantity' : 134,
    'Cupboard' : 1,
    'Shelf' : 'Up',
    'Expiring' : 15,
    'WhenLastUsed' : 1,
    'UserLastUsed' : 'Marios'
},
{
    'Label' : 'Rice',
    'Location_start' : 60,
    'Location_end' : 70,
    'Quantity' : 170,
    'Cupboard' : 1,
    'Shelf' : 'Bottom',
    'Expiring' : 15,
    'WhenLastUsed' : 1,
    'UserLastUsed' : 'Unused'
},
{
    'Label' : 'Sugar',
    'Location_start' : 75,
    'Location_end' : 85,
    'Quantity' : 13,
    'Cupboard' : 1,
    'Shelf' : 'Bottom',
    'Expiring' : 15,
    'WhenLastUsed' : 1,
    'UserLastUsed' : 'Antonis'
}
]

@app.route('/tester')
def tester_func():
    return jsonify(json_tester)

@app.route('/marios/' , methods = ['POST' ,'GET'])
def marios_func(): 
    return "Hello" # debug


###########
## DOOR ###
###########

@app.route('/door/<suburl>',  methods = ['POST' , 'GET'])
def door_handler(suburl = None):
    return door_func(suburl=suburl)

############
## LIGHTS ##
############

@app.route('/lights/<suburl>' ,  methods = ['POST' , 'GET'])
def lights_handler(suburl = None):
    return lights_func(suburl=suburl)
    

############
## CAMERA ##
############

@app.route('/camera/<suburl>' ,  methods = ['POST' , 'GET'])
def camera_handler(suburl = None):
    return camera_func(suburl=suburl)


#############
## Vibrate ##
#############

@app.route('/vibrate/<suburl>' ,  methods = ['POST' , 'GET'])
def vibrate_handler(suburl = None):
    return vibrate_func(suburl=suburl)
    

#############
## Weight ##
#############

@app.route('/weight/<suburl>' ,  methods = ['POST' , 'GET'])
def weight_handler(suburl = None):
    return weight_func(suburl=suburl)

#############
## Proximity ##
#############

@app.route('/proximity/<suburl>' ,  methods = ['POST' , 'GET'])
def proximity_handler(suburl = None):
    return proximity_func(suburl=suburl)

###########
## TOUCH ##
###########

@app.route('/touch/<suburl>' ,  methods = ['POST' , 'GET'])
def touch_handler(suburl = None):
    return touch_func(suburl=suburl)


def thread_func_listenToSerial(callbackFunc , arduinoBoard):
    
    while(True):
        if arduinoBoard.inWaiting():
            data = arduinoBoard.readline() # readline returns bytes
            data = data.decode("utf-8") # now it is string -- decode bytes
            
            print("Data sent by arduino : " ,  data)
            # print(type(data))

            if not (data == None or data == "" or len(data.split(",")) < 2):
                token_list = data.split(",")
                callbackFunc(token_list)


def callback (data_list):
    global redis_channel_TouchSensor # 'touchState'
    global redis_channel_DoorStatus 
    global redis_channel_CommandExec

    # LED ARDUINO

    if data_list[0] == "TouchSensorState":
        modulesCupboard.touchSensorState = data_list[1]  
        modulesCupboard.touchSensorState = modulesCupboard.touchSensorState.replace("\r\n","")         
        
        print("touch in redis --->" , modulesCupboard.touchSensorState) 

        redis_client.publish(redis_channel_TouchSensor,modulesCupboard.touchSensorState)

    elif data_list[0] == "WeightStatus":
        modulesCupboard.weightValue = data_list[1]
        modulesCupboard.weightValue = modulesCupboard.weightValue.replace("\r\n","")

        redis_client.publish(redis_channel_WeightStatus,modulesCupboard.weightValue)
    
    elif data_list[0] == "ProximityStatus":
        modulesCupboard.proximityStatus = data_list[1] 
        modulesCupboard.proximityStatus = modulesCupboard.proximityStatus.replace("\r\n","")

        redis_client.publish(redis_channel_ProximityStatus,modulesCupboard.proximityStatus)
    elif data_list[0] == "ScaleStatus":
        modulesCupboard.itemOnScale = data_list[1]
        modulesCupboard.itemOnScale = modulesCupboard.itemOnScale.replace("\r\n","")         
        print("Item on scale in redis --->" , modulesCupboard.itemOnScale)

        redis_client.publish(redis_channel_itemOnScale,modulesCupboard.itemOnScale)

    # MOTOR ARDUINO

    elif data_list[0] == "DoorStatus":
        modulesCupboard.doorStatus = data_list[1] # doorStatus must be a string ! 
        modulesCupboard.doorStatus = modulesCupboard.doorStatus.replace("\r\n","")

        redis_client.publish(redis_channel_DoorStatus,modulesCupboard.doorStatus)
    
    elif data_list[0] == "ExecOk":
        modulesCupboard.executedCommand = data_list[1].replace("\r\n","")

        redis_client.publish(redis_channel_CommandExec,modulesCupboard.executedCommand) 
    
    elif data_list[0] == "DoorPosition":
        
        doorPosition = data_list[1].replace("\r\n","")
        print("Door position is : " ,doorPosition)
    
    else:
        pass



if __name__ == '__main__':

    port1 = "/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.1:1.0-port0"  # arduino MOTOR ALWAYS
    port2 = "/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.2:1.0-port0"  # arduino LED ALWAYS

    arduino_motor = serial.Serial(port=port1, baudrate=115200, timeout=60)
    arduino_leds = serial.Serial(port=port2, baudrate=9600, timeout=60)

    light_setSerial(arduino_leds)
    camera_setSerial(arduino_motor)
    door_setSerial(arduino_motor)
    vibrate_setSerial(arduino_leds)
    weight_setSerial(arduino_leds)
    proximity_setSerial(arduino_leds)

    cameraIP = '192.168.4.19' # constant
    redisIP = configuration_params.rpi_ip
    redisPort = 6379

    redis_channel_TouchSensor = 'touchState' 
    redis_channel_DoorStatus = 'DoorStatus'
    redis_channel_CommandExec = 'CommandExec'
    redis_channel_WeightStatus = 'WeightStatus'
    redis_channel_ProximityStatus = 'ProximityStatus'
    redis_channel_itemOnScale = 'itemOnScale'

    try:
        redis_client = redis.Redis(host=redisIP , port= redisPort) 
        p = redis_client.pubsub()
        p.subscribe(redis_channel_CommandExec) 
    except Exception:
        print("Check redis server connection !")
        print("Your current attempt was to connect to " ,redisIP,":",redisPort)



    t1 = threading.Thread(target=thread_func_listenToSerial , args=(callback,arduino_leds,)) # listen serial LEDS
    
    t1.start()

    t2 = threading.Thread(target=thread_func_listenToSerial , args=(callback,arduino_motor,)) # listen serial MOTOR
    
    t2.start()


    app.run(debug=False,host='0.0.0.0',port=80)  # Run server

# from crypt import methods
from flask import Flask
import requests
from termcolor import colored
import threading
import redis 
import time 
import netifaces as ni

def getCupboardIP():
    try:
        r = requests.post('http://solertis.ics.forth.gr:4444/api/context/getAllHosts')
        hosts = r.json()
        for host in hosts:
            if host['name'] == 'SmartCupboard':
                return host['ip']
    except:
        print('Error: Could not get cupboard IP')
        print('Please check if VPN connection is established')

app = Flask(__name__)

rpi_IP = '139.91.96.156' # NEVER CHANGE THAT !  

print("RPI IP is : ",rpi_IP)

POST_dataToSend = {} # initialize dictionary / json
marios_laptop_ip = ni.ifaddresses('wlp3s0')[ni.AF_INET][0]['addr']
print("Marios laptop IP is : ",marios_laptop_ip)

redis_channel_TouchSensor = 'touchState' # change that maybe
redis_channel_ProximityStatus = 'ProximityStatus' # newline
redis_channel_itemOnScale = 'itemOnScale'

redisIP = rpi_IP # RANDOM -- mariosPC
redisPort = 6379
redis_client = redis.Redis(host=redisIP , port= redisPort)

p1 = redis_client.pubsub()
p1.subscribe(redis_channel_TouchSensor)

p2 = redis_client.pubsub()
p2.subscribe(redis_channel_ProximityStatus)

p3 = redis_client.pubsub()
p3.subscribe(redis_channel_itemOnScale)



def checkTypeTouch(): # 1.simple touch , 2.long touch , 3. double touch
    doubleTapFlag = False
    releaseTouch = False 
     
    start = time.time()
    timer_longTouch = 0 # initialize 
    
    while (timer_longTouch < 1): # Check in a 1 seconds period if exist a Release event 
        touch_message  = p1.get_message()
        
        if touch_message and isinstance(touch_message['data'], bytes): # if I have a new event => touch = 1 
            releaseTouch = True
            break

        stop = time.time()
        timer_longTouch = stop - start
    
    if not releaseTouch:
        return "longTouch"
    else:
        start2 = time.time()
        timer_doubleTouch = 0
        while(timer_doubleTouch < 1): # Check if exists a second touch event in a 1 second time period
            touch_message = p1.get_message()                    

            if touch_message and isinstance(touch_message['data'], bytes): # if I have a new event => touch = 0 
                doubleTapFlag = True
                break

            stop2 = time.time()
            timer_doubleTouch = stop2 - start2
        
        if doubleTapFlag:
            return "doubleTouch"
        else:
            return "simpleTouch"

def treadFunc_ProximityEvents(): # Proximity events

    while(True):

        proximity_message  = p2.get_message()

        if proximity_message and isinstance(proximity_message['data'], bytes):
            
            proximitySensorState = proximity_message['data']
            proximitySensorState = proximitySensorState.decode('utf-8')
            proximitySensorState = int(proximitySensorState.replace("\r\n",""))
            
            response_doorStatus = requests.post('http://' + rpi_IP + '/door/status') # get the door status 
            doorStatus = response_doorStatus.text

            doorStatus = doorStatus.replace("\r\n","")
            
            if doorStatus == "Opened" : # if it is open 

                if proximitySensorState == 0: # if door is touched
                    print(colored('Hand is close \n', 'green')) 
                    
                    requests.post('http://' + rpi_IP + '/vibrate/steady' , json={"vibrationDuration" : 4000 }) # vibrate steady for 1 seconds 
                else:
                    print(colored('No hand near \n', 'red'))

def treadFunc_TouchEvents(): # Touch events
    global learningFlag

    while(True):

        touch_message  = p1.get_message()

        if touch_message and isinstance(touch_message['data'], bytes) :
            touchSensorState = touch_message['data']
            touchSensorState = touchSensorState.decode('utf-8')
            touchSensorState = int(touchSensorState.replace("\r\n",""))
            
            if touchSensorState == 0: # if door is touched
                if learningFlag : 
                    print('The learning flag is : ' , learningFlag) 
                    requests.post('http://' + rpi_IP + '/lights/ConstantDoor' ,json={"color": "red"})
                    time.sleep(3)
                    requests.post('http://' + rpi_IP + '/lights/switchoff' ,json={"ledstripeId" : 0}) #then and switch off door lights !!! 

                else:
                    print(colored('Touching \n', 'green')) 
                    
                    touchType = checkTypeTouch() # newline here 
                    print("Touch type --> " , colored(touchType , "blue")) 

                    response_doorStatus = requests.post('http://' + rpi_IP + '/door/status') # get the door status 
                    doorStatus = response_doorStatus.text

                    doorStatus = doorStatus.replace("\r\n","")
                    
                    if doorStatus == "Opened" : # if it is open 
                        print("Closing ...")
                        requests.post('http://' + rpi_IP + '/lights/LedByLed' ,json={"reachLed": 22,"color": "blue","duration" : 500}) #then make efe on door lights 
                        requests.post('http://' + rpi_IP + '/door/close') # then close it ---------- CHANGE HERE !! 

                        time.sleep(2)
                        requests.post('http://' + rpi_IP + '/lights/switchoff' ,json={"ledstripeId" : 1}) #then and switch off inside lights !!! 

                    elif doorStatus == "Semi-opened": # if it is semi-open
                        if touchType == "simpleTouch" :
                            print("Opening ...")
                            requests.post('http://' + rpi_IP + '/lights/LedByLed' ,json={"reachLed": 22,"color": "blue","duration" : 500}) #then make efe on door lights 
                            requests.post('http://' + rpi_IP + '/door/open') # then open it

                        else:
                            print("Closing ...")
                            requests.post('http://' + rpi_IP + '/lights/LedByLed' ,json={"reachLed": 22,"color": "blue","duration" : 500}) #then make efe on door lights
                            requests.post('http://' + rpi_IP + '/door/close') # then close it 

                            print("wait 2 seconds")
                            time.sleep(2)
                            requests.post('http://' + rpi_IP + '/lights/switchoff' ,json={"ledstripeId" : 1}) #then and switch off inside lights !!! 


                    elif doorStatus == "Closed": # if it closed
                        if touchType == "simpleTouch":
                            print("opening ...")
                            requests.post('http://' + rpi_IP + '/lights/LedByLed' ,json={"reachLed": 22,"color": "blue","duration" : 500}) #then make efe on door lights 
                            requests.post('http://' + rpi_IP + '/door/open') # then open it

                        else:
                            print("Semi opening ...")
                            requests.post('http://' + rpi_IP + '/lights/LedByLed' ,json={"reachLed": 22,"color": "blue","duration" : 500}) #then make efe on door lights 
                            requests.post('http://' + rpi_IP + '/door/semiopen') # then open it 
                                                        

                    elif doorStatus == "Moving" : # Moving
                        print("Door is moving ...") 
                        print("Do nothing ... :) ")
                    else:
                        print("Some error...")
                        print("DoorStatus was : " , doorStatus) 
            else:
                print(colored('No Touch \n', 'red'))

def treadFunc_addOnScaleEvents(): # Scale
    while(True):

        scale_message  = p3.get_message()

        if scale_message and isinstance(scale_message['data'], bytes):
            
            scaleSensorState = scale_message['data']
            scaleSensorState = scaleSensorState.decode('utf-8')
            scaleSensorState = int(scaleSensorState.replace("\r\n",""))

            # DEMO CODE
            if scaleSensorState == 0: # if there is an item on scale
                print(colored('There is an item on scale \n', 'green')) 
                time.sleep(6)
                requests.post('http://'+ marios_laptop_ip  +':5001/train/Demo/Cupboard/fiveItems' , json={"cupboard_id" : 1})
                
                print("request train five items ok")

            else:
                print(colored('No item \n', 'red'))
                time.sleep(1)
                requests.post('http://' + marios_laptop_ip + ':5001/train/Demo/Cupboard/fourItems', json={"cupboard_id" : 1})
                
                print("request four items ok")
            # END OF DEMO CODE

if __name__ == '__main__':

    requests.post('http://' + rpi_IP + '/door/homing')

    learningFlag = False

    jsonFourItems = [ 
                {
                    'Label' : 'Mustard',
                    'Location_start' : 6,
                    'Location_end' : 12,
                    'Quantity' : 194,
                    'Cupboard' : 1,
                    'Shelf' : 'Up',
                    'Expiring' : 3,
                    'WhenLastUsed' : 1,
                    'UserLastUsed' : 'Asterios'
                },
                {
                    'Label' : 'Vinegar',
                    'Location_start' : 75,
                    'Location_end' : 85,
                    'Quantity' : 134,
                    'Cupboard' : 1,
                    'Shelf' : 'Bottom',
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
                    'Location_start' : 95,
                    'Location_end' : 105,
                    'Quantity' : 13,
                    'Cupboard' : 1,
                    'Shelf' : 'Bottom',
                    'Expiring' : 15,
                    'WhenLastUsed' : 1,
                    'UserLastUsed' : 'Antonis'
                },
                ]
    jsonFiveItems = [ 
                        {
                            'Label' : 'Mustard',
                            'Location_start' : 6,
                            'Location_end' : 12,
                            'Quantity' : 194,
                            'Cupboard' : 1,
                            'Shelf' : 'Up',
                            'Expiring' : 3,
                            'WhenLastUsed' : 1,
                            'UserLastUsed' : 'Asterios'
                        },
                        {
                            'Label' : 'Vinegar',
                            'Location_start' : 75,
                            'Location_end' : 85,
                            'Quantity' : 134,
                            'Cupboard' : 1,
                            'Shelf' : 'Bottom',
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
                            'Location_start' : 95,
                            'Location_end' : 105,
                            'Quantity' : 13,
                            'Cupboard' : 1,
                            'Shelf' : 'Bottom',
                            'Expiring' : 15,
                            'WhenLastUsed' : 1,
                            'UserLastUsed' : 'Antonis'
                        },
                        {
                            'Label' : 'Tomato',
                            'Location_start' : 40,
                            'Location_end' : 45,
                            'Quantity' : 400,
                            'Cupboard' : 1,
                            'Shelf' : 'Up',
                            'Expiring' : 15,
                            'WhenLastUsed' : 0,
                            'UserLastUsed' : 'Unused'
                        }
                        ]


    t1 = threading.Thread(target= treadFunc_TouchEvents)

    t1.start()

    t2 = threading.Thread(target= treadFunc_ProximityEvents)

    t2.start() 
    
    t3 = threading.Thread(target= treadFunc_addOnScaleEvents)
    t3.start()


    app.run(debug=False,host='0.0.0.0',port=5003) # Run by Marios PC 

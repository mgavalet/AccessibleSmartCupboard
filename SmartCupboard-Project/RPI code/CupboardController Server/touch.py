from flask import request
import redis 
import modulesCupboard
from subprocess import *
import configuration_params

def run_cmd(cmd):
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = str(p.communicate()[0])
        output = output[2 :-3]
        return output

def getTouchSensorState():
    return modulesCupboard.touchSensorState

redisIP = configuration_params.rpi_ip
print(redisIP)

redisPort = 6379

redis_channel_TouchSensor = 'touchState' # change that maybe
redis_client = redis.Redis(host=redisIP , port= redisPort) 


def touch_func(suburl=None):

    if request.method == 'POST': 
        if suburl == 'status':
            
            print("TouchSensorState is : " + str(getTouchSensorState())) 

            redis_client.publish(redis_channel_TouchSensor,str(getTouchSensorState()))             
            return str(modulesCupboard.touchSensorState)   #  The return type must be a string, dict, tuple, Response instance

        else :
            return "Wrong suburl in /touch/"
    return "Touch ok "

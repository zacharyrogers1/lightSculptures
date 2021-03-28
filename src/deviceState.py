from awsShadow.awsSetup import doAllAwsSetup
from animations.lightAnimations import *

import json

CONST_TIMEOUT = 5
CONST_baseReconnectQuietTimeSecond = 1
CONST_maxReconnectQuietTimeSecond = 32
CONST_stableConnectionTimeSecond = 20
QoS_Zero = 0
QoS_One = 1
QoS_Two = 2

def connectDeviceAndListenForDiff():
    (deviceShadowHandler, myAWSIoTMQTTShadowClient) = doAllAwsSetup()
    deviceShadowHandler.shadowRegisterDeltaCallback(shadowDeltaHandler)
    deviceStartup(deviceShadowHandler)

def shadowDeltaHandler(payload, responseStatus, token):
    payloadDict = json.loads(payload)["state"]
    print("The Delta issssss : ", payloadDict)
    


def deviceStartup(deviceShadowHandler):
    # deviceShadowHandler.shadowGet(srcCallback = customShadowCallback_Update, srcTimeout = 5)
    # On device startup the device should:
    # 1. Set its connected attribute in reported to true
    # 2. Perform a shadow get to see what the desired state of the device is.
    # 3. Pass the desired state of the device into the delta handler
    connectJSONDict = {
        "state": {
            "reported": {
                "connected": True
            }
        }
    }
    connectJSONString = json.dumps(connectJSONDict)
    deviceShadowHandler.shadowUpdate(
        connectJSONString, customShadowCallback_Update, CONST_TIMEOUT)
    # deviceShadowHandler.shadowGet(loadDesiredState, CONST_TIMEOUT)

def customShadowCallback_Update(payload, responseStatus, token):
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")
    if responseStatus == "accepted":
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print(payload)
        print("Update request with token: " + token + " accepted!")
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
    if responseStatus == "rejected":
        print("Update request " + token + " rejected!")

class StringLightsThing:
    num_pixels = 50

    def __init__(self, pixels):
        self.desiredState = {}
        self.pixels = pixels

    def runAnimation(self, activeAnimation):
        if(activeAnimation == 'unifiedRainbow'):
            unifiedRainbow(self.pixels, 0.2)
        elif(activeAnimation == 'pingPong'):
            pingPong(self.pixels, self.num_pixels, 0.1, (0, 0, 255))
        else:
            print('NO ACTIVE ANIMATION FOUND FOR: ', activeAnimation)
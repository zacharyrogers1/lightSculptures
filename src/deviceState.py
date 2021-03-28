from awsShadow.awsSetup import doAllAwsSetup
from animations.lightAnimations import *
import board
import neopixel

import json

CONST_TIMEOUT = 5
CONST_baseReconnectQuietTimeSecond = 1
CONST_maxReconnectQuietTimeSecond = 32
CONST_stableConnectionTimeSecond = 20
QoS_Zero = 0
QoS_One = 1
QoS_Two = 2


class StringLightsThing:
    num_pixels = 50
    reportedState = {
        "activeAnimation": "error",
    }
    deviceShadowHandler = None
    myAWSIoTMQTTShadowClient = None

    def __init__(self):
        self.desiredState = {}
        pixel_pin = board.D18
        num_pixels = 50
        ORDER = neopixel.GRB
        self.pixels = neopixel.NeoPixel(
            pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)

    def initializeHandlerAndAwsClient(self, handler, client):
        self.deviceShadowHandler = handler
        self.myAWSIoTMQTTShadowClient = client

    def updateReportedStateBasedOnDifferences(self, differenceDict):
        def dictLoopAndReplace(differenceDict, reportedDict):
            for key, value in differenceDict.items():
                if isinstance(value, dict):
                    dictLoopAndReplace(value, reportedDict[key])
                else:
                    reportedDict[key] = value
        dictLoopAndReplace(differenceDict, self.reportedState)
        self.updateReportedStateAfterSuccess()
    
    def updateReportedStateAfterSuccess(self):
        reportedJSONObj = {
            "state": {
                "reported": self.reportedState
            }
        }
        reportJson = json.dumps(reportedJSONObj)
        self.deviceShadowHandler.shadowUpdate(reportJson, customShadowCallback_Update, CONST_TIMEOUT)

    def runActiveAnimation(self):
        activeAnimation = self.reportedState["activeAnimation"]
        if(activeAnimation == 'error'):
            error(self.pixels)
        if(activeAnimation == 'countdown'):
            countdown(self.pixels, self.reportedState["animations"]["countdown"]["timeInSeconds"])
        elif(activeAnimation == 'pingPong'):
            colorTuple = tuple(self.reportedState["animations"]["pingPong"]["color"])
            pingPong(self.pixels, self.num_pixels, self.reportedState["animations"]["pingPong"]["speed"], colorTuple)
        elif(activeAnimation == 'unifiedRainbow'):
            unifiedRainbow(self.pixels, self.reportedState["animations"]["unifiedRainbow"]["speed"])
        elif(activeAnimation == 'chasingLights'):
            colorTuple = self.reportedState["animations"]["chasingLights"]["color"]
            chasingLights(self.pixels, self.num_pixels, self.reportedState["animations"]["chasingLights"]["numLitPixels"], colorTuple, self.reportedState["animations"]["chasingLights"]["speed"])
        else:
            print('NO ACTIVE ANIMATION FOUND FOR: ', activeAnimation)


singletonDevice = StringLightsThing()


def connectDeviceAndListenForDiff():
    (deviceShadowHandler, myAWSIoTMQTTShadowClient) = doAllAwsSetup()
    singletonDevice.initializeHandlerAndAwsClient(deviceShadowHandler, myAWSIoTMQTTShadowClient)
    deviceShadowHandler.shadowRegisterDeltaCallback(shadowDeltaHandler)
    deviceStartup(deviceShadowHandler)


def shadowDeltaHandler(payload, responseStatus, token):
    payloadDict = json.loads(payload)["state"]
    print("The Delta issssss : ", payloadDict)
    singletonDevice.updateReportedStateBasedOnDifferences(payloadDict)

def getActiveAnimationAndRun():
    singletonDevice.runActiveAnimation()


def deviceStartup(deviceShadowHandler):
    # deviceShadowHandler.shadowGet(srcCallback = customShadowCallback_Update, srcTimeout = 5)
    # On device startup the device should:
    # 1. Set its connected attribute in reported to true
    # 2. Perform a shadow get to see what the desired state of the device is.
    # 3. Pass the desired state of the device into the reported state
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
    deviceShadowHandler.shadowGet(loadDesiredState, CONST_TIMEOUT)

def loadDesiredState(payload, responseStatus, token):
    payloadDict = json.loads(payload)
    desiredPayloadDict = payloadDict["state"]["desired"]

    singletonDevice.reportedState = desiredPayloadDict


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

from awsShadow.awsSetup import doAllAwsSetup
from animations import lightAnimations
import board
import neopixel
import json
from rx import of, subject, operators
import time

CONST_TIMEOUT = 5
CONST_baseReconnectQuietTimeSecond = 1
CONST_maxReconnectQuietTimeSecond = 32
CONST_stableConnectionTimeSecond = 20
QoS_Zero = 0
QoS_One = 1
QoS_Two = 2

isAnimationActiveSubject = subject.BehaviorSubject(False)
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
        ORDER = neopixel.RGB
        self.pixels = neopixel.NeoPixel(
            pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)
        isAnimationActiveSubject.pipe(operators.delay(0.001)).subscribe(self.runAnimationWhenStopped)

    def initializeHandlerAndAwsClient(self, handler, client):
        self.deviceShadowHandler = handler
        self.myAWSIoTMQTTShadowClient = client

    def updateReportedStateBasedOnDifferences(self, overallDifferenceDict):
        def dictLoopAndReplace(subDifferenceDict, reportedDict):
            for key, value in subDifferenceDict.items():
                if isinstance(value, dict):
                    dictLoopAndReplace(value, reportedDict[key])
                else:
                    reportedDict[key] = value
        dictLoopAndReplace(overallDifferenceDict, self.reportedState)
        self.updateReportedStateAfterSuccess()
        isAnimationActiveSubject.on_next(False)
    
    def updateReportedStateAfterSuccess(self):
        reportedJSONObj = {
            "state": {
                "reported": self.reportedState
            }
        }
        reportJson = json.dumps(reportedJSONObj)
        self.deviceShadowHandler.shadowUpdate(reportJson, customShadowCallback_Update, CONST_TIMEOUT)

    def runAnimationWhenStopped(self, isAnimationActive):
        print("AlwaysChecking subscription: ", isAnimationActive)
        if(isAnimationActive == False):
            time.sleep(1)
            print("Always Checking subscription updating to True")
            isAnimationActiveSubject.on_next(True)
            self.runActiveAnimation()

    def runActiveAnimation(self):
        activeAnimation = self.reportedState["activeAnimation"]
        if(activeAnimation == 'error'):
            lightAnimations.error(self.pixels)
        elif(activeAnimation == 'countdown'):
            countdownSettings = self.reportedState["animations"]["countdown"]
            lightAnimations.countdown(self.pixels, countdownSettings["timeInSeconds"])
        elif(activeAnimation == 'pingPong'):
            pingPongSettings = self.reportedState["animations"]["pingPong"]
            lightAnimations.pingPong(self.pixels, self.num_pixels, pingPongSettings["speed"], pingPongSettings["color"])
        elif(activeAnimation == 'unifiedRainbow'):
            unifiedRainbowSettings = self.reportedState["animations"]["unifiedRainbow"]
            lightAnimations.unifiedRainbow(self.pixels, unifiedRainbowSettings["speed"], isAnimationActiveSubject)
        elif(activeAnimation == 'chasingLights'):
            chasingLightsSettings = self.reportedState["animations"]["chasingLights"]
            lightAnimations.chasingLights(self.pixels, self.num_pixels, chasingLightsSettings["numLitPixels"], chasingLightsSettings["color"], chasingLightsSettings["speed"])
        else:
            print('NO ACTIVE ANIMATION FOUND FOR: ', activeAnimation)


singletonDevice = StringLightsThing()


def connectDeviceAndListenForDiff():
    (deviceShadowHandler, myAWSIoTMQTTShadowClient) = doAllAwsSetup()
    singletonDevice.initializeHandlerAndAwsClient(deviceShadowHandler, myAWSIoTMQTTShadowClient)
    deviceStartup(deviceShadowHandler)
    deviceShadowHandler.shadowRegisterDeltaCallback(shadowDeltaHandler)


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

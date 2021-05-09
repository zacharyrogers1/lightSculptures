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

# isAnimationActiveSubject = subject.BehaviorSubject(False)
class StringLightsThing:
    num_pixels = 50
    reportedState = {
        "activeAnimation": "error",
    }
    deviceShadowHandler = None
    myAWSIoTMQTTShadowClient = None
    mqttConnection = None
    pixelPaintTopic = "stringLights/pixelPaint"

    def __init__(self):
        self.desiredState = {}
        pixel_pin = board.D18
        num_pixels = 50
        ORDER = neopixel.RGB
        self.pixels = neopixel.NeoPixel(
            pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER)
        # isAnimationActiveSubject.pipe(operators.delay(0.1)).subscribe(self.runAnimationWhenStopped)
    
    def deviceStartup(self):
        connectJSONDict = {
            "state": {
                "reported": {
                    "connected": True
                }
            }
        }
        connectJSONString = json.dumps(connectJSONDict)
        self.deviceShadowHandler.shadowUpdate(
            connectJSONString, None, CONST_TIMEOUT)
        self.deviceShadowHandler.shadowGet(self.loadDesiredState, CONST_TIMEOUT)
        # self.mqttConnection.subscribe(singletonDevice.pixelPaintTopic, 0, pixelPaintOnMessage)
        self.deviceShadowHandler.shadowRegisterDeltaCallback(shadowDeltaHandler)

    def initializeHandlerAndAwsClient(self, handler, client):
        self.deviceShadowHandler = handler
        self.myAWSIoTMQTTShadowClient = client
        self.mqttConnection = client.getMQTTConnection()

    def updateReportedStateBasedOnDifferences(self, overallDifferenceDict):
        def dictLoopAndReplace(subDifferenceDict, reportedDict):
            for key, value in subDifferenceDict.items():
                if isinstance(value, dict):
                    dictLoopAndReplace(value, reportedDict[key])
                else:
                    reportedDict[key] = value
        dictLoopAndReplace(overallDifferenceDict, self.reportedState)
        self.updateReportedStateAfterSuccess()
        print("INTERRUPT: Setting Subject False", isAnimationActiveSubject.observers.length())
        # isAnimationActiveSubject.on_next(False)
    
    def updateReportedStateAfterSuccess(self):
        reportedJSONObj = {
            "state": {
                "reported": self.reportedState
            }
        }
        reportJson = json.dumps(reportedJSONObj)
        self.deviceShadowHandler.shadowUpdate(reportJson, None, CONST_TIMEOUT)
    
    def loadDesiredState(self, payload, responseStatus, token):
        payloadDict = json.loads(payload)
        desiredPayloadDict = payloadDict["state"]["desired"]

        self.reportedState = desiredPayloadDict
        print("fetched Desired State ", self.reportedState)

    # def runAnimationWhenStopped(self, isAnimationActive):
    #     print("AlwaysChecking subscription: ", isAnimationActive)
    #     if(isAnimationActive == False):
    #         isAnimationActiveSubject.on_next(True)
    #         self.runActiveAnimation()

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
            lightAnimations.unifiedRainbow(self.pixels, unifiedRainbowSettings["speed"])
        elif(activeAnimation == 'chasingLights'):
            chasingLightsSettings = self.reportedState["animations"]["chasingLights"]
            lightAnimations.chasingLights(self.pixels, self.num_pixels, chasingLightsSettings["numLitPixels"], chasingLightsSettings["color"], chasingLightsSettings["speed"])
        else:
            print('NO ACTIVE ANIMATION FOUND FOR: ', activeAnimation)


singletonDevice = StringLightsThing()


def connectDeviceAndListenForDiff():
    (deviceShadowHandler, myAWSIoTMQTTShadowClient) = doAllAwsSetup()
    singletonDevice.initializeHandlerAndAwsClient(deviceShadowHandler, myAWSIoTMQTTShadowClient)
    singletonDevice.deviceStartup()

# def pixelPaintOnMessage(client, userdata, message):
#     print("Message from pixelPaint: ", message)
#     payloadDict = json.loads(message)["payload"]

def shadowDeltaHandler(payload, responseStatus, token):
    payloadDict = json.loads(payload)["state"]
    print("The Delta issssss : ", payloadDict)
    singletonDevice.updateReportedStateBasedOnDifferences(payloadDict)

def getActiveAnimationAndRun():
    singletonDevice.runActiveAnimation()



# def customShadowCallback_Update(payload, responseStatus, token):
#     return
#     # if responseStatus == "timeout":
#     #     print("Update request " + token + " time out!")
#     # if responseStatus == "accepted":
#     #     print("~~~~~~~~~~~~~~~~~~~~~~~")
#     #     print(payload)
#     #     print("Update request with token: " + token + " accepted!")
#     #     print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
#     # if responseStatus == "rejected":
#     #     print("Update request " + token + " rejected!")

# PIXEL PAINT LOGIC
# 1. The desired state is always being changed asynchronously by updates to device state
# 2. When updating desired state -> activeAnimation = "pixelPaint" keep activeAnimation always true and do not reset. Also fill the pixels with blank to start with a clean canvas.
# 3. Separately becuase we are subsribed to topic stringLights/pixelPaint we will get updates whenever it fires
#    During this callback check if the active animation is pixelPaint and then start running pixelPaint animation

from awsShadow.awsSetup import initialAwsSetup
from animations import lightAnimations, pixelPaint, twoDAnimations
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
    num_pixels = 400
    xAxisLength = 20
    reportedState = {
        "activeAnimation": "error",
    }
    deviceShadowHandler = None
    myAWSIoTMQTTShadowClient = None
    mqttConnection = None
    pixelPaintTopic = "stringLights/pixelPaint"
    pixelPaintUpdateList = []

    def __init__(self):
        self.desiredState = {}
        pixel_pin = board.D18
        ORDER = neopixel.RGB
        self.pixels = neopixel.NeoPixel(
            pixel_pin, self.num_pixels, auto_write=False, pixel_order=ORDER)
    
    def deviceStartup(self):
        self.awsInitialization()
        self.updatedConnectedState()
        self.listenForPixelPaintUpdate()

        self.deviceShadowHandler.shadowGet(self.loadDesiredState, CONST_TIMEOUT)
        self.deviceShadowHandler.shadowRegisterDeltaCallback(self.shadowDeltaHandler)

    def listenForPixelPaintUpdate(self):
        self.mqttConnection.subscribe(self.pixelPaintTopic, 0, self.pixelPaintOnMessage)
    
    def pixelPaintOnMessage(self, client, userdata, message):
        payload = message.payload.decode('UTF-8')
        pixelsToUpdate = json.loads(payload)["pixelPaint"]
        self.pixelPaintUpdateList.extend(pixelsToUpdate)
        print("Update list: ", self.pixelPaintUpdateList)
    
    def awsInitialization(self):
        (deviceShadowHandler, myAWSIoTMQTTShadowClient, mqttConnection) = initialAwsSetup()
        self.deviceShadowHandler = deviceShadowHandler
        self.myAWSIoTMQTTShadowClient = myAWSIoTMQTTShadowClient
        self.mqttConnection = mqttConnection
    
    def updatedConnectedState(self):
        connectJSONDict = {
            "state": {
                "reported": {
                    "connected": True,
                    "numPixels": self.num_pixels,
                    "xAxisLength": self.xAxisLength
                }
            }
        }
        connectJSONString = json.dumps(connectJSONDict)
        self.deviceShadowHandler.shadowUpdate(
            connectJSONString, None, CONST_TIMEOUT)

    def updateReportedStateBasedOnDifferences(self, overallDifferenceDict):
        def dictLoopAndReplace(subDifferenceDict, reportedDict):
            for key, value in subDifferenceDict.items():
                if isinstance(value, dict):
                    dictLoopAndReplace(value, reportedDict[key])
                else:
                    reportedDict[key] = value
        dictLoopAndReplace(overallDifferenceDict, self.reportedState)
        self.updateReportedStateAfterSuccess()

    def shadowDeltaHandler(self, payload, responseStatus, token):
        payloadDict = json.loads(payload)["state"]
        print("The Delta issssss : ", payloadDict)
        self.updateReportedStateBasedOnDifferences(payloadDict)
    
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

    def runActiveAnimation(self):
        activeAnimation = self.reportedState["activeAnimation"]
        self.pixels.brightness = self.reportedState["brightness"]
        if(activeAnimation == 'error'):
            lightAnimations.error(self.pixels)
        elif(activeAnimation == 'countdown'):
            countdownSettings = self.reportedState["animations"]["countdown"]
            lightAnimations.countdown(self.pixels, countdownSettings["timeInSeconds"])
        elif(activeAnimation == 'pingPong'):
            pingPongSettings = self.reportedState["animations"]["pingPong"]
            lightAnimations.pingPong(self.pixels, pingPongSettings["speed"], pingPongSettings["color"])
        elif(activeAnimation == 'unifiedRainbow'):
            unifiedRainbowSettings = self.reportedState["animations"]["unifiedRainbow"]
            lightAnimations.unifiedRainbow(self.pixels, unifiedRainbowSettings["speed"])
        elif(activeAnimation == 'twinkle'):
            twinkleSettings = self.reportedState["animations"]["twinkle"]
            lightAnimations.twinkle(self.pixels, twinkleSettings["speed"], twinkleSettings["color"])
        elif(activeAnimation == 'scanningStripe'):
            scanningStripeSettings = self.reportedState["animations"]["scanningStripe"]
            twoDAnimations.scanningStripe(self.pixels, self.xAxisLength, scanningStripeSettings["speed"], scanningStripeSettings["color"])
        elif(activeAnimation == 'chasingLights'):
            chasingLightsSettings = self.reportedState["animations"]["chasingLights"]
            lightAnimations.chasingLights(self.pixels, chasingLightsSettings["numLitPixels"], chasingLightsSettings["color"], chasingLightsSettings["speed"])
        elif(activeAnimation == 'pixelPaint'):
            pixelPaint.pixelPaint(self.pixels, self.xAxisLength, self.pixelPaintUpdateList)
        else:
            print('NO ACTIVE ANIMATION FOUND FOR: ', activeAnimation)


singletonDevice = StringLightsThing()

def connectDeviceAndListenForDiff():
    singletonDevice.deviceStartup()

def getActiveAnimationAndRun():
    singletonDevice.runActiveAnimation()

# PIXEL PAINT LOGIC
# 1. The desired state is always being changed asynchronously by updates to device state
# 2. When updating desired state -> activeAnimation = "pixelPaint" keep activeAnimation always true and do not reset. Also fill the pixels with blank to start with a clean canvas.
# 3. Separately becuase we are subsribed to topic stringLights/pixelPaint we will get updates whenever it fires
#    During this callback check if the active animation is pixelPaint and then start running pixelPaint animation

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
        color = self.reportedState["color"]
        speed = self.reportedState["speed"]
        self.pixels.brightness = self.reportedState["brightness"]
        if(activeAnimation == 'error'):
            lightAnimations.error(self.pixels)
        elif(activeAnimation == 'pingPong'):
            lightAnimations.pingPong(self.pixels, speed, color)
        elif(activeAnimation == 'unifiedRainbow'):
            lightAnimations.unifiedRainbow(self.pixels, speed)
        elif(activeAnimation == 'twinkle'):
            lightAnimations.twinkle(self.pixels, speed, color)
        elif(activeAnimation == 'scanningStripe'):
            twoDAnimations.scanningStripe(self.pixels, self.xAxisLength, speed, color)
        elif(activeAnimation == 'fillAndEmpty'):
            lightAnimations.fillAndEmpty(self.pixels,speed, color)
        elif(activeAnimation == 'chasingLights'):
            chasingLightsSettings = self.reportedState["animations"]["chasingLights"]
            lightAnimations.chasingLights(self.pixels, chasingLightsSettings["numLitPixels"], color, chasingLightsSettings["chaserCount"])
        elif(activeAnimation == 'static'):
            lightAnimations.static(self.pixels, color)
        elif(activeAnimation == 'movingRainbow'):
            twoDAnimations.movingRainbow(self.pixels, self.xAxisLength, speed)
        elif(activeAnimation == 'circle'):
            twoDAnimations.circle(self.pixels, self.xAxisLength, speed, color)
        elif(activeAnimation == 'rainbowCircle'):
            twoDAnimations.rainbowCircle(self.pixels, self.xAxisLength, speed)
        elif(activeAnimation == 'off'):
            lightAnimations.off(self.pixels)
        elif(activeAnimation == 'pixelPaint'):
            pixelPaint.pixelPaint(self.pixels, self.xAxisLength, self.pixelPaintUpdateList)
        else:
            lightAnimations.error(self.pixels)


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

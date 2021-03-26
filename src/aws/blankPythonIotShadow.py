from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging
import time
import json
import argparse
import datetime

CONST_TIMEOUT = 5
CONST_baseReconnectQuietTimeSecond = 1
CONST_maxReconnectQuietTimeSecond = 32
CONST_stableConnectionTimeSecond = 20
QoS_Zero = 0
QoS_One = 1
QoS_Two = 2



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


def shadowDeltaHandler(payload, responseStatus, token):
    payloadDict = json.loads(payload)["state"]
    print("The Delta issssss : ", payloadDict)


def deviceStartup():
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

def initialAwsSetup():
    myAWSIoTMQTTShadowClient = None
    host = "a1n8ytbh0zio90-ats.iot.us-east-1.amazonaws.com"
    rootCAPath = "certs/root-CA.crt"
    certificatePath = "certs/92183126a9-certificate.pem.crt"
    privateKeyPath = "certs/92183126a9-private.pem.key"
    port = 8883
    thingName = "stringLights"
    clientId = "AngryPresbyterianHouseWife"
    # lastWillTestamentTopic = "lastWillTestamentTopic"
    # lastWillTestamentMessage = {
    #     "state": {        
    #         "reported": {
    #             "connected": False,
    #             "schedule": None
    #         }
    #     }
    # }
    # lastWillTestamentMessageString = json.dumps(lastWillTestamentMessage)
    myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId)
    myAWSIoTMQTTShadowClient.configureEndpoint(host, port)
    myAWSIoTMQTTShadowClient.configureCredentials(
        rootCAPath, privateKeyPath, certificatePath)

    # AWSIoTMQTTShadowClient configuration
    myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(CONST_baseReconnectQuietTimeSecond, CONST_maxReconnectQuietTimeSecond, CONST_stableConnectionTimeSecond)
    myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)
    myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(CONST_TIMEOUT)

    # Configure Last Will and Testament in Case of disconnect
    # myAWSIoTMQTTShadowClient.configureLastWill(
    #     lastWillTestamentTopic, lastWillTestamentMessageString, QoS_Zero)

    # Connect to AWS IoT
    myAWSIoTMQTTShadowClient.connect()

    # Create a deviceShadow with persistent subscription
    deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(
        thingName, True)
    return (deviceShadowHandler, myAWSIoTMQTTShadowClient)

(deviceShadowHandler,myAWSIoTMQTTShadowClient) = initialAwsSetup()

# Listen on deltas
deviceShadowHandler.shadowRegisterDeltaCallback(shadowDeltaHandler)
deviceStartup()


# Loop forever
while True:
    time.sleep(CONST_TIMEOUT)
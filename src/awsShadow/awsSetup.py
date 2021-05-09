from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import time
import json
import os
dirname = os.path.dirname(__file__)

CONST_TIMEOUT = 5
CONST_baseReconnectQuietTimeSecond = 1
CONST_maxReconnectQuietTimeSecond = 32
CONST_stableConnectionTimeSecond = 20
QoS_Zero = 0
QoS_One = 1
QoS_Two = 2

def initialAwsSetup():
    myAWSIoTMQTTShadowClient = None
    host = "a1n8ytbh0zio90-ats.iot.us-east-1.amazonaws.com"
    rootCAPath = os.path.join(dirname,"certs/root-CA.crt")
    certificatePath = os.path.join(dirname,"certs/92183126a9-certificate.pem.crt")
    privateKeyPath = os.path.join(dirname,"certs/92183126a9-private.pem.key")
    port = 8883
    thingName = "stringLights"
    clientId = "AngryPresbyterianHouseWife"
    myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId)
    myAWSIoTMQTTShadowClient.configureEndpoint(host, port)
    myAWSIoTMQTTShadowClient.configureCredentials(
        rootCAPath, privateKeyPath, certificatePath)

    # AWSIoTMQTTShadowClient configuration
    myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(CONST_baseReconnectQuietTimeSecond, CONST_maxReconnectQuietTimeSecond, CONST_stableConnectionTimeSecond)
    myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)
    myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(CONST_TIMEOUT)

    # Connect to AWS IoT
    myAWSIoTMQTTShadowClient.connect()

    # Create handler and mqtt connection
    deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(
        thingName, True)
    mqttConnection = myAWSIoTMQTTShadowClient.getMQTTConnection()

    return (deviceShadowHandler, myAWSIoTMQTTShadowClient, mqttConnection)
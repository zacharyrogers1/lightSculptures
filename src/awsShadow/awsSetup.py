from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import time
import json

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
    rootCAPath = "certs/root-CA.crt"
    certificatePath = "certs/92183126a9-certificate.pem.crt"
    privateKeyPath = "certs/92183126a9-private.pem.key"
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

    # Create a deviceShadow with persistent subscription
    deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(
        thingName, True)
    return (deviceShadowHandler, myAWSIoTMQTTShadowClient)

def doAllAwsSetup():
    (deviceShadowHandler,myAWSIoTMQTTShadowClient) = initialAwsSetup()
    return (deviceShadowHandler, myAWSIoTMQTTShadowClient)
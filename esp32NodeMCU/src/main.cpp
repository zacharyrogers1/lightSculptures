#include <WiFiClientSecure.h>
#include <FastLED.h>
#include <MQTTClient.h>
#include <ArduinoJson.h>
#include "secrets.h"
#include "WiFi.h"

// The MQTT topics that this device should publish/subscribe
#define AWS_IOT_PUBLISH_TOPIC "$aws/things/stringLightsEsp32/shadow/name/defaultShadow/update"
#define AWS_IOT_SUBSCRIBE_TOPIC "$aws/things/stringLightsEsp32/shadow/name/defaultShadow/update/delta"

#define NUM_LEDS 400
#define DATA_PIN 27
#define CHIPSET WS2811Controller800Khz
#define BRIGHTNESS 128
#define COLOR_CORRECTION TypicalPixelString
#define ONBOARD_LED 2

CRGB leds[NUM_LEDS];

int msgReceived = 0;
String rcvdPayload;
char sndPayloadOff[512];
char sndPayloadOn[512];

WiFiClientSecure net = WiFiClientSecure();
MQTTClient client = MQTTClient(256);

void messageHandler(String &topic, String &payload)
{
    msgReceived = 1;
    rcvdPayload = payload;
}

void connectAWS()
{
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.println("");
    Serial.println("###################### Starting Execution ########################");
    Serial.println("Connecting to Wi-Fi");

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    // Configure WiFiClientSecure to use the AWS IoT device credentials
    net.setCACert(AWS_CERT_CA);
    net.setCertificate(AWS_CERT_CRT);
    net.setPrivateKey(AWS_CERT_PRIVATE);

    // Connect to the MQTT broker on the AWS endpoint we defined earlier
    client.begin(AWS_IOT_ENDPOINT, 8883, net);

    // Create a message handler
    client.onMessage(messageHandler);

    Serial.println("Connecting to AWS IOT");

    while (!client.connect(THINGNAME))
    {
        Serial.print(".");
        delay(100);
    }

    if (!client.connected())
    {
        Serial.println("AWS IoT Timeout!");
        return;
    }

    // Subscribe to a topic
    client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC);

    Serial.println("AWS IoT Connected!");
}

void setup()
{
    Serial.begin(115200);
    sprintf(sndPayloadOn, "{\"state\": { \"reported\": { \"status\": \"on\" } }}");
    sprintf(sndPayloadOff, "{\"state\": { \"reported\": { \"status\": \"off\" } }}");

    connectAWS();

    Serial.println("Setting Lamp Status to Off");
    client.publish(AWS_IOT_PUBLISH_TOPIC, sndPayloadOff);

    Serial.println("##############################################");
    FastLED.addLeds<CHIPSET, DATA_PIN, RGB>(leds, NUM_LEDS);
    FastLED.setBrightness(BRIGHTNESS);
    FastLED.setCorrection(COLOR_CORRECTION); // After some experimenting TypicalPixelString matches the white color correction best
}

void loop()
{
    if (msgReceived == 1)
    {
        //      This code will run whenever a message is received on the SUBSCRIBE_TOPIC_NAME Topic
        delay(100);
        msgReceived = 0;
        Serial.print("Received Message:");
        Serial.println(rcvdPayload);
        StaticJsonDocument<200> sensor_doc;
        DeserializationError error_sensor = deserializeJson(sensor_doc, rcvdPayload);
        const char *color = sensor_doc["state"]["color"];

        Serial.print("AWS Says: ");
        Serial.println(color);
        if (strcmp(color, "blue") == 0) // strcmp outputs 0 when the strings are equal 
        {
            Serial.println("Setting Blue");
            fill_solid(leds, NUM_LEDS, CRGB::Blue);
        }
        else if (strcmp(color, "red") == 0)
        {
            Serial.println("Setting Red");
            fill_solid(leds, NUM_LEDS, CRGB::Red);
        }
        else
        {
            fill_solid(leds, NUM_LEDS, CRGB::Green);
        }
        FastLED.show();
        // if(strcmp(sensor, "on") == 0)
        // {
        //  Serial.println("IF CONDITION");
        //  Serial.println("Turning Lamp On");
        //  digitalWrite(22, HIGH);
        //  client.publish(AWS_IOT_PUBLISH_TOPIC, sndPayloadOn);
        // }
        // else
        // {
        //  Serial.println("ELSE CONDITION");
        //  Serial.println("Turning Lamp Off");
        //  digitalWrite(22, LOW);
        //  client.publish(AWS_IOT_PUBLISH_TOPIC, sndPayloadOff);
        // }
        Serial.println("##############################################");
    }
    client.loop();
}
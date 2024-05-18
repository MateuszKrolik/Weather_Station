#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecureBearSSL.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

const char* ssid = "";
const char* password = "";

const char* serverName = "";

String apiKeyValue = "";
String sensorName = "BME280";
String sensorLocation = "Office";

Adafruit_BME280 bme;  // I2C Bus = SCL(Clock)->D1, SDA(Data)->D2

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);// 5 seconds
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

  bool status = bme.begin(0x76);// I2C sensor address 0x76
  if (!status) {
    Serial.println("Could not find a valid BME280 sensor, check wiring or change I2C address!");
    while (1);// halt program via infinite loop
  }
  
  Serial.println("Timer set to 30 seconds (timerDelay variable), it will take 30 seconds before publishing the first reading.");
}

void loop() {
  if(WiFi.status()== WL_CONNECTED){

    BearSSL::WiFiClientSecure client;

    client.setInsecure();// don't validate SSL cert
    
    HTTPClient https;
    
    https.begin(client, serverName);

    https.addHeader("Content-Type", "application/x-www-form-urlencoded");

    String httpRequestData = "api_key=" + apiKeyValue + "&sensor=" + sensorName
                          + "&location=" + sensorLocation + "&temperature=" + String(bme.readTemperature())
                          + "&humidity=" + String(bme.readHumidity()) + "&pressure=" + String(bme.readPressure()/100.0F) + "";
    Serial.print("httpRequestData: ");
    Serial.println(httpRequestData);

    int httpResponseCode = https.POST(httpRequestData);

    if (httpResponseCode>0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
    }
    else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
    https.end();// free up resources
  }
  else {
    Serial.println("WiFi Disconnected");
  }
  delay(30000);// 30 seconds
}
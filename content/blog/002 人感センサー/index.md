---
title: 人感センサーでデータを取得
date: "2021-07-01"
description: "ESP32とKP-IR612で、データ取得"
---

人感センサー"KP-IR612"(*1)とESP32で、人感データを取得してみる。

(*1)https://prod.kyohritsu.com/KP-IR612.html


##接続

こういう感じ

コードサンプル

```c 
#include <WiFi.h>
#include <ThingSpeak.h> // https://thingspeak.com/

//define your wifi access point here
#define WIFI_SSID "your wifi ssid code"
#define WIFI_PASS "your ssid password"

//define your ThingSpeak keys here
#define Channel_ID 9999999
#define Write_API_Key "YOUR_WRITEAPIKEY"

//define your device pin 
#define Sensor_Pin 13
#define LED_Pin 2

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println();

  // initialize digital pin sensorPin as an input.
  pinMode(Sensor_Pin, INPUT);

  // initialize digital pin ledPin as an output.
  pinMode(LED_Pin, OUTPUT);
  digitalWrite(LED_Pin, HIGH);
      
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WIFI_SSID);

  WiFi.begin(WIFI_SSID, WIFI_PASS);

  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  digitalWrite(LED_Pin, LOW);
}

void loop() {
  int count = 0;

  for (int i=0; i < 60; i++){

    if(digitalRead(Sensor_Pin)) {
      count++;
      Serial.print("count: ");
      Serial.println(count);
      digitalWrite(LED_Pin,HIGH);
      delay(1000); // delay a second
      digitalWrite(LED_Pin,LOW);
    } else {
      delay(1000); // delay a second
    }
  }
  if (count > 0) httpRequest(count);
}

void httpRequest(int field1Data) {
  // Initialize ThingSpeak
  WiFiClient client;
  ThingSpeak.begin(client);
 
  // Set the fields with the values
  ThingSpeak.setField(1, field1Data);

  // Write to the ThingSpeak channel
  int res = ThingSpeak.writeFields(Channel_ID, Write_API_Key);
  if (res == 200) {
    Serial.println("Channel update success.");
  } else{
    Serial.print("Channel update error: ");
    Serial.println(res);
  }
  client.stop();
}

```

参考にしたサイト：https://kghr.blog.fc2.com/blog-entry-160.html

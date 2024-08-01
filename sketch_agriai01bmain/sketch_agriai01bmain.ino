#include <WiFi.h>
#include <DHT.h>
#include <HTTPClient.h>

#define DHTPIN 4          // Digital pin connected to the DHT11 sensor
#define DHTTYPE DHT11     // DHT 11
#define SOIL_MOISTURE_PIN 34 // Analog pin for Soil Moisture Sensor

const char* ssid = "Kothiyal family-4G";
const char* password = "@beena1234";
const char* serverName = "http://192.168.29.172:5000/data"; // Flask server endpoint

DHT dht(DHTPIN, DHTTYPE);
void setup() {
  Serial.begin(115200);
  dht.begin();
  
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi...");
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  
  Serial.println("Connected to WiFi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Put your main code here, to run repeatedly
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  int soilMoisture = analogRead(SOIL_MOISTURE_PIN);
  
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Log the data to Serial
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.print(" °C, Humidity: ");
  Serial.print(humidity);
  Serial.print(" %, Soil Moisture: ");
  Serial.println(soilMoisture);

  // Send data to the Flask server
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    String jsonData = "{\"temperature\":" + String(temperature) + ",\"humidity\":" + String(humidity) + ",\"soilMoisture\":" + String(soilMoisture) + "}";
    int httpResponseCode = http.POST(jsonData);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  }

  delay(2000); // Wait 2 seconds before sending the next data
}

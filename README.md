# AgriAI Streamlit web Application

## Idea Brief

The proposed solution is an innovative mobile application designed to empower smallholder farmers with data-driven insights, optimizing their farming practices, increasing crop yields, and building resilience to climate change. By integrating IoT sensors, satellite imagery, weather data, and advanced analytics, the app provides actionable recommendations for crop selection, irrigation, fertilizer management, pest and disease control, and market intelligence. This comprehensive approach addresses the core challenges faced by smallholder farmers, enabling them to make informed decisions and improve their agricultural productivity sustainably.

## Sensors We Used

- **Soil Moisture Sensor**
- **DHT11 Sensor** (for humidity and temperature)
- **ESP32 Module**
- **Jumper Wires**
- **USB Cable**

### Setup Instructions

1. **Hardware Setup**:
   - Connect the soil moisture sensor to the ESP32 module.
   - Connect the DHT11 sensor to the ESP32 module.
   - Use jumper wires for connections.
   - Connect the ESP32 module to your computer using a USB cable.

2. **Arduino Code**:
   - Open the Arduino IDE.
   - Load the provided Arduino sketch file: `sketch_agriai01bmain.ino`.
   - Upload the code to the ESP32 module.

### Running the Code

1. **Clone the Repository**:
   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Run Flask API**:
   ```sh
   python server_esp.py
   ```

3. **Run Streamlit App**:
   ```sh
   streamlit run app.py
   ```
   Make sure you have set your weather API key in the necessary configuration files.

## Conclusion

Once the setup is complete and the code is running, you will get real-time data and crop recommendations displayed on the Streamlit app. This information will help farmers make informed decisions to enhance their agricultural productivity and sustainability.


---

**Happy Farming!** 🌾

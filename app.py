

import streamlit as st
from utils import pred_crop, pred_rainfall, pred_temp_hum
import streamlit as st
import requests
import time
import json
import plotly.graph_objects as go
from datetime import datetime
from utils import pred_crop, pred_rainfall, pred_temp_hum

# Define the URLs of the server endpoint and weather API
server_url = "http://localhost:5000/latest"
weather_api_url = "https://api.openweathermap.org/data/2.5/weather?"
forecast_api_url = "https://api.openweathermap.org/data/2.5/forecast?"
api_key = "Your_api_key_use_from_openweathermap"
lat = "28.9600661"  # Example latitude
lon = "77.7348613"  # Example longitude

def fetch_sensor_data():
    try:
        response = requests.get(server_url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        return data
    except Exception as e:
        st.write("Error fetching sensor data:", e)
        return {}

# Function to fetch current weather data from OpenWeatherMap API
def fetch_weather_data():
    complete_url = f"{weather_api_url}lat={lat}&lon={lon}&appid={api_key}&units=metric"
    try:
        response = requests.get(complete_url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        return data
    except Exception as e:
        st.write("Error fetching weather data:", e)
        return {}

# Function to fetch 5-day weather forecast from OpenWeatherMap API
def fetch_forecast_data():
    complete_url = f"{forecast_api_url}lat={lat}&lon={lon}&appid={api_key}&units=metric"
    try:
        response = requests.get(complete_url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        return data
    except Exception as e:
        st.write("Error fetching forecast data:", e)
        return {}

# Function to analyze the data and provide insights
def analyze_data(sensor_data):
    temperature = sensor_data.get("temperature")
    humidity = sensor_data.get("humidity")
    soil_moisture = sensor_data.get("soilMoisture")

    if temperature is None or humidity is None or soil_moisture is None:
        return ["Incomplete data."]

    insights = []
    # Irrigation management
    if humidity > 60.0 and (20.0 <= temperature <= 30.0):
        insights.append("High Humidity & Optimal Temperature: Less frequent irrigation may be needed.")
    elif humidity < 40.0 and temperature > 30.0:
        insights.append("Low Humidity & High Temperature: Increase irrigation to prevent water stress and ensure the crops have enough moisture.")

    # Crop health monitoring
    if temperature > 35.0 and humidity < 40.0:
        insights.append("High Temperature & Low Humidity: Heat stress can cause wilting or reduced growth. Additional irrigation or shade might be necessary.")
    elif 20.0 <= temperature <= 30.0 and 40.0 <= humidity <= 60.0:
        insights.append("Consistent Optimal Conditions: The plants are in a healthy environment.")

    # Disease prevention
    if humidity > 80.0:
        insights.append("High Humidity: Monitor and possibly adjust watering schedules to prevent diseases.")
    elif humidity < 20.0:
        insights.append("Low Humidity: While generally less problematic, it might affect some plant species that require more moisture in the air.")

    # Pest management
    if humidity > 70.0 and temperature > 30.0:
        insights.append("High Humidity & Temperature: These conditions can attract pests. Appropriate pest control measures may need to be taken.")

    # Climate control
    insights.append("Climate Control: Continuous monitoring helps in understanding microclimatic conditions of the field. Plan and implement climate control measures like installing windbreaks, shade nets, or adjusting planting schedules.")

    # Water conservation
    if humidity > 60.0 and temperature < 25.0:
        insights.append("Efficient Use of Water: Monitor the data to optimize water use, ensuring that water is only applied when necessary, conserving water resources.")

    return insights

# Function to display the data and insights
def display_data():
    sensor_data = st.session_state.get("sensor_data", {})
    weather_data = st.session_state.get("weather_data", {})
    forecast_data = st.session_state.get("forecast_data", {})

    st.write(f"### Welcome sohan, check your real time dashboard")

    # Sensor Data
    temp = sensor_data.get("temperature", "N/A")
    humidity = sensor_data.get("humidity", "N/A")
    soil_moisture = sensor_data.get("soilMoisture", "N/A")

    st.markdown("<h4>Sensor Data</h4>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div style="background-color: #f0f0f5; padding: 10px; border-radius: 10px; margin: 10px;">'
                    '<h5 style="color: #0066cc;">🌡️ Temperature</h5>'
                    f'<h3>{temp} °C</h3></div>', unsafe_allow_html=True)
    # temp
    with col2:
        st.markdown('<div style="background-color: #f0f0f5; padding: 10px; border-radius: 10px; margin: 10px;">'
                    '<h5 style="color: #0066cc;"><i class="fa fa-tint"></i>💧 Humidity</h5>'
                    f'<h3>{humidity} %</h3></div>', unsafe_allow_html=True)
        # humidity
    with col3:
        st.markdown('<div style="background-color: #f0f0f5; padding: 10px; border-radius: 10px; margin: 10px;">'
                    '<h5 style="color: #0066cc;"><i class="fa fa-leaf"></i>🌱 Soil Moisture</h5>'
                    f'<h3>{soil_moisture}</h3></div>', unsafe_allow_html=True)
    # soil_moisture
    # Weather Data
    st.write("#### Weather Data")
    weather_city = weather_data.get("name", "N/A")
    weather_country = weather_data.get("sys", {}).get("country", "N/A")
    weather_lat = weather_data.get("coord", {}).get("lat", "N/A")
    weather_lon = weather_data.get("coord", {}).get("lon", "N/A")
    weather_temp = weather_data.get("main", {}).get("temp", "N/A")
    weather_feels_like = weather_data.get("main", {}).get("feels_like", "N/A")
    weather_temp_min = weather_data.get("main", {}).get("temp_min", "N/A")
    weather_temp_max = weather_data.get("main", {}).get("temp_max", "N/A")
    weather_pressure = weather_data.get("main", {}).get("pressure", "N/A")
    weather_humidity = weather_data.get("main", {}).get("humidity", "N/A")
    weather_desc = weather_data.get("weather", [{}])[0].get("description", "N/A")
    weather_wind_speed = weather_data.get("wind", {}).get("speed", "N/A")
    weather_wind_deg = weather_data.get("wind", {}).get("deg", "N/A")
    weather_rain_1h = weather_data.get("rain", {}).get("1h", "N/A")
    weather_clouds = weather_data.get("clouds", {}).get("all", "N/A")
    weather_visibility = weather_data.get("visibility", "N/A")
    weather_sunrise = weather_data.get("sys", {}).get("sunrise", "N/A")
    weather_sunset = weather_data.get("sys", {}).get("sunset", "N/A")
    weather_timezone = weather_data.get("timezone", "N/A")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div style="background-color: #f0f0f5; padding: 10px; border-radius: 10px; margin: 10px;">'
                    '<h5 style="color: #0066cc;"><i class="fa fa-map-marker"></i> City</h5>'
                    f'<h3>{weather_city}</h3></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="background-color: #f0f0f5; padding: 10px; border-radius: 10px; margin: 10px;">'
                    '<h5 style="color: #0066cc;"><i class="fa fa-flag"></i> Country</h5>'
                    f'<h3>{weather_country}</h3></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div style="background-color: #f0f0f5; padding: 10px; border-radius: 10px; margin: 10px;">'
                    '<h5 style="color: #0066cc;"><i class="fa fa-globe"></i> Coordinates</h5>'
                    f'<h3>Lat: {weather_lat} | Lon: {weather_lon}</h3></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div style="background-color: #f0f0f5; padding: 10px; border-radius: 10px; margin: 10px;">'
                    '<h5 style="color: #0066cc;">🌡️ Temperature</h5>'
                    f'<h3>{weather_temp} °C</h3>'
                    f'<h5>Feels Like: {weather_feels_like} °C</h5></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="background-color: #f0f0f5; padding: 10px; border-radius: 10px; margin: 10px;">'
                    '<h5 style="color: #0066cc;">Pressure</h5>'
                    f'<h3>{weather_pressure} hPa</h3>'
                    f'<h5>Humidity: {weather_humidity} %</h5></div>', unsafe_allow_html=True)

    st.markdown('<div style="background-color: #f0f0f5; padding: 10px; border-radius: 10px; margin: 10px;">'
                '<h5 style="color: #0066cc;">Weather Description</h5>'
                f'<h3>{weather_desc}</h3>'
                f'<h5>Wind Speed: {weather_wind_speed} m/s | Direction: {weather_wind_deg}°</h5>'
                f'<h5>Rain (1h): {weather_rain_1h} mm</h5>'
                f'<h5>Cloud Cover: {weather_clouds} %</h5>'
                f'<h5>Visibility: {weather_visibility} m</h5>'
                f'<h5>Sunrise: {datetime.fromtimestamp(weather_sunrise).strftime("%H:%M:%S")} | Sunset: {datetime.fromtimestamp(weather_sunset).strftime("%H:%M:%S")}</h5>'
                f'<h5>Timezone: {weather_timezone}</h5></div>', unsafe_allow_html=True)

    # 5-Day Forecast
    forecast_option = st.selectbox("Select a day for 5-day forecast", ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"])
    forecast_day_index = {"Day 1": 0, "Day 2": 8, "Day 3": 16, "Day 4": 24, "Day 5": 32}.get(forecast_option, 0)

    if forecast_data:
        forecast_list = forecast_data.get("list", [])
        if len(forecast_list) > forecast_day_index:
            forecast = forecast_list[forecast_day_index]
            forecast_temp = forecast.get("main", {}).get("temp", "N/A")
            forecast_feels_like = forecast.get("main", {}).get("feels_like", "N/A")
            forecast_pressure = forecast.get("main", {}).get("pressure", "N/A")
            forecast_humidity = forecast.get("main", {}).get("humidity", "N/A")
            forecast_desc = forecast.get("weather", [{}])[0].get("description", "N/A")
            forecast_wind_speed = forecast.get("wind", {}).get("speed", "N/A")
            forecast_wind_deg = forecast.get("wind", {}).get("deg", "N/A")
            forecast_rain = forecast.get("rain", {}).get("3h", "N/A")
            forecast_clouds = forecast.get("clouds", {}).get("all", "N/A")

            st.markdown(f"### Forecast for {forecast_option}")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div style="background-color: #f0f0f5; padding: 10px; border-radius: 10px; margin: 10px;">'
                            '<h5 style="color: #0066cc;">🌡️ Temperature</h5>'
                            f'<h3>{forecast_temp} °C</h3>'
                            f'<h5>Feels Like: {forecast_feels_like} °C</h5></div>', unsafe_allow_html=True)
            with col2:
                st.markdown('<div style="background-color: #f0f0f5; padding: 10px; border-radius: 10px; margin: 10px;">'
                            '<h5 style="color: #0066cc;">Pressure</h5>'
                            f'<h3>{forecast_pressure} hPa</h3>'
                            f'<h5>Humidity: {forecast_humidity} %</h5></div>', unsafe_allow_html=True)

            st.markdown('<div style="background-color: #f0f0f5; padding: 10px; border-radius: 10px; margin: 10px;">'
                        '<h5 style="color: #0066cc;">Weather Description</h5>'
                        f'<h3>{forecast_desc}</h3>'
                        f'<h5>Wind Speed: {forecast_wind_speed} m/s | Direction: {forecast_wind_deg}°</h5>'
                        f'<h5>Rain (3h): {forecast_rain} mm</h5>'
                        f'<h5>Cloud Cover: {forecast_clouds} %</h5></div>', unsafe_allow_html=True)
            # Forecast Data
            st.write("#### 5-Day Weather Forecast")
            forecast_data_list = forecast_data.get("list", [])

            dates = []
            temperatures = []

            for forecast in forecast_data_list:
                date = datetime.strptime(forecast.get("dt_txt", ""), "%Y-%m-%d %H:%M:%S")
                temperature = forecast.get("main", {}).get("temp")
                dates.append(date)
                temperatures.append(temperature)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=temperatures, mode="lines", name="Temperature"))
            fig.update_layout(
                title="5-Day Temperature Forecast",
                xaxis_title="Date",
                yaxis_title="Temperature (°C)"
            )

            st.plotly_chart(fig)

# Function to display the data and insights
# def display_data():
#     sensor_data = st.session_state.get("sensor_data", {})
#     weather_data = st.session_state.get("weather_data", {})
#     forecast_data = st.session_state.get("forecast_data", {})
#
#     st.write(f"### Welcome sohan, check your real time dashboard")
#
#     # Sensor Data
#     temp = sensor_data.get("temperature", "N/A")
#     humidity = sensor_data.get("humidity", "N/A")
#     soil_moisture = sensor_data.get("soilMoisture", "N/A")
#
#     st.markdown("<h4>Sensor Data</h4>", unsafe_allow_html=True)
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.markdown('<div style="background-color: #f0f0f5; padding: 10px; border-radius: 10px; margin: 10px;">'
#                     '<h5 style="color: #0066cc;">🌡️ Temperature</h5>'
#                     f'<h3>{temp} °C</h3></div>', unsafe_allow_html=True)
#
#     with col2:
#         st.markdown('<div style="background-color: #f0f0f5; padding: 10px; border-radius: 10px; margin: 10px;">'
#                     '<h5 style="color: #0066cc;"><i class="fa fa-tint"></i>💧 Humidity</h5>'
#                     f'<h3>{humidity} %</h3></div>', unsafe_allow_html=True)
#     with col3:
#         st.markdown('<div style="background-color: #f0f0f5; padding: 10px; border-radius: 10px; margin: 10px;">'
#                     '<h5 style="color: #0066cc;"><i class="fa fa-leaf"></i>🌱 Soil Moisture</h5>'
#                     f'<h3>{soil_moisture}</h3></div>', unsafe_allow_html=True)
#
#     # Weather Data
#     st.write("#### Weather Data")
#     weather_city = weather_data.get("name", "N/A")
#     weather_country = weather_data.get("sys", {}).get("country", "N/A")
#     weather_lat = weather_data.get("coord", {}).get("lat", "N/A")
#     weather_lon = weather_data.get("coord", {}).get("lon", "N/A")
#     weather_temp = weather_data.get("main", {}).get("temp", "N/A")
#     weather_feels_like = weather_data.get("main", {}).get("feels_like", "N/A")
#     weather_temp_min = weather_data.get("main", {}).get("temp_min", "N/A")
#     weather_temp_max = weather_data.get("main", {}).get("temp_max", "N/A")
#     weather_pressure = weather_data.get("main", {}).get("pressure", "N/A")
#     weather_humidity = weather_data.get("main", {}).get("humidity", "N/A")
#     weather_desc = weather_data.get("weather", [{}])[0].get("description", "N/A")
#     weather_wind_speed = weather_data.get("wind", {}).get("speed", "N/A")
#     weather_wind_deg = weather_data.get("wind", {}).get("deg", "N/A")
#     weather_rain_1h = weather_data.get("rain", {}).get("1h", "N/A")
#     weather_clouds = weather_data.get("clouds", {}).get("all", "N/A")
#     weather_visibility = weather_data.get("visibility", "N/A")
#     weather_sunrise = weather_data.get("sys", {}).get("sunrise", "N/A")
#     weather_sunset = weather_data.get("sys", {}).get("sunset", "N/A")
#     weather_timezone = weather_data.get("timezone", "N/A")
#
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.markdown('<div style="background-color: #f0f0f5; padding: 10px; border-radius: 10px; margin: 10px;">'
#                     '<h5 style="color: #0066cc;"><i class="fa fa-map-marker"></i> City</h5>'
#                     f'<h3>{weather_city}</h3></div>', unsafe_allow_html=True)
#     with col2:
#         st.markdown('<div style="background-color: #f0f0f5; padding: 10px; border-radius: 10px; margin: 10px;">'
#                     '<h5 style="color: #0066cc;"><i class="fa fa-flag"></i> Country</h5>'
#                     f'<h3>{weather_country}</h3></div>', unsafe_allow_html=True)
#     with col3:
#         st.markdown('<div style="background-color: #f0f0f5; padding: 10px; border-radius: 10px; margin: 10px;">'
#                     '<h5 style="color: #0066cc;"><i class="fa fa-globe"></i> Coordinates</h5>'
#                     f'<h3>{weather_lat}, {weather_lon}</h3></div>', unsafe_allow_html=True)
#
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.markdown('<div style="background-color: #f0f0f5; padding: 10px; border-radius: 10px; margin: 10px;">'
#                     '<h5 style="color: #0066cc;"><i class="fa fa-thermometer-half"></i> Temperature</h5>'
#                     f'<h3>{weather_temp} °C</h3></div>', unsafe_allow_html=True)
#     with col2:
#         st.markdown('<div style="background-color: #f0f0f5; padding: 10px; border-radius: 10px; margin: 10px;">'
#                     '<h5 style="color: #0066cc;"><i class="fa fa-tint"></i> Humidity</h5>'
#                     f'<h3>{weather_humidity} %</h3></div>', unsafe_allow_html=True)
#     with col3:
#         st.markdown('<div style="background-color: #f0f0f5; padding: 10px; border-radius: 10px; margin: 10px;">'
#                     '<h5 style="color: #0066cc;"><i class="fa fa-wind"></i> Wind Speed</h5>'
#                     f'<h3>{weather_wind_speed} m/s</h3></div>', unsafe_allow_html=True)
#
#     # Forecast Data
#     st.write("#### 5-Day Weather Forecast")
#     forecast_data_list = forecast_data.get("list", [])
#
#     dates = []
#     temperatures = []
#
#     for forecast in forecast_data_list:
#         date = datetime.strptime(forecast.get("dt_txt", ""), "%Y-%m-%d %H:%M:%S")
#         temperature = forecast.get("main", {}).get("temp")
#         dates.append(date)
#         temperatures.append(temperature)
#
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=dates, y=temperatures, mode="lines", name="Temperature"))
#     fig.update_layout(
#         title="5-Day Temperature Forecast",
#         xaxis_title="Date",
#         yaxis_title="Temperature (°C)"
#     )
#
#     st.plotly_chart(fig)
#
#     # Generate and display insights
#     insights = analyze_data(sensor_data)
#     st.write("### Data Insights")
#     for insight in insights:
#         st.markdown(f"* {insight}")

# Function to display the Crop Prediction page
def display_crop_prediction():
    # Streamlit setup
    st.title("Crop Prediction")
    st.write("Enter the details to predict the suitable crop.")

    # Inputs
    nitrogen = st.number_input("Nitrogen content of the soil:", min_value=0.0, format="%.2f")
    phosphorous = st.number_input("Phosphorous content of the soil:", min_value=0.0, format="%.2f")
    potassium = st.number_input("Potassium content of the soil:", min_value=0.0, format="%.2f")
    ph = st.number_input("pH of the soil:", min_value=0.0, format="%.2f")

    # Dropdowns for state, district, and month
    states = ["ANDHRA PRADESH", "ARUNACHAL PRADESH", "ASSAM", "BIHAR", "CHHATTISGARH", "GOA", "GUJARAT", "HARYANA", "HIMACHAL PRADESH", "JAMMU AND KASHMIR", "JHARKHAND", "KARNATAKA", "KERALA", "MADHYA PRADESH", "MAHARASHTRA", "MANIPUR", "MEGHALAYA", "MIZORAM", "NAGALAND", "ODISHA", "PUNJAB", "RAJASTHAN", "SIKKIM", "TAMIL NADU", "TRIPURA", "UTTARANCHAL", "UTTAR PRADESH", "WEST BENGAL", "ANDAMAN AND NICOBAR ISLANDS", "CHANDIGARH", "DADAR NAGAR HAVELI", "DAMAN AND DUI", "DELHI", "LAKSHADWEEP", "PONDICHERRY"]
    state = st.selectbox("State", states)

    districts = {
        "ANDHRA PRADESH": ["EAST GODAVARI", "WEST GODAVARI", "GUNTUR", "KRISHNA", "NELLORE", "PRAKASAM", "SRIKAKULAM", "VISAKHAPATNAM", "VIZIANAGARAM", "ANANTAPUR", "CHITTOOR", "KURNOOL", "CUDDAPAH", "KADAPA"],
        "ARUNACHAL PRADESH": ["ANJAW", "CHANGLANG", "DIBANG VALLEY", "EAST KAMENG", "EAST SIANG", "KRA DADAR NAGAR HAVELI", "LOHIT", "LONGDING", "LOWER DIBANG VALLEY", "LOWER SUBANSIRI", "NAMSAI", "PAPUM PARE", "SIANG", "TAWANG", "TIRAP", "UPPER SIANG", "UPPER SUBANSIRI", "WEST KAMENG", "WEST SIANG"],
        # Add other states and districts here
    }
    district = st.selectbox("District", districts.get(state, []))

    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    month = st.selectbox("Month", months)

    # Predict button
    if st.button("Predict"):
        data = {
            "nitrogen": nitrogen,
            "phosphorous": phosphorous,
            "potassium": potassium,
            "ph": ph,
            "state": state,
            "district": district,
            "month": month
        }
        try:
            rainfall = pred_rainfall.get_rainfall(state, district, month)
            temperature, humidity = pred_temp_hum.get_temp_hum(district)

            prediction = pred_crop.predict_crop(
                nitrogen, phosphorous, potassium, temperature, humidity, ph, rainfall)
            st.success(f"Suitable crop for now is : {prediction[0]}")
        except Exception as e:
            st.error(f"Error: {str(e)}")



# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ("Home", "Crop Prediction"))

# Load data once when the app starts
if "sensor_data" not in st.session_state:
    st.session_state["sensor_data"] = fetch_sensor_data()
if "weather_data" not in st.session_state:
    st.session_state["weather_data"] = fetch_weather_data()
if "forecast_data" not in st.session_state:
    st.session_state["forecast_data"] = fetch_forecast_data()

# Show the selected page
if page == "Home":
    display_data()
elif page == "Crop Prediction":
    display_crop_prediction()

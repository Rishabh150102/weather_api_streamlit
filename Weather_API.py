import requests
import streamlit as st
import plotly.express as px


st.set_page_config(layout="wide")

with st.container(border=True):
  latitude = 26.0100
  longitude = 80.4221

  def fetch_weather_forecast():
      url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relativehumidity_2m,precipitation"
      response = requests.get(url)
      data = response.json()
      return (data['hourly']['time'], 
              data['hourly']['temperature_2m'], 
              data['hourly']['relativehumidity_2m'], 
              data['hourly']['precipitation'])

  # Fetch data
  time_data, temperature_data, humidity_data, precipitation_data = fetch_weather_forecast()

  # Create the charts
  fig_temp = px.line(x=time_data, y=temperature_data, title='Temperature Forecast')
  fig_humidity = px.line(x=time_data, y=humidity_data, title='Relative Humidity Forecast (%)')
  fig_rain = px.bar(x=time_data, y=precipitation_data, title='Precipitation Forecast (mm)')

  # Display in Streamlit (using tabs for better organization)
  tab1, tab2, tab3 = st.tabs(["Temperature", "Humidity", "Rain"])

  with tab1:
      st.plotly_chart(fig_temp)

  with tab2:
      st.plotly_chart(fig_humidity)

  with tab3:
      st.plotly_chart(fig_rain)

# Display Current Temprature (MAIN)   
      
def get_current_temperature():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"  
    response = requests.get(url)
    data = response.json()

    if 'current_weather' in data:
        return data['current_weather']['temperature']
    else:
        return None

with st.container(border=True):
   # Get the current temperature
  current_temperature = get_current_temperature()

  if current_temperature is not None:
      st.subheader("Current Temperature")
      st.metric("", f"{current_temperature}°C") 
      if current_temperature > 0:
         progress_bar_value = current_temperature / 60
         st.progress(progress_bar_value)
  else:
      st.warning("Unable to fetch current temperature data.")
import streamlit as st
from datetime import datetime
import requests
import openai
from apikey import openai_api_key, weather_api_key

# Function to get data from OpenWeatherMap
def get_weather_data(city, weather_api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    complete_url = base_url + "?q=" + city + "&APPID=" + weather_api_key
    response = requests.get(complete_url)
    return response.json()

# Function to generate a weather description using OpenAI's GPT model
def genrate_weather_description(data, open_api_key):
    # openai_api_key = openai_api_key

    try:
        # Convert temperature from Kelvin to Celsius
        temperature = data['main']['temp'] - 273.15 # Convert Kelvin to Celsius
        description = data['weather'][0]['description']
        prompt = f"La météo actuelle de votre ville {description} avec une température de {temperature: .1f} °C."

        response = openai.completions.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=60
        )
        return response.choices[0].text.strip()
    
    except Exception as e:
        return str(e)

# Weekly weather function
def get_weekly_forcast(weather_api_key, lat, lon):
    base_url = "https://api.openweathermap.org/data/2.5/"
    complete_url = f"{base_url}forecast?lat={lat}&lon={lon}&APPID={weather_api_key}"
    response = requests.get(complete_url)
    return response.json()

# Function to lunch streamlit app
def main():
    # Sidebar configuration
    st.sidebar.title("Infos météo")
    city = st.sidebar.text_input("Entrez le nom de la ville", "Brest")

    # # API keys
    # weather_api_key = "" # Replace with your own OpenWeatherMap API Key 
    # open_api_key = "" # Replace with your own OpanAI API Key

    # Button to fetch and display weather data
    submit  = st.sidebar.button("Afficher la météo")
    dateTime = datetime.now()

    if submit:
        st.title("Heure : " + str(dateTime))
        st.title("La météo à " + city + " : ")
        with st.spinner('Chargement des informations ...'):
            weather_data = get_weather_data(city, weather_api_key)
            print (weather_data)

            # Check if yhe city was found and diplay the weather data
            if weather_data.get("cod") != 404:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Température", f"{weather_data['main']['temp'] - 273.15:.0f} °C")
                    st.metric("Humidité", f"{weather_data['main']['humidity']} %")
                with col2:
                    st.metric("Pression ", f"{weather_data['main']['pressure']} hPa")
                    st.metric("Vent", f"{weather_data['wind']['speed'] * 3.6:.0f} km/h") # 1m/s = 3.6 km/h
    else:
        # Display a message for the city not found
        st.error("Service non disponible pour la ville choisie !")

if __name__ == "__main__":
    main()
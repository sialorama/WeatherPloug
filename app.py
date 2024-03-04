import streamlit as st
import pandas as pd
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

def display_weekly_forcast(data):
    try:
        st.image("./img/bandeau.png", output_format="auto")
        st.write("## Météo 7 jours")
        displayed_dates = set() # To keep track of dates for which forecast has been displayed

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("", "Jour")
        with c2:
            st.metric("", "Desription")
        with c3:
            st.metric("", "Minimale")
        with c4:
            st.metric("", "Maximale")

        for day in data['list']:

            date = datetime.fromtimestamp(day['dt']).strftime('%A, %B %d')
            # Check if the date has been displayed
            if date not in displayed_dates:
                displayed_dates.add(date)

                temp_min = day['main']['temp_min'] - 273.15
                temp_max = day['main']['temp_max'] - 273.15
                description = day['weather'][0]['description']

                with c1:
                    st.write(f"{date}")
                with c2:
                    st.write(f"{description.capitalize()}")
                with c3:
                    st.write(f"{temp_min:.1f} °C")
                with c4:
                    st.write(f"{temp_max:.1f} °C")

    except Exception as e:
        # Display an errro message for the weekly forecast
        st.error("Service non disponible pour le moment : " + str(e))

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

    if submit:
      
        st.title("Météo " + city)
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
                
                lat = weather_data['coord']['lat']
                lon = weather_data['coord']['lon']

                # Create a map with the data
                data = pd.DataFrame({
                    'latitude': [lat],
                    'longitude': [lon]
                    })
                st.map(data)
                
                # 
                weather_description = genrate_weather_description(weather_data, openai_api_key)
                st.write(weather_description)

                # 
                forecast_data = get_weekly_forcast(weather_api_key, lat, lon)
                print(forecast_data)

                if forecast_data.get ("cod") != "404":
                    display_weekly_forcast(forecast_data)
                
                else:
                    st.error("Service non disponible pour le moment!")
                
    else:
        # Display a message for the city not found
        st.error("Service non disponible pour la ville choisie !")

if __name__ == "__main__":
    main()
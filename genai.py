from config import GEN_AI_KEY
from google import genai

def generate_itinerary(flight_data, weather_data_origin, weather_data_destination, places):  

  client = genai.Client(api_key=GEN_AI_KEY)

  interaction = client.interactions.create(
      model="gemini-2.5-flash",
      input= f'Tell me about these jsons {flight_data}, {weather_data_origin}, {weather_data_destination}, {places}'
  )
  
  print(interaction.output_text)










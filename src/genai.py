from src.config import GEN_AI_KEY
from google import genai


def generate_itinerary(
    flight_data, weather_data_origin, weather_data_destination, places
):

    client = genai.Client(api_key=GEN_AI_KEY)

    interaction = client.interactions.create(
        model="gemini-2.5-flash",
        system_instruction="""
      You are a professional travel planning assistant.

      Your task is to generate a clear, structured travel itinerary based on the data provided.
      You will be given:
      1. Flight information containing one outbound flight and one return flight, each with (price, duration, routes, times, airline, and airplane)
      2. Weather information for the origin location
      3. Weather forecast for the destination for the travel dates
      4. A list of recommended places/attractions at the destination
      
      Requirements: 

      - Create a day-by-day itinerary for the trip.
      - Align activities with weather conditions (e.g., outdoor activities on good weather days, indoor activities on bad weather days).
      - Use flight arrival time to plan Day 1 realistically.
      - Include rest time after long flights.
      - Prioritize efficiency (group nearby attractions together).
      - Do NOT assume missing data—only use what is provided.
      - If weather is uncertain, mention flexibility in plans.
      
      Output Format:
      Return a structured response in this format while bolding key information:

      TITLE:
      - Trip summary (origin → destination + dates (am/pm))

      FLIGHT SUMMARY:
      - Key outbound flight details
      - Return flight details

      WEATHER SUMMARY:
      - Origin weather (departure day)
      - Destination weather overview during trip

      ITINERARY:

      Day 1:
      - Morning:
      - Afternoon:
      - Evening:

      Day 2:
      - Morning:
      - Afternoon:
      - Evening:

      (Continue for full trip duration)

      TIPS:
      - Packing suggestions based on weather
      - Travel optimization tips
      - Any warnings or considerations
      """,
        input=f"""
      Input Data:
      
      FLIGHTS: 
      OUTBOUND: {flight_data["outbound"]}
      RETURN: {flight_data["return"]}
      
      ORIGIN WEATHER:
      {weather_data_origin} 
      
      DESTINATION WEATHER:
      {weather_data_destination}
      
      PLACES DATA: 
      {places}
      
      """,
    )

    return interaction.output_text

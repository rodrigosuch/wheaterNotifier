import requests
import datetime
import os
from twilio.rest import Client

openweather_key = os.environ['OPEN_WEATHER_KEY']
# This is a sample Python script.

def get_city_coordinates(city_name):
    r = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={openweather_key}")
    return r.json()[0]['lat'],r.json()[0]['lon']

def composeSMS(latlong):
    json_weather = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?lat={latLong[0]}&lon={latLong[1]}&units=metric&appid={openweather_key}")
    result = ""
    # Print windspeed and weather for the next 24h
    time_now = datetime.datetime.now()
    for idx in range(0, 9):
        localhour = f"{time_now.hour}:{time_now.minute}\t"
        windspeed = f"Wind: {json_weather.json()['list'][idx]['wind']['speed']}m/s, "
        gusts = f"Gust: {json_weather.json()['list'][0]['wind']['gust']}m/s, "
        temperature = f"{json_weather.json()['list'][0]['main']['temp']}°C "
        description = json_weather.json()['list'][0]['weather'][0]['description']
        result = result + localhour + windspeed + gusts + temperature + description + "\n"
        time_now = time_now + datetime.timedelta(hours=3)

    result = result + f"Query status:{json_weather.status_code}\n"
    return result

def sendSMS(message):
    #send sms
    twilio_sid = os.environ['TWILIO_SID']
    twilio_token = os.environ['TWILIO_TOKEN']
    client = Client(twilio_sid, twilio_token)
    my_phone = os.environ['MY_PHONE']
    twilio_phone = os.environ['TWILIO_PHONE']
    twilio_whatsapp = os.environ['TWILIO_WHATSAPP']

    message = client.messages.create(
        body=message,
        to=my_phone,
        from_=twilio_phone
    )
    print(message.sid)

    message = client.messages.create(
    from_=f'whatsapp:{twilio_whatsapp}',
    body=message,
    to=f'whatsapp:{my_phone}'
    )
    print(message.sid)
    print(message)

latLong = get_city_coordinates("Lomma")
sms_message = composeSMS(latLong)
sendSMS(sms_message)
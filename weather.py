import datetime
import python_weather

import asyncio


async def getWeather() -> None:

  # Declare the client. The measuring unit used defaults to the metric system (celcius, km/h, etc.)
  async with python_weather.Client(unit=python_weather.METRIC) as client:
    # Fetch a weather forecast from a city.
    weather = await client.get('Eindhoven')
    output = u''
    daily = ''
    hourly = ''

    # Fetch the temperature for today.
    output += f'{weather.kind.emoji}  {weather.temperature} C {weather.feels_like} C\n'
    daily = f'{weather.kind.emoji}{weather.temperature} C {weather.feels_like} C\n'

    dc = 0
    for d in weather:
      if dc == 0:
        for h in d:
          if datetime.datetime.now().hour <= h.time.hour:
            output += f'{h.time.hour}h: {h.kind.emoji}  {h.temperature} C {h.chances_of_rain} %\n'
            hourly += f'{h.time.hour}h: {h.kind.emoji}{h.temperature} C {h.chances_of_rain} %, '
      dc += 1
  return daily, hourly, output


if __name__ == '__main__':
  d, h, out = asyncio.run(getWeather())
  print(out)
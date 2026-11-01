import datetime
import python_weather

import asyncio

class hourWeather:
    def __init__(self):
        self.time = 0
        self.timeStr = ''
        self.emoji = ''
        self.temperature = 0
        self.rain = 0
        self.wID = 0
        self.feelsLike = 0

async def getWeather() -> None:
    # Declare the client. The measuring unit used defaults to the metric system (celcius, km/h, etc.)
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        # Fetch a weather forecast from a city.
        weather = await client.get('Eindhoven')
        output = u''
        daily = ''
        hourly = []

        # Fetch the temperature for today.
        output += f'{weather.kind.emoji}  {weather.temperature} C {weather.feels_like} C\n'
        dailyStr = f'{weather.kind.emoji}{weather.temperature} C {weather.feels_like} C\n'
        day = hourWeather()
        day.wID = 0
        day.time = 0
        day.timeStr = 'Today'
        day.temperature = weather.temperature
        day.feelsLike = weather.feels_like
        day.emoji = weather.kind.emoji
        hourly.append(day)

        dc = 0
        for d in weather:
            if dc == 0:
                hc = 1
                for h in d:
                    if (datetime.datetime.now().hour <= h.time.hour) and (0 <= hc <= 3):
                        output += f'{h.time.hour}h: {h.kind.emoji}  {h.temperature} C {h.chances_of_rain} %\n'
                        hw = hourWeather()
                        hw.wID = hc
                        hw.time = h.time.hour
                        hw.timeStr = f'{h.time.hour} h'
                        hw.emoji = h.kind.emoji
                        hw.temperature = h.temperature
                        hw.rain = h.chances_of_rain
                        hourly.append(hw)
                        hc += 1
            dc += 1
    return dailyStr, hourly, output


if __name__ == '__main__':
    day, hour, out = asyncio.run(getWeather())
    for h in hour:
        print(f'{h.wID} and {h.temperature}')
    print(out)
from bs4 import BeautifulSoup
import requests


def getWeatherData(cityName):
    weatherDataArray = []

    sinoptikURL = 'https://ua.sinoptik.ua/погода-' + cityName + '/10-днів'
    sinoptikHTML = requests.get(sinoptikURL).text
    parsedHTMLpage = BeautifulSoup(sinoptikHTML, "html.parser")

    for dayNumber in range(1, 11):
        currentDayDiv = parsedHTMLpage.find("div", {"id": "bd" + str(dayNumber)})
        date = currentDayDiv.find("p", {"class": "date"}).getText()
        month = currentDayDiv.find("p", {"class": "month"}).getText()
        minTemp = currentDayDiv.find("div", {"class": "min"}).find("span").getText()
        maxTemp = currentDayDiv.find("div", {"class": "max"}).find("span").getText()
        weatherInfo = currentDayDiv.find("div", {"class": "weatherIco"}).get('title')

        weatherDataArray.append({
            'date': date,
            'month': month,
            'minTemp': minTemp,
            'maxTemp': maxTemp,
            'weatherInfo': weatherInfo
        })

    return weatherDataArray


def getWeatherTextMessage(weatherDataArray, cityName):
    outputCity = cityName[0].upper() + cityName[1:]

    weatherTextMessage = f'Погода у місті {outputCity} \n' \
                         f'Сьогодні {weatherDataArray[0].get("date")} {weatherDataArray[0].get("month")} \n' \
                         f'Від {weatherDataArray[0].get("minTemp")} до {weatherDataArray[0].get("maxTemp")}. \n' \
                         f'{weatherDataArray[0].get("weatherInfo")} \n' \
                         f'Завтра \n' \
                         f'Від {weatherDataArray[1].get("minTemp")} до {weatherDataArray[1].get("maxTemp")}. \n' \
                         f'{weatherDataArray[0].get("weatherInfo")}'

    return weatherTextMessage


def get10DaysWeatherForecast(weatherDataArray, cityName):
    outputCity = cityName[0].upper() + cityName[1:]
    weatherTextMessage = f'Погода у місті {outputCity} на 10 днів \n' \
                         f'Сьогодні '
    for day in weatherDataArray:
        weatherTextMessage += f'{day.get("date")} ' \
                            f'{day.get("month")}: ' \
                            f'від {day.get("minTemp")} до {day.get("maxTemp")} \n'

    return weatherTextMessage
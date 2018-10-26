import pyowm
#a class that simplifies the pyowm data for easy acessability with the headcase program
owmObject = None
forecast = None
observation = None
weather = None

ini = 0

NOINIT = 'Error: headWeather is not initialized'
def init(location='New York, New York'):
	global owmObject
	global forecast
	global observation
	global weather
	global ini

	owmObject = pyowm.OWM('f728080bbe4bec79a270a47aef733b7f')
	forecast = owmObject.daily_forecast(location)
	observation = owmObject.weather_at_place(location)
	weather = observation.get_weather()
	ini = 1

def getTemperature(unit='fahrenheit', point='temp'):
	global weather
	global ini
	global NOINIT
	if ini == 1:
		temp = weather.get_temperature(unit)[point]
		return temp
	else:
		return NOINIT
def HotOrCold(upper=25, lower=15):
	global ini
	global NOINIT
	temp = getTemperature(unit='celsius')
	if ini == 1:
		if temp > upper:
			return 'Hot'
		elif temp < lower:
			return 'Cold'
		else:
			return 'Neither'
	else:
		return NOINIT

def getWindSpeed():
	global weather
	global ini
	global NOINIT
	if ini == 1:
		windSpeed = weather.get_wind()['speed']
		return windSpeed
	else:
		return NOINIT


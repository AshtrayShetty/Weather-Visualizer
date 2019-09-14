import requests,json

try:
	#Entered bangalore into the search query only for the current problem statement
	r=requests.get("https://www.metaweather.com/api/location/search/?query=bangalore")
except:
	print("Page not found")
	exit()

packages_json=r.json()

woeid=packages_json[0]["woeid"]

try:
	r=requests.get(f"https://www.metaweather.com/api/location/{woeid}/")
except:
	print("Page not found")
	exit()

weather_data=r.json()

results=[]

weather_on_date=weather_data["consolidated_weather"]

for data in weather_on_date:

	weather_state_name=data["weather_state_name"]
	weather_state_abbr=data["weather_state_abbr"]
	wind_direction_compass=data["wind_direction_compass"]
	applicable_date=data["applicable_date"]

	#rounded off the values to the third decimal for better readability
	min_temp=round(data["min_temp"],3)
	max_temp=round(data["max_temp"],3)
	the_temp=round(data["the_temp"],3)
	wind_speed=round(data["wind_speed"],3)
	air_pressure=round(data["air_pressure"],3)
	visibility=round(data["visibility"],3)

	#wasn't sure wheter to round off the value of wind direction 
	wind_direction=data["wind_direction"]
	humidity=data["humidity"]
	predictability=data["predictability"]

	weather={

		"applicable_date":applicable_date,

		"weather_state":{
			"weather_state_name":weather_state_name,
			"weather_state_abbr":weather_state_abbr
		},

		"direction":{
			"wind_direction_compass":wind_direction_compass,
			"wind_direction":wind_direction
		},

		"analytics":{

			"min_temp":min_temp,
			"max_temp":max_temp,
			"the_temp":the_temp,
			"wind_speed":wind_speed,
			"air_pressure":air_pressure,
			"visibility":visibility,
			"humidity":humidity,
			"predictability":predictability

		}
		
	}

	results.append(weather)

#Writing the data into a .json file so that it can be accessed later for plotting graphs
with open("weather_data.json", "w") as wd:
	json.dump(results, wd, indent=2)

import matplotlib.pyplot as plt
import numpy as np

#Plotting temperature v/s date and wind_speed v/s date
with open("weather_data.json","r") as wd:

	dataset=json.load(wd)

	dates=[]
	temperatures=[]
	wind_speeds=[]

	#Creating lists so that the data can be read in the plotting funcitons
	for data in dataset:

		dates.append(data['applicable_date'])
		temperatures.append(data['analytics']['the_temp'])
		wind_speeds.append(data['analytics']['wind_speed'])

	#To avoid overlapping of the graphs
	indices=range(len(dates))
	width=np.min(np.diff(indices))/3.

	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.bar(indices-width/2., temperatures , width, color='b', label='temperature')
	ax.bar(indices+width/2., wind_speeds, width, color='r', label='wind speed')
	ax.axes.set_xticklabels(dates)
	ax.legend(loc='upper right')
	ax.set_xlabel('Prediction Date')
	ax.set_ylabel('Values')
	plt.show()

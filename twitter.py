import json
import pyowm
import requests
import sys
import tweepy
import us

def convert(temp, unit):
    unit = unit.lower()
    if unit == "c":
        return 9.0 / 5.0 * temp + 32
    if unit == "f":
        return (temp - 32)  / 9.0 * 5.0

# Returns the api object of twitter enabling tweet posting
def get_api(cfg):
	auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
	auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
	return tweepy.API(auth)

# Extracts a json packet from the webiste and returns a json packet of strings
def get_cur_loc():
	send_url = 'https://ipinfo.io'
	r = requests.get(send_url)
	return json.loads(r.text, "utf-8")

def get_heat_index(c_temp, out_humidity):
	# The input temperature is in celsius so convert to fahrenheit
	f_temp = convert(c_temp, 'C')

	# Calculate what the temperature actually feels like
	feel_temp = float(0)

	if (f_temp >= 80):
		feel_temp = -42.379 + 									\
				(2.04901523 * f_temp) + 						\
				(10.14333127 * out_humidity) - 					\
				(0.22475541 * f_temp * out_humidity) - 			\
				(6.83783 * 10**-3 * f_temp**2) - 				\
				(5.481717 * 10**-2 * out_humidity**2 ) + 		\
				(1.22874 * 10**-3 * f_temp**2 * out_humidity) + \
				(8.5282 * 10**-4 * f_temp * out_humidity**2 ) - \
				(1.99 * 10**-6 * f_temp**2 * out_humidity**2)
		
		adjustment = 0

		if (f_temp >= 80 and f_temp <= 112 and out_humidity < 13):
			adjustment = -(((13 - out_humidity) / 4) * ((17 - abs(f_temp - 95.)) / 17) ** (0.5))
		elif (f_temp >= 80 and f_temp <= 87 and out_humidity > 85):
			adjustment = ((out_humidity - 85) / 10) * ((87 - f_temp) / 5)

		feel_temp = feel_temp + adjustment
	else:
		feel_temp = 0.5 * (f_temp + 61.0 + ((f_temp - 68.0) * 1.2) + (out_humidity * 0.094))	

	# Return the converted value of the actual temperature in Celsius
	return convert(feel_temp, 'F')

# Extracts the actual and temperature of a place given the coordinates
def get_temp_and_humidity(lat, lon):
	owm = pyowm.OWM('13ff05b52e1127ce27d6c06b1b1cc411')
	w = owm.weather_at_coords(lat, lon).get_weather()
	return [w.get_temperature('celsius'), w.get_humidity()]
	# return [json.loads(w.get_temperature('celsius'), 'utf-8'), w.get_humidity()]

# Main function
def main():
	# Store the keys necessary to access the Twitter API
	cfg = {
		"consumer_key"			: "lG608JQsOPZrEUuLBGyW6OUv5",
		"consumer_secret"		: "vDNOXfjkXJ1NDVNMmO603uaMmmrhltj29NiUGBisSfJCScSO75",
		"access_token"			: "987595171914072064-nJcpTl7DP8cKe5alMgen6k6USmWVU84",
		"access_token_secret"	: "1OEVW9qw3HAHYtvbGqFF5sjJTLcw7EluMboCYYpGiJGAV"
	}

	# Get functions
	api = get_api(cfg)
	cur_loc = get_cur_loc()
	temp_and_humidity = get_temp_and_humidity(float(cur_loc['loc'].split(',')[0]), float(cur_loc['loc'].split(',')[1]))
	out_temp = temp_and_humidity[0]['temp']
	out_humidity = temp_and_humidity[1]
	# Compute the heat index based on the current temperature and humidity
	out_heat_index = get_heat_index(out_temp, out_humidity)

	temp_msg = ""

	org = " ".join(cur_loc['org'].split()[1:])
	city = cur_loc['city']
	# Get the two letter abbreviation rather than the state's full name
	region = us.states.mapping('name', 'abbr')[cur_loc['region']]
	postal = cur_loc['postal']

	# Store the inside value data
	in_temp = float(sys.argv[1])
	in_humidity = int(sys.argv[2])
	in_heat_index = get_heat_index(in_temp, in_humidity)

	tweet = temp_msg + " in " + org + ", " + city + ", " + region + " " + postal + '\n' +											\
			'\n' 																													\
			"Outside: T = " + str(round(out_temp, 2)) + " C, H = " + str(out_humidity) + "%, Feels like " + str(round(out_heat_index, 2)) + " C" + '\n'	\
			"Inside:    T = " + str(round(in_temp, 2)) + " C, H = " + str(in_humidity) + "%, Feels like " + str(round(in_heat_index, 2)) + " C"
	status = api.update_status(status=tweet)

if __name__ == "__main__":
	main()
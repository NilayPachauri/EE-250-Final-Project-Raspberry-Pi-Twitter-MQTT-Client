import json
import requests
import tweepy

# Extracts a json packet from the webiste and returns a json packet of strings
def get_cur_loc():
	send_url = 'https://ipinfo.io'
	r = requests.get(send_url)
	return json.loads(r.text, "utf-8")

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

	tweet = "Hello World"
	status = api.update_status(status=tweet)

if __name__ == "__main__":
	main()
import tweepy

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
	
	tweet = "Hello World"
	status = api.update_status(status=tweet)

if __name__ == "__main__":
	main()
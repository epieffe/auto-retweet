import os
import logging
from sys import stdout
from tweepy import Client
from dotenv import load_dotenv

from util import get_cache, set_cache

load_dotenv()

logging.basicConfig(
    stream=stdout,
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)

logger = logging.getLogger("main")

# User mention to be monitored.
# Eg: "elonmusk"
MENTION = os.getenv("MENTION")

# List of twitter usernames to monitor
# Eg: ["ferrariep", "VitalikButerin"]
USERS = os.getenv("USERS").split(",")

client = Client(
    bearer_token=os.getenv("BEARER_TOKEN"),
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_KEY_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
)

# Eg: "from:ferrariep OR from:VitalikButerin"
from_users_query = " OR ".join(map(lambda user: "from:" + user, USERS))

# Eg: "@elonmusk (from:ferrariep OR from:VitalikButerin) -is:retweet -is:reply"
query = "@%s (%s) -is:retweet -is:reply" % (MENTION, from_users_query)

logger.debug("Executing query=\"%s\"" % query)

# Load cache from file if exists, otherwise set default
cache = get_cache() or {"mostRecentRetweetedId": None}

logger.info("Loaded cache=%s" % cache)

# Search tweets using the Twitter API v2
data, includes, errors, meta = client.search_recent_tweets(query=query, since_id=cache["mostRecentRetweetedId"])

# Check for Twitter api response errors
if len(errors) > 0:
    raise Exception("Error: " + errors[0])

if not data or len(data) == 0:
    logger.info("Did not find any new tweets")
    exit(0)

logger.info("Loaded tweets=%s" % data)

for tweet in data:
    client.retweet(tweet.id)

# Update cache
cache["mostRecentRetweetedId"] = data[0].id
set_cache(cache)

logger.info("Updated cache=%s" % cache)

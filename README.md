# tweet-graph

## Description
This repo contains code to build a graph of connected hashtags in a set of tweets. Some assumptions made in the code are:
1. Input tweets need to be a JSON object
2. Hashtags in tweets are accurately represented in the individual tweet object under ```tweet['entities']['hashtags']```
3. To either run the insertion or deletion step, a JSON file needs to be provided as input

## Running the code
1. To run the code in basic mode, use the following command ```python process_tweets --filepath TWEETS_TXT_FILE```
2. To add a new tweet, use the command ```python process_tweets --filepath TWEETS_TXT_FILE --add_tweet PATH_TO_JSON_OF_NEW_TWEET```
3. To delete an old tweet, use the command ```python process_tweets --filepath TWEETS_TXT_FILE --delete_tweet PATH_TO_JSON_OF_TWEET_TO_BE_DELETED```

## Tests
Unit tests have been written to test base functionality. To run the tests, run the command ```python -m unittest``` in the root directory
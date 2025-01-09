import process_tweets
import unittest
import json

class TestProcessTweets(unittest.TestCase):
    def setUp(self):
        process_tweets.tweet_graph = {}
        self.tweets = [
        {
            "text": "Some tweet regarding something #bored",
            "entities": {
                "hashtags":[
                    {
                        "text": "bored"
                    }
                ]
            }
        },
        {
            "text": "Not much to do in the winters!! #bored #cold",
            "entities": {
                "hashtags":[
                    {
                        "text": "bored"
                    },
                    {
                        "text": "cold"
                    }
                ]
            }
        },
        {
            "text": "Summers in Chennai are super hooooot #heat #hot",
            "entities": {
                "hashtags":[
                    {
                        "text": "heat"
                    },
                    {
                        "text": "hot"
                    }
                ]
            }
        }
        ]

        self.tweet_to_be_deleted = {
            "text": "Summers in Chennai are super hooooot #heat #hot",
            "entities": {
                "hashtags":[
                    {
                        "text": "heat"
                    },
                    {
                        "text": "hot"
                    }
                ]
            }
        }

    # Test if tweets are inserted to graph correctly
    def test_insert_to_graph(self):
        for item in self.tweets:
            process_tweets.insert_to_graph(json.dumps(item))
        
        expected_result = {
            "bored":{
                "cold": 1
            },
            "cold":{
                "bored": 1
            },
            "heat":{
                "hot": 1
            },
            "hot": {
                "heat": 1
            }
        }
        self.assertEqual(expected_result, process_tweets.tweet_graph)
    
    # Test if degree calculation is correct
    def test_calculate_avg_degree(self):
        for item in self.tweets:
            process_tweets.insert_to_graph(json.dumps(item))
        
        avg_degree = process_tweets.calculate_avg_degree()
        self.assertEqual(avg_degree, 1.0)
    
    # Test if tweet deletion works
    def test_delete_from_graph(self):
        for item in self.tweets:
            process_tweets.insert_to_graph(json.dumps(item))
        
        new_avg = process_tweets.delete_from_graph(json.dumps(self.tweet_to_be_deleted))
        expected_result = expected_result = {
            "bored":{
                "cold": 1
            },
            "cold":{
                "bored": 1
            }
        }
        self.assertEqual(expected_result, process_tweets.tweet_graph)
        self.assertEqual(new_avg, 1.0)


if __name__=='__main__':
    unittest.main()


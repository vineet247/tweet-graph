import json

tweet_graph = {}

# Function takes a path to open tweets
def parse_tweets(file_path):
    """
    tweet_graph is a dictionary where the keys are individual hashtags and 
    the values stored are all the other hashtags associated with it
    """
    global tweet_graph
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
            for line in lines:
                insert_to_graph(line)
            
        file.close()
    
    except FileNotFoundError:
        print("File could not found")
        quit()

    

# Function to take a tweet and a tweet graph and insert the tweet's hashtags into the tweet_graph
def insert_to_graph(tweet):
    global tweet_graph
    
    tweet_string = json.loads(str(tweet))
    
    # Process only tweets with hashtags
    if(tweet_string.get('entities') and tweet_string.get('entities').get('hashtags') 
    and len(tweet_string.get('entities').get('hashtags')) != 0):
        #get all hashtags in a given tweet
        tag_list = list(map(lambda x:x.get('text').lower(), tweet_string.get('entities').get('hashtags')))

        """
        If a tag doesnt exist in the tweet_graph, add it as a key and store the tag_list as its value.
        Else, insert all elements of the tag_list into the key for the tweet_graph
        """
        for individual_tag in tag_list:
            if individual_tag not in tweet_graph.keys():
                tweet_graph[individual_tag] = {}
                for unique_tag in tag_list:
                    if unique_tag != individual_tag:
                        if unique_tag in tweet_graph[individual_tag].keys():
                            tweet_graph[individual_tag][unique_tag] += 1
                        else:
                            tweet_graph[individual_tag][unique_tag] = 1
                    else:
                        continue
            else:
                for item in tag_list:
                    if item != individual_tag:
                        if item in tweet_graph[individual_tag].keys():
                            tweet_graph[individual_tag][item] += 1
                        else:
                            tweet_graph[individual_tag][item] = 1
                       
                        
#Function to calculate average degree
def calculate_avg_degree():
    global tweet_graph
    nodes = 0
    sum_of_degrees = 0

    for key in tweet_graph.keys():
        nodes += 1
        sum_of_degrees += len(tweet_graph[key].keys())
    
    return sum_of_degrees/nodes

def delete_from_graph(tweet):
    global tweet_graph

    tweet_string = json.loads(str(tweet))
    if (tweet_string.get('entities') == None or tweet_string.get('entities').get('hashtags') == None 
    or len(tweet_string.get('entities').get('hashtags')) == 0):
        raise Exception("No hashtag in tweet")
    else:
        tag_list = list(map(lambda x:x.get('text').lower(), tweet_string.get('entities').get('hashtags')))
        for tag in tag_list:
            if tag not in tweet_graph.keys():
                raise Exception("Tag not in tweet graph. Cannot be deleted")

            for unique_tag in tag_list:
                if tag not in tweet_graph.keys():
                    raise Exception("Tag not in tweet graph. Cannot be deleted")

                if unique_tag != tag:
                    tweet_graph[tag][unique_tag]-=1
                    if tweet_graph[tag][unique_tag] <= 0:
                        del tweet_graph[tag][unique_tag]
    return calculate_avg_degree()
    
                    

def main():
    file_path = str(input("Enter file path: "))
    parse_tweets(file_path)
    avg_degree = calculate_avg_degree()
    print(avg_degree)

    # tweet = "{\"created_at\":\"Mon Mar 28 23:23:12 +0000 2016\",\"id\":714593712366620672,\"id_str\":\"714593712366620672\",\"text\":\"@gbvigo miga isso nao existe vc \\u00e9 taurina rssa\",\"source\":\"\\u003ca href=\\\"http:\\/\\/twitter.com\\/download\\/iphone\\\" rel=\\\"nofollow\\\"\\u003eTwitter for iPhone\\u003c\\/a\\u003e\",\"truncated\":false,\"in_reply_to_status_id\":714593258802905089,\"in_reply_to_status_id_str\":\"714593258802905089\",\"in_reply_to_user_id\":154304713,\"in_reply_to_user_id_str\":\"154304713\",\"in_reply_to_screen_name\":\"gbvigo\",\"user\":{\"id\":1486482758,\"id_str\":\"1486482758\",\"name\":\"raphaella\",\"screen_name\":\"voudaropapo\",\"location\":\"Rio de Janeiro, Brasil\",\"url\":null,\"description\":\"arquitetei universos s\\u00f3 com a minha paranoia\",\"protected\":false,\"verified\":false,\"followers_count\":394,\"friends_count\":287,\"listed_count\":0,\"favourites_count\":9598,\"statuses_count\":29616,\"created_at\":\"Thu Jun 06 01:15:57 +0000 2013\",\"utc_offset\":null,\"time_zone\":null,\"geo_enabled\":true,\"lang\":\"pt\",\"contributors_enabled\":false,\"is_translator\":false,\"profile_background_color\":\"000000\",\"profile_background_image_url\":\"http:\\/\\/abs.twimg.com\\/images\\/themes\\/theme18\\/bg.gif\",\"profile_background_image_url_https\":\"https:\\/\\/abs.twimg.com\\/images\\/themes\\/theme18\\/bg.gif\",\"profile_background_tile\":false,\"profile_link_color\":\"F5ABB5\",\"profile_sidebar_border_color\":\"000000\",\"profile_sidebar_fill_color\":\"000000\",\"profile_text_color\":\"000000\",\"profile_use_background_image\":false,\"profile_image_url\":\"http:\\/\\/pbs.twimg.com\\/profile_images\\/712411700436320256\\/V0FuQVuG_normal.jpg\",\"profile_image_url_https\":\"https:\\/\\/pbs.twimg.com\\/profile_images\\/712411700436320256\\/V0FuQVuG_normal.jpg\",\"profile_banner_url\":\"https:\\/\\/pbs.twimg.com\\/profile_banners\\/1486482758\\/1459036011\",\"default_profile\":false,\"default_profile_image\":false,\"following\":null,\"follow_request_sent\":null,\"notifications\":null},\"geo\":null,\"coordinates\":null,\"place\":{\"id\":\"97bcdfca1a2dca59\",\"url\":\"https:\\/\\/api.twitter.com\\/1.1\\/geo\\/id\\/97bcdfca1a2dca59.json\",\"place_type\":\"city\",\"name\":\"Rio de Janeiro\",\"full_name\":\"Rio de Janeiro, Brasil\",\"country_code\":\"BR\",\"country\":\"Brasil\",\"bounding_box\":{\"type\":\"Polygon\",\"coordinates\":[[[-43.795449,-23.083020],[-43.795449,-22.739823],[-43.087707,-22.739823],[-43.087707,-23.083020]]]},\"attributes\":{}},\"contributors\":null,\"is_quote_status\":false,\"retweet_count\":0,\"favorite_count\":0,\"entities\":{\"hashtags\":[],\"urls\":[],\"user_mentions\":[{\"screen_name\":\"gbvigo\",\"name\":\"gab.\",\"id\":154304713,\"id_str\":\"154304713\",\"indices\":[0,7]}],\"symbols\":[]},\"favorited\":false,\"retweeted\":false,\"filter_level\":\"low\",\"lang\":\"pt\",\"timestamp_ms\":\"1459207392194\"}\r\n"
    # new_avg = delete_from_graph(tweet)
    # print("new avg: ", new_avg)

if __name__ == '__main__':
    main()
        
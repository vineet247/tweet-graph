import json
import argparse

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
        print("Tweet file could not found")
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
    
                    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Process some tweets')
    parser.add_argument('--filepath',type = str, required = False, help = "Path of inputs tweet file")
    parser.add_argument('--add_tweet', type = str, required = False, help = "Tweet to be added to graph")
    parser.add_argument('--delete_tweet', type = str, required = False, help = "Tweet to be removed from graph")
    args = parser.parse_args()

    if not args.filepath:
        print("No filepath provided")
        quit()
    parse_tweets(args.filepath)
    avg_degree = calculate_avg_degree()
    print(avg_degree)

    #if user wants to add a tweet to the graph
    if args.add_tweet:
        try:
            with open(args.add_tweet) as input:
                tweet = json.load(input)
                insert_to_graph(json.dumps(tweet))
                new_avg_degree = calculate_avg_degree()
                print("new average degree: ", new_avg_degree)
        except FileNotFoundError:
            print("Input file could not found")
            quit()
        
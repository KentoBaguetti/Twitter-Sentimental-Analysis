import string

# The read_keywords() function takes a tsv file of keywords and their sentiment values and stores it into a dicitonary for future use
def read_keywords(keyword_file_name):
    keyword_dict = {} # the dictionary that stores information on the keywords
    try:
        infile = open(keyword_file_name, "r")
        line = infile.readline()
        while line != "": 
            temp = line.rstrip().split("\t")
            keyword_dict[temp[0]] = int(temp[1])
            line = infile.readline()
        infile.close()
        return keyword_dict
    except IOError:
        print("Invalid file.")
        return keyword_dict
            
 

# The clean_tweet_text() function takes a tweet and removes any numbers and punctuation, as well as making the tweet all lowercase
# Returns a clean version of the text.
# I used the string module to make sure I have all the punctuation characters
def clean_tweet_text(tweet_text):
    PUNC = string.digits + string.punctuation
    clean_tweet = ""
    for char in tweet_text:
        if char not in PUNC:
            clean_tweet += char
    return clean_tweet.lower()
    

# The calc_sentiment() function takes a clean text and compares each word in it with the keywords dictionary.
# If a word has a sentimental value, add it to the sum of the tweet sentiment and return that sum
def calc_sentiment(tweet_text, keyword_dict):
    sentiment = 0
    word_list = tweet_text.split()
    for word in word_list:
        if word in keyword_dict:
            sentiment += keyword_dict[word]
    return sentiment

# Classify what was returned from the calc_sentiment() function as a string. Either positive, negative, or neutral
def classify(score):
    if score > 0:
        return("positive")
    elif score < 0:
        return("negative")
    else:
        return("neutral")

# The read_tweets() function takes a csv file of tweets and their information, and stores each tweet as a dictionary with its information
# Into a list. The dictionary is then returned
def read_tweets(tweet_file_name):
    list = []
    try:
        infile = open(tweet_file_name, "r")
        line = infile.readline()
        while line != "":
            temp = line.rstrip().split(",")
            tweet_info = {}
            tweet_info["city"] = temp[8]
            tweet_info["country"] = temp[6]
            tweet_info["date"] = temp[0]
            tweet_info["favorite"] = int(temp[4])
            tweet_info["lang"] = temp[5]
            if temp[9] == "NULL":
                tweet_info["lat"] = "NULL"
            else:
                tweet_info["lat"] = float(temp[9])
            if temp[10] == "NULL":
                tweet_info["lon"] = "NULL"
            else:
                tweet_info["lon"] = float(temp[10])
            tweet_info["retweet"] = int(temp[3])
            tweet_info["state"] = temp[7]
            tweet_info["text"] = clean_tweet_text(temp[1])
            tweet_info["user"] = temp[2]
            list.append(tweet_info)
            line = infile.readline()
        infile.close()
        return list
    except IOError:
        print(f"Could not open {tweet_file_name}")
        return list


# The make_report() function returns a dictionary of the information from the read_tweets() function into a legible dictionary
def make_report(tweet_list, keyword_dict):
    report_dict = {}
    # The below varaibles will store the information that will be stored in the above report_dict dictionary
    avg_favourite_value = 0
    avg_retweet_sentiment = 0
    avg_tweet_sentiment = 0
    num_liked_tweets = 0
    num_negative_tweets = 0
    num_neutral_tweets = 0
    num_positive_tweets = 0
    num_retweeted_tweets = 0
    num_total_tweets = 0
    top_five_countries = ""
    
    temp_country_dict = {}
    
    for tweet in tweet_list: # For every tweet in the tweet_list, it will process the information
        tweet_sentiment = round(calc_sentiment(clean_tweet_text(tweet["text"]), keyword_dict), 2)
        num_total_tweets += 1
        if int(tweet["retweet"]) > 0:
            avg_retweet_sentiment += tweet_sentiment
            num_retweeted_tweets += 1
        if int(tweet["favorite"]) > 0:
            avg_favourite_value += tweet_sentiment
            num_liked_tweets += 1
        avg_tweet_sentiment += tweet_sentiment
        
        if tweet_sentiment > 0:
            num_positive_tweets += 1
        elif tweet_sentiment < 0:
            num_negative_tweets += 1
        else:
            num_neutral_tweets += 1
            
        if tweet["country"] not in temp_country_dict and tweet["country"] != "NULL":
            temp_country_dict[tweet["country"]] = [1, calc_sentiment(tweet["text"], keyword_dict)]
        elif tweet["country"] in temp_country_dict:
            temp_country_dict[tweet["country"]][0] += 1
            temp_country_dict[tweet["country"]][1] += calc_sentiment(tweet["text"], keyword_dict)
    
    avg_favourite_value = round(avg_favourite_value / num_liked_tweets, 2)
    avg_retweet_sentiment = round(avg_retweet_sentiment / num_retweeted_tweets, 2)
    avg_tweet_sentiment = round(avg_tweet_sentiment / num_total_tweets, 2)
    
    country_dict = {}
    for key in temp_country_dict:
        country_dict[key] = (temp_country_dict[key][1]/temp_country_dict[key][0]) # find the avg sentimental value of each country
        
    sorted_country_list = sorted(country_dict.items(), key=lambda x:x[1], reverse=1) # sort the country list
    
    top_country_list = []
    for i in range(0,5):
        try:
            top_country_list.append(sorted_country_list[i][0]) # sort the countries in the list by the average sentimental value
        except IndexError:
            break
        
    top_five_countries = ", ".join(top_country_list) # join the list of countries that are sorted into one string
    
    if num_liked_tweets != 0:
        report_dict["avg_favorite"] = avg_favourite_value
    else:
        report_dict["avg_favorite"] = "NAN"
    if num_retweeted_tweets != 0:
        report_dict["avg_retweet"] = avg_retweet_sentiment
    else:
        report_dict["avg_retweet"] = "NAN"
    if num_total_tweets != 0:
        report_dict["avg_sentiment"] = avg_tweet_sentiment
    else:
        report_dict["avg_sentiment"] = "NAN"
    
    # The below code stores the processed informatuon into the report_dict
    report_dict["num_favorite"] = num_liked_tweets
    report_dict["num_negative"] = num_negative_tweets
    report_dict["num_neutral"] = num_neutral_tweets
    report_dict["num_positive"] = num_positive_tweets
    report_dict["num_retweet"] = num_retweeted_tweets
    report_dict["num_tweets"] = num_total_tweets
    report_dict["top_five"] = top_five_countries
    
    return report_dict

# The write_report() function writes the information from the make_report() function into a txt file.
def write_report(report, output_file):
    try:
        outfile = open(output_file, "w")
        outfile.write("Average sentiment of all tweets: {}\n".format(report["avg_sentiment"]))
        outfile.write("Total number of tweets: {}\n".format(report["num_tweets"]))
        outfile.write("Number of positive tweets: {}\n".format(report["num_positive"]))
        outfile.write("Number of negative tweets: {}\n".format(report["num_negative"]))
        outfile.write("Number of neutral tweets: {}\n".format(report["num_neutral"]))
        outfile.write("Number of favorited tweets: {}\n" .format(report["num_favorite"]))
        outfile.write("Average sentiment of favorited tweets: {}\n".format(report["avg_favorite"]))
        outfile.write("Number of retweeted tweets: {}\n".format(report["num_retweet"]))
        outfile.write("Average sentiment of retweeted tweets: {}\n".format(report["avg_retweet"]))
        outfile.write("Top five countries by average sentiment: {}\n".format(report["top_five"]))
        outfile.close()
        print(f"Wrote report to {output_file}")
    except IOError:
        print(f"Could not open filf {output_file}")

# Import the sentiment_analysis module
from sentiment_analysis import *

# The main function calls the functions from the sentimental_analysis.py and makes everything look clean
# It raises exceptions when required.
def main():
	keyword_file = input("Input keyword filename (.tsv file): ")
	if not keyword_file.endswith(".tsv"):
		raise Exception("Must have tsv file extension!")
	tweet_file = input("Input tweet filename (.csv file): ")
	if not tweet_file.endswith(".csv"):
		raise Exception("Must have csv file extension!")
	outputfile_name = input("Input filename to output report in (.txt file): ")
	if not outputfile_name.endswith(".txt"):
		raise Exception("Must have txt file extension!")

	keyword_dict = read_keywords(keyword_file)
	tweets = read_tweets(tweet_file)
	build_report = make_report(tweets, keyword_dict)
	write_report(build_report, outputfile_name)
 
     
	

main()

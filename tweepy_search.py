import tweepy
import api_keys
import json 
import argparse
import argcomplete

'''''
python tweepy_search.py --keywords-file search_keys.txt --number 100 --lang en -gl 37.781157 -122.398720 1mi
'''''


auth = tweepy.OAuthHandler(api_keys.consumer_key, api_keys.consumer_secret)
auth.set_access_token(api_keys.access_token, api_keys.access_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)


parser = argparse.ArgumentParser(description='collect tweets based on keywords')
parser.add_argument('-k', '--keywords-file', type=argparse.FileType(mode='r', encoding='utf-8'),
                    help='keywords or hashtags file. The file should contain one keyword/hashtag per line',
                    required=True)
parser.add_argument('-n', '--number', type=int,
                    help='the number of tweets that you want to collect', required=True)
parser.add_argument('-l', '--lang', type=str,
                    help='language', required=True)
parser.add_argument('-gl', '--geo-file', type=argparse.FileType(mode='r', encoding='utf-8'),
                    help='geo location file. The file should contain one [longtitude,latitude,radius #CountryName] per line',
                    required=False)


if __name__ == '__main__':
    args = parser.parse_args()
    argcomplete.autocomplete(parser)
    queries = args.keywords_file.read().splitlines()
    number = args.number
    lang = args.lang
    geo = args.geo
    location_str = "52.251231,5.712159,3000km #Netherlands"
    location_geo = location_str.split(" #",1)[0]
    location_name = location_str.split(" #", 1)[1]
    try:
        for query in queries:
            print('query: {}'.format(query))
            print('count: {}'.format(number))
            print('lang: {}'.format(lang))
            count = 0
            tweets = tweepy.Cursor(api.search, q=query, count=number,
                               lang=lang, tweet_mode='extended',geocode = location_geo).items()

            outfile = open('{}.json'.format('query'), mode='a+')
            for tweet in tweets:
                if count == number:
                    break;
                else:
                    tload = tweet._json
                    tload['TweetLocation'] = location_name
                    outfile.write(json.dumps(tload))
                    outfile.write('\n')
                    count +=1
            print('{} tweets'.format(count))
    except:
        print('429 TwitterAPI: Too many requests')

import requests
import os
import csv
import json
import time
import pandas as pd
# To set your environment variables in your terminal run the following line:
os.environ['BEARER_TOKEN'] = 'AAAAAAAAAAAAAAAAAAAAAJqkhgEAAAAA36Ulevx8gH%2Fq9W%2BEtFBAtcJ9uh0%3DatvIqCtKBZTngxq5rdNQd2CJoBJ5R9eveVP9qKG1JkPst2P6NZ'
bearer_token = os.environ.get("BEARER_TOKEN")
keyword = "tesla lang:en"
start_date = "2022-09-29T00:00:00.000Z" #can search from 28th sept as of 4th october (that is, within the past 5 to 6 days)
end_date = "2022-10-03T00:00:00.000Z"
max_results = 100 #change to get more tweets (min = 10 ,max = 100)

search_url = "https://api.twitter.com/2/tweets/search/recent" #only recent tweets can be searched with elevated access

query_params = {'query': keyword,
                    'start_time': start_date,
                    'end_time': end_date,
                    'max_results': max_results,
                    'next_token': [],
                    'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                    'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    'place.fields': 'full_name,id,country,country_code,geo,name,place_type'
                }


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    next_token = ''
    first_time= True
    page = 0
    requests = 0
    # Create file
    csvFile = open("twitternews.csv", "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(
        ['author id', 'created_at', 'geo', 'id', 'lang', 'like_count', 'quote_count', 'reply_count', 'retweet_count',
         'source', 'tweet'])
    while(query_params["next_token"]!=None or first_time==True ):
        json_response = connect_to_endpoint(search_url, query_params)
        """
        Tried converting it to csv here but nothing is fucking working!
        with open('twitternews.csv', 'w') as f:
            for key in json_response.keys():
                f.write("%s,%s\n" % (key, json_response[key]))
        #append_to_csv(json_response, "data.csv")
        """
        first_time = False
        print(json.dumps(json_response, indent=4, sort_keys=True))
        query_params["next_token"] = str(json_response["meta"]["next_token"]) #Loads the next page
        print("\nOverall stats : \n")
        page = page +1
        print("Page Number : ",page)
        requests = requests + json_response["meta"]["result_count"]
        print("Total requests : ",requests)
        time.sleep(5) #Wait for 5 seconds
    csvFile.close()

if __name__ == "__main__":
    main()

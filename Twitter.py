import twarc
# For sending GET requests from the API
import requests
# For saving access tokens and for file management when creating and adding to the dataset
import os
# For dealing with json responses we receive from the API
import json
# For displaying the data after
import pandas as pd
# For saving the response data in CSV format
import csv
# For parsing the dates received from twitter in readable formats
import datetime
import dateutil.parser
import unicodedata
#To add wait time between requests
import time

bearer_token = auth()
headers = create_headers(bearer_token)
keyword = "xbox lang:en"
start_time = "2021-03-01T00:00:00.000Z"
end_time = "2021-03-31T00:00:00.000Z"
max_results = 15

os.environ['TOKEN'] = 'AAAAAAAAAAAAAAAAAAAAAJqkhgEAAAAAyJBw4tDg5fMLgeOwkeNXaagXHpw%3DzwaKKC66IDiKqIaDwQe0v1m4ct4wTcPVFvS7pptz2s9dgP9SiT'
def auth():
    return os.getenv('TOKEN')

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def create_url(keyword, start_date, end_date, max_results=10):
    search_url = "https://api.twitter.com/2/tweets/search/all"  # Change to the endpoint you want to collect data from

    # change params based on the endpoint you are using
    query_params = {'query': keyword,
                    'start_time': start_date,
                    'end_time': end_date,
                    'max_results': max_results,
                    'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                    'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                    'next_token': {}}
    return (search_url, query_params)

def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()
#__init__(self, consumer_key="SzYyczhqY3B4Mm9lcXlVMWNqYTU6MTpjaQ", consumer_secret="sucYhaeRmMBQusAO_YGuRNi9F_jTJ9FoqlqaQfEYt81seXDOUC", access_token="1574686656732405761-FUaB3X4p4gZ7jodcavJG9XjlBhzBBj", access_token_secret="CQ53fTkZea65Ixd9yJFqIyVtsY50qM0PAeo8hYAzMYwb7", bearer_token="AAAAAAAAAAAAAAAAAAAAAJqkhgEAAAAAyJBw4tDg5fMLgeOwkeNXaagXHpw%3DzwaKKC66IDiKqIaDwQe0v1m4ct4wTcPVFvS7pptz2s9dgP9SiT", connection_errors=0, metadata=True)
import os
import requests

# get environment variables
APIFY_USER_ID = os.getenv('APIFY_USER_ID', '')
APIFY_CRAWLER_ID = os.getenv('APIFY_CRAWLER_ID', '')
APIFY_TOKEN = os.getenv('APIFY_TOKEN', '')

# start crawler execution run
r = requests.post(f'https://api.apify.com/v1/{APIFY_USER_ID}/crawlers/{APIFY_CRAWLER_ID}/execute?token={APIFY_TOKEN}&wait=60')
crawler_run = r.json()

# get results from crawler run
r = requests.get(crawler_run['resultsUrl'])
crawler_results = r.json()
rawdata  = crawler_results[0]['pageFunctionResult']

# format results
pollen = {
    'yesterday': {},
    'today': {},
    'tomorrow': {}
}
for item in rawdata:
    pollen[item['day'].lower()] = { 'count': item['count'], 'desc': item['desc'] }

# create pushover notification
title = f"pollen count is {pollen['today']['count']} ({pollen['today']['desc']})"
msg = f"""Tomorrow: {pollen['tomorrow']['count']} ({pollen['tomorrow']['desc']})
Yesterday: {pollen['yesterday']['count']} ({pollen['yesterday']['desc']})
"""
r = requests.post('https://api.pushover.net/1/messages.json', data = {
    'token': os.environ['POLLEN_PUSHOVER_APP_KEY'],
    'user': os.environ['PUSHOVER_USER_KEY'],
    'message': msg,
    'title': title,
    'url': os.getenv('POLLEN_URL', 'https://www.pollen.com'),
    'device': os.environ['PUSHOVER_DEVICE']
})

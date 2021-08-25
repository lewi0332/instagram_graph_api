import requests

url = 'https://graph.facebook.com/v10.0/SOMETHINGHERE/insights?metric=impressions,reach,video_views,saved,engagement&access_token=SOMETHING HERE'


r = requests.get(url)
r = json.loads(r.content)

# Only getting media for IGTV that includes a preview in feed.

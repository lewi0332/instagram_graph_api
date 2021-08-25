from defines import getCreds, makeApiCall
from get_user_media import getUserMedia
import argparse


def getMediaInsights(params):
    """ Get insights for a specific media id

    API Endpoint:
            https://graph.facebook.com/{graph-api-version}/{ig-media-id}/insights?metric={metric}

    Returns:
            object: data from the endpoint

    """
    endpointParams = dict()  # parameter to send to the endpoint
    endpointParams['metric'] = params['metric']  # fields to get back
    endpointParams['access_token'] = params['access_token']  # access token

    url = params['endpoint_base'] + \
        params['latest_media_id'] + '/insights'  # endpoint url

    # make the api call
    return makeApiCall(url, endpointParams, params['debug'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--card_id',
        type=int,
        default=None,
        help='Number of previous days.'
    )
    args = parser.parse_args()
    if args.card_id == None:
        print("\nYou must specify card_id with the flag: --card_id")
        exit()
    card_id = args.card_id
    params = getCreds(card_id)  # get creds
    response = getUserMedia(params)  # get users media from the api

    print("\n---- LATEST POST -----\n")  # section header
    print("\tLink to post:")  # link to post
    print("\t" + response['json_data']['data'][0]['permalink'])  # link to post
    print("\n\tPost caption:")  # post caption
    print("\t" + response['json_data']['data'][0]['caption'])  # post caption
    print("\n\tMedia Type:")  # type of media
    print("\t" + response['json_data']['data']
          [0]['media_type'])  # type of media
    print("\n\tMedia Product:")  # type of media
    print("\t" + response['json_data']['data']
          [0]['media_product_type'])  # type of media
    print("\n\tVideo Title:")  # label
    print("\t" + response['json_data']['data']
          [0]['video_title'])  # Video Title
    print("\n\tPosted at:")  # when it was posted
    print("\t" + response['json_data']['data']
          [0]['timestamp'])  # when it was posted

    for i in range(len(response['json_data']['data'])):
        # store latest post id
        params['latest_media_id'] = response['json_data']['data'][i]['id']

        if 'VIDEO' == response['json_data']['data'][i]['media_type']:  # media is a video
            params['metric'] = 'engagement,impressions,reach,saved,video_views'
        else:  # media is an image
            params['metric'] = 'engagement,impressions,reach,saved'

        # get insights for a specific media id
        response_ = getMediaInsights(params)

        print("\n---- LATEST POST INSIGHTS -----\n")  # section header

        for insight in response_['json_data']['data']:  # loop over post insights
            print("\t" + insight['title'] + " (" + insight['period'] +
                  "): " + str(insight['values'][0]['value']))  # display info

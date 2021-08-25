from defines import getCreds, makeApiCall
import argparse


def getUserStories(params, pagingUrl=''):
    """ Get users media

    API Endpoint:
            https://graph.facebook.com/{graph-api-version}/{ig-user-id}/media?fields={fields}&access_token={access-token}

    Returns:
            object: data from the endpoint

    """

    endpointParams = dict()  # parameter to send to the endpoint
    # fields to get back
    endpointParams['fields'] = 'id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username'
    endpointParams['access_token'] = params['access_token']  # access token

    if ('' == pagingUrl):  # get first page
        url = params['endpoint_base'] + \
            params['instagram_account_id'] + '/stories'  # endpoint url
    else:  # get specific page
        url = pagingUrl  # endpoint url

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
    params['debug'] = 'no'  # set debug
    response = getUserStories(params)  # get users media from the api

    # display page 1 of the posts
    print("\n\n\n\t\t\t >>>>>>>>>>>>>>>>>>>> PAGE 1 <<<<<<<<<<<<<<<<<<<<\n")

    for post in response['json_data']['data']:
        print("\n\n---------- POST ----------\n")  # post heading
        print("Link to post:")  # label
        print(post['permalink'])  # link to post
        print("\nPost caption:")  # label
        try:
            print(post['caption'])  # post caption
        except:
            print('No Caption')
        print("\nMedia type:")  # label
        print(post['media_type'])  # type of media
        print("\nPosted at:")  # label
        print(post['timestamp'])  # when it was posted

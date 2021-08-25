from defines import getCreds, makeApiCall
import argparse


def getUserPages(params):
    """ Get facebook pages for a user

    API Endpoint:
            https://graph.facebook.com/{graph-api-version}/me/accounts?access_token={access-token}

    Returns:
            object: data from the endpoint

    """

    endpointParams = dict()  # parameter to send to the endpoint
    endpointParams['fields'] = 'biography,id,ig_id,followers_count,follows_count,media_count,name,profile_picture_url,username,website'
    endpointParams['access_token'] = params['access_token']  # access token

    url = params['endpoint_base'] + \
        params['instagram_account_id']  # endpoint url

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
    response = getUserPages(params)  # get debug info

    print("\n---- IG PAGE INFO ----\n")  # section heading
    print("Page Name:")  # label
    print(response['json_data']['name'])  # display name
    print("\nPage Followers:")  # label
    print(response['json_data']['followers_count'])  # display category
    print("\nPage Id:")  # label
    print(response['json_data']['id'])  # display id

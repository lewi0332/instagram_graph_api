from defines import getCreds, makeApiCall
import datetime
import argparse


def debugAccessToken(params):
    """ Get info on an access token 

    API Endpoint:
            https://graph.facebook.com/debug_token?input_token={input-token}&access_token={valid-access-token}

    Returns:
            object: data from the endpoint

    """

    endpointParams = dict()  # parameter to send to the endpoint
    # input token is the access token
    endpointParams['input_token'] = params['access_token']
    # access token to get debug info on
    endpointParams['access_token'] = 'SOMETHING HERE'

    url = params['endpoint_base'] + 'debug_token'  # endpoint url

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
    print(card_id)
    params = getCreds(card_id)  # get creds
    params['debug'] = 'yes'  # set debug
    response = debugAccessToken(params)  # hit the api for some data!
    print("\n\nData Access Expires at: ")  # label
    # display out when the token expires
    print(datetime.datetime.fromtimestamp(
        response['json_data']['data']['data_access_expires_at']))

    print("\nToken Expires at: ")  # label
    # display out when the token expires
    print(datetime.datetime.fromtimestamp(
        response['json_data']['data']['expires_at']))

    print("\nScopes Avaialble for this Auth Token: ")  # label
    # display the Scopes
    for i in range(len(response['json_data']['data']['scopes'])):
        print("\t", response['json_data']['data']['scopes'][i])

import requests
import json
from tunnel import query_json


def getCreds(card_id):
    """ Get creds required for use in the applications
    Returns:
            dictonary: credentials needed globally
    """
    temp = query_json(f"""
        SELECT username, facebook_page_id, instagram_facebook_id, instagram_facebook_access_token
        FROM card_authentication_instagrams
        WHERE card_id = {card_id};
        """)

    creds = dict()  # dictionary to hold everything
    # access token for use with all api calls
    creds['access_token'] = temp[0]['instagram_facebook_access_token']
    # client id from facebook app IG Graph API Test
    #TODO
    creds['client_id'] = 'ENTER SOMETHING HERE'
    # client secret from facebook app
    #TODO
    creds['client_secret'] = 'ENTER SOMETHING HERE'
    # base domain for api calls
    creds['graph_domain'] = 'https://graph.facebook.com/'
    creds['graph_version'] = 'v10.0'  # version of the api we are hitting
    creds['endpoint_base'] = creds['graph_domain'] + \
        creds['graph_version'] + '/'  # base endpoint with domain and version
    creds['debug'] = 'no'  # debug mode for api call
    creds['page_id'] = temp[0]['facebook_page_id']  # users page id
    # users instagram account id
    creds['instagram_account_id'] = temp[0]['instagram_facebook_id']
    creds['ig_username'] = temp[0]['username']  # ig usernameN

    return creds


def makeApiCall(url, endpointParams, debug='no'):
    """ Request data from endpoint with params

    Args:
            url: string of the url endpoint to make request from
            endpointParams: dictionary keyed by the names of the url parameters


    Returns:
            object: data from the endpoint

    """

    data = requests.get(url, endpointParams)  # make get request

    response = dict()  # hold response info
    response['url'] = url  # url we are hitting
    response['endpoint_params'] = endpointParams  # parameters for the endpoint
    response['endpoint_params_pretty'] = json.dumps(
        endpointParams, indent=4)  # pretty print for cli
    response['json_data'] = json.loads(
        data.content)  # response data from the api
    response['json_data_pretty'] = json.dumps(
        response['json_data'], indent=4)  # pretty print for cli

    if ('yes' == debug):  # display out response info
        displayApiCallData(response)  # display response

    return response  # get and return content


def displayApiCallData(response):
    """ Print out to cli response from api call """

    print("\nURL: ")  # title
    print(response['url'])  # display url hit
    print("\nEndpoint Params: ")  # title
    # dis(lay params passed to the endpoint
    print(response['endpoint_params_pretty'])
    print("\nResponse: ")  # title
    print(response['json_data_pretty'])  # make look pretty for cli

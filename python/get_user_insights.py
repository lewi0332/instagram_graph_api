from defines import getCreds, makeApiCall
from datetime import datetime, timedelta
import argparse


def getUserInsights(params, METRIC='', PERIOD='', SINCE='', UNTIL='', pagingUrl=''):
    """ Get users media

    Metrics that support lifetime periods will have results returned in an array of 24 hour periods, 
    with periods ending on UTC−07:00.

    METRIC: [audience_city, audience_country, audience_gender_age, audience_locale, email_contacts
            follower_count, get_directions_clicks, impressions, online_followers, phone_call_clicks
            profile_views, reach, text_message_clicks, website_clicks]

    PERIOD: [lifetime, day, week, days_28]

    RANGE:
        SINCE: unix time stamp
        UNTIL: unix time stamp

    API Endpoint:
            https://graph.facebook.com/{graph-api-version}/{ig-user-id}/insights/metric={metric}&period={period}&since={since}&until={until}&access_token={access-token}

    Returns:
            object: data from the endpoint

    """

    endpointParams = dict()  # parameter to send to the endpoint
    # fields to get back
    endpointParams['metric'] = METRIC
    endpointParams['period'] = PERIOD
    if SINCE != '':
        endpointParams['since'] = SINCE
        endpointParams['until'] = UNTIL
    endpointParams['access_token'] = params['access_token']  # access token

    if ('' == pagingUrl):  # get first page
        url = params['endpoint_base'] + \
            params['instagram_account_id'] + '/insights'  # endpoint url
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
        help='Card ID.'
    )
    parser.add_argument(
        '--metric',
        type=str,
        nargs='+',
        help="Metrics to return."
    )
    parser.add_argument(
        '--period',
        type=str,
        default=None,
        help='Period of time to aggregate results '
    )
    parser.add_argument(
        '--since',
        type=int,
        default=30,
        help='Single Integer refering to Days ago'
    )
    parser.add_argument(
        '--until',
        type=int,
        default=1,
        help='Single Integer refering to Days ago'
    )
    args = parser.parse_args()
    if args.card_id == None:
        print("\nYou must specify card_id with the flag: --card_id")
        exit()
    card_id = args.card_id
    params = getCreds(card_id)  # get creds
    since = datetime.now() - timedelta(days=args.since)
    since = int(since.timestamp())
    until = datetime.now() - timedelta(days=args.until)
    until = int(until.timestamp())
    params['debug'] = 'no'  # set debug
    # get users insights from the api
    response = getUserInsights(
        params, args.metric, args.period, since, until)

    # display page 1 of the posts
    print("\n\n\n\t\t\t >>>>>>>>>>>>>>>>>>>> PAGE 1 <<<<<<<<<<<<<<<<<<<<\n")

    print("\n---- DAILY USER ACCOUNT INSIGHTS -----\n")  # section header

    # loop over user account insights
    for insight in response['json_data']['data']:
        print("\t" + insight['title'] + " (" + insight['period'] +
              "): " + str(insight['values'][0]['value']))  # display info

        for value in insight['values']:  # loop over each value
            # print out counts for the date
            print("\t\t" + value['end_time'] + ": " + str(value['value']))

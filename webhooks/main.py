from flask import Flask, request
from datetime import datetime
import psycopg2
from psycopg2 import sql
import os
from insert_query import post_insert

DB = os.environ['RDS_DB']

app = Flask(__name__)

VERIFY_TOKEN = os.environ['RDS_DB']  # <paste your verify token here>
PAGE_ACCESS_TOKEN = ''  # paste your page access token here>"


def get_payload(request):
    """This is the function to insert the request into SQL"""
    try:
        conn = psycopg2.connect(DB)
    except psycopg2.Error as e:
        print('Error: Could not make connection to the Postgres Database')
        print(e)
        # TODO Convert to logger
    try:
        cur = conn.cursor()
    except psycopg2.Error as e:
        print("Error could not get cursor to the Database")
        print(e)
        # TODO Convert to logger

        conn.set_session(autocommit=True)
        payload = request.json
        for x in payload:
            post = {}
            post['id'] = x['entry'][0]['id']
            post['published_at'] = datetime.fromtimestamp(
                x['entry'][0]['time'])
            post['media_id'] = x['entry'][0]['changes'][0]['value']['media_id']
            post['exits'] = int(x['entry'][0]['changes'][0]['value']['exits'])
            post['replies'] = int(x['entry'][0]['changes']
                                  [0]['value']['replies'])
            post['reach'] = int(x['entry'][0]['changes'][0]['value']['reach'])
            post['taps_forward'] = int(
                x['entry'][0]['changes'][0]['value']['taps_forward'])
            post['taps_back'] = int(
                x['entry'][0]['changes'][0]['value']['taps_back'])
            post['impressions'] = int(
                x['entry'][0]['changes'][0]['value']['impressions'])
            try:
                cur.execute(sql.SQL(post_insert).format(
                    table=sql.Identifier('story_insights')), post)
            except Exception as e:
                # TODO Convert to logger
                print('could not Update reach table', e)
        cur.close()
    return "This is a dummy response to '{}'".format(message)


def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        print(req.args.get("hub.challenge"))
        return req.args.get("hub.challenge")
    else:
        return "incorrect"


def temp_print(req):
    print(req.json)
    return "200 OK HTTPS"


@app.route("/webhooks", methods=['GET', 'POST'])
def listen():
    """This is the main function flask uses to 
    listen at the `/webhook` endpoint"""
    if request.method == 'GET':
        return verify_webhook(request)

    if request.method == 'POST':
        try:
            temp_print(request)
            # TODO add logger
            return "200 OK HTTPS"
        except:
            return "400"

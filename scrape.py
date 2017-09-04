#!/usr/bin/env python
import csv
import time
import yaml

from datetime import datetime, timedelta
from slacker import Slacker

with open("config.yaml", 'r') as config_file:
    config = yaml.load(config_file)
TOKEN = config['token']
CHANNEL_NAME = config['channel_name']
WEEKS = datetime.now() - timedelta(weeks=config.get('weeks', 12))


def timestamp(dt, epoch=datetime(1970,1,1)):
    td = dt - epoch
    return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6

def run():
    slack = Slacker(TOKEN)

    groups = slack.groups.list().body['groups']
    for group in groups:
        if group['name'] == CHANNEL_NAME:
            partner_channel = group

    messages = []
    try:
        oldest = WEEKS.timestamp()
    except AttributeError:
        # Python2
        oldest = timestamp(WEEKS)

    print("Fetching messages...")
    history = slack.groups.history(channel=partner_channel['id'], oldest=oldest, count=1000).body
    messages.extend(history['messages'])

    while history['has_more']:
        if not history['ok']:
            print("Something went wrong... here's what the Slack api sent back:")
            print(history)

        print("Fetching more messages, starting from %s..." % datetime.fromtimestamp(float(oldest)))

        history = slack.groups.history(channel=partner_channel['id'], oldest=oldest, count=1000, inclusive=0).body
        oldest = history['messages'][0]['ts']
        messages.extend(history['messages'])

    print("Total number of messages since %s: %s" % (WEEKS, len(messages)))

    users = {}
    for message in messages:
        if 'user' in message and message['user'] != 'USLACKBOT':
            user_id = message['user']
        elif message.get('subtype') == 'file_comment':
            message = message['comment']
            user_id = message['user']

        if user_id not in users:
            user_info = slack.users.info(user=user_id).body
            users[user_id] = dict(email=user_info['user']['profile']['email'], messages=[])

        users[user_id]['messages'].append(message)

    print("Total users: %s" % len(users))
    print("User breakdown:")
    for user, user_details in users.items():
        print("%s: %s" % (user_details['email'], len(user_details['messages'])))

    output = [{'email': values['email'], 'messages': len(values['messages'])} for key, values in users.items()]
    with open('slack_results.csv', 'w') as f:
        w = csv.DictWriter(f, output[0].keys())
        w.writeheader()
        w.writerows(output)


if __name__ == "__main__":
    run()

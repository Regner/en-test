

import os
import logging

from gcloud import pubsub

from flask import Flask, request
from flask_restful import Resource, Api, reqparse


app = Flask(__name__)
api = Api(app)

# App Settings
app.config['BUNDLE_ERRORS'] = True

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
app.logger.addHandler(stream_handler)

# PubSub Settings
PS_CLIENT = pubsub.Client()
PS_TOPIC = PS_CLIENT.topic(os.environ.get('NOTIFICATION_TOPIC', 'send_notification'))

if not PS_TOPIC.exists():
    PS_TOPIC.create()


class TestResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('subtitle', type=str, required=True)
        parser.add_argument('url', type=str, required=True)

        args = parser.parse_args(strict=True)
        
        app.logger.info('Sending test notification with the following args: {}.'.format(args))
        
        PS_TOPIC.publish(
            '',
            url=args['url'],
            title=args['title'],
            subtitle=args['subtitle'],
            service='en-test',
            topic='testing',
        )
        
        return {}, 201
    
api.add_resource(TestResource, '/external/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

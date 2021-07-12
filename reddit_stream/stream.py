#!/usr/bin/env python3

# Stream comments from a subreddit and write to kafka topic named `comments`.

from dotenv import load_dotenv
import os
import click
import praw
from kafka import KafkaProducer
import json
import logging

from reddit import comment_to_json

load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent="your user agent",
)

print('Kafka bootstrap server set to ' + os.getenv('KAFKA_BOOTSTRAP_SERVER'))

producer = KafkaProducer(bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVER'), api_version=(2, 8, 0))

@click.command()
@click.option('--subreddit', help='Subbreddit to stream from (wallstreebets by default)',
              default='wallstreetbets')
@click.option('--quiet', default=False, is_flag=True)
def stream_subreddit(subreddit, quiet):
    '''Stream comments from the given subreddit and write to kafka'''
    logging.info(f'Streaming comments from subreddit r/{subreddit}')
    
    for comment in reddit.subreddit(subreddit).stream.comments():
        payload = json.dumps(comment_to_json(comment)).encode()
        if not quiet:
            print(payload)
        future = producer.send('comments', payload)
        # logger.debug(payload)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    stream_subreddit()
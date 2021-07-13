#!/usr/bin/env python3

import logging
from dotenv import load_dotenv
import json
import os
import time
from flair.models import TextClassifier
from flair.data import Sentence
from flair.models import SequenceTagger

from termcolor import colored
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from datetime import datetime
import pdb

load_dotenv()

# logging.basicConfig(level=logging.INFO)

classifier = TextClassifier.load("en-sentiment")
tagger = SequenceTagger.load("ner-fast")


def label_to_float(label):
    """Convert flair sentiment label to float"""
    if str(label.value) == "POSITIVE":
        return label.score
    else:
        return -label.score


es = Elasticsearch(hosts=[os.getenv("ES_HOST")])
consumer = KafkaConsumer(bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVER"))
consumer.subscribe(["comments"])
logging.info("Connected to kakfa")

for comment in consumer:
    comment = json.loads(comment.value.decode())
    # logging.info(doc)
    sentence = Sentence(comment["body"])
    classifier.predict(sentence)
    sent = label_to_float(sentence.labels[0])
    tagger.predict(sentence)

    comment["sentiment"] = sent
    timestamp = datetime.utcfromtimestamp(comment["created_utc"])
    comment["created_utc"] = timestamp

    logging.info(colored(sent, "green"))
    logging.info(sentence)
    has_keyword = False
    for idx, entity in enumerate(sentence.get_spans("ner")):
        # pdb.set_trace()
        if entity.tag not in ("PER", "ORG"):
            continue
        has_keyword = True
        keywords = {
            "comment_id": comment["id"],
            "author": comment["author"],
            "keyword_id": idx,
            "text": entity.text,
            "tag": entity.tag,
            "created_utc": comment["created_utc"],
        }
        logging.debug(keywords)
        es.index(index="comment_keywords", body=keywords)
    if has_keyword:
        es.index(
            index="logs-comments",
            body={
                "author": comment["author"],
                "message": comment["body"],
                "timestamp": comment["created_utc"],
            },
        )
    es.index(index="sentiments", id=comment["id"], body=comment)

#!/usr/bin/env python3

from dotenv import load_dotenv
import os
from elasticsearch import Elasticsearch
from kafka import KafkaConsumer, consumer
import logging
import json
from datetime import datetime

load_dotenv()
logging.basicConfig(level=logging.INFO)

es = Elasticsearch(hosts=[os.getenv("ES_HOST")])
logging.info("Connected to elasticsearch")

consumer = KafkaConsumer(bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVER"))
logging.info("Connected to kafka")

consumer.subscribe(["comments"])
for comment in consumer:
    doc = json.loads(comment.value.decode())
    doc["created_utc"] = datetime.utcfromtimestamp(doc["created_utc"])
    logging.info(doc)
    res = es.index(index="comments", id=doc["id"], body=doc)

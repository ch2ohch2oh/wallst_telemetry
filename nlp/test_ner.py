#!/usr/bin/env python3

from flair.models import TextClassifier
from flair.data import Sentence
from flair.models import SequenceTagger


classifier = TextClassifier.load("en-sentiment")
tagger = SequenceTagger.load("ner-fast")

sentence = Sentence("CLOV to the moon!!! CLOV CLOV CLOV")
classifier.predict(sentence)
tagger.predict(sentence)

print(sentence.labels)
print(sentence.get_spans("ner"))

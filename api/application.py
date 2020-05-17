import time
import os
import certifi
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from flask import Flask

application = Flask(__name__)

# Connect to cluster over SSL using auth for best security:
es_header = [{
    'host': os.environ.get('ES_HOST'),
    'port': os.environ.get('ES_PORT'),
    'use_ssl': True,
    'ca_certs': certifi.where(),
    'http_auth': (os.environ.get('ES_AUTH_USER'), os.environ.get('ES_AUTH_PWD'))
}]

es = Elasticsearch(es_header)


@application.route('/words_for_letter/<letter>')
def fetch_words_for_letter(letter):
    query = Search(using=es, index='words').query(
        "prefix", word=letter)[0:10000]
    res = query.execute()
    ten_words = list(word_doc['_source']['word']
                     for word_doc in res['hits']['hits'])

    return {'count': res['hits']['total']['value'], 'time': time.time(), 'words': ten_words}


@application.route('/words_all')
def fetch_words_for_all_letters():
    query = Search(using=es, index='words').query(
        "match_all")[0:10000]
    res = query.execute()
    ten_words = list(word_doc['_source']['word']
                     for word_doc in res['hits']['hits'])

    return {'count': res['hits']['total']['value'], 'time': time.time(), 'words': ten_words}

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    # application.debug = True
    application.run()


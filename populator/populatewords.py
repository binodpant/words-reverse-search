from elasticsearch import Elasticsearch
import certifi
import json

# Connect to cluster over SSL using auth for best security:
es_header = [{
    'host': 'words-reverse-match-5971522899.us-east-1.bonsaisearch.net',
    'port': 443,
    'use_ssl': True,
    'ca_certs': certifi.where(),
    'http_auth': ('d3a4bikzsa', 'lm2gdpetci')
}]

es = Elasticsearch(es_header)

# read all words fro dict file
dict_file = open('corncob_lowercase.txt', 'r')
words_dict_from_file = dict_file.read()
json_words = words_dict_from_file.split("\n")
json_words = [i for i in json_words if i]


def reindex_byword(words_list):
    '''returns a new dict where each key
       is an alphabet letter and points to 
       a value that is a dictionary of all words
       that start with that letter
       '''
    final_dict = dict()
    for k in words_list:
        # k is the word being processed
        first_letter = k[0]
        if not first_letter:
            continue
        if first_letter in final_dict:
            final_dict[first_letter].append(k)
        else:
            final_dict[first_letter] = [k]
    return final_dict


final_dict = reindex_byword(json_words)

to_store_list = []
for word in json_words:
    reversed = word[::-1]
    last_letter = word[-1]
    if not last_letter:
        continue
    if reversed == word:
        continue
    # grab the list of words corresponding to last_letter
    dict_for_letter = final_dict[last_letter]
    if reversed in dict_for_letter:
        to_store_list.append(word)

# now to_store_list contains all words which have matching reversals in the entire dictionary!
# for now let's store as multi docs, where each doc contains words starting with a letter

# each key of final_dict is a letter of the alphabet
index = 0
es.indices.create(index="words", ignore=400)
for word in to_store_list:
    # create index for this letter
    letter = word[0]
    # store all words under this index
    es.index(index="words", doc_type='word', id=index,
             body={'word': word})
    print(f"{index}:Saved words for ", letter, " ", word, " into the index")
    index += 1
print(f'Saved {index} words with reverse matches in the dictionary, into the index "words"')
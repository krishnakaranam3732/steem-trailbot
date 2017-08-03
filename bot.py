from piston import Steem
from piston.post import Post
from piston.blockchain import Blockchain
from piston.amount import Amount
from piston.block import Block
from pistonbase import transactions
from pistonapi.steemnoderpc import SteemNodeRPC
import json
import math
import sys
import time
import os
#mongodb
import pymongo

from pymongo import MongoClient

#change this to needed url
client = MongoClient('mongodb://naughtyprince5678:heroku_4j3zgpqc@ds137207.mlab.com:37207/heroku_4j3zgpqc')

#create this db
db = client.heroku_4j3zgpqc

#create collection
collection = db.iamgrootbot_collection

steemPostingKey = os.environ.get('steemPostingKey')
steemAccountName = os.environ.get('steemAccountName')

votewith = steemAccountName
wif = steemPostingKey
node = 'ws://steemd.pevo.science:8090'

print('voting with: '+votewith+ ' and wif: '+wif)
steem = Steem(wif = steemPostingKey)
tags = ["funny", "meme", "bot"]
past_authors = ["riounh34","alex-icey","amvanaken","djneontiger","midgetspinner","bubusik","amirl","hauntedbrain","riounh34","dtworker"]

for p in steem.stream_comments():
    for x in tags:
        try:
            if x in p["tags"] and collection.find({"author": p["author"]}).count() != 1 and p["author"] not in past_authors:
                print(p.get_comments())
		print("Author of post: "+p["author"])
                post = p.reply(body = "I am Groot! :D", author = steemAccountName)
		print("comment on post done.")
		autherofpost = {"author": p["author"]}
		insert_id = collection.insert_one(autherofpost).inserted_id
		print("inserted id :"+ str(insert_id))
		p.upvote(weight=+0.01, voter = steemAccountName)
		print("Upvote done.")
		print(post)
		past_authors.append(post['operations'][0][1]['parent_author'])
		time.sleep(40)
		print("Past Authors: "+past_authors)

        except:
            print("Failed to comment on post.")

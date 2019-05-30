#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# pip install TwitterAPI

# http://www.moongiant.com/fullmoons/2018/

import sys
from json import load
from time import localtime
from time import strftime
from os import path
from os import listdir
from random import randint
from TwitterAPI import TwitterAPI
from mastodon import Mastodon
from pprint import pprint

local_time = localtime()

year =  strftime("%Y", local_time)

file = open(sys.path[0]+"/ilargia-"+year+".json")
j = load(file)

local_time = strftime("%Y-%m-%d", local_time)

found = False
for date in j:
        if date == local_time:
                found = True

if found == False:
	sys.exit()

# ze motatako irudidxek okinguz kontutan
allow_extension = ['.mp4', '.gif']

# irudiaren path-a hartu
#image_path = path.dirname(path.realpath(__file__))+"/images"
image_path = sys.path[0]+"/images"

if path.isdir(image_path):
	files = listdir(image_path)
else:
	print("Karpeta "+image_path+" ez da existitzen")
	sys.exit()

# irudi danak images dict-en sartun
images = {}
j = 0
for i in files:
	file_path = path.join(image_path, i)
	if path.isfile(file_path):
		extension = path.splitext(file_path)[1]
		if extension.lower() in allow_extension:
			images[j] = file_path
			j = j+1

# twitterrera argazkidxe idxen

#r = 0
#images = [sys.path[0]+"/ilargi_gorri.jpg"]

mastodon = Mastodon(
    access_token = sys.path[0]+"/mastodon.credentials",
    api_base_url = 'https://mastodon.jalgi.eus'
)

# ikusi ia baten bat badauen
images_all = images
len = len(images.keys())
if len>0:
	r = randint(0, j-1)
	file = images[r]
	a = mastodon.media_post(file);
	images = []
	images.append([a.id])
else:
	images = []

title = 'ilargi betie... 🐺🌕 #zitalbot'

m = mastodon.status_post(title, None, images)

data = open(images_all[1], 'rb')
data = data.read()

#title = title.decode('utf-8')+"\n"

file = open(sys.path[0]+'/twitter.credentials')
j = load(file)

api = TwitterAPI(j['CONSUMER_KEY'], j['CONSUMER_SECRET'], j['ACCESS_TOKEN_KEY'], j['ACCESS_TOKEN_SECRET'])
r = api.request('media/upload', None, {'media': data})
media_id = r.json()['media_id']

r = api.request('statuses/update', {'status':title+m.url, 'media_ids':media_id})

if r.status_code == 200:
	print("Txioa ondo bidali da ;)")
else:
	print("Errorea txioa bidaltzerakoan status code: "+r.status_code)

sys.exit()

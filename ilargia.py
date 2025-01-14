#!/usr/bin/python3
# -*- coding: utf-8 -*-
#

import sys
from   json     import load
from   time     import localtime
from   time     import strftime
from   time     import sleep
from   os       import path
from   os       import listdir
from   random   import randint
from   mastodon import Mastodon

local_time = localtime()
year       = strftime("%Y", local_time)

with open(f"{sys.path[0]}/ilargia-{year}.json", 'r') as f:
	j = load(f)

local_time = strftime("%Y-%m-%d", local_time)
#local_time = "2025-12-05"

info = None
for data in j:
   if data['date'] == local_time:
      info = data

if info == None:
   sys.exit(1)

# ze motatako irudidxek okinguz kontutan
allow_extension = ['.mp4', '.gif']

# irudiaren path-a hartu
#image_path = path.dirname(path.realpath(__file__))+"/images"
image_path = f"{sys.path[0]}/images"

if path.isdir(image_path):
   files = listdir(image_path)
else:
   print(f"Karpeta {image_path} ez da existitzen")
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

#mastodon
with open(f"{sys.path[0]}/mastodon.json", 'r') as f:
   mastodon_config = load(f)

mastodon = Mastodon(
   access_token = mastodon_config['token'],
   api_base_url = mastodon_config['instance']
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

# 30 segundu utziko diogu mastodonera irudi/bideoa igotzeko...
sleep(30)

title = f"{info['name']} iletargi betie {info['emoji']}🌕\n\n#zitalbot"
m     = mastodon.status_post(title, None, images)
data  = open(images_all[2], 'rb') # 01.gif
data  = data.read()

sys.exit()

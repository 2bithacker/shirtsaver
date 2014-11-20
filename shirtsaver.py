#!/usr/bin/env python

import requests, json, pprint
import os.path

from PIL import Image,ImageStat
from StringIO import StringIO

woot_api = 'http://api.woot.com/2'
api_key = '8ad8fcd8c6bd46bebddbca0e9fea0215'
api_sec = '6211aa6bbbad42c1a2bf7e6bf19e30ad'
savedir = '/Users/chip/wootshirts'

args = {'site': 'shirt.woot.com', 'key': api_key, 'eventType': 'daily'}
#args = {'site': 'shirt.woot.com', 'key': api_key, 'eventType': 'Reckoning'}

r = requests.get(woot_api+'/events.json', params=args)

data = json.loads(r.text)

imgurls = []

for offer in data[0]['Offers']:
	for photo in offer['Photos']:
		if 'fullsize-1' in photo['Tags']:
			imgurls.append(photo['Url'])
		if 'fullsize-0' in photo['Tags']:
			imgurls.append(photo['Url'])

for url in imgurls:
	r = requests.get(url)
	i = Image.open(StringIO(r.content))
	topcorner = i.crop( (0, 0, 225, 60) )
	colors = topcorner.getcolors()
	if colors == None or len(colors) != 1:
		savefile = "%s/%s" % (savedir, url[url.rfind('/')+1:])
		if not os.path.isfile(savefile):
			i.save("%s/%s" % (savedir, url[url.rfind('/')+1:]))

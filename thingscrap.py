#!/usr/bin/env python -t
# -*- coding: utf-8 -*-
#
# thingscrap.py : 09/10/11
# g.revaillot, revaillot@archos.com
#

import string
import sys
import urllib
import re
import os 
from BeautifulSoup import BeautifulSoup

if (len(sys.argv) < 2):
	sys.exit(sys.argv[0] + " thingiverse id or object url")

obj = sys.argv[1]
if obj.startswith("http://"):
	objurl=obj
	obj=objurl.split(":")[-1]
else:
	objurl="http://www.thingiverse.com/thing:%s" % (obj)

print "fetching object %s (%s)" % (obj, objurl)

soup = BeautifulSoup(urllib.urlopen(objurl))

title = soup.title.renderContents().split(" - Thingiverse")[0]

urls = set()
for dl in soup.findAll(href=re.compile("^/download:")):
	urls.add("http://thingiverse.com/"+dl["href"])

print "got thing \"%s\", %s parts" % (title, len(urls))

folder="%s-Thingiverse_%s" % (title.replace(" ", "_").lower(), obj)

try:
	os.mkdir(folder)
except os.error:
	pass

for url in urls:
	redir = urllib.urlopen(url).geturl()
	fn = redir.split("/")[-1]
	print "downloading %s at %s/%s" % (fn, folder, fn)
	urllib.urlretrieve(redir, folder + "/" + fn)

#mkdir 

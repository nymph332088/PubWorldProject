# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
class PaperItem(Item):
	year = Field()    # Year of Paper: values can take from (2012,2013, 2014)
	conf = Field()    # Always 'CIKM'
	ptrack = Field()  # Paper Track: values can take from (DB, IR, KM)
	ptype = Field()   # Paper Type: values can take from (Regular, poster, long, short, demo)
	pid = Field()     # Paper number given the conference
	pname = Field()   # Paper Name
	authors = Field() # Paper authors a list of dictionary. Each author has first name, last name and affliation

class CommiteeItem(Item):
	year = Field()       # Year of Paper: values can take from (2012,2013, 2014)
	conf = Field()       # Always 'CIKM'
	ctrack = Field()     # Commitee member track: values can take from (DB, IR, KM)
	ctitle = Field()     # Commitee member title: values can take from (senior or junior)
	fname = Field()      # Commitee first name
	lname = Field()      # Commitee last name
	afl = Field()        # Commitee affiliation
	cotherinfo = Field() # Such as interest


	
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request  
from scrapy.exceptions import DropItem  
from scrapy.contrib.pipeline.images import ImagesPipeline  
import time  
import MySQLdb  
import MySQLdb.cursors
import socket
import select
import sys
import os
import errno

class Pipelines(object):
	def __init__(self):
		self.dbpool = adbapi.ConnectionPool('MySQLdb',
			db = 'PubWorld',
			user = 'root',
			passwd = '1234',
			cursorclass = MySQLdb.cursors.DictCursor,
			charset = 'utf8',
			use_unicode = False
		)

	def process_item(self, item, spider):
		if 'papers' in getattr(spider, 'pipelines', [])[0]:
			query = self.dbpool.runInteraction(self._conditional_insert_paper, item, spider)
		elif 'pcs' in getattr(spider, 'pipelines', [])[0]:
			query = self.dbpool.runInteraction(self._conditional_insert_pc, item, spider)
		return item

	def _conditional_insert_paper(self, tx, item, spider):
		tx.execute("""SELECT PaperID FROM Papers WHERE Title = %s""", (item['pname']))
		ret = tx.fetchone()
		if ret:
			pId = ret['PaperID']
			spider.log("The paper with pId %s is already existed" % pId)
		else:
			tx.execute("""
				INSERT INTO Papers(PaperNo, Title, Type, Track, Year) VALUES (%s, %s, %s, %s, %s)
			""", (item['pid'], item['pname'], item['ptype'], item['ptrack'], item['year']))
			spider.log("Item stored in papers: %s" % item['pid'])
			tx.execute("""SELECT LAST_INSERT_ID()""")
			pId = tx.fetchone()['LAST_INSERT_ID()']

		aIds = list()
		for ele in item['authors']:
			firstName = ele['firstName']
			lastName = ele['lastName']
			affiliation = ele['affiliation']

			# conn.execute("""SELECT EXISTS (SELECT 1 FROM Authors WHERE firstName = %s AND lastName = %s)""", (item['firstName'], item['lastName']))
			# ret = conn.fetchone()[0]

			tx.execute("""SELECT AuthorID FROM Authors WHERE FirstName = %s AND LastName = %s AND Affiliation = %s""", (firstName, lastName, affiliation))
			ret = tx.fetchone()

			if ret:
				aIds.append(ret['AuthorID'])
			else:
				tx.execute("""
					INSERT INTO Authors(FirstName, LastName, Affiliation) VALUES (%s, %s, %s)
				""", (firstName, lastName, affiliation))
				spider.log("Item stored in authors: %s" % lastName)
				tx.execute("""SELECT LAST_INSERT_ID()""")
				aId_ret = tx.fetchone()['LAST_INSERT_ID()']
				aIds.append(aId_ret)

		year = item['year']
		for index, aId in enumerate(aIds):	
			tx.execute("""SELECT * FROM Paper_Author WHERE PaperID = %s AND AuthorID = %s""", (pId, aId))
			ret = tx.fetchone()

			if ret:
				spider.log("The pair %s and %s is already existed. " % (pId, aId))
			else:
				tx.execute("""
					INSERT INTO Paper_Author(PaperID, AuthorID, ConfName, Year, AuthorPos) VALUES (%s, %s, 'CIKM', %s, %s)
				""", (pId, aId, year, index+1))
				spider.log("The pair %s and %s is already inserted into PaperAuthor. " % (pId, aId))


	def _conditional_insert_pc(self, tx, item, spider):
		firstName = item['fname']
		lastName = item['lname']
		affiliation = item['afl']

		tx.execute("""SELECT PCMemberID FROM PCMembers WHERE FirstName = %s AND LastName = %s AND Affiliation = %s""", (firstName, lastName, affiliation))
		ret = tx.fetchone()

		if ret:
			pcid = ret['PCMemberID']
			spider.log("The paper with lastName %s is already existed" % lastName)
		else:
			tx.execute("""
				INSERT INTO PCMembers(FirstName, LastName, Affiliation) VALUES (%s, %s, %s)
			""", (firstName, lastName, affiliation))
			spider.log("Item stored in pcmembers: %s" % lastName)
			tx.execute("""SELECT LAST_INSERT_ID()""")
			pcid = tx.fetchone()['LAST_INSERT_ID()']

		year = item['year']
		title = item['ctitle']
		track = item['ctrack']
		tx.execute("""SELECT * FROM PC_Conf WHERE PCMemberID = %s AND Year = %s AND Track = %s AND Title = %s""", (pcid, year, title, track))
		ret = tx.fetchone()
		if ret:
			spider.log("The pair %s and %s is already existed. " % (pcid, year))
		else:
			tx.execute("""
				INSERT INTO PC_Conf(PCMemberID, Year, ConfName, Track, Title) VALUES (%s, %s, 'CIKM', %s, %s)
			""", (pcid, year, title, track))
			spider.log("The pair %s and %s is already inserted into PaperAuthor. " % (pcid, year))

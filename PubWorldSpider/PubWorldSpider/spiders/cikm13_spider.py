from scrapy.spider import BaseSpider
from scrapy.selector import Selector	
from PubWorldSpider.items import PaperItem, CommiteeItem

class PaperSpider(BaseSpider):
	pipelines= ['papers']
	name = "paperspider13"
	allowed_domains = ["fudan.edu.cn"]
	start_urls = [
	"http://www.cikm2013.org/accepted.php/"
	]
	def parse(self, response):
		sel = Selector(response)
		filename = '13paper'
		f = open(filename,'wb')
		tracktypes = [{'tr':'IR', 'ty': 'Full'}, {'tr':'IR', 'ty': 'Short'}, {'tr':'KM', 'ty': 'Full'},{'tr':'KM', 'ty': 'Short'},{'tr':'DB', 'ty': 'Full'},{'tr':'DB', 'ty': 'Short'}]
		paperuls = sel.xpath("//ul")
		paperuls = paperuls[:6]
		items = []
		for index, ul in enumerate(paperuls):
			ptrack = tracktypes[index]['tr']
			ptype = tracktypes[index]['ty']
			lists = ul.xpath(".//li/text()").extract()
			# Or lists = ul.xpath("li/text()").extract()
			print >>f, len(lists), ptrack, ptype
			for count, paperstr in enumerate(lists):
				item = PaperItem()
				item['year'] = 2013
				item['conf'] = 'CIKM'
				item['ptrack'] = ptrack
				item['ptype'] = ptype
				item['pid'], item['pname'], item['authors'] = self.paperStrTokenize(paperstr, index)
				items.append(item)
				# print >>f, item 
		return items
	def paperStrTokenize(self, paperstr, index):
		strdelete = ['&quot;','&nbsp;','&eacute;','&uuml;','&ccedil','&aacute;','&amp;']
		for substr in strdelete:
			paperstr.replace(substr,"")
		firstlist = paperstr.split(',')

		pid = firstlist[0].split()[-1].encode('ascii','ignore')
		name = " ".join(firstlist[1].split()).encode('ascii','ignore')
		joinstr = ",".join(firstlist[2:]).split(";")
		authors = []
		for author in joinstr:
			authordict = {}
			if "," in author:
				authordict["firstName"] = " ".join(author.split(",")[0].split()[:-1]).title().encode('ascii','ignore')
				authordict['lastName'] = " ".join(author.split(",")[0].split()[-1:]).title().encode('ascii','ignore')
				authordict['affiliation'] = " ".join(author.split(",")[1].split()).encode('ascii','ignore')
			else:
				authordict["firstName"] = " ".join(author.split()[:-1]).title().encode('ascii','ignore')
				authordict["lastName"] = " ".join(author.split()[-1:]).title().encode('ascii','ignore')
				authordict["affiliation"] = ""
			authors.append(authordict)
		return pid, name, authors


class CommiteeSpider(BaseSpider):
	pipelines= ['pcs']
	name = "commiteespider13"
	allowed_domains = ["fudan.edu.cn"]
	start_urls = [
	"http://www.cikm2013.org/pcmembers.php"
	]
	def parse(self, response):
		sel = Selector(response)
		filename = '13commitee'
		f = open(filename,'wb')
		tracktitles = [{'tr':'KM', 'tl': 'Senior'}, {'tr':'KM', 'tl': 'Junior'}, {'tr':'IR', 'tl': 'Senior'}, {'tr':'IR', 'tl': 'Junior'}, {'tr':'DB', 'tl': 'Senior'}, {'tr':'DB', 'tl': 'Junior'}]
		pculs = sel.xpath("//ul")
		pculs = pculs[:6]
		items = []
		for index, ul in enumerate(pculs):
			ctrack = tracktitles[index]['tr']
			ctitle = tracktitles[index]['tl']
			lists = ul.xpath(".//li/text()").extract()
			# Or lists = ul.xpath("li/text()").extract()
			print >>f, len(lists), ctrack, ctitle
			for count, pcstr in enumerate(lists):
				item = CommiteeItem()
				item['year'] = 2013
				item['conf'] = 'CIKM'
				item['ctrack'] = ctrack
				item['ctitle'] = ctitle
				item['fname'], item['lname'], item['afl'], item['cotherinfo'] = self.pcStrTokenize(pcstr, index)
				items.append(item)
				# print >>f, item
		return items
	
	def pcStrTokenize(self, pcstr, index):
		strdelete = ['&quot;','&nbsp;','&eacute;','&uuml;','&ccedil','&aacute;','&amp;']
		for substr in strdelete:
			pcstr.replace(substr,"")
		firstlist = pcstr.split(',')

		fname = " ".join(firstlist[0].split()[:-1]).title().encode('ascii','ignore')
		lname = " ".join(firstlist[0].split()[-1:]).title().encode('ascii','ignore')
		afl = " ".join(",".join(firstlist[1:]).split()).encode('ascii','ignore')
		cotherinfo = ""
		return fname, lname, afl, cotherinfo

class DemoSpider(BaseSpider):
	pipelines= ['papers']
	name = "demospider13"
	allowed_domains = ["fudan.edu.cn"]
	start_urls = [
	"http://www.cikm2013.org/accepted_demos.php"
	]
	def parse(self, response):
		sel = Selector(response)
		filename = '13demo'
		f = open(filename,'wb')
		paperuls = sel.xpath("//ul")
		paperuls = paperuls[0]
		items = []
		lists = paperuls.xpath(".//li/text()").extract()
		# Or lists = ul.xpath("li/text()").extract()
		print >>f, len(lists)
		for count, paperstr in enumerate(lists):
			item = PaperItem()
			item['year'] = 2013
			item['conf'] = 'CIKM'
			item['ptrack'] = ''
			item['ptype'] = 'Demo'
			item['pid'], item['pname'], item['authors'] = self.paperStrTokenize(paperstr, 0)
			items.append(item)
			# print >>f, item 
		return items
		
	def paperStrTokenize(self, paperstr, index):
		strdelete = ['&quot;','&nbsp;','&eacute;','&uuml;','&ccedil','&aacute;','&amp;']
		for substr in strdelete:
			paperstr.replace(substr,"")
		firstlist = paperstr.split(',')

		pid = firstlist[0].split()[-1].encode('ascii','ignore')
		name = " ".join(firstlist[1].split()).encode('ascii','ignore')
		joinstr = ",".join(firstlist[2:]).split(";")
		authors = []
		for author in joinstr:
			authordict = {}
			if "," in author:
				authordict["firstName"] = " ".join(author.split(",")[0].split()[:-1]).title().encode('ascii','ignore')
				authordict['lastName'] = " ".join(author.split(",")[0].split()[-1:]).title().encode('ascii','ignore')
				authordict['affiliation'] = " ".join(author.split(",")[1].split()).encode('ascii','ignore')
			else:
				authordict["firstName"] = " ".join(author.split()[:-1]).title().encode('ascii','ignore')
				authordict["lastName"] = " ".join(author.split()[-1:]).title().encode('ascii','ignore')
				authordict["affiliation"] = ""
			authors.append(authordict)
		return pid, name, authors

class PosterSpider(BaseSpider):
	pipelines= ['papers']
	name = "posterspider13"
	allowed_domains = ["fudan.edu.cn"]
	start_urls = [
	"http://www.cikm2013.org/accepted_posters.php"
	]
	def parse(self, response):
		sel = Selector(response)
		filename = '13poster'
		f = open(filename,'wb')
		paperuls = sel.xpath("//ul")
		paperuls = paperuls[0]
		items = []
		lists = paperuls.xpath(".//li/text()").extract()
		# Or lists = ul.xpath("li/text()").extract()
		print >>f, len(lists)
		for count, paperstr in enumerate(lists):
			item = PaperItem()
			item['year'] = 2013
			item['conf'] = 'CIKM'
			item['ptrack'] = ''
			item['ptype'] = 'Poster'
			item['pid'], item['pname'], item['authors'] = self.paperStrTokenize(paperstr, 0)
			items.append(item)
			# print >>f, item 
		return items

	def paperStrTokenize(self, paperstr, index):
		strdelete = ['&quot;','&nbsp;','&eacute;','&uuml;','&ccedil','&aacute;','&amp;']
		for substr in strdelete:
			paperstr.replace(substr,"")
		firstlist = paperstr.split(',')

		pid = firstlist[0].split()[-1].encode('ascii','ignore')
		name = " ".join(firstlist[1].split()).encode('ascii','ignore')
		joinstr = ",".join(firstlist[2:]).split(";")
		authors = []
		for author in joinstr:
			authordict = {}
			if "," in author:
				authordict["firstName"] = " ".join(author.split(",")[0].split()[:-1]).title().encode('ascii','ignore')
				authordict['lastName'] = " ".join(author.split(",")[0].split()[-1:]).title().encode('ascii','ignore')
				authordict['affiliation'] = " ".join(author.split(",")[1].split()).encode('ascii','ignore')
			else:
				authordict["firstName"] = " ".join(author.split()[:-1]).title().encode('ascii','ignore')
				authordict["lastName"] = " ".join(author.split()[-1:]).title().encode('ascii','ignore')
				authordict["affiliation"] = ""
			authors.append(authordict)
		return pid, name, authors
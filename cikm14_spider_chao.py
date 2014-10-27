# from scrapy.spider import BaseSpider
# from scrapy.selector import Selector	
# from PubWorldSpider.items import PaperItem, CommiteeItem

# class PaperSpider(BaseSpider):
# 	pipelines= ['PubworldspiderPipeline']
# 	name = "paperspider14"
# 	allowed_domains = ["fudan.edu.cn"]
# 	start_urls = [
# 	"http://cikm2014.fudan.edu.cn/index.php/Index/info/id/11/"
# 	]
# 	def parse(self, response):
# 		sel = Selector(response)
# 		filename = '14paper'
# 		f = open(filename,'wb')
# 		tracks = ['DB','DB','IR','IR','KM','KM']
# 		types = ['Regular','Poster','Regular','Poster','Regular','Poster']
# 		paperuls = sel.xpath("//div[@class='pageContentDivider']//ul")
# 		items = []
# 		for index, ul in enumerate(paperuls):
# 			ptrack = tracks[index]
# 			ptype = types[index]
# 			lists = ul.xpath(".//li/text()").extract()
# 			print >>f, len(lists), ptrack, ptype
# 			for count, paperstr in enumerate(lists):
# 				item = PaperItem()
# 				item['year'] = 2014
# 				item['conf'] = 'CIKM'
# 				item['ptrack'] = ptrack
# 				item['ptype'] = ptype
# 				item['pid'], item['pname'], item['authors'] = self.paperStrTokenize(paperstr, index)
# 				items.append(item)
# 				print >>f, item 
# 		return items

# 	def paperStrTokenize(self, paperstr, index):
# 		strdelete = ['&quot;','&nbsp;','&eacute;','&uuml;','&ccedil','&aacute;','&amp;']
# 		for substr in strdelete:
# 			paperstr.replace(substr,"")
# 		firstlist = paperstr.split(',')

# 		pid = firstlist[0].split()[-1].encode('ascii','ignore')
# 		name = " ".join(firstlist[1].split()).encode('ascii','ignore')
# 		joinstr = ",".join(firstlist[2:]).split(";")
# 		authors = []
# 		for author in joinstr:
# 			authordict = {}
# 			if index <= 3:
# 				authordict["firstName"] = " ".join(author.split("(")[0].split()[:-1]).title().encode('ascii','ignore')
# 				authordict['lastName'] = " ".join(author.split("(")[0].split()[-1:]).title().encode('ascii','ignore')
# 				authordict['affiliation'] = " ".join(author.split("(")[1][:-1].split()).encode('ascii','ignore')
# 			else:
# 				authordict["firstName"] = " ".join(author.split(",")[0].split()[:-1]).title().encode('ascii','ignore')
# 				authordict['lastName'] = " ".join(author.split(",")[0].split()[-1:]).title().encode('ascii','ignore')
# 				authordict['affiliation'] = " ".join(author.split(",")[1].split()).encode('ascii','ignore')
# 			authors.append(authordict)
# 		return pid, name, authors


# class CommiteeSpider(BaseSpider):
# 	pipelines= ['PubworldspiderPipeline']
# 	name = "commiteespider14"
# 	allowed_domains = ["fudan.edu.cn"]
# 	start_urls = [
# 	"http://cikm2014.fudan.edu.cn/index.php/Index/info/id/10/"
# 	]
# 	def parse(self, response):
# 		sel = Selector(response)
# 		filename = "14commitee"
# 		f = open(filename,'wb')
# 		tracktitles = [{'tr':'DB', 'tl': 'Senior'},{'tr':'IR', 'tl': 'Senior'}, {'tr':'KM', 'tl': 'Senior'}, {'tr':'DB', 'tl': 'Junior'}, {'tr':'IR', 'tl': 'Junior'},{'tr':'KM', 'tl': 'Junior'}]
# 		pculs = sel.xpath("//ul")
# 		pculs = pculs[-6:]
# 		items = []
# 		for index, ul in enumerate(pculs):
# 			ctrack = tracktitles[index]['tr']
# 			ctitle = tracktitles[index]['tl']
# 			lists = ul.xpath(".//li/text()").extract()
# 			# Or lists = ul.xpath("li/text()").extract()
# 			print >>f, len(lists), ctrack, ctitle
# 			for count, pcstr in enumerate(lists):
# 				item = CommiteeItem()
# 				item['year'] = 2014
# 				item['conf'] = 'CIKM'
# 				item['ctrack'] = ctrack
# 				item['ctitle'] = ctitle
# 				item['fname'], item['lname'], item['afl'], item['cotherinfo'] = self.pcStrTokenize(pcstr, index)
# 				items.append(item)
# 				# if count == 10:
# 				# 	break
# 				print >>f, item
# 		return items
	
# 	def pcStrTokenize(self, pcstr, index):
# 		strdelete = ['&quot;','&nbsp;','&eacute;','&uuml;','&ccedil','&aacute;','&amp;']
# 		for substr in strdelete:
# 			pcstr.replace(substr,"")
# 		firstlist = pcstr.split(',')

# 		fname = " ".join(firstlist[0].split()[:-1]).title().encode('ascii','ignore')
# 		lname = " ".join(firstlist[0].split()[-1:]).title().encode('ascii','ignore')
		
# 		if index <= 2:
# 			print 'true'
# 			joinstr = ",".join(firstlist[1:]).split("(")
# 			afl = " ".join(joinstr[0].split()).encode('ascii','ignore')
# 			cotherinfo = " ".join(joinstr[1][:-1].split()).encode('ascii','ignore')
# 		else:
# 			afl = " ".join(",".join(firstlist[1:]).split()).encode('ascii','ignore')
# 			cotherinfo = ""
# 		return fname, lname, afl, cotherinfo


# class DemoSpider(BaseSpider):
# 	pipelines= ['PubworldspiderPipeline']
# 	name = "demospider14"
# 	allowed_domains = ["fudan.edu.cn"]
# 	start_urls = [
# 	"http://cikm2014.fudan.edu.cn/index.php/Index/info/id/13"
# 	]
# 	def parse(self, response):
# 		sel = Selector(response)
# 		filename = '14demo'
# 		f = open(filename,'wb')
# 		paperuls = sel.xpath("//ul")
# 		paperuls = paperuls[-2:]
# 		items = []
# 		for index, ul in enumerate(paperuls):
# 			lists = ul.xpath(".//li/text()").extract()
# 			# Or lists = ul.xpath("li/text()").extract()
# 			print >>f, len(lists)
# 			for count, paperstr in enumerate(lists):
# 				item = PaperItem()
# 				item['year'] = 2014
# 				item['conf'] = 'CIKM'
# 				item['ptrack'] = ''
# 				item['ptype'] = 'Demo'
# 				item['pid'], item['pname'], item['authors'] = self.paperStrTokenize(paperstr, index)
# 				items.append(item)
# 				# if count == 10:
# 				# 	break
# 				print >>f, item
# 		return items
# 	def paperStrTokenize(self, paperstr, index):
# 		strdelete = ['&quot;','&nbsp;','&eacute;','&uuml;','&ccedil','&aacute;','&amp;']
# 		for substr in strdelete:
# 			paperstr.replace(substr,"")
# 		firstlist = paperstr.split(',')

# 		pid = firstlist[0].split()[-1].encode('ascii','ignore')
# 		name = " ".join(firstlist[1].split()).encode('ascii','ignore')
# 		joinstr = ",".join(firstlist[2:]).split(";")
# 		authors = []
# 		for author in joinstr:
# 			authordict = {}
# 			if "," in author:
# 				authordict["firstName"] = " ".join(author.split(",")[0].split()[:-1]).title().encode('ascii','ignore')
# 				authordict['lastName'] = " ".join(author.split(",")[0].split()[-1:]).title().encode('ascii','ignore')
# 				authordict['affiliation'] = " ".join(author.split(",")[1].split()).encode('ascii','ignore')
# 			else:
# 				authordict["firstName"] = " ".join(author.split()[:-1]).encode('ascii','ignore')
# 				authordict["lastName"] = " ".join(author.split()[-1:]).encode('ascii','ignore')
# 				authordict["affiliation"] = ""
# 			authors.append(authordict)
# 		return pid, name, authors
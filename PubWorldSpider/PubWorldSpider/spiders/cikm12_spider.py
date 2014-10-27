from scrapy.spider import BaseSpider
from scrapy.selector import Selector	
from PubWorldSpider.items import PaperItem, CommiteeItem

class PaperSpider(BaseSpider):
	pipelines= ['papers']
	name = "paperspider12"
	allowed_domains = ["fudan.edu.cn"]
	start_urls = [
	"http://www.cikm2012.org/accepted_papers.php"
	]
	def parse(self, response):
		sel = Selector(response)
		filename = '12paper'
		f = open(filename,'wb')
		tracktypes = [{'tr':'', 'ty': 'Full'}, {'tr':'', 'ty': 'Short'},{'tr':'', 'ty': 'Poster'},{'tr':'', 'ty': 'Demo'},]
		paperuls = sel.xpath("//table[@class='speakers']")
		items = []
		for index, ul in enumerate(paperuls):
			ptrack = tracktypes[index]['tr']
			ptype = tracktypes[index]['ty']
			lists = ul.xpath(".//tr")
			# Or lists = ul.xpath("li/text()").extract()
			print >>f, len(lists)/2, ptrack, ptype
			for count in range(len(lists)/2):
				
				item = PaperItem()
				item['year'] = 2012
				item['conf'] = 'CIKM'
				item['ptrack'] = ptrack
				item['ptype'] = ptype
				item['pid'] = "".join(lists[2*count].xpath("(.//td)[1]/text()").extract()).encode('ascii','ignore')
				item['pname'] = "".join(lists[2*count].xpath("(.//td)[2]/text()").extract()).encode('ascii','ignore')
				authorstr = "".join(lists[2*count + 1].xpath("(.//td)[1]/text()").extract())
				item['authors'] = self.paperStrTokenize(authorstr, index)
				items.append(item)
				# print >>f, item
		return items
	def paperStrTokenize(self, authorstr, index):
		strdelete = ['&quot;','&nbsp;','&eacute;','&uuml;','&ccedil','&aacute;','&amp;']
		for substr in strdelete:
			authorstr.replace(substr,"")
		firstlist = authorstr.split(',')
		authors = []
		for author in firstlist:
			authordict = {}
			authordict["firstName"] = " ".join(author.split()[:-1]).title().encode('ascii','ignore')
			authordict['lastName'] = " ".join(author.split()[-1:]).title().encode('ascii','ignore')
			authordict['affiliation'] = ""
			authors.append(authordict)
		return authors


class CommiteeSpider(BaseSpider):
	pipelines= ['pcs']
	name = "commiteespider12"
	allowed_domains = ["fudan.edu.cn"]
	start_urls = [
	"http://www.cikm2012.org/program_committee.php"
	]
	def parse(self, response):
		sel = Selector(response)
		filename = '12commitee'
		f = open(filename,'wb')
		tracktitles = [{'tr':'KM', 'tl': 'Senior'}, {'tr':'KM', 'tl': 'Junior'}, {'tr':'IR', 'tl': 'Senior'}, {'tr':'IR', 'tl': 'Junior'}, {'tr':'DB', 'tl': 'Senior'}, {'tr':'DB', 'tl': 'Junior'}]
		pculs = sel.xpath("//ul[@class = 'nolist']")
		items = []
		for index, ul in enumerate(pculs):
			ctrack = tracktitles[index]['tr']
			ctitle = tracktitles[index]['tl']
			lists = ul.xpath(".//li//table[@class = 'noborder']")
			# Or lists = ul.xpath("li/text()").extract()
			print >>f, len(lists), ctrack, ctitle
			for commitee in lists:
				item = CommiteeItem()
				item['year'] = 2012
				item['conf'] = 'CIKM'
				item['ctrack'] = ctrack
				item['ctitle'] = ctitle
				name = "".join(commitee.xpath(".//span[@class='pc_name']/text()").extract())
				item['fname'] = " ".join(name.split()[:-1]).title().encode('ascii','ignore')
				item['lname'] = " ".join(name.split()[-1:]).title().encode('ascii','ignore')
				item['afl'] = "".join(commitee.xpath(".//span[@class='pc_aff']/text()").extract()).encode('ascii','ignore')
				items.append(item)
				# print >>f, item
		return items
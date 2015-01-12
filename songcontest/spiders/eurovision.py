from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from songcontest.items import ReceivedItem
from songcontest.items import GivenItem
from songcontest.items import VoteItem

class EurovisionSpider(CrawlSpider):
	name = 'eurovision'
	allowed_domains = ['eurovision.tv']
	start_urls = ['http://www.eurovision.tv/page/history/by-year/contest?event=291',
		'http://www.eurovision.tv/page/history/by-year/contest?event=292',
		'http://www.eurovision.tv/page/history/by-year/contest?event=293',
		'http://www.eurovision.tv/page/history/by-year/contest?event=294',
		'http://www.eurovision.tv/page/history/by-year/contest?event=295',
		'http://www.eurovision.tv/page/history/by-year/contest?event=296',
		'http://www.eurovision.tv/page/history/by-year/contest?event=297',
		'http://www.eurovision.tv/page/history/by-year/contest?event=298',
		'http://www.eurovision.tv/page/history/by-year/contest?event=299',
		'http://www.eurovision.tv/page/history/by-year/contest?event=300',
		'http://www.eurovision.tv/page/history/by-year/contest?event=301',
		'http://www.eurovision.tv/page/history/by-year/contest?event=302',
		'http://www.eurovision.tv/page/history/by-year/contest?event=303',
		'http://www.eurovision.tv/page/history/by-year/contest?event=304',
		'http://www.eurovision.tv/page/history/by-year/contest?event=305',
		'http://www.eurovision.tv/page/history/by-year/contest?event=306',
		'http://www.eurovision.tv/page/history/by-year/contest?event=307',
		'http://www.eurovision.tv/page/history/by-year/contest?event=308',
		'http://www.eurovision.tv/page/history/by-year/contest?event=235',
		'http://www.eurovision.tv/page/history/by-year/contest?event=309',
		'http://www.eurovision.tv/page/history/by-year/contest?event=310',
		'http://www.eurovision.tv/page/history/by-year/contest?event=311',
		'http://www.eurovision.tv/page/history/by-year/contest?event=312',
		'http://www.eurovision.tv/page/history/by-year/contest?event=313',
		'http://www.eurovision.tv/page/history/by-year/contest?event=314',
		'http://www.eurovision.tv/page/history/by-year/contest?event=315',
		'http://www.eurovision.tv/page/history/by-year/contest?event=266',
		'http://www.eurovision.tv/page/history/by-year/contest?event=316',
		'http://www.eurovision.tv/page/history/by-year/contest?event=217',
		'http://www.eurovision.tv/page/history/by-year/contest?event=8',
		'http://www.eurovision.tv/page/history/by-year/contest?event=159',
		'http://www.eurovision.tv/page/history/by-year/contest?event=334',
		'http://www.eurovision.tv/page/history/by-year/contest?event=435',
		'http://www.eurovision.tv/page/history/by-year/contest?event=1469',
		'http://www.eurovision.tv/page/history/by-year/contest?event=1482',
		'http://www.eurovision.tv/page/history/by-year/contest?event=1493',
		'http://www.eurovision.tv/page/history/by-year/contest?event=1553',
		'http://www.eurovision.tv/page/history/by-year/contest?event=1593',
		'http://www.eurovision.tv/page/history/by-year/contest?event=1773',
		'http://www.eurovision.tv/page/history/by-year/contest?event=1893']

	def chunker(self, seq, size):
		return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

	def createVoteItem(self, points, fromP, toP, year):
		voteItem = VoteItem()
		voteItem['points'] = int(points)
		voteItem['fromParticipant'] = str(fromP)
		voteItem['toParticipant'] = str(toP)
		voteItem['year'] = year
		return voteItem

	def parse(self, response):
		sel = Selector(response)
		
		year = int(sel.xpath('/html/head/title/text()').re('Eurovision Song Contest (\d+)')[0])
		
		votes = []
		
		# First column is alway the participant. The final two are always Points and Place
		items = sel.xpath('.//td/@title').re('(\d*)pt from ([A-Za-z .&]+) goes to ([A-Za-z .&]+)')
		items = [unicode(0) if x == '' else x for x in items]
		
		for vote in self.chunker(items, 3):
			points = vote[0]
			
			# Special cases
			if vote[1] == 'Serbia & Montenegro' or vote[2] == 'Serbia & Montenegro' or vote[1] == 'Yugoslavia' or vote[2] == 'Yugoslavia':
				continue
			else:
				votes.append(self.createVoteItem(points, vote[1], vote[2], year))
			
		return votes

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ReceivedItem(Item):
	year = Field()
	participant = Field()
	points = Field()
	totalPoints = Field()
	rank = Field()
	pass

class GivenItem(Item):
	year = Field()
	participant = Field()
	points = Field()
	pass

class VoteItem(Item):
	year = Field()
	fromParticipant = Field()
	toParticipant = Field()
	points = Field()
	pass

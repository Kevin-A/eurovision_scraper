# Scrapy settings for songcontest project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'songcontest'

SPIDER_MODULES = ['songcontest.spiders']
NEWSPIDER_MODULE = 'songcontest.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36)'

ITEM_PIPELINES = { 'songcontest.pipelines.SQLiteStorePipeline':500 }

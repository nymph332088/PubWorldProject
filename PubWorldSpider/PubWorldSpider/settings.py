# -*- coding: utf-8 -*-

# Scrapy settings for PubWorldSpider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'PubWorldSpider'

SPIDER_MODULES = ['PubWorldSpider.spiders']
NEWSPIDER_MODULE = 'PubWorldSpider.spiders'
ITEM_PIPELINES = ['PubWorldSpider.pipelines.Pipelines']
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'PubWorldSpider (+http://www.yourdomain.com)'

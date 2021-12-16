import scrapy
import requests
import configparser
import tg
from demo.items import RfdItem
from scrapy.crawler import CrawlerProcess
from urllib.parse import quote


class RfdSpider(scrapy.Spider):
	name = 'rfd'
	allowed_domains = ['redflagdeals.com']
	start_urls = ['https://forums.redflagdeals.com/hot-deals-f9/?sk=tt&rfd_sk=tt&sd=d']

	def parse(self, response):
		######################################################################### 
		#  Configuration
		######################################################################### 
		CONFIG_FILE='config_loader.ini'
		CONFIG_MAIN='main'
		configParser = configparser.ConfigParser()
		configParser.read(CONFIG_FILE)
		UID = configParser.get(CONFIG_MAIN, "uid") 

		for s in response.xpath('//div[@class="forumbg"]/div/ul[@class="topiclist topics with_categories"]'):
			item = RfdItem()
			item['uid'] = s.xpath('./li/@data-thread-id').extract()
			item['retailer'] = s.xpath('//h3/a[@class="topictitle_retailer"]/text()').extract()
			item['title'] = s.xpath('//h3/a[@class="topic_title_link"]/text()').extract()
			retailers = s.xpath('//h3[contains(@class,"topictitle")]/text()[1]').extract()
			class_values = s.xpath('//h3[contains(@class,"topictitle")]/@class').extract()
			#item['link'] = s.xpath('//h3/a[@class="topic_title_link"]/@href').extract()
			#item['time'] = s.xpath('//span[@class="first-post-time"]/text()').extract()

		#set retailer couter
		retailer_c = len(item['retailer']) - 1

		for i in reversed(range(len(item['uid']))):
			#get title
			retailer = retailers[i].replace('\n','')
			title = item['title'][i].replace('\n','')

			if retailer:
				title = '%s%s' % (retailer, title)
			elif 'topictitle_has_retailer' in class_values[i]:
				title = '[%s] %s' % (item['retailer'][retailer_c], title)
				retailer_c -= 1

			#check uid
			if item['uid'][i] > UID:
				UID = item['uid'][i]

				title = quote(title, safe='')
				link = 'https://forums.redflagdeals.com/viewtopic.php?t=%s' % item['uid'][i]
				bot_message = '*%s*\n%s' % (title, link)

				tg.bot_sendtext_channel(bot_message)


		# update uid to config file
		configParser.set(CONFIG_MAIN, "uid", UID)
		# save to the file
		with open(CONFIG_FILE, 'w') as configfile:
			configParser.write(configfile)

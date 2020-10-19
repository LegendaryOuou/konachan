import scrapy
import os
from konachan.items import KonachanItem


class KonchanSpider(scrapy.Spider):
    name = 'konchan'
    allowed_domains = ['konachan.net']
    format_url = 'http://konachan.net/post?page=%d&tags='
    start = 2684
    end = 12000
    start_urls = [format_url % start]

    def __init__(self):
        if os.path.exists('images') is False:
            os.makedirs('images')
			
    def parse(self, response):
        img_list = response.xpath("//img[@class='preview']/@src").extract()

        for img in img_list:
        	# img_url = img.xpath('./@href').extract()[0]

        	img_name = os.path.join('images', img.split('/')[-1])

        	# print("链接",img,img_name)
        	if os.path.exists(img_name):
        		continue


        	item = KonachanItem(img_url=img)
        	
        	yield item
        	
        
        for i in range(self.start, self.end + 1):
        # for i in range(self.page_size-1):
        	yield scrapy.Request(self.format_url % (i+1), callback=self.parse)

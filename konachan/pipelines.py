# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import requests
import scrapy
import os
import traceback


class KonachanPipeline:

	def __init__(self):
		if os.path.exists('images') is False:
			os.makedirs('images')

	def process_item(self, item, spider):
		try:
			r = requests.get(item['img_url'], stream=True, timeout=60)
			r.raise_for_status()
			with open(item['img_name'], 'wb') as f:
				for chunk in r.iter_content(chunk_size=1024):
					if chunk:  # filter out keep-alive new chunks
						f.write(chunk)
						f.flush()
			# return filename
		except KeyboardInterrupt:
			if os.path.exists(item['img_name']):
				os.remove(item['img_name'])
			raise KeyboardInterrupt
		except Exception:
			traceback.print_exc()
			if os.path.exists(item['img_name']):
				os.remove(item['img_name'])


class ImgPipeline(ImagesPipeline):
	def get_media_requests(self, item, info):
		yield scrapy.Request(item['img_url'])

	def file_path(self, request, response=None, info=None):
		img_name = request.url.split('/')[-1]
		return img_name	# 返回文件名

	def item_completed(self, results, item, info):
		return item # 返回给下一个即将被执行的管道类
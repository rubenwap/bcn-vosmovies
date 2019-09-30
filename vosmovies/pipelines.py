# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2
from psycopg2.extras import RealDictCursor

pg_config = {"host": "docker.for.mac.host.internal",
             "database": "ruben", "user": "ruben", "password": ""}
conn = psycopg2.connect(**pg_config)


class VosmoviesPipeline(object):
	def process_item(self, item, spider):

		cinema = item["cinema"]
		date = item["date"]
		details = item["details"]
		hour = item["hour"]
		title = item["title"]

		print(item["cinema"])
		print(item)

		sql_insert = """
			INSERT INTO public.movies(
	cinema, movie_date, details, movie_time, title)
	VALUES (%(cinema)s,
			%(date)s,
			%(details)s,
			%(hour)s,
			%(title)s
			);
			"""

		with conn.cursor(cursor_factory=RealDictCursor) as cursor:
			cursor.execute(sql_insert, item)
			conn.commit()
		return item

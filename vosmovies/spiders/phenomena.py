# -*- coding: utf-8 -*-
import scrapy
import datetime
import re
import locale


class PhenomenaSpider(scrapy.Spider):
    name = "phenomena"
    locale.setlocale(locale.LC_ALL, "es_ES")
    year = datetime.datetime.now().year

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.current_date = datetime.datetime.now().strftime("%m-%Y")

    def start_requests(self):
        allowed_domains = ["http://www.phenomena-experience.com"]
        start_urls = [
            f"http://www.phenomena-experience.com/programacion-mensual/{self.current_date}.html"
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def extract(self, movie):
        title = " - ".join([item.strip() for item in movie.xpath(".//div[contains(@class, 'event-titulo')]/a/text()").getall()])
        details = movie.xpath(".//div[contains(@class, 'event-datos')]/text()").get()
        hour = movie.xpath(
            ".//div[contains(@class, 'event-entrada-hora')]/text()"
        ).get().strip()
        day = (
            movie.xpath("//*[contains(@class, 'clasemensual')]")[0]
            .xpath("./preceding-sibling::div/*[contains(@class, 'dia-titulo')]/text()")
            .get()
        )
        textual_date = datetime.datetime.strptime(re.sub("\n", "", day).strip(
        ) + " " + str(datetime.datetime.now().year), "%A %d %B %Y").strftime("%d/%m/%Y")
        return {
            "title": title,
            "details": re.sub("\n|\t|·|&middot|\s{2}", "", details).strip(),
            "hour": hour,
            "date": textual_date,
            "datetime": datetime.datetime.strptime(textual_date+hour, "%d/%m/%Y%H:%Mh"),
            "cinema": "Phenomena Experience",
        }

    def parse(self, response):
        day = response.xpath("//*[contains(@class, 'clasemensual')]")[0]
        movies = day.xpath(".//*[contains(@class, 'event-content')]")
        return map(self.extract, movies)

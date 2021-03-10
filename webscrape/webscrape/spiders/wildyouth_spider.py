import json


import scrapy



class WildyouthSpider(scrapy.Spider):
    name = "wildyouth"

    def start_requests(self):
        urls = [
            'https://www.ulule.com/wild-vlees/',

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(response.body)

        json_data = response.xpath("//script[contains(., 'CURRENT')]/text()").extract()[0].split("\n")[120].replace("project:", "")[:-1]
        data = json.loads(json_data)

        print(data)

        nametag = data['name']['en']
        short_description = data['subtitle']['en']





        yield {
            'name': nametag,
            'short_description': short_description,


        }










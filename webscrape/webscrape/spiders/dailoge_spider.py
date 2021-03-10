import json


import scrapy



class DailogeSpider(scrapy.Spider):
    name = "dailoge"

    def start_requests(self):
        urls = [
            'https://www.ulule.com/dialogue_paris/',

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(response.body)

        json_data = response.xpath("//script[contains(., 'CURRENT')]/text()").extract()[0].split("\n")[120].replace("project:", "")[:-1]
        data = json.loads(json_data)


        nametag = data['name']['en']
        short_description = data['subtitle']['en']
        no_of_supporters = str(data['supporters_count']) + ' Contributions'

        goal = data['goal']
        video = data['video']['url']





        yield {
            'name': nametag,
            'short_description': short_description,
            'no_of_supporters': no_of_supporters,

            'goal': goal,
            'url': video,



        }










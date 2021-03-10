import json


import scrapy



class WalkSpider(scrapy.Spider):
    name = "walkintonight"

    def start_requests(self):
        urls = [
            'https://www.ulule.com/une_balade_dans_la_nuit/',

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
        fund_raised ='amount: ' + str(data['amount_raised']) + ', currency: ' + data['currency']
        goal ='amount: ' + str(data['goal']) + ', currency: ' + data['currency']
        percentage_funded = str(data['percent']) + '.00'
        creator = '{name: ' + data['name']['en'] + ', location: ' + data['owner']['location'] + ', url: ' + data['absolute_url']  + '}'





        yield {
            'name': nametag,
            'short_description': short_description,
            'no_of_supporters': no_of_supporters,
            'fund_raised': fund_raised,
            'goal': goal,
            'percentage_funded': percentage_funded,
            'creator': creator,

        }



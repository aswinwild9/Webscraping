import json
import urllib
import scrapy
import requests
from scrapy.selector import Selector


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        apiUrl = "https://api.ulule.com/v1/search/projects?q=sort:popular+status:currently&offset=0&extra_fields=main_image,main_tag,owner,partnerships&lang=en"
        myUrl = apiUrl
        yield scrapy.Request(myUrl, callback=self.parse)

    def parse(self, response):
        baseUrl = "https://api.ulule.com/v1/search/projects"
        data = json.loads(response.body)
        print(data['meta']['next'])
        while data['meta']['next'] != None:
            myUrl = baseUrl+data['meta']['next']
            projects = []
            for project in data['projects']:
                projects.append(project['absolute_url'])
            urls = projects
            for url in urls:
                yield scrapy.Request(url=url, callback=self.firstparse)
            yield scrapy.Request(myUrl, callback=self.parse)

    def firstparse(self, response):
        json_data = response.xpath("//script[contains(., 'CURRENT')]/text()").extract()[
            0].split("\n")[120].replace("project:", "")[:-1]
        data = json.loads(json_data)
        nametag = ""
        if 'en' in data['name']:
            nametag = data['name']['en']
        else:
            nametag = data['name'][data['lang']]
        short_description = data['subtitle'][data['lang']]
        no_of_supporters = str(data['supporters_count']) + ' Contributions'
        fund_raised = 'amount: ' + \
            str(data['amount_raised']) + ', currency: ' + data['currency']
        goal = 'amount: ' + str(data['goal']) + \
            ', currency: ' + data['currency']
        
        if 'time_left' in data:
            days_left = data['time_left']
        else:
            days_left = None
        if 'video' in data:
            video = data['video']['url']
        else:
            video = None
        percentage_funded = str(data['percent']) + '.00'
        creator = '{name: ' + data['name'][data['lang']] + ', location: ' + \
            data['owner']['location'] + ', url: ' + data['absolute_url'] + ',}'
        description = ""
        if 'description_yourself_en' in data:
            description = '{name: ' + data['description_yourself_en'] + ',}'
        elif 'description_yourself_fr' in data:
            description = '{name: ' + data['description_yourself_fr'] + ',}'
        elif 'description_yourself_it' in data:
            description = '{name: ' + data['description_yourself_it'] + ',}'
            
        project_owner = '{name: ' + data['owner']['name'] + ', desc: ' + \
            str(data['owner']['description']) + ',}' 
        
        f = open("D:/Python Tutorials/WebScrapping/webscrape/Output.txt",
                 "a+", encoding='utf-8')
        myData = {
            "Data": {
                'name': nametag,
                'short_description': short_description,
                'no_of_supporters': no_of_supporters,
                'fund_raised': fund_raised,
                'goal': goal,
                'days_left': days_left,
                'video': video,
                'percentage_funded': percentage_funded,
                'creator': creator,
                'description': description,
                'project_owner': project_owner,
                
            }
        }
        f.write(str(myData))
        f.close()
        print(myData)

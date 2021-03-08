import sys
from scrapy import cmdline
def main(name):
    if name:
        cmdline.execute(name.split())



if __name__ == '__main__':
    print('[*] beginning main thread')
    name = "scrapy crawl quotes"
    #name = "scrapy crawl spa"
    main(name)
    print('[*] main thread exited')
    print('main stop====================================================')
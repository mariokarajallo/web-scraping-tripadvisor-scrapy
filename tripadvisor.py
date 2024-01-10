from scrapy.item import Item, Field
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.selector import Selector

class Hotel (Item):
    name = Field()
    #price = Field()
    address = Field()
    description = Field()
    #amenities = Field()

class TripAdvisor(CrawlSpider):
    name = "tripadvisor"

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    allowed_domains = ["tripadvisor.com"]
    start_urls = ["https://www.tripadvisor.com/Hotels-g294080-Asuncion-Hotels.html"]

    download_delay = 2

    rules = (
        Rule(LinkExtractor(allow=r'/Hotel_Review-g294080-', restrict_xpaths="//div[@data-automation='hotel-card-title']/a"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        sel = Selector(response)
        item = ItemLoader(Hotel(), sel)

        item.add_xpath('name', '//h1[@id="HEADING"]/text()')
        #item.add_xpath('price', '//div[@class="biGQs _P fiohW uuBRH"]/div/text()')
        item.add_xpath('address', '//div[contains(@data-test-target,"hr-atf-info")]/div[3]/div/div[2]/span[2]/span/text()')
        item.add_xpath('description', '//div[@id="ABOUT_TAB"]//div[@class="ui_column  "][1]//div[@class="ssr-init-26f"][1]//div[1]//div[1]/text()')
        #item.add_xpath('amenities', '//div[contains(@data-test-target="amenity_text")]/span/text()')

        yield item.load_item()


# EJECUCION
# scrapy runspider 1_tripadvisor.py -o tripadvisor.csv
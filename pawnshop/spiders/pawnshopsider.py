import scrapy


class PawnshopsiderSpider(scrapy.Spider):
    name = "pawnshopsider"
    allowed_domains = ["www.pawnshops.net"]
    start_urls = ["https://www.pawnshops.net/search.php?whatcountry=US&whatstate=&s=1"]
    page = 1

    def parse(self, response):
        link = response.css('a[href^="https://www.pawnshops.net/store/"]::attr(href)').getall()
        for url in link:
            yield scrapy.Request(url, callback=self.getinfo)
        
        next_page = f"https://www.pawnshops.net/search.php?whatcountry=US&whatstate=&s={str(PawnshopsiderSpider.page)}"
        if PawnshopsiderSpider.page <= 1292:
            yield scrapy.Request(next_page, callback=self.parse)
            PawnshopsiderSpider.page += 1

    def getinfo(self, response):
        pawnshop_name = response.css('span[itemprop="name"]::text').get()
        street_address = response.css('span[itemprop="streetAddress"]::text').get()
        locality = response.css('span[itemprop="addressLocality"]::text').get()
        region = response.css('span[itemprop="addressRegion"]::text').get()
        postal_code = response.css('span[itemprop="postalCode"]::text').get()
        telephone = response.css('span[itemprop="telephone"] a::text').get()
        yield {
            "name": pawnshop_name,
            "street_adress": street_address,
            "locality": locality,
            "region": region,
            "postal_code": postal_code,
            "telephone": telephone
        }

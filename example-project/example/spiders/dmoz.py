from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class DmozSpider(CrawlSpider):
    """Follow categories and extract links."""

    name = "dmoz"
    allowed_domains = ["dmoz-odp.com"]
    start_urls = ["https://www.dmoz-odp.com/"]

    rules = [
        Rule(
            LinkExtractor(restrict_css=(".top-cat", ".sub-cat", ".cat-item")),
            callback="parse_directory",
            follow=True,
        ),
    ]

    def parse_directory(self, response):
        for div in response.css(".site-item"):
            yield {
                "name": div.css(".site-title::text").extract_first(),
                "description": div.css(".title-and-desc>p::text").extract_first().strip(),
                "link": div.css("a::attr(href)").extract_first(),
            }

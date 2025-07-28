import scrapy

class VisaoglobalimoveisSpider(scrapy.Spider):
    name = "VisaoGlobalImoveis"
    allowed_domains = ["visaoglobalimoveis.com.br"]
    start_urls = ["https://visaoglobalimoveis.com.br/"]

    def parse(self, response):
        pass

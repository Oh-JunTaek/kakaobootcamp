import scrapy

class KakaoSpider(scrapy.Spider):
    name = 'kakao_spider'
    allowed_domains = ['ko.wikipedia.org']
    start_urls = ['https://ko.wikipedia.org/wiki/%EC%B9%B4%EC%B9%B4%EC%98%A4_(%EA%B8%B0%EC%97%85)']

    def parse(self, response):
        title = response.xpath('//h1/text()').get()
        paragraphs = response.xpath('//p//text()').getall()

        yield {
            'title': title,
            'paragraphs': paragraphs,
        }
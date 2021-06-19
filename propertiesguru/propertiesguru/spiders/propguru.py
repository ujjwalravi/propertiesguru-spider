import scrapy


class PropguruSpider(scrapy.Spider):
    name = 'propguru'
    limit = 0
    num = 0
    single_time = True
    allowed_domains = ['propertiesguru.com']
    # Instead of following thtough it's URL, I did it by getting it's AJAX calls because the page was lazily-loaded
    start_urls = ['https://propertiesguru.com/search?viewtype=list&propertytype=sell&cityid=1081&reffid=1&cat=3,28,29,30&bedroom=2&type=ajax&slimit']

    def parse(self, response):
        global limit, single_time, num
        if self.single_time is True:
            # Getting the number of items quotient upon divided by 10 fr iteration
            self.num = int(response.xpath('//h1//text()').extract_first().split(' ')[0])//10
            self.single_time = False
        else:
            pass
        properties = response.xpath('//div[@class="filter-property-list detailurl"]')
        if properties is not None:
            for flats in properties:
                yield {
                'title' :flats.xpath('.//h1/text()').extract_first(),
                'location': flats.xpath('.//a/text()').extract_first(),
                'price': flats.xpath('.//span[@class="price"]/text()').extract_first(),
                'sq_ft' :flats.xpath('.//span[@class="price-per-unit"]/text()').extract_first()[1:],
                'property_image': flats.xpath('.//img[@class="img-fluid"]/@src').extract_first(),
                'area' :flats.xpath('.//div[@class="col-4"]/text()').extract_first().strip(),
                'facing': flats.xpath('.//div[@class="col-4"]/following-sibling::div/text()').extract_first(),
                'status': flats.xpath('.//div[@class="col-4"]/following-sibling::div[2]/text()').extract_first(),
                'floor': flats.xpath('.//ul[@class="pro-list"]/li[1]/text()').extract_first(),
                'furnishing': flats.xpath('.//ul[@class="pro-list"]/li[2]/text()').extract_first(),
                'hold_type' :flats.xpath('.//ul[@class="pro-list"]/li[3]/text()').extract_first(),
                'bathroom': flats.xpath('.//ul[@class="pro-list"]/li[4]/text()').extract_first(),
                'map_url' :flats.xpath('.//a/@href').extract_first()
                }
            
            # Iteration 'num' no of times on it's AJAX page
            self.limit = self.limit + 10
            if (self.limit // 10) != self.num + 1:
                next_url = 'https://propertiesguru.com/search?viewtype=list&propertytype=sell&cityid=1081&reffid=1&cat=3,28,29,30&bedroom=2&type=ajax&slimit=' + str(self.limit)
                yield scrapy.Request(next_url, callback=self.parse)


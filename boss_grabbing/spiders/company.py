import scrapy
from scrapy import Request

import re

from boss_grabbing.items import BossGrabbingItem
from boss_grabbing.sqlite import Sqlite


class BossSpider(scrapy.Spider):
    # 这里是将爬虫定义为scrapy.Spider这个类下的一个实例。
    # Spider这个类定义了爬虫的很多基本功能，我们直接实例化就好，
    # 省却了很多重写方法的麻烦。
    name = 'bossZhiPin'
    # 这是爬虫的名字，这个非常重要。
    # start_urls = ['https://www.zhipin.com/c101210400-p100101/h_101210400/?page=2']
    base_url = 'https://www.zhipin.com/c101210400-p100101/h_101210400/?page='

    # 这是爬虫开始干活的地址，必须是一个可迭代对象。

    def start_requests(self):
        # 构造网址列表
        for i in range(0, 2):
            url = self.base_url + str(i)
            yield Request(url, self.parse)

    def parse(self, response):
        titles = response.xpath("//div[@class='company-text']").extract()  # xpath的内容网上搜
        # 爬虫收到上面的地址后，就会发送requests请求，在收到服务器返回的内容后，就将内容传递给parse函数。在这里我们重写函数，达到我们想要的功能。
        for context in titles:
            item = BossGrabbingItem()
            item['url'] = re.findall('/[^/]*html', context)[0][1:-5]
            print(item['url'])
            count = Sqlite.select_db(item['url'])[0][0]  # 没有具体研究过，默认返回的是tuple类型，类似二维数组
            if count > 0:
                return
            item['name'] = re.findall('_blank">.*</a>', context)[0][8:-4]
            item['area'] = re.findall('<p>[^<]*<em', context)[0][3:-3]
            finance = re.findall('em>.*<em', context)
            if len(finance) > 0:
                item['finance'] = finance[0][3:-3]
            else:
                item['finance'] = ''
            item['size'] = re.findall('em>[^<]*</p', context)[0][3:-3]
            url = 'https://www.zhipin.com/gongsi/' + item['url'] + ".html"
            yield Request(url, callback=self.get_detail, meta={'item': item})  # 这样就会调用get_detail()方法，并且把item传过去

    # 获取公司的详情和地址
    def get_detail(self, response):
        item = response.meta['item']
        detail_content = response.xpath("//div[@class='detail-content']//div[@class='text fold-text']").extract()
        address_content = response.xpath("//div[@class='detail-content']//div[@class='job-location']").extract()
        print(detail_content)
        print(address_content)
        addresses = re.findall("a>[^<]+</div", str(address_content))
        description = ""
        descriptions = re.findall('text\">.+<a', str(detail_content))
        if len(descriptions) > 0:
            description = descriptions[0][6:-2]
        address_list = ""
        for address in addresses:
            address_list = address_list + ";" + address[2:-5]
        item['description'] = description
        item['addresses'] = address_list[1:]  # 去掉第一个分号
        yield item

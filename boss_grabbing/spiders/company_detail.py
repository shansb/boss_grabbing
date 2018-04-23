import sqlite3
import re
import scrapy
from scrapy import Request

# 这个类在最终整合后不再使用
class BossSpider(scrapy.Spider):
    # 这里是将爬虫定义为scrapy.Spider这个类下的一个实例。
    # Spider这个类定义了爬虫的很多基本功能，我们直接实例化就好，
    # 省却了很多重写方法的麻烦。
    name = 'bossDetail'
    # 这是爬虫的名字，这个非常重要。
    # start_urls = ['https://www.zhipin.com/c101210400-p100101/h_101210400/?page=2']
    base_url = 'https://www.zhipin.com/gongsi/'
    con = sqlite3.connect('sqlite3.db')
    cur = con.cursor()
    cur.execute('select * from(SELECT *,rowid FROM company where description is null) '
                'where rowid < ((select min(rowid) from company where description is null) + 40)')
    # cur.execute('SELECT *,rowid FROM company where rowid=1 ')
    company_list = cur.fetchall()

    # 这是爬虫开始干活的地址，必须是一个可迭代对象。

    def start_requests(self):
        # 构造网址列表
        for i in self.company_list:
            # print("hello")
            # print(i)
            url = self.base_url + str(i[0]) + ".html"
            yield Request(url, self.parse, meta={'id': i[0]})

    def parse(self, response):
        detail_content = response.xpath("//div[@class='detail-content']//div[@class='text fold-text']").extract()
        address_content = response.xpath("//div[@class='detail-content']//div[@class='job-location']").extract()
        print(detail_content)
        print(address_content)
        url = str(response.meta['id'])
        addresses = re.findall("a>[^<]+</div", str(address_content))
        description = ""
        descriptions = re.findall('text\">.+<a', str(detail_content))
        if len(descriptions) > 0:
            description = descriptions[0][6:-3]
        address_list = ""
        for address in addresses:
            address_list = address_list + ";" + address[2:-6]
        self.cur.execute('update company set description=?,address=? where id=?',
                         (description, str(address_list), int(url)))
        self.con.commit()

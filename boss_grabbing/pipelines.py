# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from boss_grabbing.sqlite import Sqlite


class BossGrabbingPipeline(object):

    def process_item(self, item, spider):
        print("process")
        count = Sqlite.select_db(item['url'])[0][0]
        print("count:" + str(count))
        if count == 0:
            Sqlite.insert_db(item)
        return item

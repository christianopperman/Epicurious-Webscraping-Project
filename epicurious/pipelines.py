# -*- coding: utf-8 -*-

from scrapy.exporters import CsvItemExporter

# Create a class to write each given scraped recipe to a CSV using Scrapy's CsvItemExporter class
class WriteItemPipeline(object):
    def __init__(self):
        self.filename = 'epicurious_final.csv'
    def open_spider(self, spider):
        self.csvfile = open(self.filename, 'wb')
        self.exporter = CsvItemExporter(self.csvfile)
        self.exporter.start_exporting()
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.csvfile.close()
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
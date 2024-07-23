# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScraprealestatePipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        fields_name = adapter.field_names()
        for field_name in fields_name:
            if field_name != "description":
                adapter[field_name] = adapter.get(field_name)[0]
        return item

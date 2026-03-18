class JobPipeline:
    def process_item(self, item, spider):
        # Clean
        for field in item.fields:
            if not item.get(field):
                item[field] = ''
        return item


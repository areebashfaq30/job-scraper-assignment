BOT_NAME = 'scrapy_project'

SPIDER_MODULES = ['scrapy_project.spiders']
NEWSPIDER_MODULE = 'scrapy_project.spiders'

ROBOTSTXT_OBEY = True
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = 0.5

FEEDS = {
    '../../../data/final/jobs.json': {'format': 'json'},
    '../../../data/final/jobs.csv': {'format': 'csv', 'headers': True},
}

ITEM_PIPELINES = {
    'scrapy_project.pipelines.JobPipeline': 300,
}


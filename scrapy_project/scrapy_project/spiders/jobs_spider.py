import scrapy
from scrapy_project.items import JobItem
import csv
import os

class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['boards.greenhouse.io', 'greenhouse.io']

    def start_requests(self):
        links_file = '../../../data/raw/job_links.csv'
        if os.path.exists(links_file):
            with open(links_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    yield scrapy.Request(url=row['job_url'], callback=self.parse, meta={'url': row['job_url']})
        else:
            self.logger.error(f'{links_file} not found')

    def parse(self, response):
        item = JobItem()
        item['job_url'] = response.url

        # Greenhouse selectors
        item['job_title'] = response.css('h1.application-name::text').get(default='').strip() or response.xpath('//h1[contains(@class,"posting")]/text()').get()
        item['company_name'] = response.css('[data-qa="job-company"]::text').get(default='').strip()
        item['location'] = response.css('.posting-header-location::text').get(default='').strip()
        item['department'] = response.css('[data-qa="job-category"]::text').get(default='').strip()
        item['employment_type'] = response.css('[data-qa="job-type"]::text').get(default='Full-time').strip()
        item['posted_date'] = response.css('.posted-date::text').get(default='').strip()  # Adjust selector

        description = ' '.join(response.css('.description *::text').getall()).strip()[:2000]  # Truncate
        item['job_description'] = description

        # Skills: simple keyword extract or list
        skills_text = response.css('.skills-list *::text, .requirements *::text').getall()
        item['required_skills'] = ', '.join([s.strip() for s in skills_text if len(s.strip()) > 3])[:500]

        yield item


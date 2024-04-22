import scrapy
import os
import requests

class MySpider(scrapy.Spider):
    name = 'myspider'

    def __init__(self, url=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]

    def parse(self, response):
        # Create directory to store scraped content
        if not os.path.exists('scrapedContent'):
            os.makedirs('scrapedContent')

        # Save HTML content
        file_path = os.path.join('scrapedContent', 'scraped_page.html')
        with open(file_path, 'wb') as f:
            f.write(response.body)

        # Extract and save JavaScript files
        js_files = response.css('script[src$=".js"]::attr(src)').extract()
        for js_file in js_files:
            js_content = requests.get(response.urljoin(js_file)).content
            js_filename = os.path.join('scrapedContent', os.path.basename(js_file))
            with open(js_filename, 'wb') as f:
                f.write(js_content)

        # Extract and save CSS files
        css_files = response.css('link[rel="stylesheet"]::attr(href)').extract()
        for css_file in css_files:
            css_content = requests.get(response.urljoin(css_file)).content
            css_filename = os.path.join('scrapedContent', os.path.basename(css_file))
            with open(css_filename, 'wb') as f:
                f.write(css_content)

        # Extract and save images
        img_urls = response.css('img::attr(src)').extract()
        for img_url in img_urls:
            img_content = requests.get(response.urljoin(img_url)).content
            img_filename = os.path.join('scrapedContent', os.path.basename(img_url))
            with open(img_filename, 'wb') as f:
                f.write(img_content)

        # You can add more logic here to extract and save other types of resources if needed

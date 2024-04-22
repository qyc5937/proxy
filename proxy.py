from flask import Flask, request, Response,jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
import os
import subprocess

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/proxy')
def proxy():
    # Get the URL from the query parameter `url`
    url = request.args.get('url')
    if not url:
        return "Missing URL parameter", 400

    # Configure Selenium WebDriver
    options = Options()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')  # Disable GPU (useful for headless mode)
    options.add_argument('--no-sandbox')  # Bypass the OS security model (necessary on some systems)
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    options.add_argument("--enable-javascript")
    options.binary_location = '/usr/bin/chromium-browser'
    caps = DesiredCapabilities.CHROME
    caps['pageLoadStrategy'] = 'normal'  # Waits for full page load (default)
    service = Service(executable_path="/usr/bin/chromedriver")

    # Specify the path to the ChromeDriver
    chrome_service = Service(executable_path='path/to/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Use Selenium to fetch the URL content
        driver.get(url)
        rendered_html = driver.page_source

        # Close the driver
        driver.quit()

        # Return the rendered HTML to the client
        return Response(rendered_html, mimetype='text/html')
    except Exception as e:
        # Ensure the driver is quit properly
        driver.quit()
        return f"Error rendering the URL with JavaScript: {e}", 500





# Create directory for scraped content if it doesn't exist
if not os.path.exists('scrapedContent'):
    os.makedirs('scrapedContent')

@app.route('/scrape')
def scrape():
    url = request.args.get('url')
    if not url:
        return "Missing URL parameter", 400

    try:
        # Run Scrapy spider using subprocess
        subprocess.run(['scrapy', 'runspider', 'scrapy_spider.py', '-a', f'url={url}'])
        
        # Return success message
        file_path = os.path.join('scrapedContent', 'scraped_page.html')
        return jsonify({"message": "Content scraped successfully", "file_path": file_path}), 200
    except Exception as e:
        logging.error(f"Error during web scraping: {e}")
        return f"Error scraping the URL: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12504)

# def proxy():
#     # Get the URL from the query parameter `url`
#     url = request.args.get('url')
#     if not url:
#         return "Missing URL parameter", 400
    
#     try:
#         # Set up Chrome options
#         chrome_options = Options()
#         chrome_options.add_argument("--headless")
#         chrome_options.add_argument("--no-sandbox")
#         chrome_options.add_argument("--disable-dev-shm-usage")
#         chrome_options.add_argument("--disable-gpu")
#         chrome_options.binary_location = '/usr/bin/chromium-browser'
#         service = Service(executable_path="/usr/bin/chromedriver")

#         # Initialize the Chrome WebDriver with Chrome options
#         driver = webdriver.Chrome(service=service,options=chrome_options)
#         #driver.implicitly_wait(10) 
#         logging.debug(f"Fetching URL: {url}")
#         # Fetch the URL content using Selenium WebDriver
#         driver.get(url)
#         wait = WebDriverWait(driver, 10)  # Maximum wait time (in seconds)
#         wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))  # Wait for the <body> element to be present


#         # Get the rendered HTML
#         html_content = driver.page_source
#         # Log the HTML content (for debugging purposes)
#         logging.debug(f"HTML content: {html_content}")
#         driver.quit()
    
        

        
#         # Return the rendered HTML to the client
#         return Response(html_content, mimetype='text/html')
#     except Exception as e:
#         return f"Error fetching the URL with Selenium: {e}", 500



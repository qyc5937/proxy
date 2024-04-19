from bs4 import BeautifulSoup

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url:
        return "Missing URL parameter", 400
    
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.binary_location = '/usr/bin/chromium-browser'

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        driver.implicitly_wait(10)
        html_content = driver.page_source
        driver.quit()

        # Modify the HTML content to include a base tag
        soup = BeautifulSoup(html_content, 'html.parser')
        if soup.head:
            base = soup.new_tag('base', href=url)
            soup.head.insert(0, base)
            html_content = str(soup)

        return Response(html_content, mimetype='text/html')
    except Exception as e:
        return f"Error retrieving content: {e}", 500


from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/proxy')
def proxy():
    # Get the URL from the query parameter `url`
    url = request.args.get('url')
    if not url:
        return "Missing URL parameter", 400
    
    try:
        # Use requests to fetc`h the URL content
        resp = requests.get(url)
        
        # Return the fetched content to the client
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        return Response(resp.content, resp.status_code, headers)
    except requests.RequestException as e:
        return f"Error fetching the URL: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)


import urllib3
import certifi

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED', # Force certificate check.
    ca_certs=certifi.where(),  # Path to the Certifi bundle.
)

base_url = "https://api.github.com/repos/jasonrudolph/keyboard"


res = http.request('GET', base_url, headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36',
'Content-Type': 'text/plain; charset=utf-8 ',
'Accept': '*/*',
'Accept-Encoding': 'gzip, deflate, sdch',
'Accept-Language': 'en-US,en;q=0.8,vi;q=0.6',
'Cookie': '_octo=GH1.1.410384889.1403930039; logged_in=yes; dotcom_user=tuanchauict; _ga=GA1.2.1332205087.1380126985',
    })

print(res.status)
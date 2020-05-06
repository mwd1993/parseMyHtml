# parseMyHtml
Html DOM Parser Written in Python (library for data scraping)

Example Usage:

`
import requests
import parseMyHtml


url = 'https://markets.businessinsider.com/currencies/btc-usd'
_request = requests.get(url)
_request_html = _request.text

parser = parseMyHtml.parseMyHtml()
parser.parse(_request_html)

_price_element = parser.get_by_full_element('<span class="push-data " data-format="maximumFractionDigits:2" data-animation=""')

if len(_price_element) > 0:
    print("Bitcoin Price: " + str(_price_element[0].getAttribute("jsvalue")))
else:
    print(parser.html)
    print("Nothing found")
`

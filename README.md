# parseMyHtml
Html DOM Parser Written in Python (library for data scraping)

Example Usage:

```python
# --------------------------------------------------
# Gets the price of bitcoin from businessinsider.com
# --------------------------------------------------

# Import Requests
import requests
# Import parseMyHtml
import parseMyHtml

# URL Where the bitcoin price is located
url = 'https://markets.businessinsider.com/currencies/btc-usd'

# Get request html
# --------------------------
_request = requests.get(url)
_request_html = _request.text
# --------------------------

# Initiate the parseMyHtml Class
parser = parseMyHtml.parseMyHtml()

# Pass in the request html
parser.parse(_request_html)

# Get a list of elements that match this element text (Bitcoin price element)
_price_element = parser.get_by_full_element('<span class="push-data " data-format="maximumFractionDigits:2" data-animation=""')

# Make sure the list contains atleast one object
if len(_price_element) > 0:
    # The Bit Coin Price value is stored in the html webpage under the attribute jsvalue
    print("Bitcoin Price: " + str(_price_element[0].getAttribute("jsvalue")))
else:
    # Display the html returned from the request
    print(parser.html)
    print("Nothing found")

```

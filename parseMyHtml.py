# --------------------------------------------------
# Gets the price of bitcoin from businessinsider.com
# --------------------------------------------------

# Import Requests
import requests
# Import parseMyHtml
import parseMyHtml

# URL Where the bitcoin price is located
url = 'https://www.yahoo.com/news/weather'

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
# _price_element = parser.get_by_full_element('<a href="/questions/')
_price_element = parser.get_by_class('<span class="Va(t)" data-reactid="37">')

# Make sure the list contains atleast one object
if len(_price_element) > 0:
    # The Bit Coin Price value is stored in the html webpage under the attribute jsvalue
    # print("Bitcoin Price: " + str(_price_element[1].getAttribute("href")))
    _l =[]
    for _a in _price_element:
        _l.append(_a.text)

    print(str(_l))
else:
    # Display the html returned from the request
    print(parser.html)
    print("Nothing found")


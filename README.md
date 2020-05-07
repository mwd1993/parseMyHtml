# parseMyHtml
Html DOM Parser Written in Python (library for data scraping)

# Example 1:

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
    # OR print("Bitcoin Price: " + str(_price_element[0].text))
else:
    # Display the html returned from the request
    print(parser.html)
    print("Nothing found")

```

# Example 2:

```python
# ---------------------------------------------------------------
# Gets the amount of jobs available from the python jobs website
# ---------------------------------------------------------------

# Import Requests
import requests
# Import parseMyHtml
import parseMyHtml

# URL where the amount of available jobs is located
url = 'https://www.python.org/jobs/'

# Get request html
# --------------------------
_request = requests.get(url)
_request_html = _request.text
# --------------------------

# Initiate the parseMyHtml Class
parser = parseMyHtml.parseMyHtml()

# Pass in the request html
parser.parse(_request_html)

# Get a list of elements that match this element fully (remove trailing >)
_jobs_element = parser.get_by_full_element('<h1 class="call-to-action"')

# Make sure the list contains atleast one object
if len(_jobs_element) > 0:
    
    # Get the first returned element in the list
    __jobs_element = _jobs_element[0]
    
    # Scrape the value of the string and remove the excess string
    _text_jobs_available = "( " + __jobs_element.text[:__jobs_element.text.rfind("jobs on")].strip() + " )"
    
    # Get the attributes of the element object
    _text_jobs_attributes = __jobs_element.attributes
    
    # Get the value of the attribute 'class'
    _text_jobs_class = __jobs_element.getAttribute("class")
    
    # Print the jobs available, the attributes the element object contains, the value of 'class' of the object and the objects raw HTML
    # -----------------------------------------------------------------------------------------------------------------------------------
    print("Jobs available:\t\t" + _text_jobs_available + "\nElement Object Attributes:\t\t" + _text_jobs_attributes + "\nElement Object Class Value:\t\t" + _text_jobs_class)
    print("Element Object HTML:\t\t" + __jobs_element.getHtml())
    # -----------------------------------------------------------------------------------------------------------------------------------
else:
    # Display the html returned from the request
    print(parser.html)
    print("Nothing found")

```

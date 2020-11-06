def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def find_between_r(s, first, last):
    try:
        start = s.rindex(first) + len(first)
        end = s.rindex(last, start)
        return s[start:end]
    except ValueError:
        return ""


class parseMyHtml:
    def __init__(self):
        # HTML
        self.html = ""
        # List of accepted tags
        self.element_list = ["div", "font", "small", "p", "h1", "h2", "h3", "h4", "h5", "a", "span", "body","input"]

        # List of all tags that contain respective objects
        # -------------------------------------------------
        self.divs = []
        self.ps = []
        self.h1s = []
        self.h2s = []
        self.h3s = []
        self.h4s = []
        self.h5s = []
        self.bodys = []
        self.links = []
        self.spans = []
        self.smalls = []
        self.fonts = []
        self.inputs = []
        self.all = []
        # -------------------------------------------------

    # Loads in the html and creates objects in which you can extract data from
    def parse(self, html):
        # Clean HTML a bit
        self.html = html.replace("\n", "").replace("<br/>", "")
        # Array from html string split by >
        _array = self.html.split(">")

        _element_list = self.element_list

        # Define some variables
        _obj = ""
        _last_obj = ""
        _last_last_obj = ""
        _index = -1
        _type = ""
        # ----------------------

        # Each 'element' in the _array is the string split of the html >
        for element in _array:
            # Index of current element
            _index = _index + 1

            # If this element has opening but no closing bracket
            if "<" in element and "</" not in element:
                # Get the tag name _type
                if " " in element:
                    _type = element.strip().split(" ")[0]
                    _type = _type[1:]
                else:
                    _type = element.strip()
                    _type = _type[1:]

                # If our above attempt returns nothing
                if not _type:
                    # Make sure there is an opening bracket in the element
                    if "<" in element:
                        # Might be nested
                        _type = element.split("<")
                        _type = _type[1][0:].strip()
                        _type = _type.split(" ")[0]

                        # Clean up element since it was nested
                        element = element[element.rfind("<"):]

                        # print("in? " + (str(_type in _element_list)) + " type: " + _type + " - " + str(_element_list))

                # If we have a valid tag name from the element
                if _type:
                    # Make sure the tag name is an accepted element list item
                    if _type in _element_list:

                        # Initiate Values
                        _obj_vals = {
                            "type": _type,
                            "full": element + ">".strip(),
                            "attributes": element.replace("<" + _type, "").strip(),
                            "index": _index,
                            "text": ""
                        }

                        # Create a PMH Object
                        _obj = parseMyHtmlObject(self, _obj_vals)

                        __type = _type
                        if _type == "a":
                            __type = "link"

                        eval("self." + __type + "s.append(_obj)")
                else:
                    print("no type of " + element)

                if _obj:
                    _obj.full = _obj.full.strip()
                    # Append object to our all list
                    self.all.append(_obj)
            else:
                # -----------------------------------------------------------------------
                # We are probably in an element with a text value we can assign to the obj
                # -----------------------------------------------------------------------

                # If we have a previous object and no text value set to it
                if _last_obj and not _last_obj.text:
                    element_list = self.element_list
                    # Make sure it's a valid element
                    if _last_obj.type in element_list:
                        # Format and assign the text to the object
                        _last_obj.text = element
                        _last_obj.text = _last_obj.text[0:_last_obj.text.rfind("<")]
                        # Last last object?
                        _last_last_obj = _last_obj

            # Set the last object to the current object, we are at the end of the iteration
            _last_obj = _obj

    # Get a list of elements by the full element itself, or a partial match
    def get_by_full_element(self, el):
        _list = []
        for _obj in self.all:
            if el in _obj.full:
                _list.append(_obj)

        return _list

    # Get a list of elements specified by the class partial match or full match
    def get_by_class(self, _class):
        _list = []

        for _obj in self.all:
            if _class in _obj.attributes:
                _list.append(_obj)

        return _list


class parseMyHtmlObject:
    # _vals is a dictionary of values to assign
    def __init__(self, _parent, _vals):
        self.parent = _parent

        self.text = _vals["text"]
        self.attributes = _vals["attributes"]
        self.type = _vals["type"]
        self.full = _vals["full"]
        self.index = _vals["index"]

    def getHtml(self):

        # Split HTML into an array
        _html = self.parent.html
        _html_array = _html.split(">")

        # Level of depth inside of an element
        _down_level = 0

        # The initial starting element tag name
        _start = _html_array[self.index].strip()
        _start = _start.split(" ")[0]

        # We need this for now
        if _start == "a":
            _start = "<a"

        # Dictionary of closing syntax for html elements
        _closers = {
            "<p": "</p",
            "<div": "</div",
            "<a": "</a",
            "<div": "</div",
            "<h1": "</h1",
            "<h2": "</h2",
            "<span": "</span",
            "<a": "</a",
            "<input":"</input"
        }

        # Get the closer element key
        _closer = _closers[_start]

        # init some vars
        _build = ""
        _index = -1
        # --------------

        # Loop through all elements in the html array
        for _element in _html_array:

            _index = _index + 1

            # If the current element is less than our current element then do nothing
            if _index < self.index:
                continue

            # Concatenate Html String
            _build = _build + _element + ">"

            # If we find another element with the same tag name as our main tag name
            if _start in _element and _closer not in _element and _index > 0 and self.full not in _element:
                _down_level = _down_level + 1
                # print("going down a level " + _element)

            # If we find a closing tag with the same as our mains closing tag
            elif _closer in _element:
                _down_level = _down_level - 1
                # print("going up a level " + _element)

            # If we found the closing tag and we are at our main depth level
            # Then it is the final closing tag and everything in between is the 'innerHtml'
            if _closer in _element and _down_level == 0:
                break

        # Return the innerHtml of the object
        return _build.strip()

    # Gets the value of an element attribute
    def getAttribute(self, _type):
        _str = find_between(self.attributes, _type + "='", "'")
        if not _str:
            _str = find_between(self.attributes, _type + '="', '"')
        if not _str:
            _str = False
        return _str
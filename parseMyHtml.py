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
        self.html = ""

        self.elements = []

        self.divs = []
        self.ps = []
        self.h1s = []
        self.h2s = []
        self.h3s = []
        self.h4s = []
        self.bodys = []
        self.links = []
        self.spans = []
        self.smalls = []
        self.fonts = []
        self.all = []

    def get_index(self, type, index):
        _array = self.html.split("<" + type)
        print("<" + type + " - " + str(_array[index]) + "  " + str(len(_array)))

    def parse(self,html):
        self.html = html
        _array = self.html.split(">")
        _obj = ""
        for element in _array:
            # print(element)
            if "<" in element and "</" not in element:
                if "<div" in element:
                    _obj = parseMyHtmlObject()
                    _obj.type = "div"
                    _obj.full = element + ">"
                    _obj.attributes = element.replace("<div", "").strip()
                    # print("attributes (" + _obj.attributes + ")")
                    self.divs.append(_obj)

                if "<font" in element:
                    _obj = parseMyHtmlObject()
                    _obj.type = "font"
                    _obj.full = element + ">"
                    _obj.attributes = element.replace("<font", "").strip()
                    # print("attributes (" + _obj.attributes + ")")
                    self.fonts.append(_obj)

                if "<small" in element:
                    _obj = parseMyHtmlObject()
                    _obj.type = "small"
                    _obj.full = element + ">"
                    _obj.attributes = element.replace("<small", "").strip()
                    # print("attributes (" + _obj.attributes + ")")
                    self.smalls.append(_obj)
                    print("found small")

                if "<p" in element:
                    _obj = parseMyHtmlObject()
                    _obj.type = "p"
                    _obj.full = element + ">"
                    _obj.attributes = element.replace("<p", "").strip()
                    # print("attributes (" + _obj.attributes + ")")
                    self.ps.append(_obj)

                if "<h1" in element:
                    _obj = parseMyHtmlObject()
                    _obj.type = "h1"
                    _obj.full = element + ">"
                    _obj.attributes = element.replace("<h1", "").strip()
                    # print("attributes (" + _obj.attributes + ")")
                    self.h1s.append(_obj)

                if "<h2" in element:
                    _obj = parseMyHtmlObject()
                    _obj.type = "h2"
                    _obj.full = element + ">"
                    _obj.attributes = element.replace("<h2", "").strip()
                    # print("attributes (" + _obj.attributes + ")")
                    self.h2s.append(_obj)

                if "<h3" in element:
                    _obj = parseMyHtmlObject()
                    _obj.type = "h3"
                    _obj.full = element + ">"
                    _obj.attributes = element.replace("<h3", "").strip()
                    # print("attributes (" + _obj.attributes + ")")
                    self.h3s.append(_obj)

                if "<h4" in element:
                    _obj = parseMyHtmlObject()
                    _obj.type = "h4"
                    _obj.full = element + ">"
                    _obj.attributes = element.replace("<h4", "").strip()
                    # print("attributes (" + _obj.attributes + ")")
                    self.h4s.append(_obj)

                if "<a" in element:
                    _obj = parseMyHtmlObject()
                    _obj.type = "a"
                    _obj.full = element + ">"
                    _obj.attributes = element.replace("<a", "").strip()
                    _obj.link = find_between(_obj.attributes, "href='", "'")
                    # print("attributes (" + _obj.attributes + ")")
                    self.links.append(_obj)

                if "<span" in element:
                    _obj = parseMyHtmlObject()
                    _obj.type = "span"
                    _obj.full = element + ">"
                    _obj.attributes = element.replace("<span", "").strip()
                    # _obj.link = find_between(_obj.attributes,"href='","'")
                    # print("attributes (" + _obj.attributes + ")")
                    self.spans.append(_obj)

                if "<body" in element:
                    _obj = parseMyHtmlObject()
                    _obj.type = "body"
                    _obj.full = element + ">"
                    _obj.attributes = element.replace("<body", "").strip()
                    # print("attributes (" + _obj.attributes + ")")
                    self.bodys.append(_obj)

                if _obj:
                    _obj.full = _obj.full.strip()
                    self.all.append(_obj)
            else:
                if _last_obj and not _last_obj.text:
                    element_list = [
                        "a",
                        "div",
                        "small",
                        "p",
                        "h",
                        "span",
                        "font"
                    ]
                    if _last_obj.type in element_list:
                        _last_obj.text = element
                        _last_obj.text = _last_obj.text[0:_last_obj.text.rfind("<")]
                        # print(_last_obj.type + " -> " + _last_obj.text)
            _last_obj = _obj

    def get_by_full_element(self, el):
        _list = []
        for _obj in self.all:
            if el in _obj.full:
                _list.append(_obj)

        return _list

    def get_by_class(self, _class):
        _list = []

        for _obj in self.all:
            if _class in _obj.attributes:
                _list.append(_obj)

        return _list


class parseMyHtmlObject:
    def __init__(self):
        self.text = ""
        self.attributes = ""

    def getAttribute(self, _type):
        _str = find_between(self.attributes, _type + "='", "'")
        if not _str:
            _str = find_between(self.attributes, _type + '="', '"')

        if not _str:
            _str = False

        return _str

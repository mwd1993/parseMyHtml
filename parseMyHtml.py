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

    def parse(self, html):
        self.html = html.replace("\n", "")
        self.html = self.html.replace("<br/>", "")
        _array = self.html.split(">")
        # print(str(_array))
        _element_list = ["div", "font", "small", "p", "h1", "h2", "h3", "h4", "h5", "a", "span", "body"]
        _obj = ""
        _last_obj = ""
        _last_last_obj = ""
        _index = -1
        _type = ""
        for element in _array:
            _index = _index + 1
            if "<" in element and "</" not in element:

                if " " in element:
                    _type = element.strip().split(" ")[0]
                    _type = _type[1:]
                else:
                    _type = element.strip()
                    _type = _type[1:]

                # print(element)

                if not _type:
                    if "<" in element:
                        _type = element.split("<")
                        _type = _type[1][0:].strip()
                        _type = _type.split(" ")[0]
                        element = element[element.rfind("<"):]

                        #print("in? " + (str(_type in _element_list)) + " type: " + _type + " - " + str(_element_list))

                if _type:
                    #print("type = " + _type + " in element " + element)
                    if _type in _element_list:

                        _obj = parseMyHtmlObject(self)
                        _obj.type = _type
                        _obj.full = element + ">".strip()
                        _obj.attributes = element.replace("<" + _type, "").strip()
                        _obj.index = _index

                        __type = _type

                        if _type == "a":
                            __type = "link"

                        eval("self." + __type + "s.append(_obj)")
                else:
                    print("no type of " + element)

                if _obj:
                    _obj.full = _obj.full.strip()
                    self.all.append(_obj)
            else:
                if "</" in element:

                    if _last_obj and _last_last_obj:
                        # print("closer " + element + "\nlast_obj = " + _last_last_obj.full)
                        pass

                if _last_obj and not _last_obj.text:
                    element_list = [
                        "a",
                        "div",
                        "small",
                        "p",
                        "h1",
                        "h2",
                        "h3",
                        "h4",
                        "h5",
                        "span",
                        "font"
                    ]
                    if _last_obj.type in element_list:
                        # print(_last_obj.type + " setting text to " + _last_obj.attributes)

                        _last_obj.text = element
                        _last_obj.text = _last_obj.text[0:_last_obj.text.rfind("<")]

                        _last_last_obj = _last_obj

            _last_obj = _obj

    def get_by_full_element(self, el):
        # print(el[:-1])
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
    def __init__(self, _parent):
        self.parent = _parent
        self.text = ""
        self.attributes = ""

    def getHtml(self):
        _down_level = 0
        _html = self.parent.html

        _html_array = _html.split(">")

        _start = _html_array[self.index].strip()
        _start = _start.split(" ")[0]

        if _start == "a":
            _start = "<a"

        # print("start = " + _start)

        _closers = {
            "<p": "</p",
            "<div": "</div",
            "<a": "</a",
            "<div": "</div",
            "<h1": "</h1",
            "<h2": "</h2",
            "<span": "</span",
            "<a":"</a"
        }

        _closer = _closers[_start]

        _build = ""

        _index = -1
        for _element in _html_array:
            _index = _index + 1
            if _index < self.index:
                # print("passing " + str(_index))
                continue
            _build = _build + _element + ">"
            if _start in _element and not _closer in _element and _index > 0 and self.full not in _element:
                _down_level = _down_level + 1
                # print("going down a level " + _element)
            elif _closer in _element:
                _down_level = _down_level - 1
                # print("going up a level " + _element)

            if _closer in _element and _down_level == 0:
                # print("found closer -> " + _element)
                break

        # print(str(_html_array) + " - start " + _start + " - closer " + _closer)
        # print("build: " + _build)
        return _build.strip()

    def getAttribute(self, _type):
        _str = find_between(self.attributes, _type + "='", "'")
        if not _str:
            _str = find_between(self.attributes, _type + '="', '"')

        if not _str:
            _str = False

        return _str

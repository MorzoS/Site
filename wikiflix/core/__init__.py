from flask import url_for

class NavBar:
    _default_bar = None

    class NavElement:

        def __init__(self, text: str, link: str = "#", active: bool = False):
            self.text = text
            self.link = link
            self.active = active
        
        def __str__(self):
            return f"[{self.text}, {self.link}, {self.active}]"

    def __init__(self, *elements):
        self.elements = elements

    def __str__(self):
        return str(self.elements)

    @classmethod
    def default_bar(cls, active_page=None):
        if not cls._default_bar:
            cls._default_bar = NavBar(
                cls.NavElement("home", url_for("home.home")),
                cls.NavElement("404", "Anywhere")
            )
        for element in cls._default_bar.elements:
            element.active = True if element.text == active_page else False

        return cls._default_bar
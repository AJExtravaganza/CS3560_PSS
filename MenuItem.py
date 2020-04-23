class MenuItem:
    def __init__(self, text: str, on_select_function=None):
        self.text = text
        self.on_select = on_select_function

    def __str__(self):
        return self.text

    def process(self):
        if self.on_select is not None:
            return self.on_select()

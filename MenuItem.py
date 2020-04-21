class MenuItem:
    def __init__(self, text: str, on_select):
        self.text = text
        self.on_select = on_select

    def __str__(self):
        return self.text

    def do(self):
        self.on_select()

    def get(self):
        return self.on_select()

class Word:
    def __init__(self, word, pos, word_class=None):
        self.word = word
        self.pos = pos
        self.gematria = self.get_gematria(word)
        self.r2r = self.route_to_root(self.gematria)
        self.word_class=word_class
        if word_class not in ["NOUN", "VERB", "ADJECTIVE", "ADVERB"]:
            self.word_class = None

        self.children = []

    def route_to_root(self, gematria):
        route = []
        while gematria > 0:
            route.append(gematria % 22)
            gematria = gematria // 22
        return route

    def add_child(self, child):
        self.children.append(child)

    def get_gematria(self, word):
        gematria = 0
        for letter in word:
            gematria += ord(letter) - 1487
        return gematria

    def __str__(self):
        return self.word + " " + self.pos

    def __repr__(self):
        return self.word + " " + self.pos
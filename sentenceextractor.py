class SentenceExtractor:
    def __init__(self, path):
        self.path = path
        self.unprocessed_tokens = []
        self.sentence_iterator = None
    
    def _is_end_of_sentence(self, text):
        text = str(text)
        sentence_end_chars = [".", "?", "!", ";"]
        return True in (text.endswith(char) for char in sentence_end_chars)

    def lines(self):
        with open(self.path) as file:
            for line in file:
                yield line

    def sentence_generator(self):
        lines = self.lines()
        next_sentence = []
        
        while True:
            if len(self.unprocessed_tokens) == 0:
                try: #Token habis, ambil baris selanjutnya dari teks.
                    new_line = next(lines)
                    new_tokens = self.separate_tokens(new_line)
                    self.unprocessed_tokens += new_tokens
                except StopIteration:
                    if len(self.unprocessed_tokens) > 0:
                        last_sentence = ' '.join(self.unprocessed_tokens) 
                        yield last_sentence
                    raise StopIteration

            while len(self.unprocessed_tokens) > 0:
                token = self.unprocessed_tokens.pop(0)  #Ambil token selanjutnya.
                next_sentence.append(token)
                if self._is_end_of_sentence(token):
                    new_sentence = ' '.join(next_sentence)
                    next_sentence = [] 
                    yield new_sentence

    def __iter__(self):
        self.sentence_iterator = self.sentence_generator()
        return self

    def __next__(self): return next(self.sentence_iterator)

    def separate_tokens(self, line):
            tokens = line.split(" ")

            #filter token kosong
            return [token.strip() for token in tokens if token != ""]

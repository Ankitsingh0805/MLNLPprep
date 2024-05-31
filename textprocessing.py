import re

class TextProcess:
    def __init__(self, text):
        self.text = text
    
    def tokenize(self):
        self.text = re.findall(r'\b\w+\b', self.text)
    
    def remove_stopwords(self):
        stopwords = set([
            "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves",
            "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",
            "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are",
            "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
            "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about",
            "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up",
            "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when",
            "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no",
            "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don",
            "should", "now", "n't", "'s", "'re", "'ve", "'ll", "'d"
        ])
        self.text = [word for word in self.text if word.lower() not in stopwords]
    
    def stem(self, word):
        suffixes = ['ing', 'ly', 'es', 's']
        for suffix in suffixes:
            if word.endswith(suffix):
                word = word[:-len(suffix)]
        return word
        
    def lemmatize(self, word):
        if word.endswith('s'):
            return word[:-1]
        elif word.endswith('ing'):
            return word[:-3]
        elif word.endswith('ly'):
            return word[:-2]
        return word
        
    def handle_negations(self):
        self.text = [word.replace("n't", " not") if word.endswith("n't") else word for word in self.text]
    
    def handle_contractions(self):
        contractions = {
            "'s": " is", "'re": " are", "'ve": " have", "'ll": " will", "'d": " would"
        }
        self.text = [contractions[word] if word in contractions else word for word in self.text]
    
    def clean(self, options):
        if options.get('tokenize', False):
            self.tokenize()
        if options.get('remove_stopwords', False):
            self.remove_stopwords()
        if options.get('stem', False):
            self.text = [self.stem(word) for word in self.text]
        if options.get('lemmatize', False):
            self.text = [self.lemmatize(word) for word in self.text]
        if options.get('handle_negations', False):
            self.handle_negations()
        if options.get('handle_contractions', False):
            self.handle_contractions()
        return ' '.join(self.text)

class FileTextCleaner:
    def __init__(self, input_filepath, output_filepath):
        self.input_filepath = input_filepath
        self.output_filepath = output_filepath
    
    def read_file(self):
        with open(self.input_filepath, 'r') as file:
            text = file.read()
        return text
    
    def write_file(self, text):
        with open(self.output_filepath, 'w') as file:
            file.write(text)
    
    def clean_text(self, options):
        text_cleaner = TextProcess(self.read_file())
        cleaned_text = text_cleaner.clean(options)
        self.write_file(cleaned_text)  

if __name__ == "__main__":
    input_filepath = input("Enter the path to the input file: ")
    output_filepath = input("Enter the path to the output file: ")

    cleaner = FileTextCleaner(input_filepath, output_filepath)

    options = {
        'tokenize': True,
        'remove_stopwords': True,
        'stem': True, 
        'lemmatize': True,
        'handle_negations': True,
        'handle_contractions': True
    }
    cleaner.clean_text(options)

    print(f"Processed data has been saved to: {output_filepath}")




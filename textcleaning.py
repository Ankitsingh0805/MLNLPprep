import string
import re

class TextCleaner:
    def __init__(self, text):
        self.text = text
    
    def lowercase(self):
        self.text = self.text.lower()
    
    def remove_punctuation(self):
        self.text = self.text.translate(str.maketrans('', '', string.punctuation))
    
    def remove_special_characters(self):
        self.text = re.sub(r'[^a-zA-Z0-9\s]', '', self.text)
    
    def remove_numbers(self):
        self.text = re.sub(r'\d+', '', self.text)
    
    def remove_whitespace(self):
        self.text = ' '.join(self.text.split())
    
    def clean(self, options):
        if options.get('lowercase', False):
            self.lowercase()
        if options.get('remove_punctuation', False):
            self.remove_punctuation()
        if options.get('remove_special_characters', False):
            self.remove_special_characters()
        if options.get('remove_numbers', False):
            self.remove_numbers()
        if options.get('remove_whitespace', False):
            self.remove_whitespace()
        return self.text

class TextFileCleaner:
    def __init__(self, input_filepath, output_filepath, delimiter=' '):
        self.input_filepath = input_filepath
        self.output_filepath = output_filepath
        self.delimiter = delimiter
        self.headers, self.data = self.read_file_data()

    def read_file_data(self):
        with open(self.input_filepath, 'r') as file:
            lines = file.readlines()
            headers = lines[0].strip().split(self.delimiter)
            data = [line.strip().split(self.delimiter) for line in lines[1:]]
        return headers, data

    def write_file_data(self, headers, data):
        with open(self.output_filepath, 'w') as file:
            file.write(self.delimiter.join(headers) + '\n')
            for row in data:
                file.write(self.delimiter.join(row) + '\n')
    
    def clean_text_columns(self, options):
        num_columns = len(self.headers)
        
        for row_index, row in enumerate(self.data):
            if len(row) < num_columns:
                row.extend([''] * (num_columns - len(row)))
            elif len(row) > num_columns:
                row = row[:num_columns]

            for col_index in range(num_columns):
                cleaner = TextCleaner(row[col_index])
                row[col_index] = cleaner.clean(options)
        
        self.write_file_data(self.headers, self.data)








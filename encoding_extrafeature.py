import csv
import numpy as np
from collections import defaultdict

class DataProcessor:
    def __init__(self, filepath):
        self.filepath = filepath
        self.headers, self.data = self.read_csv_data()
        self.categorical_indices = []
        self.numerical_indices = []
        self.unique_values = defaultdict(list)
        self.selected_column_indices = []

    def read_csv_data(self):
        with open(self.filepath, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)
            data = [row for row in reader]
        return headers, data

    def write_csv_data(self, filepath, data, headers=None):
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            if headers:
                writer.writerow(headers)
            writer.writerows(data)

    def one_hot_encode(self):
        for col_index in self.categorical_indices:
            self.unique_values[col_index] = list(set(row[col_index] for row in self.data))
        
        encoded_data = []
        for row in self.data:
            encoded_row = []
            for col_index, value in enumerate(row):
                if col_index in self.categorical_indices:
                    for unique_value in self.unique_values[col_index]:
                        encoded_row.append(1 if value == unique_value else 0)
                else:
                    encoded_row.append(value)
            encoded_data.append(encoded_row)
        self.data = encoded_data

    def label_encode(self):
        label_encoded_data = []
        for col_index in self.categorical_indices:
            self.unique_values[col_index] = {value: idx for idx, value in enumerate(set(row[col_index] for row in self.data))}
        
        for row in self.data:
            encoded_row = []
            for col_index, value in enumerate(row):
                if col_index in self.categorical_indices:
                    encoded_row.append(self.unique_values[col_index][value])
                else:
                    encoded_row.append(value)
            label_encoded_data.append(encoded_row)
        self.data = label_encoded_data

    def create_new_feature(self, index1, index2):
        for row in self.data:
            row.append(float(row[index1]) * float(row[index2]))

    def select_features(self, column_indices):
        selected_data = [[row[idx] for idx in column_indices] for row in self.data]
        selected_headers = [self.headers[idx] for idx in column_indices]
        self.data = selected_data
        self.headers = selected_headers

    def remove_low_variance_features(self, threshold=0.0):
        numeric_data = np.array(self.data, dtype=float)
        variances = np.var(numeric_data, axis=0)
        selected_indices = [i for i, var in enumerate(variances) if var > threshold]
        
        self.select_features(selected_indices)

    def process(self, feature_method='select'):
        if feature_method == 'select':
            self.select_features(self.selected_column_indices)
        elif feature_method == 'remove_low_variance':
            self.remove_low_variance_features()

    def set_categorical_indices(self, categorical_indices):
        self.categorical_indices = categorical_indices

    def set_numerical_indices(self, numerical_indices):
        self.numerical_indices = numerical_indices

    def set_selected_column_indices(self, selected_column_indices):
        self.selected_column_indices = selected_column_indices




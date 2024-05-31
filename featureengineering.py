import csv

class CSVScaler:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = self.read_csv_data()

    def read_csv_data(self):
        with open(self.filepath, 'r') as file:
            data = []
            for line in file:
                data.append(line.strip().split(','))
        return data

    def write_csv_data(self, filepath, data):
        with open(filepath, 'w') as file:
            for row in data:
                file.write(','.join(row) + '\n')

    def get_columns_to_process(self):
        headers = self.data[0]
        print("Columns in the dataset:")
        for idx, header in enumerate(headers):
            print(f"{idx}: {header}")

        selected_columns = input("Enter the column numbers to process, separated by commas: ")
        column_indices = list(map(int, selected_columns.split(',')))
        return column_indices

    def normalize(self, columns):
        normalized_data = [self.data[0]] 
        for i in range(len(self.data[0])):
            if i in columns:
                column = [float(row[i]) for row in self.data[1:]]
                min_val, max_val = min(column), max(column)
                normalized_column = [(x - min_val) / (max_val - min_val) if max_val != min_val else 0 for x in column]
                for j, value in enumerate(normalized_column):
                    if len(normalized_data) <= j + 1:
                        normalized_data.append(self.data[j + 1][:]) 
                    normalized_data[j + 1][i] = str(value)
            else:
                for j, row in enumerate(self.data[1:]):
                    if len(normalized_data) <= j + 1:
                        normalized_data.append(row[:])  
        return normalized_data

    def standardize(self, columns):
        standardized_data = [self.data[0]]  
        for i in range(len(self.data[0])):
            if i in columns:
                column = [float(row[i]) for row in self.data[1:]]
                mean_val = sum(column) / len(column)
                std_dev = (sum([(x - mean_val) ** 2 for x in column]) / len(column)) ** 0.5
                standardized_column = [(x - mean_val) / std_dev if std_dev != 0 else 0 for x in column]
                for j, value in enumerate(standardized_column):
                    if len(standardized_data) <= j + 1:
                        standardized_data.append(self.data[j + 1][:]) 
                    standardized_data[j + 1][i] = str(value)
            else:
                for j, row in enumerate(self.data[1:]):
                    if len(standardized_data) <= j + 1:
                        standardized_data.append(row[:]) 
        return standardized_data

    def robust_scale(self, columns):
        robust_scaled_data = [self.data[0]]  
        for i in range(len(self.data[0])):
            if i in columns:
                column = [float(row[i]) for row in self.data[1:]]
                median_val = sorted(column)[len(column) // 2]
                q1 = sorted(column)[len(column) // 4]
                q3 = sorted(column)[3 * len(column) // 4]
                iqr = q3 - q1
                robust_scaled_column = [(x - median_val) / iqr if iqr != 0 else 0 for x in column]
                for j, value in enumerate(robust_scaled_column):
                    if len(robust_scaled_data) <= j + 1:
                        robust_scaled_data.append(self.data[j + 1][:]) 
                    robust_scaled_data[j + 1][i] = str(value)
            else:
                for j, row in enumerate(self.data[1:]):
                    if len(robust_scaled_data) <= j + 1:
                        robust_scaled_data.append(row[:])  
        return robust_scaled_data

    def mean_normalize(self, columns):
        mean_normalized_data = [self.data[0]] 
        for i in range(len(self.data[0])):
            if i in columns:
                column = [float(row[i]) for row in self.data[1:]]
                mean_val = sum(column) / len(column)
                min_val, max_val = min(column), max(column)
                mean_normalized_column = [(x - mean_val) / (max_val - min_val) if max_val != min_val else 0 for x in column]
                for j, value in enumerate(mean_normalized_column):
                    if len(mean_normalized_data) <= j + 1:
                        mean_normalized_data.append(self.data[j + 1][:])  
                    mean_normalized_data[j + 1][i] = str(value)
            else:
                for j, row in enumerate(self.data[1:]):
                    if len(mean_normalized_data) <= j + 1:
                        mean_normalized_data.append(row[:]) 
        return mean_normalized_data

    def process(self, scaling_method):
        columns = self.get_columns_to_process()
        if scaling_method == 'normalize':
            scaled_data = self.normalize(columns)
        elif scaling_method == 'standardize':
            scaled_data = self.standardize(columns)
        elif scaling_method == 'robust_scale':
            scaled_data = self.robust_scale(columns)
        elif scaling_method == 'mean_normalize':
            scaled_data = self.mean_normalize(columns)
        else:
            print("Invalid scaling method!")
            scaled_data = self.data

        return scaled_data




 



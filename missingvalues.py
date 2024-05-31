class CSVProcessor:
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

    def find_missing_values(self):
        missing_values = []
        for i, row in enumerate(self.data):
            for j, cell in enumerate(row):
                if cell == '':
                    missing_values.append((i, j))
        return missing_values

    def delete_rows(self, missing_values):
        cleaned_data = [row for i, row in enumerate(self.data) if i not in {idx[0] for idx in missing_values}]
        return cleaned_data

    def delete_cols(self, missing_values):
        cleaned_data = []
        num_cols = len(self.data[0])
        cols_to_delete = {idx[1] for idx in missing_values}
        for row in self.data:
            cleaned_row = [cell for j, cell in enumerate(row) if j not in cols_to_delete]
            cleaned_data.append(cleaned_row)
        return cleaned_data

    def remove_duplicates(self):
        unique_data = []
        seen_rows = set()
        for row in self.data:
            row_tuple = tuple(row)
            if row_tuple not in seen_rows:
                unique_data.append(row)
                seen_rows.add(row_tuple)
        return unique_data

    def impute_mean(self, missing_values):
        for idx in missing_values:
            row_idx, col_idx = idx
            numeric_values = [float(row[col_idx]) for row in self.data if row[col_idx] != '']
            mean_value = sum(numeric_values) / len(numeric_values) if numeric_values else 0
            self.data[row_idx][col_idx] = str(mean_value)
        return self.data

    def impute_median(self, missing_values):
        for idx in missing_values:
            row_idx, col_idx = idx
            numeric_values = [float(row[col_idx]) for row in self.data if row[col_idx] != '']
            numeric_values.sort()
            mid_index = len(numeric_values) // 2
            if len(numeric_values) % 2 == 0:
                median_value = (numeric_values[mid_index - 1] + numeric_values[mid_index]) / 2
            else:
                median_value = numeric_values[mid_index]
            self.data[row_idx][col_idx] = str(median_value)
        return self.data

    def impute_mode(self, missing_values):
        for idx in missing_values:
            row_idx, col_idx = idx
            non_missing_values = [row[col_idx] for row in self.data if row[col_idx] != '']
            value_counts = {}
            for value in non_missing_values:
                value_counts[value] = value_counts.get(value, 0) + 1
            mode_value = max(value_counts, key=value_counts.get)
            self.data[row_idx][col_idx] = mode_value
        return self.data

    def process(self, actions):
        missing_values = self.find_missing_values()
        for action in actions:
            if action == 'delete_rows':
                self.data = self.delete_rows(missing_values)
            elif action == 'delete_cols':
                self.data = self.delete_cols(missing_values)
            elif action == 'impute_mean':
                self.data = self.impute_mean(missing_values)
            elif action == 'impute_median':
                self.data = self.impute_median(missing_values)
            elif action == 'impute_mode':
                self.data = self.impute_mode(missing_values)
            elif action == 'remove_duplicates':
                self.data = self.remove_duplicates()
            else:
                print(f"Invalid action: {action}")
        return self.data


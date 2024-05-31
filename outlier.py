import csv

class CSVDataHandler:
    def __init__(self, filepath):
        self.filepath = filepath
        self.header, self.data = self.read_csv_data()

    def read_csv_data(self):
        try:
            with open(self.filepath, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)
                data = list(reader)
                return header, data
        except FileNotFoundError:
            print(f"Error: File '{self.filepath}' not found.")
            return None, None

    def z_score_outliers(self, column_name, threshold=3):
        if self.data is not None:
            try:
                column_index = self.header.index(column_name)
                values = [float(row[column_index]) for row in self.data]
                mean = sum(values) / len(values)
                std = (sum((x - mean) ** 2 for x in values) / len(values)) ** 0.5
                z_scores = [(x - mean) / std for x in values]
                outlier_flags = [abs(z) > threshold for z in z_scores]
                outliers = [self.data[i] for i, flag in enumerate(outlier_flags) if flag]
                return outlier_flags, outliers
            except ValueError:
                print(f"Error: Column '{column_name}' does not exist.")
                return None, None
        else:
            return None, None

    def handle_outliers(self, column_name, outlier_flags):
        if self.data is not None:
            print(f"Handling outliers in '{column_name}'")
            choice = input("Choose (r)emove or (c)ap outliers? (default: r): ").lower()
            if choice == 'c':
                cap_value = float(input("Enter the capping value (a number within the data range): "))
                column_index = self.header.index(column_name)
                for i, flag in enumerate(outlier_flags):
                    if flag:
                        self.data[i][column_index] = str(cap_value)
            else:
                self.data = [row for i, row in enumerate(self.data) if not outlier_flags[i]]

    def save_filtered_data(self, new_filepath):
        if self.data is not None:
            with open(new_filepath, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.header)
                writer.writerows(self.data)
                print(f"Filtered data saved to: {new_filepath}")
        else:
            print("No data to save.")







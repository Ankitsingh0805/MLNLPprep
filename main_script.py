import typer
from missingvalues import CSVProcessor
from featureengineering import CSVScaler
from encoding_extrafeature import DataProcessor
from outlier import CSVDataHandler
from textcleaning import TextFileCleaner
from textprocessing import FileTextCleaner

app = typer.Typer()

@app.command()
def handle_csv_data(csv_filepath: str, output_filepath: str):
    handler = CSVDataHandler(csv_filepath)
    if handler.data is not None and len(handler.data) > 0:
        column_name = input("Enter the name of the column to analyze for outliers: ")
        if column_name in handler.header:
            outlier_flags, outliers = handler.z_score_outliers(column_name)
            if outlier_flags is not None:
                if outliers:
                    print(f"Identified outliers: {outliers}")
                handler.handle_outliers(column_name, outlier_flags)
                handler.save_filtered_data(output_filepath)
            else:
                print("No outliers detected.")
        else:
            print(f"Error: Column '{column_name}' not found in the CSV file.")
    else:
        print("Data loading failed. Please check the file path and try again.")

@app.command()
def process_csv_file(input_filepath: str, output_filepath: str):
    perform_action = input("Do you want to process CSV file? (yes/no): ").lower()
    if perform_action == 'yes':
        actions = input("Enter the actions you want to perform (comma-separated) [delete_rows,delete_cols,impute_mean,impute_median,impute_mode,remove_duplicates]: ").split(',')
        processor = CSVProcessor(input_filepath)
        processed_data = processor.process(actions)
        processor.write_csv_data(output_filepath, processed_data)
    else:
        print("Skipping processing CSV file.")

@app.command()
def scale_csv_data(input_filepath: str, output_filepath: str, scaling_method: str):
    scaler = CSVScaler(input_filepath)
    scaled_data = scaler.process(scaling_method)
    scaler.write_csv_data(output_filepath, scaled_data)
    print(f"Scaled data saved to: {output_filepath}")

@app.command()
def process_data_file(input_filepath: str, output_filepath: str):
    perform_action = input("Do you want to process data file? (yes/no): ").lower()
    if perform_action == 'yes':
        processor = DataProcessor(input_filepath)
        processor.process()
        processor.write_csv_data(output_filepath, processor.data, processor.headers)  # Pass data and headers
    else:
        print("Skipping processing data file.")


@app.command()
def clean_text_file(input_filepath: str, output_filepath: str):
    perform_action = input("Do you want to clean text file? (yes/no): ").lower()
    if perform_action == 'yes':
        options = {
            'lowercase': input("Convert text to lowercase? (yes/no): ").lower() == 'yes',
            'remove_punctuation': input("Remove punctuation? (yes/no): ").lower() == 'yes',
            'remove_special_characters': input("Remove special characters? (yes/no): ").lower() == 'yes',
            'remove_numbers': input("Remove numbers? (yes/no): ").lower() == 'yes',
            'remove_whitespace': input("Remove extra whitespace? (yes/no): ").lower() == 'yes'
        }
        
        delimiter = input("Enter the delimiter used in the file (leave blank for whitespace): ")
        delimiter = delimiter if delimiter else ' '
        
        cleaner = TextFileCleaner(input_filepath, output_filepath, delimiter)
        cleaner.clean_text_columns(options)
        print(f"Processed data has been saved to: {output_filepath}")
    else:
        print("Skipping cleaning text file.")

@app.command()
def clean_text_file(input_filepath: str, output_filepath: str):
    perform_action = input("Do you want to clean text file? (yes/no): ").lower()
    if perform_action == 'yes':
        options = {
            'tokenize': input("Tokenize text? (yes/no): ").lower() == 'yes',
            'remove_stopwords': input("Remove stopwords? (yes/no): ").lower() == 'yes',
            'stem': input("Apply stemming? (yes/no): ").lower() == 'yes',
            'lemmatize': input("Apply lemmatization? (yes/no): ").lower() == 'yes',
            'handle_negations': input("Handle negations? (yes/no): ").lower() == 'yes',
            'handle_contractions': input("Handle contractions? (yes/no): ").lower() == 'yes'
        }
        
        cleaner = TextFileCleaner(input_filepath, output_filepath)
        cleaner.clean_text(options)
        print(f"Processed data has been saved to: {output_filepath}")
    else:
        print("Skipping cleaning text file.")

if __name__ == "__main__":
    app()












# this python file samples number_of_rows of class 1 and class 2 data 
# from input_csv_file
import pandas as pd


input_csv_file = './processed_en_dataset.csv'  # Replace with your input CSV file path
output_csv_file = './sample.csv'  # Replace with your desired output CSV file path
number_of_rows = 5000  # Replace with the desired number of rows for each class


def filter_and_write_csv(input_file, output_file, number_of_rows):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_file)

    # Filter rows for class1 (success == 1)
    class1_df = df[df['success'] == 1].head(number_of_rows)

    # Filter rows for class2 (assuming success != 1, adjust as needed)
    class2_df = df[df['success'] != 1].head(number_of_rows)

    # Concatenate the two DataFrames
    result_df = pd.concat([class1_df, class2_df])

    # Write the result to a new CSV file
    result_df.to_csv(output_file, index=False)


filter_and_write_csv(input_csv_file, output_csv_file, number_of_rows)

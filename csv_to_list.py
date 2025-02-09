import pandas as pd

def csv_to_list(csv_file_path):
    """
    Converts a CSV file to a list of dictionaries.

    Args:
        csv_file_path (str): The file path of the CSV file.

    Returns:
        list: A list of dictionaries where each row is represented as a dictionary.
    """
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)

        # Convert DataFrame to a list of dictionaries
        data_list = df.to_dict(orient="records")

        return data_list

    except Exception as e:
        print(f"❌ Error processing CSV file: {e}")
        return []

# Example Usage
if __name__ == "__main__":
    file_path = "example.csv"  # Change this to your CSV file path
    result = csv_to_list(file_path)

    print("Converted List of Dictionaries:")
    for item in result[:5]:  # Print only first 5 rows for readability
        print(item)

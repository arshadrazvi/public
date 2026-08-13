'''
prompt:
    Create a Python function to export logs to CSV format:
    - Function name: export_logs_to_csv
    - Use Python's csv module
    - Write headers: Timestamp, Level, Message
    - Write each log as a row in the CSV
    - Print confirmation message when done
    - Include example usage

'''
import csv
from datetime import datetime
from itertools import islice
import os

# Constants
CHUNK_SIZE = 1000  # Number of lines to process at a time

def parse_log_line(line):
    """
    Parses a single log line into a dictionary with keys: timestamp, level, message.
    
    Parameters:
    - line (str): A single line from the log file.
    
    Returns:
    - dict: A dictionary containing the timestamp, level, and message of the log entry.
    """
    # Split the line into components
    date, timestamp, level, *message = line.lstrip().split(' ', 3)
    # Join the message parts back into a single string
    message = ' '.join(message)
    # Return a dictionary
    return {'date': date, 'timestamp': timestamp, 'level': level, 'message': message}

def parse_log_file(file_path, chunk_size=CHUNK_SIZE):
    """
    Generator function to read a log file in chunks and yield parsed log lines.
    
    Parameters:
    - file_path (str): Path to the log file.
    - chunk_size (int): Number of lines to read at a time.
    
    Yields:
    - list: A list of dictionaries, each representing a parsed log line.
    """
    with open(file_path, 'r') as file:
        while True:
            lines = list(islice(file, chunk_size))
            if not lines:
                break
            yield [parse_log_line(line) for line in lines]

def filter_logs_by_date_range(parsed_logs, start_date, end_date):
    """
    Filters logs based on a specified date range.
    
    Parameters:
    - parsed_logs (list): A list of dictionaries, each representing a parsed log line.
    - start_date (str): The start date of the range in 'YYYY-MM-DD' format.
    - end_date (str): The end date of the range in 'YYYY-MM-DD' format.
    
    Returns:
    - list: A list of dictionaries representing logs within the specified date range.
    """
    # Convert start_date and end_date to datetime objects for comparison
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Filter logs based on the date range
    filtered_logs = [
        log for log in parsed_logs
        if start_date <= datetime.strptime(log['date'], '%Y-%m-%d') <= end_date
    ]
    
    return filtered_logs

def export_logs_to_csv(parsed_logs, filename):
    """
    Exports logs to a CSV file.
    
    Parameters:
    - parsed_logs (list): A list of dictionaries, each representing a parsed log line.
    - filename (str): The name of the output CSV file.
    """
    # Define the headers for the CSV file
    headers = ['Timestamp', 'Level', 'Message']
    
    # Open the file in write mode and create a CSV writer object
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        
        # Write the headers to the CSV file
        writer.writeheader()
        
        # Write each log as a row in the CSV file
        for log in parsed_logs:
            writer.writerow({
                'Timestamp': log['timestamp'],
                'Level': log['level'],
                'Message': log['message']
            })
    
    # Print confirmation message
    print(f"Logs successfully exported to {filename}")

def process_large_log_file(file_path):
    """
    Processes a large log file efficiently by reading and parsing in chunks.
    
    Parameters:
    - file_path (str): Path to the log file.
    
    Returns:
    - list: A list of dictionaries, each representing a parsed log line.
    """
    log_chunks = parse_log_file(file_path)
    all_logs = []
    for chunk in log_chunks:
        all_logs.extend(chunk)
    return all_logs

def main():
    # Simulate a large log file by creating a temporary file with 100,000 lines
    temp_log_file = 'temp_large_log_file.log'
    with open(temp_log_file, 'w') as file:
        for i in range(100000):
            line = f"2023-01-01 12:{i%1440//60:02d}:{i%60:02d} INFO Sample log message {i}\n"
            file.write(line)
    
    # Process the large log file
    parsed_logs = process_large_log_file(temp_log_file)
    
    # Filtering logs by date range
    start_date = '2023-01-02'
    end_date = '2023-01-05'
    filtered_logs = filter_logs_by_date_range(parsed_logs, start_date, end_date)
    
    # Exporting filtered logs to CSV
    export_logs_to_csv(filtered_logs, 'filtered_logs.csv')
    
    # Clean up the temporary log file
    os.remove(temp_log_file)

# This if statement allows the script to be imported as a module without running main()
# or running main() if the script is executed directly.
if __name__ == "__main__":
    main()
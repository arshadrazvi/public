'''
Prompt:
    Enhance the existing log parser code to add error pattern detection features:

    1. Add a function to detect repeated errors (same error message appearing multiple times)
    2. Add a function to detect error spikes (3 or more errors within a 5-minute window)
    3. Create an alert report showing:
    - Top 3 most frequent errors
    - Any detected error spikes with their time windows
    4. Use the existing code structure and add these new features
    5. Update the main execution to demonstrate the new features
    6. Keep the code beginner-friendly with clear comments
'''


import os
import sys
from itertools import islice

# Constants
CHUNK_SIZE = 1000  # Number of lines to process at a time

def read_log_file(file_path, chunk_size=CHUNK_SIZE):
    """
    Generator function to read a log file in chunks.
    
    Parameters:
    - file_path (str): Path to the log file.
    - chunk_size (int): Number of lines to read at a time.
    
    Yields:
    - list: A list of lines from the log file.
    """
    with open(file_path, 'r') as file:
        while True:
            lines = list(islice(file, chunk_size))
            if not lines:
                break
            yield lines

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

def parse_log_chunk(log_chunk):
    """
    Parses a chunk of log lines into a list of dictionaries.
    
    Parameters:
    - log_chunk (list): A list of log lines.
    
    Returns:
    - list: A list of dictionaries, each representing a parsed log line.
    """
    return [parse_log_line(line) for line in log_chunk]

def count_log_levels_in_chunk(log_chunk):
    """
    Counts the occurrence of each log level in a chunk of log dictionaries.
    
    Parameters:
    - log_chunk (list): A list of dictionaries, each representing a parsed log line.
    
    Returns:
    - dict: A dictionary with keys as log levels and values as their counts.
    """
    # Initialize a dictionary to hold counts
    level_counts = {'INFO': 0, 'ERROR': 0, 'WARNING': 0, 'DEBUG': 0}
    # Iterate over logs in the chunk and count levels
    for log in log_chunk:
        if log['level'] in level_counts:
            level_counts[log['level']] += 1
    return level_counts

def aggregate_log_levels(log_chunks):
    """
    Aggregates log level counts from multiple chunks.
    
    Parameters:
    - log_chunks (generator): A generator yielding chunks of log lines.
    
    Returns:
    - dict: A dictionary with keys as log levels and values as their counts.
    """
    # Initialize a dictionary to hold aggregated counts
    aggregated_counts = {'INFO': 0, 'ERROR': 0, 'WARNING': 0, 'DEBUG': 0}
    for chunk in log_chunks:
        chunk_counts = count_log_levels_in_chunk(parse_log_chunk(chunk))
        for level, count in chunk_counts.items():
            aggregated_counts[level] += count
    return aggregated_counts

def process_large_log_file(file_path):
    """
    Processes a large log file efficiently by reading and parsing in chunks.
    
    Parameters:
    - file_path (str): Path to the log file.
    
    Returns:
    - dict: Aggregated log level counts from the entire log file.
    """
    log_chunks = read_log_file(file_path)
    return aggregate_log_levels(log_chunks)

def main():
    # Simulate a large log file by creating a temporary file with 100,000 lines
    temp_log_file = 'temp_large_log_file.log'
    with open(temp_log_file, 'w') as file:
        for i in range(100000):
            line = f"2023-01-01 12:{i%1440//60:02d}:{i%60:02d} INFO Sample log message {i}\n"
            file.write(line)
    
    # Process the large log file
    log_level_counts = process_large_log_file(temp_log_file)
    
    # Display the log level counts
    print("Log Level Counts:")
    for level, count in log_level_counts.items():
        print(f"{level}: {count}")
    
    # Clean up the temporary log file
    os.remove(temp_log_file)

# This if statement allows the script to be imported as a module without running main()
# or running main() if the script is executed directly.
if __name__ == "__main__":
    main()
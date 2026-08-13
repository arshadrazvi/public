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

def parse_log_file(log_data):
    """
    Parses multiple log lines from a string and returns a list of dictionaries.
    
    Parameters:
    - log_data (str): A string containing multiple lines of log data.
    
    Returns:
    - list: A list of dictionaries, each representing a parsed log line.
    """
    # Split the log data into lines and parse each line
    log_lines = log_data.strip().split('\n')
    parsed_logs = [parse_log_line(line) for line in log_lines if line]
    return parsed_logs

def count_log_levels(logs):
    """
    Counts the occurrence of each log level in a list of log dictionaries.
    
    Parameters:
    - logs (list): A list of dictionaries, each representing a parsed log line.
    
    Returns:
    - dict: A dictionary with keys as log levels and values as their counts.
    """
    # Initialize a dictionary to hold counts
    level_counts = {'INFO': 0, 'ERROR': 0, 'WARNING': 0, 'DEBUG': 0}
    # Iterate over logs and count levels
    for log in logs:
        if log['level'] in level_counts:
            level_counts[log['level']] += 1
    return level_counts

def main():
    # Sample log data
    sample_log_data = """
    2023-01-01 12:00:00 INFO Starting the application
    2023-01-01 12:01:00 ERROR An unexpected error occurred
    2023-01-01 12:02:00 WARNING Low disk space
    2023-01-01 12:03:00 DEBUG Initializing module A
    2023-01-01 12:04:00 INFO Loading configuration
    2023-01-01 12:05:00 ERROR Connection failed
    """

    # Parsing the sample log data
    parsed_logs = parse_log_file(sample_log_data)

    # Counting log levels
    log_level_counts = count_log_levels(parsed_logs)

    # Expected output
    print("Parsed Logs:")
    for log in parsed_logs:
        print(log)

    print("\nLog Level Counts:")
    for level, count in log_level_counts.items():
        print(f"{level}: {count}")

# This if statement allows the script to be imported as a module without running main()
# or running main() if the script is executed directly.
if __name__ == "__main__":
    main()
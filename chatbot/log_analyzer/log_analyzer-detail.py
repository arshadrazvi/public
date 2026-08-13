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


from collections import defaultdict

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

def detect_repeated_errors(logs):
    """
    Detects repeated errors in the log entries.
    
    Parameters:
    - logs (list): A list of dictionaries, each representing a parsed log line.
    
    Returns:
    - dict: A dictionary with error messages as keys and their counts as values for errors appearing more than once.
    """
    error_counts = defaultdict(int)
    repeated_errors = {}
    for log in logs:
        if log['level'] == 'ERROR':
            error_counts[log['message']] += 1
            if error_counts[log['message']] > 1 and log['message'] not in repeated_errors:
                repeated_errors[log['message']] = error_counts[log['message']]
    return repeated_errors

def detect_error_spikes(logs):
    """
    Detects error spikes in the log entries.
    
    Parameters:
    - logs (list): A list of dictionaries, each representing a parsed log line.
    
    Returns:
    - list: A list of tuples, each representing a time window of an error spike (start time, end time).
    """
    error_logs = sorted([log for log in logs if log['level'] == 'ERROR'], key=lambda x: x['timestamp'])
    error_spikes = []
    i = 0
    while i < len(error_logs):
        start_time = error_logs[i]['timestamp']
        count = 1
        j = i + 1
        
        while j < len(error_logs) and (
            error_logs[j]['timestamp'] <= (
                start_time[:11] + ' ' +
                (str(int(start_time[-8:-6]) + 5) + start_time[-6:])
            )
        ):      
            count += 1
            j += 1
        if count >= 3:
            end_time = error_logs[j-1]['timestamp']
            error_spikes.append((start_time, end_time))
        i = j
    return error_spikes

def generate_alert_report(logs):
    """
    Generates an alert report showing top 3 most frequent errors and any detected error spikes.
    
    Parameters:
    - logs (list): A list of dictionaries, each representing a parsed log line.
    """
    # Counting log levels
    log_level_counts = count_log_levels(logs)
    
    # Detect repeated errors and error spikes
    repeated_errors = detect_repeated_errors(logs)
    error_spikes = detect_error_spikes(logs)
    
    # Generating the alert report
    print("\nAlert Report:")
    print("Top 3 Most Frequent Errors:")
    top_errors = sorted(repeated_errors.items(), key=lambda x: x[1], reverse=True)[:3]
    for error, count in top_errors:
        print(f"{error}: {count} occurrences")
    
    if error_spikes:
        print("\nError Spikes Detected:")
        for start_time, end_time in error_spikes:
            print(f"From {start_time} to {end_time}")

def main():
    # Sample log data
    sample_log_data = """
    2023-01-01 12:00:00 INFO Starting the application
    2023-01-01 12:01:00 ERROR An unexpected error occurred
    2023-01-01 12:02:00 WARNING Low disk space
    2023-01-01 12:03:00 DEBUG Initializing module A
    2023-01-01 12:04:00 INFO Loading configuration
    2023-01-01 12:05:00 ERROR Connection failed
    2023-01-01 12:06:00 ERROR An unexpected error occurred
    2023-01-01 12:07:00 ERROR An unexpected error occurred
    2023-01-01 12:08:00 ERROR Connection failed
    """

    # Parsing the sample log data
    parsed_logs = parse_log_file(sample_log_data)

    # Displaying parsed logs
    print("Parsed Logs:")
    for log in parsed_logs:
        print(log)

    # Generating and displaying the alert report
    generate_alert_report(parsed_logs)

# This if statement allows the script to be imported as a module without running main()
# or running main() if the script is executed directly.
if __name__ == "__main__":
    main()
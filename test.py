import pandas as pd
import re
from urllib.parse import urlparse
from fuzzywuzzy import fuzz
from tqdm import tqdm
from sklearn.preprocessing import LabelEncoder

common_regex = '^(?P<client>\S+) \S+ (?P<userid>\S+) \[(?P<datetime>[^\]]+)\] "(?P<method>[A-Z]+) (?P<request>[^ "]+)? HTTP/[0-9.]+" (?P<status>[0-9]{3}) (?P<size>[0-9]+|-)'
combined_regex = '^(?P<client>\S+) \S+ (?P<userid>\S+) \[(?P<datetime>[^\]]+)\] "(?P<method>[A-Z]+) (?P<request>[^ "]+)? HTTP/[0-9.]+" (?P<status>[0-9]{3}) (?P<size>[0-9]+|-) "(?P<referrer>[^"]*)" "(?P<useragent>[^"]*)'
columns = ['client', 'userid', 'datetime', 'method', 'request', 'status', 'size', 'referer', 'user_agent']

def process_logs(logfile, percentage=0.001):
    with open(logfile, 'r') as f:
        lines = f.readlines()

    num_lines_to_keep = int(len(lines) * percentage)
    kept_lines = lines[:num_lines_to_keep]

    # Writing the subset of lines to a new file
    with open('new_file.log', 'w') as f:
        f.writelines(kept_lines)

    # Parsing logs to DataFrame
    logs_df = logs_to_df('new_file.log')

    # Additional processing steps
    logs_df['client'] = logs_df['client'].astype('category')
    del logs_df['userid']
    logs_df['datetime'] = pd.to_datetime(logs_df['datetime'], format='%d/%b/%Y:%H:%M:%S %z')
    logs_df['method'] = logs_df['method'].astype('category')
    logs_df['status'] = logs_df['status'].astype('int16')
    logs_df['size'] = logs_df['size'].astype('int32')
    logs_df['referer'] = logs_df['referer'].astype('category')
    logs_df['user_agent'] = logs_df['user_agent'].astype('category')

    logs_df['referer'] = logs_df['referer'].str.lower()

    logs_df['traffic-label'] = logs_df['referer'].apply(classify_traffic)

    logs_df['ref'] = logs_df['referer'].apply(extract_netloc)

    logs_df['refers'] = ''

    threshold = 75
    logs_df['refers'] = logs_df['refers'].apply(lambda x: classify_traffic(x))
    canonical_urls = {}

    for idx, url in enumerate(logs_df['ref']):
        canonical_url = None
        for key, value in canonical_urls.items():
            if compare_urls(url, key) >= threshold:
                canonical_url = key
                break

        if canonical_url is None:
            canonical_url = url
            canonical_urls[canonical_url] = canonical_url

        logs_df.at[idx, 'refers'] = canonical_url

    threshold = 25
    logs_df['user-agent'] = ''
    logs_df['user_agent'] = logs_df['user_agent'].str.lower()
    canonical_urls = {}

    for idx, url in enumerate(logs_df['user_agent']):
        canonical_url = None
        for key, value in canonical_urls.items():
            if compare_urls(url, key) >= threshold:
                canonical_url = key
                break

        if canonical_url is None:
            canonical_url = url
            canonical_urls[canonical_url] = canonical_url

        logs_df.at[idx, 'user-agent'] = canonical_url

    encoder = LabelEncoder()
    logs_df.loc[:, 'encoded_refers'] = encoder.fit_transform(logs_df['refers'])

    unique_codes = logs_df['encoded_refers'].unique()
    num_unique_urls = len(unique_codes)
    print("Unique codes:", unique_codes)
    print("Number of unique URLs:", num_unique_urls)

    logs_df.loc[:, 'encoded_user-agent'] = encoder.fit_transform(logs_df['user-agent'])
    logs_df.loc[:, 'encoded_status'] = encoder.fit_transform(logs_df['status'])
    logs_df.loc[:, 'encoded_method'] = encoder.fit_transform(logs_df['method'])
    logs_df['traffic-label'] = encoder.fit_transform(logs_df['traffic-label'])

    return logs_df

def logs_to_df(logfile):
    parsed_lines = []
    with open(logfile) as source_file:
        linenumber = 0
        for line in tqdm(source_file):
            try:
                log_line = re.findall(combined_regex, line)[0]
                parsed_lines.append(log_line)
            except Exception as e:
                # Handle parsing errors, if any
                continue
            linenumber += 1

    # Creating DataFrame from parsed lines
    df = pd.DataFrame(parsed_lines, columns=columns)
    return df

def classify_traffic(referrer):
    if '-' in referrer and len(referrer) < 2:
        return 'direct'
    elif any(keyword in referrer.lower() for keyword in ['google', 'bing', 'yahoo','yandex','baidu','torob','search']):
        return 'search'
    elif any(keyword in referrer.lower() for keyword in ['facebook', 'twitter', 'linkedin','instagram','pinterest','youtube','reddit','ask','telegram']):
        return 'social'
    else:
        return 'other'

def extract_netloc(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def compare_urls(url1, url2):
    return fuzz.ratio(url1, url2)

# Example usage
logs_df_processed = process_logs('access.log', percentage=0.001)
print(logs_df_processed.head())

import pandas as pd
import re
import os
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
from urllib.parse import urlparse
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import time
import re
import pandas as pd

# from gensim.models import Word2Vec
import random

import time
from tqdm import tqdm

common_regex = '^(?P<client>\S+) \S+ (?P<userid>\S+) \[(?P<datetime>[^\]]+)\] "(?P<method>[A-Z]+) (?P<request>[^ "]+)? HTTP/[0-9.]+" (?P<status>[0-9]{3}) (?P<size>[0-9]+|-)'
combined_regex = '^(?P<client>\S+) \S+ (?P<userid>\S+) \[(?P<datetime>[^\]]+)\] "(?P<method>[A-Z]+) (?P<request>[^ "]+)? HTTP/[0-9.]+" (?P<status>[0-9]{3}) (?P<size>[0-9]+|-) "(?P<referrer>[^"]*)" "(?P<useragent>[^"]*)'
columns = ['client', 'userid', 'datetime', 'method', 'request', 'status', 'size', 'referer', 'user_agent']

def keep_data_percent(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    num_lines_to_keep = int(len(lines) * 0.02)

    kept_lines = lines[:num_lines_to_keep]

    with open(output_file, 'w') as f:
        f.writelines(kept_lines)

keep_data_percent("access.log", "new_file.log")


def logs_to_df(logfile, output_dir, errors_file):
    with open(logfile) as source_file:
        linenumber = 0
        parsed_lines = []
        for line in tqdm(source_file):
            try:
                log_line = re.findall(combined_regex, line)[0]
                parsed_lines.append(log_line)
            except Exception as e:
                with open(errors_file, 'at') as errfile:
                    print((line, str(e)), file=errfile)
                continue
            linenumber += 1
            if linenumber % 250_000 == 0:
                df = pd.DataFrame(parsed_lines, columns=columns)
                df.to_parquet(f'{output_dir}/file_{linenumber}.parquet')
                parsed_lines.clear()
        else:
            df = pd.DataFrame(parsed_lines, columns=columns)
            df.to_parquet(f'{output_dir}/file_{linenumber}.parquet')
            parsed_lines.clear()

logs_to_df(logfile='./new_file.log', output_dir='parquet_dir/', errors_file='errors.txt')
logs_df = pd.read_parquet('parquet_dir/')
logs_df['client'] = logs_df['client'].astype('category')
del logs_df['userid']
logs_df['datetime'] = pd.to_datetime(logs_df['datetime'], format='%d/%b/%Y:%H:%M:%S %z')
logs_df['method'] = logs_df['method'].astype('category')
logs_df['status'] = logs_df['status'].astype('int16')
logs_df['size'] = logs_df['size'].astype('int32')
logs_df['referer'] = logs_df['referer'].astype('category')
logs_df['user_agent'] = logs_df['user_agent'].astype('category')


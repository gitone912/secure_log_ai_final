import requests

# Set your Instabase API key
api_key = "69OcGovq6uLhXQPd9MtcSdrFsRrbKz"

text_to_summarize = 'what is god'

url = 'https://api.instabase.com/v1/summarization'

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}',
}

data = {
    'text': text_to_summarize,
    'other_parameters': 'value',
}

try:
    response = requests.post(url, json=data, headers=headers)

    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

    summary = response.json().get('summary')
    print(f'Summary: {summary}')

except requests.exceptions.RequestException as e:
    print(f'Error: {e}')

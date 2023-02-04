import requests
import json
from datetime import datetime, date, timedelta


def get_openai_usage(api_key, start_date):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    params = {
        'start_date': start_date,
        'end_date': end_date
    }
    response = requests.get("https://api.openai.com/dashboard/billing/usage", headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to retrieve OpenAI usage data: " + response.text)

tomorrow = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
if __name__ == "__main__":
    api_key = "API_KEY"
    start_date = date.today().strftime("%Y-%m-%d")
    end_date = tomorrow
    usage_data = get_openai_usage(api_key, start_date)
    print(json.dumps(usage_data, indent=4))


import requests

def get_stock_data():
    api_url = "https://twelve-data1.p.rapidapi.com/stocks/"

    headers = {
        "X-RapidAPI-Key": "2c38f10f19mshac5cb1b2f507b15p11892ajsnfdeba9deec01",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  
        json_data = response.json()

        return json_data

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

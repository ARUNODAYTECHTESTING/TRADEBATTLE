
import requests

def get_stock_data():
    url = "https://latest-stock-price.p.rapidapi.com/any"

    headers = {
        "X-RapidAPI-Key": "ea14030d32msha888fd2d309cf5bp1c98c6jsnde5748e469da",
        "X-RapidAPI-Host": "latest-stock-price.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        json_data = response.json()

        print(json_data)

    except requests.exceptions.RequestException as e:
        print({"error": str(e)})

get_stock_data()
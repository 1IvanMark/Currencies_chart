import requests
import pandas as pd
from datetime import datetime

class DataSource:
    def __init__(self):
        self.base_currency = "HUF"
        self.currencies = ["USD", "EUR", "GBP", "AUD", "PLN"] #<- you can add more currencies here
        self.api_url = f"https://open.er-api.com/v6/latest/{self.base_currency}"

    def get_currency_rates(self):
        try:
            response = requests.get(self.api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                rates = data.get("rates", {})
                currency_list = []
                for cur in self.currencies:
                    if cur in rates:
                        currency_list.append({
                            "name": cur,
                            "price": rates[cur],
                            "time": datetime.now()
                        })
                return pd.DataFrame(currency_list)
        except Exception as e:
            print(f"Error fetching currency rates: {e}")
        return pd.DataFrame()

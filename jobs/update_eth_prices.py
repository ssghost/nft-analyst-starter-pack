from datetime import datetime, timedelta
from time import sleep

import pandas as pd
import requests


def update_eth_prices(filename):
    # Update ETH prices file
    print("Updating ETH prices...")

    # Find today's date
    t0 = datetime.today().date()

    # Read from existing file and find the date last updated
    eth_prices_df = pd.read_csv(filename)
    last_date_updated = datetime.strptime(
        eth_prices_df.iloc[-1]["date"], "%Y-%m-%d"
    ).date()

    # Count the number of days to update
    days_to_update = t0 - last_date_updated

    # Update ETH prices using CoinGecko API calls
    eth_prices = pd.DataFrame(columns=("date", "price_of_eth"))

    for days_prior in range(days_to_update.days):
        date_updated = t0 - timedelta(days=days_prior)
        date_updated_input = str(date_updated.strftime("%d-%m-%Y"))
        date_updated_ouput = str(date_updated.strftime("%Y-%m-%d"))

        # Sleep for 10 seconds between API calls to avoid hitting rate limits
        sleep(10)

        # CoinGecko API Request
        url = "https://api.coingecko.com/api/v3/coins/ethereum/history?date={date_updated}".format(
            date_updated=date_updated_input
        )
        headers = {
            "Accept": "application/json",
        }

        r = requests.get(url, headers=headers, timeout=90)
        j = r.json()

        price_of_eth = j["market_data"]["current_price"]["usd"]

        new_dict = {"date": [date_updated_ouput], "price_of_eth": [price_of_eth]}
        new_df = pd.DataFrame(new_dict)
        eth_prices = pd.concat([eth_prices, new_df], ignore_index=True)

    eth_prices.sort_values(by="date", ascending=True, inplace=True)

    # If there are updates, output data to CSV file
    if eth_prices["date"].size != 0:
        eth_prices.to_csv(filename, header=False, index=False, mode="a")

    else:
        pass

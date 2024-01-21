from datetime import datetime
from io import StringIO

import pandas as pd
import yfinance as yf

from helper.oss_storage import OSSStorage


class FXService:
    def __init__(self):
        self.oss_storage = OSSStorage()
        self.fx_data_path = "fx_data/fx_rates.csv"

    def fetch_latest_exchange_rate(self):
        # Fetching the latest available data for today
        today_str = datetime.now().strftime("%Y-%m-%d")
        data = yf.download("CADUSD=X", start=today_str, end=today_str)
        return data["Close"].iloc[-1] if not data.empty else None

    def get_csv_data(self):
        csv_content = self.oss_storage.get(self.fx_data_path).decode("utf-8")
        return pd.read_csv(StringIO(csv_content))

    def update_csv_data(self, new_data):
        csv_content = new_data.to_csv(index=False)
        self.oss_storage.put(csv_content, self.fx_data_path)

    def add_todays_data_if_missing(self, data_frame):
        today_str = datetime.now().strftime("%Y-%m-%d")
        if today_str not in data_frame["timestamp"].values:
            latest_rate = self.fetch_latest_exchange_rate()
            if latest_rate is not None:
                new_row = {"timestamp": today_str, "exchange_rate": latest_rate}
                return data_frame.append(new_row, ignore_index=True), latest_rate
        return data_frame, None

    def calculate_average_rate(self, data_frame):
        return data_frame["exchange_rate"].mean()

    def process_fx_data(self):
        df = self.get_csv_data()
        df, latest_rate = self.add_todays_data_if_missing(df)
        average_rate = self.calculate_average_rate(df)
        self.update_csv_data(df)
        return (
            average_rate,
            latest_rate if latest_rate is not None else df["exchange_rate"].iloc[-1],
        )


# Usage example
fx_service = FXService()
average_rate, current_rate = fx_service.process_fx_data()
print(f"Average Exchange Rate: {average_rate}")
print(f"Current Exchange Rate: {current_rate}")

# Print the CSV format
print(fx_service.get_csv_data().to_csv(index=False))

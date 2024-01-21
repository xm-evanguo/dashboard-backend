import logging
from datetime import datetime, timedelta
from io import StringIO

import pandas as pd
import yfinance as yf

from helper.oss_storage import OSSStorage

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class FXService:
    def __init__(self):
        self.oss_storage = OSSStorage()
        self.fx_data_path = "fx_data/fx_rates.csv"
        logging.info("FXService initialized")

    def fetch_latest_exchange_rate(self):
        try:
            # Fetch data for the last 5 days
            end_date = datetime.now()
            start_date = end_date - timedelta(days=5)
            data = yf.download(
                "CADUSD=X",
                start=start_date.strftime("%Y-%m-%d"),
                end=end_date.strftime("%Y-%m-%d"),
            )

            if data.empty:
                logging.warning("No data available for the requested period")
                return None

            # Get the last non-NaN 'Close' value
            latest_rate = data["Close"].dropna().iloc[-1]
            logging.info(f"Latest exchange rate fetched: {latest_rate}")
            return latest_rate
        except Exception as e:
            logging.error(f"Error fetching the latest exchange rate: {e}")
            return None

    def get_csv_data(self):
        logging.info("Retrieving CSV data from OSS")
        csv_content = self.oss_storage.get(self.fx_data_path).decode("utf-8")
        return pd.read_csv(StringIO(csv_content))

    def update_csv_data(self, new_data):
        logging.info("Updating CSV data in OSS")
        csv_content = new_data.to_csv(index=False)
        self.oss_storage.put(csv_content, self.fx_data_path)

    def add_todays_data_if_missing(self, data_frame):
        # Convert 'date' column to string to ensure proper comparison
        data_frame["date"] = data_frame["date"].astype(str)

        today_str = datetime.now().strftime("%Y-%m-%d")
        if today_str not in data_frame["date"].values:
            logging.info(f"Today's data ({today_str}) is missing, adding it.")
            latest_rate = self.fetch_latest_exchange_rate()
            if latest_rate is not None:
                new_row = pd.DataFrame(
                    {"date": [today_str], "exchange_rate": [latest_rate]}
                )
                new_data_frame = pd.concat([data_frame, new_row], ignore_index=True)
                logging.info(f"Added today's rate to DataFrame: {latest_rate}")
                return new_data_frame, latest_rate
            else:
                logging.warning(f"Failed to fetch latest rate for {today_str}.")
                return data_frame, None
        else:
            logging.info(f"Today's data ({today_str}) already exists in DataFrame.")
            return data_frame, None

    def calculate_average_rate(self, data_frame):
        average_rate = data_frame["exchange_rate"].mean()
        logging.info(f"Calculated average exchange rate: {average_rate}")
        return average_rate

    def process_fx_data(self):
        logging.info("Processing FX data")
        df = self.get_csv_data()
        df, latest_rate = self.add_todays_data_if_missing(df)
        average_rate = self.calculate_average_rate(df)
        self.update_csv_data(df)
        return (
            average_rate,
            latest_rate if latest_rate is not None else df["exchange_rate"].iloc[-1],
        )


# Usage example
# fx_service = FXService()
# average_rate, current_rate = fx_service.process_fx_data()
# print(f"Average Exchange Rate: {average_rate}")
# print(f"Current Exchange Rate: {current_rate}")

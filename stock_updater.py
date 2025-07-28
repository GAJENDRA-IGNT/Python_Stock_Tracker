import requests
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
import time # Import the time module for delays
# Import necessary classes for SharePoint/OneDrive interaction
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
# Removed smtplib, MIMEText, MIMEMultipart as email functionality is removed

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
STOCK_TICKERS = ["IBM", "MSFT", "GOOGL", "AAPL"]
CSV_FILE_PATH = "stock_prices.csv"

# SharePoint/OneDrive Configuration (retrieved from .env)
SHAREPOINT_USERNAME = os.getenv("SHAREPOINT_USERNAME")
SHAREPOINT_PASSWORD = os.getenv("SHAREPOINT_PASSWORD")
SHAREPOINT_SITE_URL = os.getenv("SHAREPOINT_SITE_URL")
SHAREPOINT_FOLDER_PATH = os.getenv("SHAREPOINT_FOLDER_PATH")

# Email Configuration has been removed

# --- Functions ---

def fetch_stock_price(ticker):
    """
    Fetches the current stock price for a given ticker from Alpha Vantage.
    Returns the price as a float, or None if an error occurs.
    """
    if not ALPHA_VANTAGE_API_KEY:
        print("Error: Alpha Vantage API key not found in environment variables. Please check your .env file.")
        return None

    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={ALPHA_VANTAGE_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "Error Message" in data:
            print(f"Alpha Vantage API Error for {ticker}: {data['Error Message']}")
            return None
        if "Global Quote" not in data or not data["Global Quote"]:
            print(f"No Global Quote data found for {ticker} from Alpha Vantage.")
            return None

        price = float(data["Global Quote"]["05. price"])
        return price

    except requests.exceptions.RequestException as e:
        print(f"Network or API request error for {ticker}: {e}")
        return None
    except ValueError:
        print(f"Could not parse price for {ticker} from API response. Raw data: {data}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while fetching price for {ticker}: {e}")
        return None

def update_csv_file(ticker_data):
    """
    Appends new stock data to the CSV file.
    Creates the file with headers if it doesn't exist.
    """
    new_df = pd.DataFrame(ticker_data)

    if not os.path.exists(CSV_FILE_PATH):
        new_df.to_csv(CSV_FILE_PATH, mode='w', header=True, index=False)
        print(f"Created new CSV file: {CSV_FILE_PATH} with initial data.")
    else:
        new_df.to_csv(CSV_FILE_PATH, mode='a', header=False, index=False)
        print(f"Appended new data to CSV file: {CSV_FILE_PATH}")

def upload_file_to_sharepoint(file_path):
    """
    Uploads a file to a specified SharePoint/OneDrive folder.
    Returns True on success, False on failure.
    """
    if not all([SHAREPOINT_USERNAME, SHAREPOINT_PASSWORD, SHAREPOINT_SITE_URL, SHAREPOINT_FOLDER_PATH]):
        print("SharePoint/OneDrive credentials or path not fully configured in .env. Skipping upload.")
        return False

    try:
        user_credentials = UserCredential(SHAREPOINT_USERNAME, SHAREPOINT_PASSWORD)
        ctx = ClientContext(SHAREPOINT_SITE_URL).with_credentials(user_credentials)

        target_folder = ctx.web.get_folder_by_server_relative_url(SHAREPOINT_FOLDER_PATH)
        ctx.load(target_folder)
        ctx.execute_query()

        with open(file_path, 'rb') as content_file:
            file_content = content_file.read()

        file_name = os.path.basename(file_path)
        target_folder.upload_file(file_name, file_content).execute_query()
        print(f"Successfully uploaded '{file_name}' to SharePoint/OneDrive at '{SHAREPOINT_SITE_URL}{SHAREPOINT_FOLDER_PATH}'")
        return True

    except Exception as e:
        print(f"Error uploading file to SharePoint/OneDrive: {e}")
        print("Please ensure your SharePoint/OneDrive URL, username, password, and folder path are correct.")
        print("For corporate accounts, you might need IT to configure app permissions or use a different authentication method.")
        return False

# send_notification_email function has been removed

# --- Modified main function to run every 5 seconds ---
def main():
    """
    Main function to orchestrate fetching, updating, uploading.
    This function will now run in a continuous loop, pausing for 5 seconds between runs.
    """
    while True: # Infinite loop for continuous execution
        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n--- Starting stock data update process at {current_timestamp} ---")

        all_new_records = []
        for ticker in STOCK_TICKERS:
            price = fetch_stock_price(ticker)
            if price is not None:
                all_new_records.append({
                    "Timestamp": current_timestamp,
                    "Ticker": ticker,
                    "Price": price
                })
                print(f"Successfully fetched {ticker}: ${price:.2f}")
            else:
                print(f"Failed to fetch price for {ticker}. Skipping this ticker for this run.")

        # Initialize upload_status_message inside the loop for each run
        upload_status_message = "CSV file not updated or uploaded."

        if all_new_records:
            update_csv_file(all_new_records) # Update local CSV

            upload_success = upload_file_to_sharepoint(CSV_FILE_PATH)
            if upload_success:
                upload_status_message = f"CSV file '{os.path.basename(CSV_FILE_PATH)}' successfully updated locally and uploaded to SharePoint/OneDrive."
            else:
                upload_status_message = f"CSV file '{os.path.basename(CSV_FILE_PATH)}' updated locally, but upload to SharePoint/OneDrive failed."
        else:
            upload_status_message = "No new stock data was successfully fetched or recorded."

        print(upload_status_message)

        print(f"Stock data update process completed. Waiting 5 seconds for next run...")
        time.sleep(5) # Pause for 5 seconds before the next iteration

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScript interrupted by user (Ctrl+C). Exiting.")
    except Exception as e:
        print(f"\nAn unhandled error occurred: {e}")
        print("The script has stopped.")
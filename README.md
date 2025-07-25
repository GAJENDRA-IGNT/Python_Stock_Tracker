Automated Stock Price Tracker and CSV Updater
This Python script automates the process of fetching real-time stock prices, recording them in a CSV file, uploading the updated CSV to SharePoint/OneDrive, and sending an email notification upon completion.

## Features

* Fetches current stock prices for a configurable list of tickers using the Alpha Vantage API.
* Appends new stock data (Timestamp, Ticker, Price) to a local `stock_prices.csv` file.
* Uploads the `stock_prices.csv` file to a specified folder in SharePoint or OneDrive.
* Sends an email notification with the status of the update and upload.
* Uses `.env` for secure management of API keys and credentials.

## Technologies Used

* **Python 3.x**
* `requests`: For making HTTP requests to the Alpha Vantage API.
* `pandas`: For efficient CSV file handling (reading, appending).
* `python-dotenv`: For loading environment variables from a `.env` file.
* `Office365-REST-Python-Client`: For interacting with SharePoint/OneDrive for file uploads.
* `smtplib`, `email.mime.text`, `email.mime.multipart`: For sending email notifications.

## Setup and Installation

1.  **Clone the repository (after it's on GitHub):**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Get an Alpha Vantage API Key:**
    Sign up for a free API key at [www.alphavantage.co](https://www.alphavantage.co/).

5.  **Configure environment variables:**
    Create a file named `.env` in the root of your project directory and add the following, replacing the placeholders with your actual credentials and paths:

    ```
    ALPHA_VANTAGE_API_KEY=YOUR_ALPHA_VANTAGE_API_KEY

    SHAREPOINT_USERNAME=your_sharepoint_username@yourdomain.com
    SHAREPOINT_PASSWORD=your_sharepoint_password
    SHAREPOINT_SITE_URL=https://yourcompany.sharepoint.com/sites/YourSiteName
    SHAREPOINT_FOLDER_PATH=/Shared Documents/StockData

    EMAIL_SENDER=your_email@example.com
    EMAIL_PASSWORD=your_email_app_password # For Gmail, use an App Password!
    EMAIL_RECEIVER=recipient_email@example.com
    SMTP_SERVER=smtp.gmail.com
    SMTP_PORT=587
    ```
    * **SharePoint/OneDrive:** Ensure the `SHAREPOINT_SITE_URL` and `SHAREPOINT_FOLDER_PATH` are correct and the target folder exists. Your account needs write permissions.
    * **Email:** If using Gmail with 2FA, you need to generate an "App password" from your Google Account security settings.

6.  **Initial CSV File:**
    Ensure you have an empty `stock_prices.csv` file with just the header:
    ```csv
    Timestamp,Ticker,Price
    ```

## How to Run

Execute the script from your terminal (with the virtual environment activated):
```bash
python stock_updater.py
```

## Automation (Scheduling)

To automate this script to run periodically (e.g., daily, hourly) on your system:

* **Linux/macOS:** Use `cron`.
    Edit your crontab: `crontab -e`
    Add a line like (to run every day at 9 AM):
    `0 9 * * * /path/to/your/stock_tracker/venv/bin/python /path/to/your/stock_tracker/stock_updater.py`

* **Windows:** Use Task Scheduler.
    1.  Open Task Scheduler.
    2.  Create Basic Task...
    3.  Trigger: Daily/Hourly.
    4.  Action: "Start a program".
    5.  Program/script: Full path to your virtual environment's Python executable (e.g., `C:\Users\YourUser\stock_tracker\venv\Scripts\python.exe`).
    6.  Add arguments: Full path to your script (e.g., `C:\Users\YourUser\stock_tracker\stock_updater.py`).
    7.  Start in (optional): Full path to your project directory (e.g., `C:\Users\YourUser\stock_tracker`).

## Future Improvements

* **Error Logging:** Implement more robust logging using Python's `logging` module.
* **Configuration File:** Move stock tickers and other non-sensitive configurations to a separate `config.ini` or JSON file.
* **More APIs:** Integrate with other stock APIs for redundancy or more data.
* **Data Visualization:** Add a component to generate simple charts (e.g., using `matplotlib` or `seaborn`) and include them in the email or upload them.
* **Interactive Dashboard:** Create a simple web dashboard using Flask/Django to view the data.
* **Robust SharePoint Auth:** Explore Azure AD app registration for more secure and robust authentication in corporate environments.

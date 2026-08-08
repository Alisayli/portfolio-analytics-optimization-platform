from datetime import datetime
from pathlib import Path

import pandas as pd
import yfinance as yf


def _validate_date_range(
    start_date: str,
    end_date: str,
) -> None:
    """
    Validate that two dates use YYYY-MM-DD format and are logically ordered.

    Args:
        start_date: Beginning of the analysis period.
        end_date: End of the analysis period.

    Raises:
        ValueError: If the date format is invalid or start_date is not earlier.
    """

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError as error:
        raise ValueError("Dates must use YYYY-MM-DD format.") from error

    if start >= end:
        raise ValueError("Start date must be earlier than end date.")


def _flatten_yfinance_columns(
    data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert yfinance MultiIndex columns into a single column level.

    Args:
        data: DataFrame returned by yfinance.

    Returns:
        DataFrame with simplified column labels.
    """

    cleaned_data = data.copy()

    if isinstance(cleaned_data.columns, pd.MultiIndex):
        cleaned_data.columns = cleaned_data.columns.get_level_values(0)

    cleaned_data.index.name = "Date"

    return cleaned_data


def download_stock_data(
    ticker: str,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    """
    Download historical daily market data for one ticker.

    Args:
        ticker: Yahoo Finance ticker symbol, such as "AAPL".
        start_date: Beginning of the period in YYYY-MM-DD format.
        end_date: End of the period in YYYY-MM-DD format.

    Returns:
        DataFrame containing historical market data.

    Raises:
        ValueError: If an input is invalid or no data is returned.
    """

    ticker = ticker.strip().upper()

    if not ticker:
        raise ValueError("Ticker cannot be empty.")

    _validate_date_range(start_date, end_date)

    data = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=False,
        progress=False,
    )

    if data.empty:
        raise ValueError(
            f"No market data was returned for {ticker}. "
            "Check the ticker and date range."
        )

    return _flatten_yfinance_columns(data)


def save_raw_data(
    data: pd.DataFrame,
    ticker: str,
    start_date: str,
    end_date: str,
) -> Path:
    """
    Save downloaded market data as a CSV file in data/raw.

    Args:
        data: Market data to save.
        ticker: Yahoo Finance ticker symbol.
        start_date: Beginning of the period in YYYY-MM-DD format.
        end_date: End of the period in YYYY-MM-DD format.

    Returns:
        Path of the saved CSV file.

    Raises:
        ValueError: If the supplied DataFrame is empty or ticker is invalid.
    """

    if data.empty:
        raise ValueError("Cannot save an empty dataset.")

    ticker = ticker.strip().upper()

    if not ticker:
        raise ValueError("Ticker cannot be empty.")

    _validate_date_range(start_date, end_date)

    project_root = Path(__file__).resolve().parent.parent
    raw_data_folder = project_root / "data" / "raw"
    raw_data_folder.mkdir(parents=True, exist_ok=True)

    file_name = f"{ticker}_{start_date}_{end_date}.csv"
    file_path = raw_data_folder / file_name

    data.to_csv(file_path)

    return file_path


def download_risk_free_rate(
    start_date: str,
    end_date: str,
    treasury_ticker: str = "^IRX",
) -> float:
    """
    Download the average annualized 13-week Treasury bill yield.

    Yahoo Finance reports ^IRX values in percentage points. For example,
    4.25 represents 4.25%, so this function converts it to 0.0425.

    Args:
        start_date: Beginning of the period in YYYY-MM-DD format.
        end_date: End of the period in YYYY-MM-DD format.
        treasury_ticker: Yahoo Finance symbol for the Treasury yield.

    Returns:
        Average annualized risk-free rate as a decimal.

    Raises:
        ValueError: If inputs are invalid or no valid yield data is returned.
    """

    treasury_ticker = treasury_ticker.strip().upper()

    if not treasury_ticker:
        raise ValueError("Treasury ticker cannot be empty.")

    _validate_date_range(start_date, end_date)

    treasury_data = yf.download(
        treasury_ticker,
        start=start_date,
        end=end_date,
        auto_adjust=False,
        progress=False,
    )

    if treasury_data.empty:
        raise ValueError(
            "No Treasury yield data was returned for the selected period."
        )

    treasury_data = _flatten_yfinance_columns(treasury_data)

    if "Close" not in treasury_data.columns:
        raise ValueError(
            "Treasury yield data does not contain a Close column."
        )

    treasury_yields = treasury_data["Close"].dropna()

    if treasury_yields.empty:
        raise ValueError(
            "Treasury yield data does not contain valid closing values."
        )

    average_yield_percentage = treasury_yields.mean()
    average_yield_decimal = average_yield_percentage / 100

    return float(average_yield_decimal)


def save_processed_data(
    data: pd.DataFrame,
    ticker: str,
    start_date: str,
    end_date: str,
) -> Path:
    """
    Save processed analytics data as a CSV file in data/processed.

    Args:
        data: Processed analytics data to save.
        ticker: Yahoo Finance ticker symbol.
        start_date: Beginning of the analysis period.
        end_date: End of the analysis period.

    Returns:
        Path of the saved processed CSV file.

    Raises:
        ValueError: If the supplied DataFrame is empty.
    """

    if data.empty:
        raise ValueError("Cannot save an empty processed dataset.")

    ticker = ticker.strip().upper()

    if not ticker:
        raise ValueError("Ticker cannot be empty.")

    _validate_date_range(start_date, end_date)

    project_root = Path(__file__).resolve().parent.parent
    processed_folder = project_root / "data" / "processed"
    processed_folder.mkdir(parents=True, exist_ok=True)

    file_name = f"{ticker}_{start_date}_{end_date}_processed.csv"
    file_path = processed_folder / file_name

    data.to_csv(file_path)

    return file_path

def download_multiple_adjusted_closes(
    tickers: list[str],
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    """
    Download adjusted closing prices for multiple tickers.

    Args:
        tickers: List of Yahoo Finance ticker symbols.
        start_date: Beginning of the period in YYYY-MM-DD format.
        end_date: End of the period in YYYY-MM-DD format.

    Returns:
        DataFrame where each column contains one ticker's adjusted prices.

    Raises:
        ValueError: If inputs are invalid or no usable data is returned.
    """

    if not tickers:
        raise ValueError("Ticker list cannot be empty.")

    cleaned_tickers = []

    for ticker in tickers:
        cleaned_ticker = ticker.strip().upper()

        if not cleaned_ticker:
            raise ValueError("Ticker symbols cannot be empty.")

        if cleaned_ticker in cleaned_tickers:
            raise ValueError(
                f"Duplicate ticker found: {cleaned_ticker}."
            )

        cleaned_tickers.append(cleaned_ticker)

    _validate_date_range(start_date, end_date)

    data = yf.download(
        cleaned_tickers,
        start=start_date,
        end=end_date,
        auto_adjust=False,
        progress=False,
    )

    if data.empty:
        raise ValueError(
            "No market data was returned for the selected portfolio."
        )

    if not isinstance(data.columns, pd.MultiIndex):
        raise ValueError(
            "Expected multi-asset data with MultiIndex columns."
        )

    if "Adj Close" not in data.columns.get_level_values(0):
        raise ValueError(
            "Downloaded data does not contain adjusted closing prices."
        )

    adjusted_closes = data["Adj Close"].copy()
    adjusted_closes = adjusted_closes.reindex(columns=cleaned_tickers)
    adjusted_closes.index.name = "Date"

    missing_tickers = [
        ticker
        for ticker in cleaned_tickers
        if ticker not in adjusted_closes.columns
        or adjusted_closes[ticker].dropna().empty
    ]

    if missing_tickers:
        raise ValueError(
            "No valid adjusted-close data was returned for: "
            + ", ".join(missing_tickers)
        )

    return adjusted_closes

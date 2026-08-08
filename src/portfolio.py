from math import isclose

import pandas as pd


def validate_portfolio_weights(
    portfolio_weights: dict[str, float],
) -> dict[str, float]:
    """
    Validate and standardize portfolio weights.

    Args:
        portfolio_weights:
            Dictionary mapping ticker symbols to decimal weights.
            Example: {"AAPL": 0.30, "MSFT": 0.25}

    Returns:
        Cleaned weights with uppercase ticker symbols.

    Raises:
        ValueError:
            If the portfolio is empty, contains invalid tickers,
            contains non-positive weights, or weights do not sum to 1.
    """

    if not portfolio_weights:
        raise ValueError("Portfolio cannot be empty.")

    cleaned_weights: dict[str, float] = {}

    for ticker, weight in portfolio_weights.items():
        if not isinstance(ticker, str):
            raise ValueError("Portfolio tickers must be strings.")

        cleaned_ticker = ticker.strip().upper()

        if not cleaned_ticker:
            raise ValueError("Portfolio tickers cannot be empty.")

        if not isinstance(weight, (int, float)):
            raise ValueError(
                f"Weight for {cleaned_ticker} must be numeric."
            )

        if weight <= 0:
            raise ValueError(
                f"Weight for {cleaned_ticker} must be greater than zero."
            )

        if cleaned_ticker in cleaned_weights:
            raise ValueError(
                f"Duplicate ticker found after cleaning: {cleaned_ticker}."
            )

        cleaned_weights[cleaned_ticker] = float(weight)

    total_weight = sum(cleaned_weights.values())

    if not isclose(total_weight, 1.0, abs_tol=1e-6):
        raise ValueError(
            "Portfolio weights must sum to 1.00. "
            f"Current total: {total_weight:.6f}."
        )

    return cleaned_weights
    portfolio_value = calculate_portfolio_value_index(
        portfolio_returns=portfolio_returns,
        initial_date=price_data.index[0],
        starting_value=100.0,
    )
    """
    Calculate daily returns for multiple assets.

    Args:
        price_data:
            DataFrame where each column is an asset's price series.

    Returns:
        DataFrame containing daily returns for each asset.

    Raises:
        ValueError:
            If price data is empty, has fewer than two rows,
            or contains no usable return observations.
    """

    clean_prices = price_data.dropna(how="all")

    if clean_prices.empty:
        raise ValueError("Price data cannot be empty.")

    if len(clean_prices) < 2:
        raise ValueError(
            "At least two price observations are required."
        )

    asset_returns = (
        clean_prices
        .pct_change(fill_method=None)
        .dropna(how="all")
    )

    if asset_returns.empty:
        raise ValueError(
            "No valid asset returns could be calculated."
        )

    asset_returns.columns.name = "Ticker"

    return asset_returns


def calculate_portfolio_returns(
    asset_returns: pd.DataFrame,
    portfolio_weights: dict[str, float],
) -> pd.Series:
    """
    Calculate weighted daily portfolio returns.

    Args:
        asset_returns:
            DataFrame containing daily returns for each asset.
        portfolio_weights:
            Dictionary mapping ticker symbols to portfolio weights.

    Returns:
        Series containing weighted daily portfolio returns.

    Raises:
        ValueError:
            If returns are empty, required tickers are missing,
            or no complete observations are available.
    """

    if asset_returns.empty:
        raise ValueError("Asset-return data cannot be empty.")

    validated_weights = validate_portfolio_weights(
        portfolio_weights
    )

    missing_tickers = [
        ticker
        for ticker in validated_weights
        if ticker not in asset_returns.columns
    ]

    if missing_tickers:
        raise ValueError(
            "Asset-return data is missing these tickers: "
            + ", ".join(missing_tickers)
        )

    aligned_returns = asset_returns[
        list(validated_weights.keys())
    ].dropna()

    if aligned_returns.empty:
        raise ValueError(
            "No complete return observations are available."
        )

    weights = pd.Series(
        validated_weights,
        dtype="float64",
    )

    portfolio_returns = (
        aligned_returns
        .mul(weights, axis=1)
        .sum(axis=1)
    )

    portfolio_returns.name = "Portfolio Return"

    return portfolio_returns


def calculate_portfolio_cumulative_returns(
    portfolio_returns: pd.Series,
) -> pd.Series:
    """
    Calculate compounded cumulative portfolio returns.

    Args:
        portfolio_returns:
            Series containing daily portfolio returns.

    Returns:
        Series containing cumulative portfolio returns.

    Raises:
        ValueError:
            If portfolio-return data is empty.
    """

    clean_returns = portfolio_returns.dropna()

    if clean_returns.empty:
        raise ValueError("Portfolio-return data cannot be empty.")

    cumulative_returns = (
        (1 + clean_returns).cumprod() - 1
    )

    cumulative_returns.name = "Portfolio Cumulative Return"

    return cumulative_returns


def calculate_asset_returns(
    price_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate daily returns for multiple assets.

    Args:
        price_data:
            DataFrame where each column is an asset's price series.

    Returns:
        DataFrame containing daily returns for each asset.

    Raises:
        ValueError:
            If price data is empty, has fewer than two rows,
            or contains no usable return observations.
    """

    clean_prices = price_data.dropna(how="all")

    if clean_prices.empty:
        raise ValueError("Price data cannot be empty.")

    if len(clean_prices) < 2:
        raise ValueError(
            "At least two price observations are required."
        )

    asset_returns = (
        clean_prices
        .pct_change(fill_method=None)
        .dropna(how="all")
    )

    if asset_returns.empty:
        raise ValueError(
            "No valid asset returns could be calculated."
        )

    asset_returns.columns.name = "Ticker"

    return asset_returns


def calculate_asset_contributions(
    asset_returns: pd.DataFrame,
    portfolio_weights: dict[str, float],
) -> pd.DataFrame:
    """
    Calculate each asset's daily contribution to portfolio return.

    Args:
        asset_returns:
            DataFrame containing daily returns for each asset.
        portfolio_weights:
            Dictionary mapping tickers to portfolio weights.

    Returns:
        DataFrame containing each asset's weighted daily contribution.

    Raises:
        ValueError:
            If data is empty, required tickers are missing,
            or no complete observations are available.
    """

    if asset_returns.empty:
        raise ValueError("Asset-return data cannot be empty.")

    validated_weights = validate_portfolio_weights(
        portfolio_weights
    )

    missing_tickers = [
        ticker
        for ticker in validated_weights
        if ticker not in asset_returns.columns
    ]

    if missing_tickers:
        raise ValueError(
            "Asset-return data is missing these tickers: "
            + ", ".join(missing_tickers)
        )

    aligned_returns = asset_returns[
        list(validated_weights.keys())
    ].dropna()

    if aligned_returns.empty:
        raise ValueError(
            "No complete return observations are available."
        )

    weights = pd.Series(
        validated_weights,
        dtype="float64",
    )

    contributions = aligned_returns.mul(
        weights,
        axis=1,
    )

    contributions.columns.name = "Ticker"

    return contributions
    return asset_returns
    missing_tickers = [
        ticker
        for ticker in validated_weights
        if ticker not in asset_returns.columns
    ]

    if missing_tickers:
        raise ValueError(
            "Asset-return data is missing these tickers: "
            + ", ".join(missing_tickers)
        )

    aligned_returns = asset_returns[
        list(validated_weights.keys())
    ].dropna()

    if aligned_returns.empty:
        raise ValueError(
            "No complete return observations are available."
        )

    weights = pd.Series(
        validated_weights,
        dtype="float64",
    )

    contributions = aligned_returns.mul(
        weights,
        axis=1,
    )

    contributions.columns.name = "Ticker"

    return contributions


def calculate_arithmetic_total_contributions(
    asset_contributions: pd.DataFrame,
) -> pd.Series:
    """
    Sum each asset's daily contributions over the analysis period.

    This is an arithmetic attribution measure and does not geometrically
    link contributions across multiple periods.

    Args:
        asset_contributions:
            Daily contribution data by asset.

    Returns:
        Arithmetic total contribution for each asset.

    Raises:
        ValueError:
            If contribution data is empty.
    """

    if asset_contributions.empty:
        raise ValueError("Contribution data cannot be empty.")

    total_contributions = asset_contributions.sum(axis=0)
    total_contributions.name = "Arithmetic Total Contribution"

    return total_contributions


def calculate_correlation_matrix(
    asset_returns: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate the return correlation matrix for portfolio holdings.

    Args:
        asset_returns:
            DataFrame containing daily returns for each asset.

    Returns:
        Correlation matrix for the asset-return columns.

    Raises:
        ValueError:
            If return data is empty, contains fewer than two assets,
            or produces an invalid correlation matrix.
    """

    clean_returns = asset_returns.dropna(how="all")

    if clean_returns.empty:
        raise ValueError("Asset-return data cannot be empty.")

    if clean_returns.shape[1] < 2:
        raise ValueError(
            "At least two assets are required for correlation analysis."
        )

    correlation_matrix = clean_returns.corr()

    if correlation_matrix.isna().all().all():
        raise ValueError(
            "A valid correlation matrix could not be calculated."
        )

    correlation_matrix.index.name = "Ticker"
    correlation_matrix.columns.name = "Ticker"

    return correlation_matrix


def calculate_portfolio_value_index(
    portfolio_returns: pd.Series,
    initial_date: pd.Timestamp,
    starting_value: float = 100.0,
) -> pd.Series:
    """
    Convert daily portfolio returns into a portfolio value index.

    The series includes the starting value on the initial date, followed
    by compounded values for each portfolio-return observation.

    Args:
        portfolio_returns:
            Series containing daily portfolio returns.
        initial_date:
            Date immediately before the first return observation.
        starting_value:
            Initial portfolio index value.

    Returns:
        Series showing the portfolio's compounded value over time.

    Raises:
        ValueError:
            If return data is empty, the starting value is invalid,
            or the initial date is not earlier than the first return date.
    """

    clean_returns = portfolio_returns.dropna()

    if clean_returns.empty:
        raise ValueError("Portfolio-return data cannot be empty.")

    if starting_value <= 0:
        raise ValueError("Starting value must be greater than zero.")

    initial_timestamp = pd.Timestamp(initial_date)

    if initial_timestamp >= clean_returns.index[0]:
        raise ValueError(
            "Initial date must be earlier than the first return date."
        )

    compounded_values = (
        starting_value
        * (1 + clean_returns).cumprod()
    )

    initial_value = pd.Series(
        data=[starting_value],
        index=[initial_timestamp],
        name="Portfolio Value",
        dtype="float64",
    )

    portfolio_value = pd.concat(
        [
            initial_value,
            compounded_values,
        ]
    )

    portfolio_value.name = "Portfolio Value"
    portfolio_value.index.name = "Date"

    return portfolio_value

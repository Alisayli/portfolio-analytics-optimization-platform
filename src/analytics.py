import pandas as pd


TRADING_DAYS_PER_YEAR = 252


def calculate_daily_returns(
    prices: pd.Series,
) -> pd.Series:
    """
    Calculate percentage returns between consecutive trading days.

    Args:
        prices: Series containing historical asset prices.

    Returns:
        Series containing daily percentage returns.

    Raises:
        ValueError: If fewer than two valid prices are available.
    """

    clean_prices = prices.dropna()

    if len(clean_prices) < 2:
        raise ValueError(
            "At least two valid price observations are required "
            "to calculate returns."
        )

    daily_returns = clean_prices.pct_change(fill_method=None).dropna()
    daily_returns.name = "Daily Return"

    return daily_returns


def calculate_cumulative_returns(
    daily_returns: pd.Series,
) -> pd.Series:
    """
    Calculate compounded cumulative returns from daily returns.

    Args:
        daily_returns: Series containing daily percentage returns.

    Returns:
        Series containing cumulative returns.

    Raises:
        ValueError: If no valid daily returns are available.
    """

    clean_returns = daily_returns.dropna()

    if clean_returns.empty:
        raise ValueError("Daily-return data cannot be empty.")

    cumulative_returns = (1 + clean_returns).cumprod() - 1
    cumulative_returns.name = "Cumulative Return"

    return cumulative_returns


def calculate_total_return(
    prices: pd.Series,
) -> float:
    """
    Calculate total return over the full analysis period.

    Args:
        prices: Series containing historical asset prices.

    Returns:
        Total return as a decimal.

    Raises:
        ValueError: If fewer than two valid prices are supplied.
    """

    clean_prices = prices.dropna()

    if len(clean_prices) < 2:
        raise ValueError(
            "At least two valid price observations are required."
        )

    beginning_price = clean_prices.iloc[0]
    ending_price = clean_prices.iloc[-1]

    if beginning_price <= 0:
        raise ValueError("Beginning price must be greater than zero.")

    return float((ending_price / beginning_price) - 1)


def calculate_annualized_return(
    total_return: float,
    number_of_periods: int,
    periods_per_year: int = TRADING_DAYS_PER_YEAR,
) -> float:
    """
    Convert a compounded period return into an annualized return.

    Args:
        total_return: Total return over the analysis period.
        number_of_periods: Number of return observations.
        periods_per_year: Assumed trading periods per year.

    Returns:
        Annualized compounded return as a decimal.

    Raises:
        ValueError: If any input makes annualization invalid.
    """

    if number_of_periods <= 0:
        raise ValueError("Number of periods must be positive.")

    if periods_per_year <= 0:
        raise ValueError("Periods per year must be positive.")

    if total_return <= -1:
        raise ValueError("Total return must be greater than -100%.")

    annualized_return = (
        (1 + total_return)
        ** (periods_per_year / number_of_periods)
        - 1
    )

    return float(annualized_return)


def calculate_annualized_volatility(
    daily_returns: pd.Series,
    periods_per_year: int = TRADING_DAYS_PER_YEAR,
) -> float:
    """
    Calculate annualized volatility from daily returns.

    Args:
        daily_returns: Series containing daily returns.
        periods_per_year: Assumed trading periods per year.

    Returns:
        Annualized volatility as a decimal.

    Raises:
        ValueError: If there are insufficient returns or invalid periods.
    """

    clean_returns = daily_returns.dropna()

    if len(clean_returns) < 2:
        raise ValueError(
            "At least two daily return observations are required."
        )

    if periods_per_year <= 0:
        raise ValueError("Periods per year must be positive.")

    daily_volatility = clean_returns.std(ddof=1)
    annualized_volatility = (
        daily_volatility * periods_per_year ** 0.5
    )

    return float(annualized_volatility)


def calculate_drawdown(
    prices: pd.Series,
) -> pd.Series:
    """
    Calculate drawdowns from each previous running price peak.

    Args:
        prices: Series containing historical asset prices.

    Returns:
        Series containing drawdowns as negative decimals.

    Raises:
        ValueError: If no valid prices are available.
    """

    clean_prices = prices.dropna()

    if clean_prices.empty:
        raise ValueError("Price data cannot be empty.")

    if (clean_prices <= 0).any():
        raise ValueError("Prices must be greater than zero.")

    running_peak = clean_prices.cummax()
    drawdown = clean_prices / running_peak - 1
    drawdown.name = "Drawdown"

    return drawdown


def calculate_maximum_drawdown(
    prices: pd.Series,
) -> float:
    """
    Calculate the largest peak-to-trough decline in a price series.

    Args:
        prices: Series containing historical asset prices.

    Returns:
        Maximum drawdown as a negative decimal.
    """

    drawdown = calculate_drawdown(prices)

    return float(drawdown.min())


def calculate_sharpe_ratio(
    annualized_return: float,
    annualized_volatility: float,
    risk_free_rate: float,
) -> float:
    """
    Calculate the annualized Sharpe ratio.

    Args:
        annualized_return: Annualized investment return as a decimal.
        annualized_volatility: Annualized volatility as a decimal.
        risk_free_rate: Annualized risk-free rate as a decimal.

    Returns:
        Sharpe ratio.

    Raises:
        ValueError: If annualized volatility is zero or negative.
    """

    if annualized_volatility <= 0:
        raise ValueError(
            "Annualized volatility must be greater than zero."
        )

    excess_return = annualized_return - risk_free_rate
    sharpe_ratio = excess_return / annualized_volatility

    return float(sharpe_ratio)

def calculate_best_daily_return(
    daily_returns: pd.Series,
) -> float:
    """
    Return the highest daily return.

    Args:
        daily_returns: Series containing daily returns.

    Returns:
        Best daily return as a decimal.

    Raises:
        ValueError: If no valid returns are available.
    """

    clean_returns = daily_returns.dropna()

    if clean_returns.empty:
        raise ValueError("Daily-return data cannot be empty.")

    return float(clean_returns.max())


def calculate_worst_daily_return(
    daily_returns: pd.Series,
) -> float:
    """
    Return the lowest daily return.

    Args:
        daily_returns: Series containing daily returns.

    Returns:
        Worst daily return as a decimal.

    Raises:
        ValueError: If no valid returns are available.
    """

    clean_returns = daily_returns.dropna()

    if clean_returns.empty:
        raise ValueError("Daily-return data cannot be empty.")

    return float(clean_returns.min())


def calculate_positive_day_ratio(
    daily_returns: pd.Series,
) -> float:
    """
    Calculate the proportion of trading days with positive returns.

    Args:
        daily_returns: Series containing daily returns.

    Returns:
        Proportion of positive-return days as a decimal.

    Raises:
        ValueError: If no valid returns are available.
    """

    clean_returns = daily_returns.dropna()

    if clean_returns.empty:
        raise ValueError("Daily-return data cannot be empty.")

    positive_days = (clean_returns > 0).sum()
    total_days = len(clean_returns)

    return float(positive_days / total_days)

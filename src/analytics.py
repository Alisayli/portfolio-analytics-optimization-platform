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
def calculate_value_at_risk(
    daily_returns: pd.Series,
    confidence_level: float = 0.95,
) -> float:
    """
    Calculate historical Value at Risk (VaR).

    Args:
        daily_returns: Series containing daily portfolio returns.
        confidence_level: Confidence level used for VaR.

    Returns:
        Historical VaR as a positive loss magnitude.

    Raises:
        ValueError: If return data is empty or the confidence
        level is invalid.
    """

    clean_returns = daily_returns.dropna()

    if clean_returns.empty:
        raise ValueError(
            "Daily-return data cannot be empty."
        )

    if not 0 < confidence_level < 1:
        raise ValueError(
            "Confidence level must be between 0 and 1."
        )

    tail_probability = 1 - confidence_level

    return_threshold = clean_returns.quantile(
        tail_probability
    )

    value_at_risk = -return_threshold

    return float(value_at_risk)


def calculate_conditional_value_at_risk(
    daily_returns: pd.Series,
    confidence_level: float = 0.95,
) -> float:
    """
    Calculate historical Conditional Value at Risk (CVaR).

    Args:
        daily_returns: Series containing daily portfolio returns.
        confidence_level: Confidence level used for CVaR.

    Returns:
        Historical CVaR as a positive loss magnitude.

    Raises:
        ValueError: If return data is empty or the confidence
        level is invalid.
    """

    clean_returns = daily_returns.dropna()

    if clean_returns.empty:
        raise ValueError(
            "Daily-return data cannot be empty."
        )

    if not 0 < confidence_level < 1:
        raise ValueError(
            "Confidence level must be between 0 and 1."
        )

    value_at_risk = calculate_value_at_risk(
        clean_returns,
        confidence_level=confidence_level,
    )

    return_threshold = -value_at_risk

    tail_losses = clean_returns[
        clean_returns <= return_threshold
    ]

    conditional_value_at_risk = -tail_losses.mean()

    return float(conditional_value_at_risk)

def calculate_beta(
    portfolio_returns: pd.Series,
    benchmark_returns: pd.Series,
) -> float:
    """
    Calculate portfolio beta relative to a benchmark.

    Args:
        portfolio_returns: Series containing daily portfolio returns.
        benchmark_returns: Series containing daily benchmark returns.

    Returns:
        Portfolio beta.

    Raises:
        ValueError: If aligned return data is insufficient or
        benchmark variance is zero.
    """

    aligned_returns = pd.concat(
        [portfolio_returns, benchmark_returns],
        axis=1,
        join="inner",
    ).dropna()

    if len(aligned_returns) < 2:
        raise ValueError(
            "At least two aligned return observations are required."
        )

    portfolio_series = aligned_returns.iloc[:, 0]
    benchmark_series = aligned_returns.iloc[:, 1]

    benchmark_variance = benchmark_series.var(ddof=1)

    if benchmark_variance == 0:
        raise ValueError(
            "Benchmark return variance must be greater than zero."
        )

    covariance = portfolio_series.cov(
        benchmark_series
    )

    beta = covariance / benchmark_variance

    return float(beta)

def calculate_capm_expected_return(
    beta: float,
    risk_free_rate: float,
    market_return: float,
) -> float:
    """
    Calculate the CAPM expected return.

    Args:
        beta: Portfolio beta relative to the benchmark.
        risk_free_rate: Annualized risk-free rate as a decimal.
        market_return: Annualized expected market return as a decimal.

    Returns:
        CAPM expected return as a decimal.
    """

    market_risk_premium = (
        market_return - risk_free_rate
    )

    capm_expected_return = (
        risk_free_rate
        + beta * market_risk_premium
    )

    return float(capm_expected_return)

def calculate_jensens_alpha(
    actual_portfolio_return: float,
    capm_expected_return: float,
) -> float:
    """
    Calculate Jensen's Alpha.

    Args:
        actual_portfolio_return:
            Actual annualized portfolio return as a decimal.
        capm_expected_return:
            CAPM expected portfolio return as a decimal.

    Returns:
        Jensen's Alpha as a decimal.
    """

    alpha = (
        actual_portfolio_return
        - capm_expected_return
    )

    return float(alpha)

def calculate_tracking_error(
    portfolio_returns: pd.Series,
    benchmark_returns: pd.Series,
    periods_per_year: int = TRADING_DAYS_PER_YEAR,
) -> float:
    """
    Calculate annualized tracking error relative to a benchmark.

    Args:
        portfolio_returns:
            Series containing daily portfolio returns.
        benchmark_returns:
            Series containing daily benchmark returns.
        periods_per_year:
            Number of trading periods used for annualization.

    Returns:
        Annualized tracking error as a decimal.

    Raises:
        ValueError: If aligned return data is insufficient or
        periods_per_year is invalid.
    """

    aligned_returns = pd.concat(
        [portfolio_returns, benchmark_returns],
        axis=1,
        join="inner",
    ).dropna()

    if len(aligned_returns) < 2:
        raise ValueError(
            "At least two aligned return observations are required."
        )

    if periods_per_year <= 0:
        raise ValueError(
            "Periods per year must be positive."
        )

    active_returns = (
        aligned_returns.iloc[:, 0]
        - aligned_returns.iloc[:, 1]
    )

    daily_tracking_error = active_returns.std(
        ddof=1
    )

    annualized_tracking_error = (
        daily_tracking_error
        * periods_per_year ** 0.5
    )

    return float(annualized_tracking_error)

def calculate_information_ratio(
    portfolio_return: float,
    benchmark_return: float,
    tracking_error: float,
) -> float:
    """
    Calculate the Information Ratio.

    Args:
        portfolio_return:
            Annualized portfolio return as a decimal.
        benchmark_return:
            Annualized benchmark return as a decimal.
        tracking_error:
            Annualized tracking error as a decimal.

    Returns:
        Information Ratio.

    Raises:
        ValueError: If tracking error is zero or negative.
    """

    if tracking_error <= 0:
        raise ValueError(
            "Tracking error must be greater than zero."
        )

    active_return = (
        portfolio_return
        - benchmark_return
    )

    information_ratio = (
        active_return / tracking_error
    )

    return float(information_ratio)

def calculate_sortino_ratio(
    annualized_return: float,
    daily_returns: pd.Series,
    risk_free_rate: float,
    periods_per_year: int = TRADING_DAYS_PER_YEAR,
) -> float:
    """
    Calculate the annualized Sortino ratio.

    Args:
        annualized_return:
            Annualized portfolio return as a decimal.
        daily_returns:
            Series containing daily portfolio returns.
        risk_free_rate:
            Annualized risk-free rate as a decimal.
        periods_per_year:
            Number of trading periods used for annualization.

    Returns:
        Annualized Sortino ratio.

    Raises:
        ValueError: If return data is insufficient, periods_per_year
        is invalid, or downside deviation is zero.
    """

    clean_returns = daily_returns.dropna()

    if clean_returns.empty:
        raise ValueError(
            "Daily-return data cannot be empty."
        )

    if periods_per_year <= 0:
        raise ValueError(
            "Periods per year must be positive."
        )

    daily_target_return = (
        (1 + risk_free_rate)
        ** (1 / periods_per_year)
        - 1
    )

    downside_returns = clean_returns[
        clean_returns < daily_target_return
    ]

    if downside_returns.empty:
        raise ValueError(
            "No downside returns are available."
        )

    downside_deviation = (
        (
            (
                downside_returns
                - daily_target_return
            ) ** 2
        ).mean()
        ** 0.5
    )

    annualized_downside_deviation = (
        downside_deviation
        * periods_per_year ** 0.5
    )

    if annualized_downside_deviation == 0:
        raise ValueError(
            "Downside deviation must be greater than zero."
        )

    excess_return = (
        annualized_return
        - risk_free_rate
    )

    sortino_ratio = (
        excess_return
        / annualized_downside_deviation
    )

    return float(sortino_ratio)

def calculate_calmar_ratio(
    annualized_return: float,
    maximum_drawdown: float,
) -> float:
    """
    Calculate the Calmar ratio.

    Args:
        annualized_return:
            Annualized portfolio return as a decimal.
        maximum_drawdown:
            Maximum portfolio drawdown as a negative decimal.

    Returns:
        Calmar ratio.

    Raises:
        ValueError: If maximum drawdown is zero.
    """

    if maximum_drawdown == 0:
        raise ValueError(
            "Maximum drawdown must be non-zero."
        )

    calmar_ratio = (
        annualized_return
        / abs(maximum_drawdown)
    )

    return float(calmar_ratio)

def calculate_treynor_ratio(
    annualized_return: float,
    risk_free_rate: float,
    beta: float,
) -> float:
    """
    Calculate the Treynor ratio.

    Args:
        annualized_return:
            Annualized portfolio return as a decimal.
        risk_free_rate:
            Annualized risk-free rate as a decimal.
        beta:
            Portfolio beta.

    Returns:
        Treynor ratio.

    Raises:
        ValueError: If beta is zero.
    """

    if beta == 0:
        raise ValueError(
            "Portfolio beta must be non-zero."
        )

    excess_return = (
        annualized_return
        - risk_free_rate
    )

    treynor_ratio = (
        excess_return
        / beta
    )

    return float(treynor_ratio)


def calculate_upside_capture_ratio(
    portfolio_returns: pd.Series,
    benchmark_returns: pd.Series,
) -> float:
    """
    Calculate the upside capture ratio.

    Args:
        portfolio_returns:
            Series containing daily portfolio returns.
        benchmark_returns:
            Series containing daily benchmark returns.

    Returns:
        Upside capture ratio as a decimal.

    Raises:
        ValueError: If aligned return data is insufficient or
        there are no positive benchmark-return observations.
    """

    aligned_returns = pd.concat(
        [portfolio_returns, benchmark_returns],
        axis=1,
        join="inner",
    ).dropna()

    if aligned_returns.empty:
        raise ValueError(
            "Aligned return data cannot be empty."
        )

    portfolio_series = aligned_returns.iloc[:, 0]
    benchmark_series = aligned_returns.iloc[:, 1]

    positive_benchmark_mask = (
        benchmark_series > 0
    )

    if not positive_benchmark_mask.any():
        raise ValueError(
            "No positive benchmark-return observations are available."
        )

    portfolio_upside_return = portfolio_series[
        positive_benchmark_mask
    ].mean()

    benchmark_upside_return = benchmark_series[
        positive_benchmark_mask
    ].mean()

    if benchmark_upside_return == 0:
        raise ValueError(
            "Benchmark upside return must be non-zero."
        )

    upside_capture_ratio = (
        portfolio_upside_return
        / benchmark_upside_return
    )

    return float(upside_capture_ratio)


def calculate_downside_capture_ratio(
    portfolio_returns: pd.Series,
    benchmark_returns: pd.Series,
) -> float:
    """
    Calculate the downside capture ratio.

    Args:
        portfolio_returns:
            Series containing daily portfolio returns.
        benchmark_returns:
            Series containing daily benchmark returns.

    Returns:
        Downside capture ratio as a decimal.

    Raises:
        ValueError: If aligned return data is insufficient or
        there are no negative benchmark-return observations.
    """

    aligned_returns = pd.concat(
        [portfolio_returns, benchmark_returns],
        axis=1,
        join="inner",
    ).dropna()

    if aligned_returns.empty:
        raise ValueError(
            "Aligned return data cannot be empty."
        )

    portfolio_series = aligned_returns.iloc[:, 0]
    benchmark_series = aligned_returns.iloc[:, 1]

    negative_benchmark_mask = (
        benchmark_series < 0
    )

    if not negative_benchmark_mask.any():
        raise ValueError(
            "No negative benchmark-return observations are available."
        )

    portfolio_downside_return = portfolio_series[
        negative_benchmark_mask
    ].mean()

    benchmark_downside_return = benchmark_series[
        negative_benchmark_mask
    ].mean()

    if benchmark_downside_return == 0:
        raise ValueError(
            "Benchmark downside return must be non-zero."
        )

    downside_capture_ratio = (
        portfolio_downside_return
        / benchmark_downside_return
    )

    return float(downside_capture_ratio)

def calculate_active_return(
    portfolio_return: float,
    benchmark_return: float,
) -> float:
    """
    Calculate benchmark-relative active return.

    Args:
        portfolio_return:
            Annualized portfolio return as a decimal.
        benchmark_return:
            Annualized benchmark return as a decimal.

    Returns:
        Active return as a decimal.
    """

    active_return = (
        portfolio_return
        - benchmark_return
    )

    return float(active_return)

def calculate_current_portfolio_weights(
    price_data: pd.DataFrame,
    initial_weights: dict,
) -> dict:
    """
    Calculate current portfolio weights after asset-price drift.

    Args:
        price_data:
            DataFrame containing historical adjusted close prices.
        initial_weights:
            Dictionary containing initial portfolio weights.

    Returns:
        Dictionary containing current portfolio weights.

    Raises:
        ValueError: If price data is empty or required tickers
        are missing.
    """

    if price_data.empty:
        raise ValueError(
            "Price data cannot be empty."
        )

    missing_tickers = set(initial_weights) - set(
        price_data.columns
    )

    if missing_tickers:
        raise ValueError(
            f"Missing price data for: {sorted(missing_tickers)}"
        )

    growth_factors = (
        price_data.iloc[-1]
        / price_data.iloc[0]
    )

    ending_values = {
        ticker: (
            weight * growth_factors[ticker]
        )
        for ticker, weight in initial_weights.items()
    }

    total_ending_value = sum(
        ending_values.values()
    )

    current_weights = {
        ticker: (
            ending_value / total_ending_value
        )
        for ticker, ending_value in ending_values.items()
    }

    return current_weights

def calculate_rebalancing_recommendations(
    target_weights: dict,
    current_weights: dict,
    threshold: float = 0.05,
) -> dict:
    """
    Calculate portfolio rebalancing recommendations.

    Args:
        target_weights:
            Dictionary containing target portfolio weights.
        current_weights:
            Dictionary containing current portfolio weights.
        threshold:
            Absolute weight-drift threshold required
            to trigger a Buy or Sell recommendation.

    Returns:
        Dictionary containing target weight, current weight,
        weight drift, and recommended action for each asset.

    Raises:
        ValueError: If threshold is negative or portfolio
        tickers do not match.
    """

    if threshold < 0:
        raise ValueError(
            "Rebalancing threshold cannot be negative."
        )

    if set(target_weights) != set(current_weights):
        raise ValueError(
            "Target and current portfolio tickers must match."
        )

    recommendations = {}

    for ticker in target_weights:
        target_weight = target_weights[ticker]
        current_weight = current_weights[ticker]

        weight_drift = (
            current_weight - target_weight
        )

        if weight_drift > threshold:
            action = "Sell"
        elif weight_drift < -threshold:
            action = "Buy"
        else:
            action = "Hold"

        recommendations[ticker] = {
            "target_weight": target_weight,
            "current_weight": current_weight,
            "weight_drift": weight_drift,
            "action": action,
        }

    return recommendations


def calculate_rebalancing_trades(
    target_weights: dict,
    current_weights: dict,
    threshold: float = 0.05,
) -> dict:
    """
    Calculate recommended portfolio rebalancing trades.

    Args:
        target_weights:
            Dictionary containing target portfolio weights.
        current_weights:
            Dictionary containing current portfolio weights.
        threshold:
            Absolute weight-drift threshold required
            to trigger a trade.

    Returns:
        Dictionary containing the recommended trade weight
        and direction for each asset.

    Raises:
        ValueError: If threshold is negative or portfolio
        tickers do not match.
    """

    if threshold < 0:
        raise ValueError(
            "Rebalancing threshold cannot be negative."
        )

    if set(target_weights) != set(current_weights):
        raise ValueError(
            "Target and current portfolio tickers must match."
        )

    trades = {}

    for ticker in target_weights:
        target_weight = target_weights[ticker]
        current_weight = current_weights[ticker]

        weight_drift = (
            current_weight - target_weight
        )

        if abs(weight_drift) <= threshold:
            trade_weight = 0.0
            action = "Hold"
        else:
            trade_weight = (
                target_weight - current_weight
            )

            if trade_weight > 0:
                action = "Buy"
            else:
                action = "Sell"

        trades[ticker] = {
            "trade_weight": trade_weight,
            "action": action,
        }

    return trades


def calculate_stress_scenario_return(
    portfolio_weights: dict,
    asset_shocks: dict,
) -> float:
    """
    Calculate portfolio return under a stress scenario.

    Args:
        portfolio_weights:
            Dictionary containing portfolio weights by ticker.
        asset_shocks:
            Dictionary containing scenario returns by ticker.

    Returns:
        Portfolio stress return as a decimal.

    Raises:
        ValueError: If portfolio and scenario tickers do not match.
    """

    if set(portfolio_weights) != set(asset_shocks):
        raise ValueError(
            "Portfolio and stress scenario tickers must match."
        )

    stress_return = sum(
        portfolio_weights[ticker]
        * asset_shocks[ticker]
        for ticker in portfolio_weights
    )

    return float(stress_return)

def run_stress_scenarios(
    portfolio_weights: dict,
    scenarios: dict,
) -> dict:
    """
    Evaluate multiple portfolio stress scenarios.

    Args:
        portfolio_weights:
            Dictionary containing portfolio weights by ticker.
        scenarios:
            Dictionary mapping scenario names to asset-shock dictionaries.

    Returns:
        Dictionary mapping scenario names to portfolio stress returns.

    Raises:
        ValueError: If no scenarios are provided.
    """

    if not scenarios:
        raise ValueError(
            "At least one stress scenario is required."
        )

    results = {}

    for scenario_name, asset_shocks in scenarios.items():
        results[scenario_name] = calculate_stress_scenario_return(
            portfolio_weights=portfolio_weights,
            asset_shocks=asset_shocks,
        )

    return results
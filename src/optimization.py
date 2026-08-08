import numpy as np
import pandas as pd
from scipy.optimize import minimize


TRADING_DAYS_PER_YEAR = 252


def calculate_expected_returns(
    asset_returns: pd.DataFrame,
    periods_per_year: int = TRADING_DAYS_PER_YEAR,
) -> pd.Series:
    """
    Calculate annualized expected returns for each asset.

    Args:
        asset_returns:
            DataFrame of periodic asset returns.
        periods_per_year:
            Number of return periods in one year.

    Returns:
        Annualized expected return for each asset.
    """

    if asset_returns.empty:
        raise ValueError("Asset returns cannot be empty.")

    return asset_returns.mean() * periods_per_year


def calculate_covariance_matrix(
    asset_returns: pd.DataFrame,
    periods_per_year: int = TRADING_DAYS_PER_YEAR,
) -> pd.DataFrame:
    """
    Calculate the annualized covariance matrix.

    Args:
        asset_returns:
            DataFrame of periodic asset returns.
        periods_per_year:
            Number of return periods in one year.

    Returns:
        Annualized covariance matrix.
    """

    if asset_returns.empty:
        raise ValueError("Asset returns cannot be empty.")

    return asset_returns.cov() * periods_per_year


def calculate_portfolio_statistics(
    weights: np.ndarray,
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
    risk_free_rate: float = 0.0,
) -> dict:
    """
    Calculate return, volatility, and Sharpe ratio.

    Args:
        weights:
            Portfolio weights in the same order as the assets.
        expected_returns:
            Annualized expected returns by asset.
        covariance_matrix:
            Annualized covariance matrix.
        risk_free_rate:
            Annualized risk-free rate.

    Returns:
        Dictionary containing portfolio statistics.
    """

    weights = np.asarray(weights, dtype=float)

    number_of_assets = len(expected_returns)

    if len(weights) != number_of_assets:
        raise ValueError(
            "The number of weights must match the number of assets."
        )

    if not np.isclose(weights.sum(), 1.0):
        raise ValueError("Portfolio weights must sum to 1.")

    portfolio_return = float(
        weights @ expected_returns.to_numpy()
    )

    portfolio_variance = float(
        weights
        @ covariance_matrix.to_numpy()
        @ weights
    )

    portfolio_volatility = float(
        np.sqrt(portfolio_variance)
    )

    if portfolio_volatility == 0:
        sharpe_ratio = np.nan
    else:
        sharpe_ratio = (
            portfolio_return - risk_free_rate
        ) / portfolio_volatility

    return {
        "return": portfolio_return,
        "volatility": portfolio_volatility,
        "sharpe_ratio": float(sharpe_ratio),
    }


def simulate_random_portfolios(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
    number_of_portfolios: int = 10_000,
    risk_free_rate: float = 0.0,
    maximum_weight: float = 0.40,
    random_seed: int | None = 42,
) -> pd.DataFrame:

    """
    Simulate random long-only portfolios.

    Args:
        expected_returns:
            Annualized expected returns by asset.
        covariance_matrix:
            Annualized covariance matrix.
        number_of_portfolios:
            Number of portfolios to simulate.
                risk_free_rate:
            Annualized risk-free rate.
        maximum_weight:
            Maximum permitted allocation to one asset.
        random_seed:
            Seed used to make the simulation reproducible.
    Returns:
        DataFrame containing portfolio statistics and weights.
    """

    if number_of_portfolios <= 0:
        raise ValueError(
            "Number of portfolios must be greater than zero."
        )

    if not expected_returns.index.equals(
        covariance_matrix.index
    ):
        raise ValueError(
            "Expected returns and covariance matrix "
            "must use the same asset order."
        )

    number_of_assets = len(expected_returns)

    if maximum_weight <= 0 or maximum_weight > 1:
        raise ValueError(
            "Maximum weight must be greater than zero "
            "and no greater than one."
        )

    if number_of_assets * maximum_weight < 1:
        raise ValueError(
            "Maximum weight is too restrictive for "
            "the number of assets."
        )

    random_generator = np.random.default_rng(
        random_seed
    )

    simulation_rows = []

    while len(simulation_rows) < number_of_portfolios:
        weights = random_generator.random(
            number_of_assets
        )
        weights = weights / weights.sum()

        if np.any(weights > maximum_weight):
            continue
        weights = weights / weights.sum()

        if np.any(weights > maximum_weight):
            continue

        statistics = calculate_portfolio_statistics(
            weights=weights,
            expected_returns=expected_returns,
            covariance_matrix=covariance_matrix,
            risk_free_rate=risk_free_rate,
        )

        row = {
            "Expected Return": statistics["return"],
            "Volatility": statistics["volatility"],
            "Sharpe Ratio": statistics["sharpe_ratio"],
        }

        for ticker, weight in zip(
            expected_returns.index,
            weights,
        ):
            row[f"{ticker} Weight"] = weight

        simulation_rows.append(row)

    return pd.DataFrame(simulation_rows)
def optimize_maximum_sharpe(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
    risk_free_rate: float = 0.0,
    maximum_weight: float = 0.40,
) -> dict:
    """
    Find the long-only portfolio with the maximum Sharpe ratio.

    Args:
        expected_returns:
            Annualized expected returns by asset.
        covariance_matrix:
            Annualized covariance matrix.
        risk_free_rate:
            Annualized risk-free rate.
        maximum_weight:
            Maximum permitted allocation to one asset.

    Returns:
        Dictionary containing optimized weights and statistics.
    """

    if expected_returns.empty:
        raise ValueError(
            "Expected returns cannot be empty."
        )

    if not expected_returns.index.equals(
        covariance_matrix.index
    ):
        raise ValueError(
            "Expected returns and covariance matrix "
            "must use the same asset order."
        )

    number_of_assets = len(expected_returns)

    if maximum_weight <= 0 or maximum_weight > 1:
        raise ValueError(
            "Maximum weight must be greater than zero "
            "and no greater than one."
        )

    if number_of_assets * maximum_weight < 1:
        raise ValueError(
            "Maximum weight is too restrictive for "
            "the number of assets."
        )

    initial_weights = np.repeat(
        1 / number_of_assets,
        number_of_assets,
    )

    bounds = tuple(
        (0.0, maximum_weight)
        for _ in range(number_of_assets)
    )

    constraints = (
        {
            "type": "eq",
            "fun": lambda weights: weights.sum() - 1.0,
        },
    )

    def negative_sharpe_ratio(
        weights: np.ndarray,
    ) -> float:
        statistics = calculate_portfolio_statistics(
            weights=weights,
            expected_returns=expected_returns,
            covariance_matrix=covariance_matrix,
            risk_free_rate=risk_free_rate,
        )

        return -statistics["sharpe_ratio"]

    result = minimize(
        fun=negative_sharpe_ratio,
        x0=initial_weights,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
    )

    if not result.success:
        raise RuntimeError(
            "Maximum Sharpe optimization failed: "
            f"{result.message}"
        )

    optimized_statistics = calculate_portfolio_statistics(
        weights=result.x,
        expected_returns=expected_returns,
        covariance_matrix=covariance_matrix,
        risk_free_rate=risk_free_rate,
    )

    return {
        "weights": pd.Series(
            result.x,
            index=expected_returns.index,
        ),
        "return": optimized_statistics["return"],
        "volatility": optimized_statistics["volatility"],
        "sharpe_ratio": optimized_statistics["sharpe_ratio"],
    }


def optimize_minimum_volatility(
    expected_returns: pd.Series,
    covariance_matrix: pd.DataFrame,
    risk_free_rate: float = 0.0,
    maximum_weight: float = 0.40,
) -> dict:
    """
    Find the long-only portfolio with minimum volatility.

    Args:
        expected_returns:
            Annualized expected returns by asset.
        covariance_matrix:
            Annualized covariance matrix.
        risk_free_rate:
            Annualized risk-free rate.
        maximum_weight:
            Maximum permitted allocation to one asset.

    Returns:
        Dictionary containing optimized weights and statistics.
    """

    if expected_returns.empty:
        raise ValueError(
            "Expected returns cannot be empty."
        )

    if not expected_returns.index.equals(
        covariance_matrix.index
    ):
        raise ValueError(
            "Expected returns and covariance matrix "
            "must use the same asset order."
        )

    number_of_assets = len(expected_returns)

    if maximum_weight <= 0 or maximum_weight > 1:
        raise ValueError(
            "Maximum weight must be greater than zero "
            "and no greater than one."
        )

    if number_of_assets * maximum_weight < 1:
        raise ValueError(
            "Maximum weight is too restrictive for "
            "the number of assets."
        )

    initial_weights = np.repeat(
        1 / number_of_assets,
        number_of_assets,
    )

    bounds = tuple(
        (0.0, maximum_weight)
        for _ in range(number_of_assets)
    )

    constraints = (
        {
            "type": "eq",
            "fun": lambda weights: weights.sum() - 1.0,
        },
    )

    def portfolio_volatility(
        weights: np.ndarray,
    ) -> float:
        statistics = calculate_portfolio_statistics(
            weights=weights,
            expected_returns=expected_returns,
            covariance_matrix=covariance_matrix,
            risk_free_rate=risk_free_rate,
        )

        return statistics["volatility"]

    result = minimize(
        fun=portfolio_volatility,
        x0=initial_weights,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
    )

    if not result.success:
        raise RuntimeError(
            "Minimum-volatility optimization failed: "
            f"{result.message}"
        )

    optimized_statistics = calculate_portfolio_statistics(
        weights=result.x,
        expected_returns=expected_returns,
        covariance_matrix=covariance_matrix,
        risk_free_rate=risk_free_rate,
    )

    return {
        "weights": pd.Series(
            result.x,
            index=expected_returns.index,
        ),
        "return": optimized_statistics["return"],
        "volatility": optimized_statistics["volatility"],
        "sharpe_ratio": optimized_statistics["sharpe_ratio"],
    }

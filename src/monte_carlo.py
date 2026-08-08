import numpy as np
import pandas as pd


def simulate_portfolio_paths(
    annualized_return: float,
    annualized_volatility: float,
    starting_value: float = 100.0,
    number_of_days: int = 252,
    number_of_simulations: int = 10_000,
    random_seed: int | None = 42,
) -> pd.DataFrame:
    """
    Simulate future portfolio-value paths using
    geometric Brownian motion.
    """

    if starting_value <= 0:
        raise ValueError(
            "Starting value must be greater than zero."
        )

    if number_of_days <= 0:
        raise ValueError(
            "Number of days must be greater than zero."
        )

    if number_of_simulations <= 0:
        raise ValueError(
            "Number of simulations must be greater than zero."
        )

    if annualized_volatility < 0:
        raise ValueError(
            "Annualized volatility cannot be negative."
        )

    trading_days_per_year = 252

    annualized_log_return = np.log1p(
        annualized_return
    )

    daily_drift = (
        annualized_log_return
        - 0.5 * annualized_volatility ** 2
    ) / trading_days_per_year
    daily_volatility = (
        annualized_volatility
        / np.sqrt(trading_days_per_year)
    )
    if annualized_return <= -1:
        raise ValueError(
            "Annualized return must be greater than -100%."
        )
    random_generator = np.random.default_rng(
        random_seed
    )

    random_shocks = random_generator.standard_normal(
        size=(
            number_of_days,
            number_of_simulations,
        )
    )

    daily_log_returns = (
        daily_drift
        + daily_volatility * random_shocks
    )

    cumulative_log_returns = np.cumsum(
        daily_log_returns,
        axis=0,
    )

    simulated_values = (
        starting_value
        * np.exp(cumulative_log_returns)
    )

    starting_row = np.full(
        shape=(1, number_of_simulations),
        fill_value=starting_value,
    )

    simulated_values = np.vstack(
        [
            starting_row,
            simulated_values,
        ]
    )

    simulation_index = pd.RangeIndex(
        start=0,
        stop=number_of_days + 1,
        name="Day",
    )

    simulation_columns = [
        f"Simulation {simulation_number}"
        for simulation_number in range(
            1,
            number_of_simulations + 1,
        )
    ]

    return pd.DataFrame(
        simulated_values,
        index=simulation_index,
        columns=simulation_columns,
    )
def summarize_monte_carlo_results(
    simulated_paths: pd.DataFrame,
    starting_value: float,
) -> dict:
    """
    Summarize Monte Carlo ending-value outcomes.

    Args:
        simulated_paths:
            DataFrame containing simulated portfolio-value paths.
        starting_value:
            Initial portfolio value used in the simulation.

    Returns:
        Dictionary containing Monte Carlo summary statistics.
    """

    if simulated_paths.empty:
        raise ValueError(
            "Simulated paths cannot be empty."
        )

    if starting_value <= 0:
        raise ValueError(
            "Starting value must be greater than zero."
        )

    ending_values = simulated_paths.iloc[-1]

    mean_ending_value = float(
        ending_values.mean()
    )

    median_ending_value = float(
        ending_values.median()
    )

    fifth_percentile = float(
        ending_values.quantile(0.05)
    )

    ninety_fifth_percentile = float(
        ending_values.quantile(0.95)
    )

    probability_of_loss = float(
        (ending_values < starting_value).mean()
    )

    expected_gain = (
        mean_ending_value - starting_value
    )

    downside_value_at_risk = (
        starting_value - fifth_percentile
    )

    return {
        "mean_ending_value": mean_ending_value,
        "median_ending_value": median_ending_value,
        "fifth_percentile": fifth_percentile,
        "ninety_fifth_percentile": (
            ninety_fifth_percentile
        ),
        "probability_of_loss": probability_of_loss,
        "expected_gain": expected_gain,
        "downside_value_at_risk": (
            downside_value_at_risk
        ),
    }

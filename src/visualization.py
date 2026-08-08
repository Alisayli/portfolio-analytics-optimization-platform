from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_portfolio_value(
    portfolio_value: pd.Series,
    output_folder: Path,
) -> Path:
    """
    Create and save a portfolio value chart.

    Args:
        portfolio_value:
            Series containing the portfolio value index over time.
        output_folder:
            Folder where the chart image will be saved.

    Returns:
        Path to the saved chart image.

    Raises:
        ValueError:
            If the portfolio value series is empty.
    """

    clean_values = portfolio_value.dropna()

    if clean_values.empty:
        raise ValueError("Portfolio value data cannot be empty.")

    output_folder.mkdir(parents=True, exist_ok=True)

    figure, axis = plt.subplots(figsize=(10, 6))

    axis.plot(
        clean_values.index,
        clean_values.values,
        linewidth=2,
    )

    axis.set_title("Portfolio Value Over Time")
    axis.set_xlabel("Date")
    axis.set_ylabel("Portfolio Value")
    axis.grid(True, alpha=0.3)

    figure.autofmt_xdate()
    figure.tight_layout()

    file_path = output_folder / "portfolio_value.png"

    figure.savefig(
        file_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(figure)

    return file_path
def plot_drawdown(
    portfolio_drawdown: pd.Series,
    output_folder: Path,
) -> Path:
    """
    Create and save a portfolio drawdown chart.

    Args:
        portfolio_drawdown:
            Series containing portfolio drawdowns over time.
        output_folder:
            Folder where the chart image will be saved.

    Returns:
        Path to the saved chart image.

    Raises:
        ValueError:
            If the drawdown series is empty.
    """

    clean_drawdown = portfolio_drawdown.dropna()

    if clean_drawdown.empty:
        raise ValueError("Portfolio drawdown data cannot be empty.")

    output_folder.mkdir(parents=True, exist_ok=True)

    figure, axis = plt.subplots(figsize=(10, 6))

    axis.plot(
        clean_drawdown.index,
        clean_drawdown.values,
        linewidth=2,
    )

    axis.fill_between(
        clean_drawdown.index,
        clean_drawdown.values,
        0,
        alpha=0.25,
    )

    axis.set_title("Portfolio Drawdown Over Time")
    axis.set_xlabel("Date")
    axis.set_ylabel("Drawdown")
    axis.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda value, _: f"{value:.0%}")
    )
    axis.grid(True, alpha=0.3)

    figure.autofmt_xdate()
    figure.tight_layout()

    file_path = output_folder / "portfolio_drawdown.png"

    figure.savefig(
        file_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(figure)

    return file_path

def plot_asset_contributions(
    total_contributions: pd.Series,
    output_folder: Path,
) -> Path:
    """
    Create and save a bar chart of total asset contributions.

    Args:
        total_contributions:
            Series containing total contribution by asset.
        output_folder:
            Folder where the chart image will be saved.

    Returns:
        Path to the saved chart image.

    Raises:
        ValueError:
            If contribution data is empty.
    """

    clean_contributions = total_contributions.dropna()

    if clean_contributions.empty:
        raise ValueError("Asset contribution data cannot be empty.")

    clean_contributions = clean_contributions.sort_values()

    output_folder.mkdir(parents=True, exist_ok=True)

    figure, axis = plt.subplots(figsize=(10, 6))

    axis.bar(
        clean_contributions.index,
        clean_contributions.values,
    )

    axis.axhline(
        0,
        linewidth=1,
    )

    axis.set_title("Asset Contribution to Portfolio Return")
    axis.set_xlabel("Asset")
    axis.set_ylabel("Contribution")
    axis.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda value, _: f"{value:.1%}")
    )
    axis.grid(
        True,
        axis="y",
        alpha=0.3,
    )

    figure.tight_layout()

    file_path = output_folder / "asset_contributions.png"

    figure.savefig(
        file_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(figure)

    return file_path

def plot_correlation_heatmap(
    correlation_matrix: pd.DataFrame,
    output_folder: Path,
) -> Path:
    """
    Create and save a correlation heatmap.

    Args:
        correlation_matrix:
            Correlation matrix of asset returns.
        output_folder:
            Folder where the chart image will be saved.

    Returns:
        Path to the saved chart image.

    Raises:
        ValueError:
            If the correlation matrix is empty.
    """

    if correlation_matrix.empty:
        raise ValueError(
            "Correlation matrix cannot be empty."
        )

    output_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    figure, axis = plt.subplots(figsize=(8, 6))

    sns.heatmap(
        correlation_matrix,
        annot=True,
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        linewidths=0.5,
        ax=axis,
    )

    axis.set_title("Asset Correlation Heatmap")

    figure.tight_layout()

    file_path = (
        output_folder
        / "correlation_heatmap.png"
    )

    figure.savefig(
        file_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(figure)

    return file_path

def plot_benchmark_comparison(
    portfolio_value: pd.Series,
    benchmark_value: pd.Series,
    benchmark_name: str,
    output_folder: Path,
) -> Path:
    """
    Create and save a portfolio versus benchmark chart.

    Args:
        portfolio_value:
            Portfolio value index.
        benchmark_value:
            Benchmark value index.
        benchmark_name:
            Name of the benchmark.
        output_folder:
            Folder where the chart will be saved.

    Returns:
        Path to the saved chart.
    """

    if portfolio_value.empty:
        raise ValueError(
            "Portfolio value data cannot be empty."
        )

    if benchmark_value.empty:
        raise ValueError(
            "Benchmark value data cannot be empty."
        )

    output_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    figure, axis = plt.subplots(figsize=(10, 6))

    axis.plot(
        portfolio_value.index,
        portfolio_value.values,
        label="Portfolio",
        linewidth=2,
    )

    axis.plot(
        benchmark_value.index,
        benchmark_value.values,
        label=benchmark_name,
        linewidth=2,
    )

    axis.set_title(
        "Portfolio vs Benchmark"
    )
    axis.set_xlabel("Date")
    axis.set_ylabel("Value Index")
    axis.grid(True, alpha=0.3)

    axis.legend()

    figure.autofmt_xdate()
    figure.tight_layout()

    file_path = (
        output_folder
        / "benchmark_comparison.png"
    )

    figure.savefig(
        file_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(figure)

    return file_path

def plot_rolling_volatility(
    portfolio_returns: pd.Series,
    output_folder: Path,
    window: int = 5,
    trading_periods: int = 252,
) -> Path:
    """Create and save an annualized rolling-volatility chart."""

    clean_returns = portfolio_returns.dropna()

    if clean_returns.empty:
        raise ValueError("Portfolio-return data cannot be empty.")

    if window < 2:
        raise ValueError("Rolling window must be at least 2.")

    rolling_volatility = (
        clean_returns
        .rolling(window=window)
        .std()
        * trading_periods ** 0.5
    ).dropna()

    if rolling_volatility.empty:
        raise ValueError(
            "Not enough observations to calculate rolling volatility."
        )

    output_folder.mkdir(parents=True, exist_ok=True)

    figure, axis = plt.subplots(figsize=(10, 6))

    axis.plot(
        rolling_volatility.index,
        rolling_volatility.values,
        linewidth=2,
    )

    axis.set_title(
        f"{window}-Day Rolling Annualized Volatility"
    )
    axis.set_xlabel("Date")
    axis.set_ylabel("Annualized Volatility")
    axis.yaxis.set_major_formatter(
        plt.FuncFormatter(lambda value, _: f"{value:.0%}")
    )
    axis.grid(True, alpha=0.3)

    figure.autofmt_xdate()
    figure.tight_layout()

    file_path = output_folder / "rolling_volatility.png"

    figure.savefig(
        file_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(figure)

    return file_path


def plot_rolling_sharpe_ratio(
    portfolio_returns: pd.Series,
    risk_free_rate: float,
    output_folder: Path,
    window: int = 5,
    trading_periods: int = 252,
) -> Path:
    """Create and save an annualized rolling-Sharpe-ratio chart."""

    clean_returns = portfolio_returns.dropna()

    if clean_returns.empty:
        raise ValueError("Portfolio-return data cannot be empty.")

    if window < 2:
        raise ValueError("Rolling window must be at least 2.")

    daily_risk_free_rate = (
        (1 + risk_free_rate) ** (1 / trading_periods)
        - 1
    )

    rolling_excess_return = (
        clean_returns - daily_risk_free_rate
    ).rolling(window=window).mean()

    rolling_volatility = (
        clean_returns
        .rolling(window=window)
        .std()
    )

    rolling_sharpe_ratio = (
        rolling_excess_return
        / rolling_volatility
        * trading_periods ** 0.5
    ).replace(
        [float("inf"), float("-inf")],
        pd.NA,
    ).dropna()

    if rolling_sharpe_ratio.empty:
        raise ValueError(
            "Not enough observations to calculate rolling Sharpe ratio."
        )

    output_folder.mkdir(parents=True, exist_ok=True)

    figure, axis = plt.subplots(figsize=(10, 6))

    axis.plot(
        rolling_sharpe_ratio.index,
        rolling_sharpe_ratio.values,
        linewidth=2,
    )

    axis.axhline(0, linewidth=1)

    axis.set_title(
        f"{window}-Day Rolling Annualized Sharpe Ratio"
    )
    axis.set_xlabel("Date")
    axis.set_ylabel("Sharpe Ratio")
    axis.grid(True, alpha=0.3)

    figure.autofmt_xdate()
    figure.tight_layout()

    file_path = output_folder / "rolling_sharpe_ratio.png"

    figure.savefig(
        file_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(figure)

    return file_path
def plot_efficient_frontier(
    simulated_portfolios: pd.DataFrame,
    current_portfolio_statistics: dict,
    maximum_sharpe_portfolio: dict,
    minimum_volatility_portfolio: dict,
    output_folder: Path,
) -> Path:
    """
    Create and save a constrained efficient-frontier chart.

    Args:
        simulated_portfolios:
            DataFrame containing simulated portfolio statistics.
        current_portfolio_statistics:
            Statistics for the user's current portfolio.
        maximum_sharpe_portfolio:
            Exact constrained maximum-Sharpe portfolio.
        minimum_volatility_portfolio:
            Exact constrained minimum-volatility portfolio.
        output_folder:
            Folder where the chart will be saved.

    Returns:
        Path to the saved chart.
    """

    required_columns = {
        "Expected Return",
        "Volatility",
        "Sharpe Ratio",
    }

    missing_columns = (
        required_columns
        - set(simulated_portfolios.columns)
    )

    if missing_columns:
        raise ValueError(
            "Simulated portfolios are missing required columns: "
            f"{sorted(missing_columns)}"
        )

    if simulated_portfolios.empty:
        raise ValueError(
            "Simulated portfolio data cannot be empty."
        )

    output_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    figure, axis = plt.subplots(
        figsize=(10, 6)
    )

    portfolio_cloud = axis.scatter(
        simulated_portfolios["Volatility"],
        simulated_portfolios["Expected Return"],
        c=simulated_portfolios["Sharpe Ratio"],
        alpha=0.55,
        s=14,
    )

    axis.scatter(
        current_portfolio_statistics["volatility"],
        current_portfolio_statistics["return"],
        marker="o",
        s=150,
        edgecolors="black",
        linewidths=1.5,
        label="Current Portfolio",
    )

    axis.scatter(
        maximum_sharpe_portfolio["volatility"],
        maximum_sharpe_portfolio["return"],
        marker="*",
        s=280,
        edgecolors="black",
        linewidths=1.5,
        label="Maximum Sharpe",
    )

    axis.scatter(
        minimum_volatility_portfolio["volatility"],
        minimum_volatility_portfolio["return"],
        marker="X",
        s=180,
        edgecolors="black",
        linewidths=1.5,
        label="Minimum Volatility",
    )

    colour_bar = figure.colorbar(
        portfolio_cloud,
        ax=axis,
    )
    colour_bar.set_label("Sharpe Ratio")

    axis.set_title(
        "Constrained Portfolio Efficient Frontier"
    )
    axis.set_xlabel(
        "Expected Annual Volatility"
    )
    axis.set_ylabel(
        "Expected Annual Return"
    )

    axis.xaxis.set_major_formatter(
        plt.FuncFormatter(
            lambda value, _: f"{value:.0%}"
        )
    )
    axis.yaxis.set_major_formatter(
        plt.FuncFormatter(
            lambda value, _: f"{value:.0%}"
        )
    )

    axis.grid(
        True,
        alpha=0.3,
    )
    axis.legend()

    figure.tight_layout()

    file_path = (
        output_folder
        / "efficient_frontier.png"
    )

    figure.savefig(
        file_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(figure)

    return file_path
def plot_monte_carlo_forecast(
    simulated_paths: pd.DataFrame,
    output_folder: Path,
    number_of_sample_paths: int = 50,
) -> Path:
    """
    Create and save a Monte Carlo portfolio forecast chart.

    Args:
        simulated_paths:
            DataFrame containing simulated portfolio-value paths.
        output_folder:
            Folder where the chart will be saved.
        number_of_sample_paths:
            Number of individual simulation paths to display.

    Returns:
        Path to the saved chart.
    """

    if simulated_paths.empty:
        raise ValueError(
            "Simulated portfolio paths cannot be empty."
        )

    if number_of_sample_paths <= 0:
        raise ValueError(
            "Number of sample paths must be greater than zero."
        )

    number_of_sample_paths = min(
        number_of_sample_paths,
        simulated_paths.shape[1],
    )

    median_path = simulated_paths.median(
        axis=1
    )

    fifth_percentile_path = simulated_paths.quantile(
        0.05,
        axis=1,
    )

    ninety_fifth_percentile_path = simulated_paths.quantile(
        0.95,
        axis=1,
    )

    sample_paths = simulated_paths.iloc[
        :,
        :number_of_sample_paths,
    ]

    output_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    figure, axis = plt.subplots(
        figsize=(10, 6)
    )

    for column in sample_paths.columns:
        axis.plot(
            sample_paths.index,
            sample_paths[column],
            linewidth=0.8,
            alpha=0.15,
        )

    axis.fill_between(
        simulated_paths.index,
        fifth_percentile_path,
        ninety_fifth_percentile_path,
        alpha=0.20,
        label="5th–95th Percentile Range",
    )

    axis.plot(
        median_path.index,
        median_path,
        linewidth=2.5,
        label="Median Simulated Path",
    )

    axis.axhline(
        simulated_paths.iloc[0, 0],
        linewidth=1,
        linestyle="--",
        label="Starting Value",
    )

    axis.set_title(
        "Monte Carlo Portfolio Forecast"
    )

    axis.set_xlabel(
        "Trading Day"
    )

    axis.set_ylabel(
        "Portfolio Value Index"
    )

    axis.grid(
        True,
        alpha=0.3,
    )

    axis.legend()

    figure.tight_layout()

    file_path = (
        output_folder
        / "monte_carlo_forecast.png"
    )

    figure.savefig(
        file_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(figure)

    return file_path


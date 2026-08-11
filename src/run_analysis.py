import argparse
import json
import logging
from pathlib import Path
import pandas as pd

from analytics import (
    calculate_active_return,
    calculate_annualized_return,
    calculate_annualized_volatility,
    calculate_beta,
    calculate_calmar_ratio,
    calculate_capm_expected_return,
    calculate_conditional_value_at_risk,
    calculate_daily_returns,
    calculate_downside_capture_ratio,
    calculate_drawdown,
    calculate_information_ratio,
    calculate_jensens_alpha,
    calculate_maximum_drawdown,
    calculate_sharpe_ratio,
    calculate_sortino_ratio,
    calculate_total_return,
    calculate_tracking_error,
    calculate_treynor_ratio,
    calculate_upside_capture_ratio,
    calculate_value_at_risk,
)

from download_data import (
    download_multiple_adjusted_closes,
    download_risk_free_rate,
    download_stock_data,
    save_processed_data,
)

from excel_report import (
    create_portfolio_workbook,
)
from monte_carlo import (
    simulate_portfolio_paths,
    summarize_monte_carlo_results,
)
from optimization import (
    calculate_covariance_matrix,
    calculate_expected_returns,
    calculate_portfolio_statistics,
    optimize_maximum_sharpe,
    optimize_minimum_volatility,
    simulate_random_portfolios,
)

from portfolio import (
    calculate_arithmetic_total_contributions,
    calculate_asset_contributions,
    calculate_asset_returns,
    calculate_correlation_matrix,
    calculate_portfolio_cumulative_returns,
    calculate_portfolio_returns,
    calculate_portfolio_value_index,
    validate_portfolio_weights,
)

from visualization import (
    plot_asset_contributions,
    plot_benchmark_comparison,
    plot_correlation_heatmap,
    plot_drawdown,
    plot_efficient_frontier,
    plot_monte_carlo_forecast,
    plot_portfolio_value,
    plot_rolling_sharpe_ratio,
    plot_rolling_volatility,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Run portfolio analytics, optimization, "
            "and Monte Carlo forecasting."
        )
    )

    parser.add_argument(
        "--config",
        default="config.json",
        help=(
            "Path to the JSON configuration file. "
            "Default: config.json"
        ),
    )

    parser.add_argument(
        "--start-date",
        help="Override the analysis start date (YYYY-MM-DD).",
    )

    parser.add_argument(
        "--end-date",
        help="Override the analysis end date (YYYY-MM-DD).",
    )

    parser.add_argument(
        "--benchmark",
        help="Override the benchmark ticker.",
    )

    return parser.parse_args()
def load_configuration(
    args: argparse.Namespace,
) -> dict:
    """Load the application configuration."""

    project_root = (
        Path(__file__).resolve().parent.parent
    )

    config_path = Path(args.config)

    if not config_path.is_absolute():
        config_path = (
            project_root / config_path
        )

    with config_path.open(
        "r",
        encoding="utf-8",
    ) as config_file:
        config = json.load(config_file)

    if args.start_date:
        config["analysis"]["start_date"] = (
            args.start_date
        )

    if args.end_date:
        config["analysis"]["end_date"] = (
            args.end_date
        )

    if args.benchmark:
        config["analysis"][
            "benchmark_ticker"
        ] = args.benchmark.upper()

    return config
def download_input_data(
    portfolio_weights: dict,
    start_date: str,
    end_date: str,
    optimization_start_date: str,
    optimization_end_date: str,
    benchmark_ticker: str,
):
    """Download and prepare portfolio input data."""

    validated_weights = validate_portfolio_weights(
        portfolio_weights
    )

    price_data = download_multiple_adjusted_closes(
        tickers=list(validated_weights.keys()),
        start_date=start_date,
        end_date=end_date,
    )

    optimization_price_data = (
        download_multiple_adjusted_closes(
            tickers=list(validated_weights.keys()),
            start_date=optimization_start_date,
            end_date=optimization_end_date,
        )
    )

    benchmark_data = download_stock_data(
        ticker=benchmark_ticker,
        start_date=start_date,
        end_date=end_date,
    )

    benchmark_prices = benchmark_data["Adj Close"]

    return (
        validated_weights,
        price_data,
        optimization_price_data,
        benchmark_prices,
    )
def calculate_portfolio_analytics(
    price_data: pd.DataFrame,
    benchmark_prices: pd.Series,
    validated_weights: dict,
    benchmark_ticker: str,
) -> dict:
    """Calculate portfolio performance and risk analytics."""

    asset_returns = calculate_asset_returns(
        price_data
    )

    portfolio_returns = calculate_portfolio_returns(
        asset_returns=asset_returns,
        portfolio_weights=validated_weights,
    )

    portfolio_cumulative_returns = (
        calculate_portfolio_cumulative_returns(
            portfolio_returns
        )
    )

    final_cumulative_return = (
        portfolio_cumulative_returns.iloc[-1]
    )

    portfolio_value = calculate_portfolio_value_index(
        portfolio_returns=portfolio_returns,
        initial_date=price_data.index[0],
        starting_value=100.0,
    )

    benchmark_value = (
        benchmark_prices
        / benchmark_prices.iloc[0]
        * 100
    )
    benchmark_value.name = benchmark_ticker

    asset_contributions = calculate_asset_contributions(
        asset_returns=asset_returns,
        portfolio_weights=validated_weights,
    )

    total_contributions = (
        calculate_arithmetic_total_contributions(
            asset_contributions
        )
    )

    correlation_matrix = calculate_correlation_matrix(
        asset_returns
    )

    total_return = calculate_total_return(
        portfolio_value
    )

    return_difference = abs(
        total_return - final_cumulative_return
    )

    if return_difference > 1e-10:
        raise ValueError(
            "Portfolio total return does not match "
            "the final cumulative return."
        )

    annualized_return = calculate_annualized_return(
        total_return=total_return,
        number_of_periods=len(portfolio_returns),
    )

    annualized_volatility = (
        calculate_annualized_volatility(
            daily_returns=portfolio_returns,
        )
    )

    portfolio_drawdown = calculate_drawdown(
        portfolio_value
    )

    maximum_drawdown = calculate_maximum_drawdown(
        portfolio_value
    )
    
    value_at_risk_95 = calculate_value_at_risk(
        portfolio_returns,
        confidence_level=0.95,
    )

    conditional_value_at_risk_95 = (
        calculate_conditional_value_at_risk(
            portfolio_returns,
            confidence_level=0.95,
        )
    )

    value_at_risk_99 = calculate_value_at_risk(
        portfolio_returns,
        confidence_level=0.99,
    )

    conditional_value_at_risk_99 = (
        calculate_conditional_value_at_risk(
            portfolio_returns,
            confidence_level=0.99,
        )
    )
    
    return {
        "asset_returns": asset_returns,
        "portfolio_returns": portfolio_returns,
        "portfolio_cumulative_returns": (
            portfolio_cumulative_returns
        ),
        "portfolio_value": portfolio_value,
        "benchmark_value": benchmark_value,
        "asset_contributions": asset_contributions,
        "total_contributions": total_contributions,
        "correlation_matrix": correlation_matrix,
        "total_return": total_return,
        "return_difference": return_difference,
        "annualized_return": annualized_return,
        "annualized_volatility": annualized_volatility,
        "portfolio_drawdown": portfolio_drawdown,
        "maximum_drawdown": maximum_drawdown,
        "value_at_risk_95": value_at_risk_95,
        "conditional_value_at_risk_95": (
            conditional_value_at_risk_95
        ),
        "value_at_risk_99": value_at_risk_99,
        "conditional_value_at_risk_99": (
            conditional_value_at_risk_99
        ),
        
        
    }
def calculate_market_risk_analytics(
    portfolio_returns: pd.Series,
    benchmark_prices: pd.Series,
    annualized_portfolio_return: float,
    risk_free_rate: float,
) -> dict:
    """
    Calculate benchmark-relative market risk analytics.

    Args:
        portfolio_returns:
            Series containing daily portfolio returns.
        benchmark_prices:
            Series containing historical benchmark prices.
        annualized_portfolio_return:
            Annualized portfolio return as a decimal.
        risk_free_rate:
            Annualized risk-free rate as a decimal.

    Returns:
        Dictionary containing benchmark-relative risk metrics.
    """

    benchmark_returns = calculate_daily_returns(
        benchmark_prices
    )

    benchmark_total_return = calculate_total_return(
        benchmark_prices
    )

    benchmark_annualized_return = (
        calculate_annualized_return(
            total_return=benchmark_total_return,
            number_of_periods=len(benchmark_returns),
        )
    )

    beta = calculate_beta(
        portfolio_returns=portfolio_returns,
        benchmark_returns=benchmark_returns,
    )

    capm_expected_return = (
        calculate_capm_expected_return(
            beta=beta,
            risk_free_rate=risk_free_rate,
            market_return=benchmark_annualized_return,
        )
    )

    jensens_alpha = calculate_jensens_alpha(
        actual_portfolio_return=(
            annualized_portfolio_return
        ),
        capm_expected_return=capm_expected_return,
    )

    tracking_error = calculate_tracking_error(
        portfolio_returns=portfolio_returns,
        benchmark_returns=benchmark_returns,
    )

    information_ratio = calculate_information_ratio(
        portfolio_return=annualized_portfolio_return,
        benchmark_return=benchmark_annualized_return,
        tracking_error=tracking_error,
    )
    upside_capture_ratio = calculate_upside_capture_ratio(
        portfolio_returns=portfolio_returns,
        benchmark_returns=benchmark_returns,
    )

    downside_capture_ratio = calculate_downside_capture_ratio(
        portfolio_returns=portfolio_returns,
        benchmark_returns=benchmark_returns,
    )

    active_return = calculate_active_return(
        portfolio_return=annualized_portfolio_return,
        benchmark_return=benchmark_annualized_return,
    )
    return {
        "benchmark_returns": benchmark_returns,
        "benchmark_annualized_return": (
            benchmark_annualized_return
        ),
        "beta": beta,
        "capm_expected_return": capm_expected_return,
        "jensens_alpha": jensens_alpha,
        "tracking_error": tracking_error,
        "information_ratio": information_ratio,
        "upside_capture_ratio": upside_capture_ratio,
        "downside_capture_ratio": downside_capture_ratio,
        "active_return": active_return,
    }   
    
    
def run_optimization_and_forecast(
    optimization_asset_returns: pd.DataFrame,
    validated_weights: dict,
    risk_free_rate: float,
    maximum_weight: float,
    number_of_portfolios: int,
    optimization_random_seed: int,
    monte_carlo_starting_value: float,
    monte_carlo_number_of_days: int,
    monte_carlo_number_of_simulations: int,
    monte_carlo_random_seed: int,
) -> dict:
    """Run portfolio optimization and Monte Carlo forecasting."""

    expected_returns = calculate_expected_returns(
        optimization_asset_returns
    )

    covariance_matrix = calculate_covariance_matrix(
        optimization_asset_returns
    )

    current_portfolio_statistics = (
        calculate_portfolio_statistics(
            weights=list(validated_weights.values()),
            expected_returns=expected_returns,
            covariance_matrix=covariance_matrix,
            risk_free_rate=risk_free_rate,
        )
    )

    monte_carlo_paths = simulate_portfolio_paths(
        annualized_return=(
            current_portfolio_statistics["return"]
        ),
        annualized_volatility=(
            current_portfolio_statistics["volatility"]
        ),
        starting_value=monte_carlo_starting_value,
        number_of_days=monte_carlo_number_of_days,
        number_of_simulations=(
            monte_carlo_number_of_simulations
        ),
        random_seed=monte_carlo_random_seed,
    )

    monte_carlo_summary = summarize_monte_carlo_results(
        simulated_paths=monte_carlo_paths,
        starting_value=monte_carlo_starting_value,
    )

    simulated_portfolios = simulate_random_portfolios(
        expected_returns=expected_returns,
        covariance_matrix=covariance_matrix,
        number_of_portfolios=number_of_portfolios,
        risk_free_rate=risk_free_rate,
        maximum_weight=maximum_weight,
        random_seed=optimization_random_seed,
    )

    exact_maximum_sharpe_portfolio = (
        optimize_maximum_sharpe(
            expected_returns=expected_returns,
            covariance_matrix=covariance_matrix,
            risk_free_rate=risk_free_rate,
            maximum_weight=maximum_weight,
        )
    )

    exact_minimum_volatility_portfolio = (
        optimize_minimum_volatility(
            expected_returns=expected_returns,
            covariance_matrix=covariance_matrix,
            risk_free_rate=risk_free_rate,
            maximum_weight=maximum_weight,
        )
    )

    maximum_sharpe_portfolio = simulated_portfolios.loc[
        simulated_portfolios["Sharpe Ratio"].idxmax()
    ]

    minimum_volatility_portfolio = simulated_portfolios.loc[
        simulated_portfolios["Volatility"].idxmin()
    ]

    return {
        "expected_returns": expected_returns,
        "covariance_matrix": covariance_matrix,
        "current_portfolio_statistics": (
            current_portfolio_statistics
        ),
        "monte_carlo_paths": monte_carlo_paths,
        "monte_carlo_summary": monte_carlo_summary,
        "simulated_portfolios": simulated_portfolios,
        "exact_maximum_sharpe_portfolio": (
            exact_maximum_sharpe_portfolio
        ),
        "exact_minimum_volatility_portfolio": (
            exact_minimum_volatility_portfolio
        ),
        "maximum_sharpe_portfolio": (
            maximum_sharpe_portfolio
        ),
        "minimum_volatility_portfolio": (
            minimum_volatility_portfolio
        ),
    }

def main() -> None:

    """Run the complete portfolio analytics pipeline."""
    args = parse_arguments()
    logger.info("Starting portfolio analytics pipeline.")
    config = load_configuration(args)

    portfolio_weights = config[
        "portfolio_weights"
    ]

    start_date = config[
        "analysis"
    ]["start_date"]

    end_date = config[
        "analysis"
    ]["end_date"]

    benchmark_ticker = config[
        "analysis"
    ]["benchmark_ticker"]

    optimization_start_date = config[
        "optimization"
    ]["start_date"]

    optimization_end_date = end_date

    maximum_weight = config[
        "optimization"
    ]["maximum_weight"]

    number_of_portfolios = config[
        "optimization"
    ]["number_of_portfolios"]

    optimization_random_seed = config[
    "optimization"
]["random_seed"]

    monte_carlo_starting_value = config[
        "monte_carlo"
    ]["starting_value"]

    monte_carlo_number_of_days = config[
        "monte_carlo"
    ]["number_of_days"]

    monte_carlo_number_of_simulations = config[
        "monte_carlo"
    ]["number_of_simulations"]

    monte_carlo_random_seed = config[
        "monte_carlo"
    ]["random_seed"]

    rolling_window = config[
        "rolling_metrics"
    ]["window"]
    logger.info("Downloading market data.")

    (
        validated_weights,
        price_data,
        optimization_price_data,
        benchmark_prices,
    ) = download_input_data(

        portfolio_weights=portfolio_weights,
        start_date=start_date,
        end_date=end_date,
        optimization_start_date=optimization_start_date,
        optimization_end_date=optimization_end_date,
        benchmark_ticker=benchmark_ticker,
    )


    optimization_asset_returns = (
        calculate_asset_returns(
            optimization_price_data
        )
    )
    portfolio_analytics = calculate_portfolio_analytics(
        price_data=price_data,
        benchmark_prices=benchmark_prices,
        validated_weights=validated_weights,
        benchmark_ticker=benchmark_ticker,
    )

    asset_returns = portfolio_analytics["asset_returns"]
    portfolio_returns = portfolio_analytics["portfolio_returns"]
    portfolio_cumulative_returns = portfolio_analytics[
        "portfolio_cumulative_returns"
    ]
    portfolio_value = portfolio_analytics["portfolio_value"]
    benchmark_value = portfolio_analytics["benchmark_value"]
    asset_contributions = portfolio_analytics[
        "asset_contributions"
    ]
    total_contributions = portfolio_analytics[
        "total_contributions"
    ]
    correlation_matrix = portfolio_analytics[
        "correlation_matrix"
    ]
    total_return = portfolio_analytics["total_return"]
    annualized_return = portfolio_analytics[
        "annualized_return"
    ]
    return_difference = portfolio_analytics[
    "return_difference"
    ]
    annualized_volatility = portfolio_analytics[
        "annualized_volatility"
    ]
    portfolio_drawdown = portfolio_analytics[
        "portfolio_drawdown"
    ]
    maximum_drawdown = portfolio_analytics[
        "maximum_drawdown"
    ]
    value_at_risk_95 = portfolio_analytics[
        "value_at_risk_95"
    ]

    conditional_value_at_risk_95 = portfolio_analytics[
        "conditional_value_at_risk_95"
    ]

    value_at_risk_99 = portfolio_analytics[
        "value_at_risk_99"
    ]

    conditional_value_at_risk_99 = portfolio_analytics[
        "conditional_value_at_risk_99"
    ]
    risk_free_rate = download_risk_free_rate(
        start_date=start_date,
        end_date=end_date,
    )
    market_risk_analytics = calculate_market_risk_analytics(
        portfolio_returns=portfolio_returns,
        benchmark_prices=benchmark_prices,
        annualized_portfolio_return=annualized_return,
        risk_free_rate=risk_free_rate,
    )

    benchmark_annualized_return = market_risk_analytics[
        "benchmark_annualized_return"
    ]

    beta = market_risk_analytics["beta"]

    capm_expected_return = market_risk_analytics[
        "capm_expected_return"
    ]

    jensens_alpha = market_risk_analytics[
        "jensens_alpha"
    ]

    tracking_error = market_risk_analytics[
        "tracking_error"
    ]

    information_ratio = market_risk_analytics[
        "information_ratio"
    ]
    upside_capture_ratio = market_risk_analytics[
        "upside_capture_ratio"
    ]

    downside_capture_ratio = market_risk_analytics[
        "downside_capture_ratio"
    ]

    active_return = market_risk_analytics[
        "active_return"
    ]
    market_metrics_available = (
        len(portfolio_returns) >= 252
    )
    treynor_ratio = calculate_treynor_ratio(
        annualized_return=annualized_return,
        risk_free_rate=risk_free_rate,
        beta=beta,
    )
    logger.info(
        "Running optimization and Monte Carlo forecast."
    )

    optimization_results = run_optimization_and_forecast(
        optimization_asset_returns=optimization_asset_returns,
        validated_weights=validated_weights,
        risk_free_rate=risk_free_rate,
        maximum_weight=maximum_weight,
        number_of_portfolios=number_of_portfolios,
        optimization_random_seed=optimization_random_seed,
        monte_carlo_starting_value=monte_carlo_starting_value,
        monte_carlo_number_of_days=monte_carlo_number_of_days,
        monte_carlo_number_of_simulations=(
            monte_carlo_number_of_simulations
        ),
        monte_carlo_random_seed=monte_carlo_random_seed,
    )

    expected_returns = optimization_results[
        "expected_returns"
    ]
    covariance_matrix = optimization_results[
        "covariance_matrix"
    ]
    current_portfolio_statistics = optimization_results[
        "current_portfolio_statistics"
    ]
    monte_carlo_paths = optimization_results[
        "monte_carlo_paths"
    ]
    monte_carlo_summary = optimization_results[
        "monte_carlo_summary"
    ]
    simulated_portfolios = optimization_results[
        "simulated_portfolios"
    ]
    exact_maximum_sharpe_portfolio = (
        optimization_results[
            "exact_maximum_sharpe_portfolio"
        ]
    )
    exact_minimum_volatility_portfolio = (
        optimization_results[
            "exact_minimum_volatility_portfolio"
        ]
    )
    maximum_sharpe_portfolio = optimization_results[
        "maximum_sharpe_portfolio"
    ]
    minimum_volatility_portfolio = optimization_results[
        "minimum_volatility_portfolio"
    ]

    print("\nMonte Carlo forecast:")

    print(
        f"Mean ending value: "
        f"{monte_carlo_summary['mean_ending_value']:.2f}"
    )

    print(
        f"Median ending value: "
        f"{monte_carlo_summary['median_ending_value']:.2f}"
    )

    print(
        f"5th percentile ending value: "
        f"{monte_carlo_summary['fifth_percentile']:.2f}"
    )

    print(
        f"95th percentile ending value: "
        f"{monte_carlo_summary['ninety_fifth_percentile']:.2f}"
    )

    print(
        f"Probability of loss: "
        f"{monte_carlo_summary['probability_of_loss']:.2%}"
    )

    print(
        f"Expected gain: "
        f"{monte_carlo_summary['expected_gain']:.2f}"
    )

    print(
        f"5th-percentile downside: "
        f"{monte_carlo_summary['downside_value_at_risk']:.2f}"
    )

    print("\nOptimization statistics:")

    print(
        f"Expected annual return: "
        f"{current_portfolio_statistics['return']:.2%}"
    )

    print(
        f"Expected annual volatility: "
        f"{current_portfolio_statistics['volatility']:.2%}"
    )

    print(
        f"Expected Sharpe ratio: "
        f"{current_portfolio_statistics['sharpe_ratio']:.2f}"
    )

    print("\nBest simulated portfolios:")

    print(
        f"Maximum Sharpe portfolio — "
        f"Return: "
        f"{maximum_sharpe_portfolio['Expected Return']:.2%}, "
        f"Volatility: "
        f"{maximum_sharpe_portfolio['Volatility']:.2%}, "
        f"Sharpe: "
        f"{maximum_sharpe_portfolio['Sharpe Ratio']:.2f}"
    )

    print(
        f"Minimum volatility portfolio — "
        f"Return: "
        f"{minimum_volatility_portfolio['Expected Return']:.2%}, "
        f"Volatility: "
        f"{minimum_volatility_portfolio['Volatility']:.2%}, "
        f"Sharpe: "
        f"{minimum_volatility_portfolio['Sharpe Ratio']:.2f}"
    )
    print("\nAnnualized expected returns by asset:")

    for ticker, expected_return in expected_returns.items():
        print(
            f"{ticker}: {expected_return:.2%}"
        )

    print("\nMaximum Sharpe simulated weights:")

    for ticker in expected_returns.index:
        print(
            f"{ticker}: "
            f"{maximum_sharpe_portfolio[f'{ticker} Weight']:.2%}"
        )

    print("\nMinimum volatility simulated weights:")

    for ticker in expected_returns.index:
        print(
            f"{ticker}: "
            f"{minimum_volatility_portfolio[f'{ticker} Weight']:.2%}"
        )
    print("\nExact constrained portfolios:")

    print(
        f"Maximum Sharpe portfolio — "
        f"Return: "
        f"{exact_maximum_sharpe_portfolio['return']:.2%}, "
        f"Volatility: "
        f"{exact_maximum_sharpe_portfolio['volatility']:.2%}, "
        f"Sharpe: "
        f"{exact_maximum_sharpe_portfolio['sharpe_ratio']:.2f}"
    )

    print("\nMaximum Sharpe exact weights:")

    for ticker, weight in (
        exact_maximum_sharpe_portfolio[
            "weights"
        ].items()
    ):
        print(
            f"{ticker}: {weight:.2%}"
        )

    print(
        f"\nMinimum volatility portfolio — "
        f"Return: "
        f"{exact_minimum_volatility_portfolio['return']:.2%}, "
        f"Volatility: "
        f"{exact_minimum_volatility_portfolio['volatility']:.2%}, "
        f"Sharpe: "
        f"{exact_minimum_volatility_portfolio['sharpe_ratio']:.2f}"
    )

    print("\nMinimum volatility exact weights:")

    for ticker, weight in (
        exact_minimum_volatility_portfolio[
            "weights"
        ].items()
    ):
        print(
            f"{ticker}: {weight:.2%}"
        )
    sharpe_ratio = calculate_sharpe_ratio(
        annualized_return=annualized_return,
        annualized_volatility=annualized_volatility,
        risk_free_rate=risk_free_rate,
    )
    sortino_ratio = calculate_sortino_ratio(
        annualized_return=annualized_return,
        daily_returns=portfolio_returns,
        risk_free_rate=risk_free_rate,
    )

    calmar_ratio = calculate_calmar_ratio(
        annualized_return=annualized_return,
        maximum_drawdown=maximum_drawdown,
    )

    largest_contributor = total_contributions.idxmax()
    largest_detractor = total_contributions.idxmin()

    contribution_check = asset_contributions.sum(axis=1)

    maximum_difference = (
        contribution_check - portfolio_returns
    ).abs().max()

    processed_data = pd.concat(
        [
            portfolio_returns,
            portfolio_cumulative_returns,
            portfolio_value,
            portfolio_drawdown,
        ],
        axis=1,
        sort=False,
    )

    processed_file_path = save_processed_data(
        data=processed_data,
        ticker="PORTFOLIO",
        start_date=start_date,
        end_date=end_date,
    )

    charts_folder = (
        Path(__file__).resolve().parent.parent
        / "outputs"
        / "charts"
    )

    reports_folder = (
        Path(__file__).resolve().parent.parent
        / "outputs"
        / "reports"
    )


    chart_file_path = plot_portfolio_value(
        portfolio_value=portfolio_value,
        output_folder=charts_folder,
    )


    drawdown_chart_file_path = plot_drawdown(
        portfolio_drawdown=portfolio_drawdown,
        output_folder=charts_folder,
    )

    contribution_chart_file_path = plot_asset_contributions(
        total_contributions=total_contributions,
        output_folder=charts_folder,
    )

    correlation_chart_file_path = plot_correlation_heatmap(
        correlation_matrix=correlation_matrix,
        output_folder=charts_folder,
    )

    benchmark_chart_file_path = plot_benchmark_comparison(
        portfolio_value=portfolio_value,
        benchmark_value=benchmark_value,
        benchmark_name=benchmark_ticker,
        output_folder=charts_folder,
    )
    rolling_volatility_chart_file_path = (
        plot_rolling_volatility(
            portfolio_returns=portfolio_returns,
            output_folder=charts_folder,
            window=rolling_window,
        )
    )

    rolling_sharpe_chart_file_path = (
        plot_rolling_sharpe_ratio(
            portfolio_returns=portfolio_returns,
            risk_free_rate=risk_free_rate,
            output_folder=charts_folder,
            window=rolling_window,
        )
    )
    efficient_frontier_chart_file_path = (
        plot_efficient_frontier(
            simulated_portfolios=simulated_portfolios,
            current_portfolio_statistics=(
                current_portfolio_statistics
            ),
            maximum_sharpe_portfolio=(
                exact_maximum_sharpe_portfolio
            ),
            minimum_volatility_portfolio=(
                exact_minimum_volatility_portfolio
            ),
            output_folder=charts_folder,
        )
    )

    monte_carlo_chart_file_path = (
        plot_monte_carlo_forecast(
            simulated_paths=monte_carlo_paths,
            output_folder=charts_folder,
            number_of_sample_paths=50,
        )
    )

    portfolio_summary = {
        "start_date": start_date,
        "end_date": end_date,
        "total_return": total_return,
        "annualized_return": annualized_return,
        "annualized_volatility": annualized_volatility,
        "risk_free_rate": risk_free_rate,
        "sharpe_ratio": sharpe_ratio,
        "sortino_ratio": sortino_ratio,
        "calmar_ratio": calmar_ratio,
        "treynor_ratio": treynor_ratio,
        "maximum_drawdown": maximum_drawdown,
        "value_at_risk_95": value_at_risk_95,
        "conditional_value_at_risk_95": (
            conditional_value_at_risk_95
        ),
        "value_at_risk_99": value_at_risk_99,
        "conditional_value_at_risk_99": (
            conditional_value_at_risk_99
        ),
        "market_metrics_available": market_metrics_available,
        "benchmark_annualized_return": (
            benchmark_annualized_return
        ),
        "beta": beta,
        "upside_capture_ratio": upside_capture_ratio,
        "downside_capture_ratio": downside_capture_ratio,
        "active_return": active_return,
        "capm_expected_return": capm_expected_return,
        "jensens_alpha": jensens_alpha,
        "tracking_error": tracking_error,
        "information_ratio": information_ratio,
        "largest_contributor": largest_contributor,
        "largest_detractor": largest_detractor,
    }

    excel_report_file_path = create_portfolio_workbook(
        portfolio_summary=portfolio_summary,
        portfolio_weights=validated_weights,
        total_contributions=total_contributions,
        processed_data=processed_data,
        chart_file_paths=[
            chart_file_path,
            drawdown_chart_file_path,
            contribution_chart_file_path,
            correlation_chart_file_path,
            benchmark_chart_file_path,
            rolling_volatility_chart_file_path,
            rolling_sharpe_chart_file_path,
            efficient_frontier_chart_file_path,
            monte_carlo_chart_file_path,
        ],
        current_portfolio_statistics=(
            current_portfolio_statistics
        ),
        maximum_sharpe_portfolio=(
            exact_maximum_sharpe_portfolio
        ),
        minimum_volatility_portfolio=(
            exact_minimum_volatility_portfolio
        ),
        optimization_start_date=(
            optimization_start_date
        ),
        optimization_end_date=(
            optimization_end_date
        ),
        maximum_weight=maximum_weight,
        monte_carlo_summary=monte_carlo_summary,
        output_folder=reports_folder,
    )

    print("Portfolio weights:")
    for ticker, weight in validated_weights.items():
        print(f"{ticker}: {weight:.2%}")

    print("\nPortfolio value index:")
    print(portfolio_value.head())

    print("\nPortfolio summary:")
    print(
        "Analysis period: "
        f"{portfolio_summary['start_date']} "
        f"to {portfolio_summary['end_date']}"
    )
    print(
        f"Total return: "
        f"{portfolio_summary['total_return']:.2%}"
    )
    print(
        f"Annualized return: "
        f"{portfolio_summary['annualized_return']:.2%}"
    )
    print(
        f"Annualized volatility: "
        f"{portfolio_summary['annualized_volatility']:.2%}"
    )
    print(
        f"Risk-free rate: "
        f"{portfolio_summary['risk_free_rate']:.2%}"
    )
    print(
        f"Sharpe ratio: "
        f"{portfolio_summary['sharpe_ratio']:.2f}"
    )
    print(
        f"Sortino ratio: "
        f"{portfolio_summary['sortino_ratio']:.2f}"
    )

    print(
        f"Calmar ratio: "
        f"{portfolio_summary['calmar_ratio']:.2f}"
    )
    print(
        f"Maximum drawdown: "
        f"{portfolio_summary['maximum_drawdown']:.2%}"
    )
    print(
        f"95% Historical VaR: "
        f"{portfolio_summary['value_at_risk_95']:.2%}"
    )

    print(
        f"95% Historical CVaR: "
        f"{portfolio_summary['conditional_value_at_risk_95']:.2%}"
    )

    print(
        f"99% Historical VaR: "
        f"{portfolio_summary['value_at_risk_99']:.2%}"
    )

    print(
        f"99% Historical CVaR: "
        f"{portfolio_summary['conditional_value_at_risk_99']:.2%}"
    )
    print("\nMarket risk and benchmark analytics:")

    print(
        f"Benchmark annualized return: "
        f"{portfolio_summary['benchmark_annualized_return']:.2%}"
    )
    print(
        f"Active return: "
        f"{portfolio_summary['active_return']:.2%}"
    )
    print(
        f"Portfolio beta: "
        f"{portfolio_summary['beta']:.2f}"
    )
    print(
        f"Upside capture ratio: "
        f"{portfolio_summary['upside_capture_ratio']:.2%}"
    )
    print(
        f"Downside capture ratio: "
        f"{portfolio_summary['downside_capture_ratio']:.2%}"
    )
    print(
    f"Treynor ratio: "
    f"{portfolio_summary['treynor_ratio']:.2f}"
    )   

    if portfolio_summary["market_metrics_available"]:
        print(
            f"CAPM expected return: "
            f"{portfolio_summary['capm_expected_return']:.2%}"
        )

        print(
            f"Jensen's Alpha: "
            f"{portfolio_summary['jensens_alpha']:.2%}"
        )
    else:
        print(
            "CAPM expected return: N/A "
            "(requires at least 252 daily observations)"
        )
        print(
            "Jensen's Alpha: N/A "
            "(requires at least 252 daily observations)"
        )

    print(
        f"Tracking error: "
        f"{portfolio_summary['tracking_error']:.2%}"
    )

    if portfolio_summary["market_metrics_available"]:
        print(
            f"Information ratio: "
            f"{portfolio_summary['information_ratio']:.2f}"
        )
    else:
        print(
            "Information ratio: N/A "
            "(requires at least 252 daily observations)"
        )
    print("\nArithmetic contribution by asset:")

    for ticker, contribution in total_contributions.items():
        print(f"{ticker}: {contribution:.2%}")

    print(
        "\nLargest contributor: "
        f"{portfolio_summary['largest_contributor']}"
    )

    print(
        "Largest detractor: "
        f"{portfolio_summary['largest_detractor']}"
    )

    print("\nCorrelation matrix:")
    print(correlation_matrix.round(3))

    print(
        "\nMaximum contribution reconciliation difference: "
        f"{maximum_difference:.12f}"
    )
    print(
        "\nTotal-return reconciliation difference: "
        f"{return_difference:.12f}"
    )
    print(
        f"\nProcessed portfolio data saved to: "
        f"{processed_file_path}"
    )
    print(
        f"Portfolio value chart saved to: "
        f"{chart_file_path}"
    )
    print(
        f"Portfolio drawdown chart saved to: "
        f"{drawdown_chart_file_path}"
    )

    print(
        f"Asset contribution chart saved to: "
        f"{contribution_chart_file_path}"
    )

    print(
        f"Correlation heatmap saved to: "
        f"{correlation_chart_file_path}"
    )
    print(
        f"Benchmark comparison chart saved to: "
        f"{benchmark_chart_file_path}"
    )
    print(
        f"Rolling volatility chart saved to: "
        f"{rolling_volatility_chart_file_path}"
    )

    print(
        f"Rolling Sharpe chart saved to: "
        f"{rolling_sharpe_chart_file_path}"
    )
    print(
        f"Monte Carlo forecast chart saved to: "
        f"{monte_carlo_chart_file_path}"
    )
    print(
        f"Excel report saved to: "
        f"{excel_report_file_path}"
    )
    logger.info("Analysis completed successfully.")

if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as exc:
        logger.error("Required file not found: %s", exc)
    except json.JSONDecodeError as exc:
        logger.error("Invalid JSON configuration: %s", exc)
    except ValueError as exc:
        logger.error("Invalid analysis input: %s", exc)
    except KeyboardInterrupt:
        logger.warning("Analysis interrupted by user.")
    except Exception:
        logger.exception("Unexpected error during analysis.")

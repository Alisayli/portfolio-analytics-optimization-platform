import pandas as pd

from analytics import (
    calculate_annualized_return,
    calculate_annualized_volatility,
    calculate_best_daily_return,
    calculate_cumulative_returns,
    calculate_daily_returns,
    calculate_drawdown,
    calculate_maximum_drawdown,
    calculate_positive_day_ratio,
    calculate_sharpe_ratio,
    calculate_total_return,
    calculate_worst_daily_return,
)
from download_data import (
    download_risk_free_rate,
    download_stock_data,
    save_processed_data,
    save_raw_data,
)


def main() -> None:
    """Download Apple data and calculate performance and risk metrics."""

    ticker = "AAPL"
    start_date = "2025-01-01"
    end_date = "2025-02-01"

    stock_data = download_stock_data(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
    )

    raw_file_path = save_raw_data(
        data=stock_data,
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
    )

    adjusted_close = stock_data["Adj Close"]

    daily_returns = calculate_daily_returns(adjusted_close)
    cumulative_returns = calculate_cumulative_returns(daily_returns)
    total_return = calculate_total_return(adjusted_close)

    annualized_return = calculate_annualized_return(
        total_return=total_return,
        number_of_periods=len(daily_returns),
    )

    annualized_volatility = calculate_annualized_volatility(
        daily_returns=daily_returns,
    )

    drawdown = calculate_drawdown(adjusted_close)
    maximum_drawdown = calculate_maximum_drawdown(adjusted_close)

    risk_free_rate = download_risk_free_rate(
        start_date=start_date,
        end_date=end_date,
    )

    sharpe_ratio = calculate_sharpe_ratio(
        annualized_return=annualized_return,
        annualized_volatility=annualized_volatility,
        risk_free_rate=risk_free_rate,
    )

    best_daily_return = calculate_best_daily_return(daily_returns)
    worst_daily_return = calculate_worst_daily_return(daily_returns)
    positive_day_ratio = calculate_positive_day_ratio(daily_returns)

    processed_data = pd.concat(
        [
            adjusted_close.rename("Adjusted Close"),
            daily_returns,
            cumulative_returns,
            drawdown,
        ],
        axis=1,
    )

    processed_file_path = save_processed_data(
        data=processed_data,
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
    )

    summary_metrics = {
        "ticker": ticker,
        "start_date": start_date,
        "end_date": end_date,
        "total_return": total_return,
        "annualized_return": annualized_return,
        "annualized_volatility": annualized_volatility,
        "risk_free_rate": risk_free_rate,
        "sharpe_ratio": sharpe_ratio,
        "maximum_drawdown": maximum_drawdown,
        "best_daily_return": best_daily_return,
        "worst_daily_return": worst_daily_return,
        "positive_day_ratio": positive_day_ratio,
    }

    print("Summary metrics:")
    print(f"Ticker: {summary_metrics['ticker']}")
    print(
        "Analysis period: "
        f"{summary_metrics['start_date']} "
        f"to {summary_metrics['end_date']}"
    )
    print(f"Total return: {summary_metrics['total_return']:.2%}")
    print(
        "Annualized return: "
        f"{summary_metrics['annualized_return']:.2%}"
    )
    print(
        "Annualized volatility: "
        f"{summary_metrics['annualized_volatility']:.2%}"
    )
    print(
        "Risk-free rate: "
        f"{summary_metrics['risk_free_rate']:.2%}"
    )
    print(f"Sharpe ratio: {summary_metrics['sharpe_ratio']:.2f}")
    print(
        "Maximum drawdown: "
        f"{summary_metrics['maximum_drawdown']:.2%}"
    )
    print(
        "Best daily return: "
        f"{summary_metrics['best_daily_return']:.2%}"
    )
    print(
        "Worst daily return: "
        f"{summary_metrics['worst_daily_return']:.2%}"
    )
    print(
        "Positive-day ratio: "
        f"{summary_metrics['positive_day_ratio']:.2%}"
    )

    print(f"\nRaw data saved to: {raw_file_path}")
    print(f"Processed data saved to: {processed_file_path}")


if __name__ == "__main__":
    main()
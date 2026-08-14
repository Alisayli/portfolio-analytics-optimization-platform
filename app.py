import pandas as pd
from pathlib import Path
import sys

import streamlit as st


SRC_DIR = Path(__file__).resolve().parent / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from run_analysis import main

st.set_page_config(
    page_title="Portfolio Analytics Platform",
    page_icon="📊",
    layout="wide",
)
@st.cache_data
def load_analysis_results():
    return main()


analysis_results = load_analysis_results()

portfolio_summary = analysis_results[
    "portfolio_summary"
]

portfolio_value = analysis_results[
    "portfolio_value"
]

portfolio_weights = analysis_results[
    "portfolio_weights"
]
current_portfolio_statistics = analysis_results[
    "current_portfolio_statistics"
]
maximum_sharpe_portfolio = analysis_results[
    "maximum_sharpe_portfolio"
]
minimum_volatility_portfolio = analysis_results[
    "minimum_volatility_portfolio"
]
monte_carlo_summary = analysis_results[
    "monte_carlo_summary"
]

st.title("📊 Portfolio Analytics & Optimization Platform")

st.markdown(
    """
Interactive dashboard for portfolio performance,
risk analytics, optimization,
stress testing, and rebalancing.
"""
)

st.sidebar.title("Dashboard Navigation")

page = st.sidebar.radio(
    "Choose a Dashboard Page",
    (
        "Overview",
        "Risk Analytics",
        "Optimization",
        "Stress Testing",
        "Rebalancing",
    ),
)

if page == "Overview":
    st.header("Portfolio Performance Overview")

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        st.metric(
            label="Total Return",
            value=f"{portfolio_summary['total_return']:.2%}",
        )
    with metric_col2:
        st.metric(
            label="Annualized Return",
            value=f"{portfolio_summary['annualized_return']:.2%}",
        )

    with metric_col3:
        st.metric(
            label="Annualized Volatility",
            value=f"{portfolio_summary['annualized_volatility']:.2%}",
        )

    with metric_col4:
        st.metric(
            label="Sharpe Ratio",
            value=f"{portfolio_summary['sharpe_ratio']:.2f}",
        )

    st.subheader("Portfolio Value Over Time")

    st.line_chart(
        portfolio_value
    )
    st.divider()
    st.subheader("Key Portfolio Insights")

    highlight_col1, highlight_col2, highlight_col3 = st.columns(3)

    with highlight_col1:
        st.metric(
            label="Maximum Drawdown",
            value=f"{portfolio_summary['maximum_drawdown']:.2%}",
        )

    with highlight_col2:
        st.metric(
            label="Top Contributor",
            value=portfolio_summary["largest_contributor"],
        )

    with highlight_col3:
        st.metric(
            label="Top Detractor",
            value=portfolio_summary["largest_detractor"],
        )
elif page == "Risk Analytics":
    st.header("Portfolio Risk Analytics")
    st.caption(
        "Analyze portfolio risk exposure, downside risk, and relationships between portfolio holdings."
)

    risk_col1, risk_col2, risk_col3 = st.columns(3)

    with risk_col1:
        st.metric(
            label="Value at Risk (95%)",
            value=f"{portfolio_summary['value_at_risk_95']:.2%}",
        )

        st.metric(
            label="Conditional VaR (95%)",
            value=f"{portfolio_summary['conditional_value_at_risk_95']:.2%}",
        )

    with risk_col2:
        st.metric(
            label="Portfolio Beta",
            value=f"{portfolio_summary['beta']:.2f}",
        )

        st.metric(
            label="Tracking Error",
            value=f"{portfolio_summary['tracking_error']:.2%}",
        )

    with risk_col3:
        st.metric(
            label="Maximum Drawdown",
            value=f"{portfolio_summary['maximum_drawdown']:.2%}",
        )

        st.metric(
            label="Treynor Ratio",
            value=f"{portfolio_summary['treynor_ratio']:.2f}",
        )

    st.subheader("Asset Correlation Matrix")

    st.image(
        "outputs/charts/correlation_heatmap.png",
        width="stretch",
    )

elif page == "Optimization":
    st.header("Portfolio Optimization & Asset Allocation")
    st.caption(
    "Evaluate optimized portfolios using Modern Portfolio Theory and compare them with the current allocation."
)

    optimization_col1, optimization_col2, optimization_col3 = st.columns(3)

    with optimization_col1:
        st.metric(
            label="Expected Return",
            value=(
                f"{current_portfolio_statistics['return']:.2%}"
            ),
        )

    with optimization_col2:
        st.metric(
            label="Expected Volatility",
            value=(
                f"{current_portfolio_statistics['volatility']:.2%}"
            ),
        )

    with optimization_col3:
        st.metric(
            label="Expected Sharpe Ratio",
            value=(
                f"{current_portfolio_statistics['sharpe_ratio']:.2f}"
            ),
        )

    st.subheader("Efficient Frontier")

    st.image(
        "outputs/charts/efficient_frontier.png",
        width="stretch",
    )

    st.divider()

    st.subheader("Optimized Portfolio Summary")

    comparison_col1, comparison_col2 = st.columns(2)

    with comparison_col1:
        st.markdown("### Maximum Sharpe Portfolio")

        st.metric(
            label="Expected Return",
            value=f"{maximum_sharpe_portfolio['return']:.2%}",
        )

        st.metric(
            label="Expected Volatility",
            value=f"{maximum_sharpe_portfolio['volatility']:.2%}",
        )

        st.metric(
            label="Sharpe Ratio",
            value=f"{maximum_sharpe_portfolio['sharpe_ratio']:.2f}",
        )

    with comparison_col2:
        st.markdown("### Minimum Volatility Portfolio")

        st.metric(
            label="Expected Return",
            value=f"{minimum_volatility_portfolio['return']:.2%}",
        )

        st.metric(
            label="Expected Volatility",
            value=f"{minimum_volatility_portfolio['volatility']:.2%}",
        )

        st.metric(
            label="Sharpe Ratio",
            value=f"{minimum_volatility_portfolio['sharpe_ratio']:.2f}",
        )

        st.subheader("Monte Carlo Simulation")

    monte_carlo_col1, monte_carlo_col2, monte_carlo_col3 = st.columns(3)

    with monte_carlo_col1:
        st.metric(
            label="Mean Ending Value",
            value=f"{monte_carlo_summary['mean_ending_value']:.2f}",
        )

        st.metric(
            label="Median Ending Value",
            value=f"{monte_carlo_summary['median_ending_value']:.2f}",
        )

    with monte_carlo_col2:
        st.metric(
            label="5th Percentile",
            value=f"{monte_carlo_summary['fifth_percentile']:.2f}",
        )

        st.metric(
            label="95th Percentile",
            value=f"{monte_carlo_summary['ninety_fifth_percentile']:.2f}",
        )

    with monte_carlo_col3:
        st.metric(
            label="Probability of Loss",
            value=f"{monte_carlo_summary['probability_of_loss']:.2%}",
        )

        st.metric(
            label="Expected Gain",
            value=f"{monte_carlo_summary['expected_gain']:.2f}",
        )

    st.image(
        "outputs/charts/monte_carlo_forecast.png",
        width="stretch",
    )

    st.divider()

    st.subheader("Portfolio Allocation Comparison")

    allocation_data = pd.DataFrame(
        {
            "Current Portfolio": portfolio_weights,
            "Maximum Sharpe": maximum_sharpe_portfolio["weights"],
            "Minimum Volatility": minimum_volatility_portfolio["weights"],
        }
    )

    allocation_data = allocation_data.map(
        lambda weight: f"{weight:.2%}"
    )

    st.dataframe(
        allocation_data,
        width="stretch",
    )

    st.divider()

    st.subheader("Optimization Results")

    sharpe_improvement = (
        maximum_sharpe_portfolio["sharpe_ratio"]
        / current_portfolio_statistics["sharpe_ratio"]
        - 1
    )

    volatility_reduction = (
        minimum_volatility_portfolio["volatility"]
        / current_portfolio_statistics["volatility"]
        - 1
    )

    improvement_col1, improvement_col2 = st.columns(2)

    with improvement_col1:
        st.metric(
            label="Sharpe Ratio",
            value=(
                f"{current_portfolio_statistics['sharpe_ratio']:.2f} "
                f"→ {maximum_sharpe_portfolio['sharpe_ratio']:.2f}"
            ),
            delta=f"{sharpe_improvement:.2%}",
        )

    with improvement_col2:
        st.metric(
            label="Portfolio Volatility",
            value=(
                f"{current_portfolio_statistics['volatility']:.2%} "
                f"→ {minimum_volatility_portfolio['volatility']:.2%}"
            ),
            delta=f"{volatility_reduction:.2%}",
            delta_color="inverse",
        )


elif page == "Stress Testing":
    st.header("Portfolio Stress Testing")

    st.caption(
        "Evaluate portfolio resilience under predefined market stress scenarios."
    )

    stress_results = portfolio_summary[
        "stress_results"
    ]

    stress_scenarios = portfolio_summary[
        "stress_scenarios"
    ]

    stress_table = pd.DataFrame(
        {
            "Portfolio Impact": stress_results,
        }
    )

    stress_table["Portfolio Impact"] = (
        stress_table["Portfolio Impact"]
        .map(lambda value: f"{value:.2%}")
    )

    st.subheader("Scenario Results")

    st.dataframe(
        stress_table,
        width="stretch",
        hide_index=False,
    )

    st.divider()

    st.subheader("Stress Scenario Assumptions")

    scenario_rows = []

    for scenario_name, shocks in stress_scenarios.items():
        row = {
            "Scenario": scenario_name,
        }

        for ticker, shock in shocks.items():
            row[ticker] = f"{shock:.2%}"

        scenario_rows.append(row)

    scenario_table = pd.DataFrame(
        scenario_rows
    )

    st.dataframe(
        scenario_table,
        width="stretch",
        hide_index=True,
    )

elif page == "Rebalancing":
    st.header("Portfolio Rebalancing Analysis")

    st.caption(
        "Compare current portfolio weights with target allocations and review recommended trades."
    )

    rebalancing_recommendations = portfolio_summary[
        "rebalancing_recommendations"
    ]

    rebalancing_trades = portfolio_summary[
        "rebalancing_trades"
    ]

    rebalancing_rows = []

    for ticker, recommendation in rebalancing_recommendations.items():
        trade = rebalancing_trades[ticker]

        rebalancing_rows.append(
            {
                "Ticker": ticker,
                "Target Weight": f"{recommendation['target_weight']:.2%}",
                "Current Weight": f"{recommendation['current_weight']:.2%}",
                "Drift": f"{recommendation['weight_drift']:.2%}",
                "Action": recommendation["action"],
                "Suggested Trade": f"{trade['trade_weight']:.2%}",
            }
        )

    rebalancing_table = pd.DataFrame(
        rebalancing_rows
    )

    if portfolio_summary["portfolio_needs_rebalancing"]:
        st.warning("Portfolio drift exceeds the rebalancing threshold. Review the suggested trades below.")
    else:
        st.success("Portfolio is within the rebalancing threshold. No trades are currently recommended.")

    st.subheader("Recommended Portfolio Trades")

    st.dataframe(
        rebalancing_table,
        width="stretch",
        hide_index=True,
    )
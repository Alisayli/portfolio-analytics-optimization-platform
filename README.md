# Portfolio Analytics & Optimization Platform

![Python](https://img.shields.io/badge/Python-3.13-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)
![Finance](https://img.shields.io/badge/Domain-Portfolio%20Analytics-darkgreen)
![Git](https://img.shields.io/badge/Git-Version%20Controlled-orange)

A professional Python platform for **portfolio analytics, portfolio optimization, Monte Carlo forecasting, risk analysis, and automated Excel reporting**.

The platform demonstrates practical quantitative finance and software engineering techniques used in **investment management, portfolio management, wealth management, capital markets, and financial data analytics**.

Built with a strong emphasis on **modular architecture, reproducible analytics, and professional reporting**, the platform combines financial theory with structured Python workflows.

---

## Core Capabilities

### Portfolio Analytics

- Multi-asset portfolio analysis
- Portfolio return calculation
- Annualized return and volatility
- Sharpe ratio
- Maximum drawdown
- Asset return contribution analysis
- Correlation matrix generation
- Benchmark comparison
- Rolling volatility
- Rolling Sharpe ratio

### Portfolio Optimization

- Modern Portfolio Theory (Markowitz)
- Mean-Variance Optimization
- Efficient Frontier visualization
- Maximum Sharpe portfolio
- Minimum Volatility portfolio
- Portfolio allocation constraints

### Monte Carlo Forecasting

- Geometric Brownian Motion simulation
- 10,000 simulated portfolio paths
- Expected ending value
- Probability of loss
- Downside risk analysis
- Percentile forecasting

### Reporting

- Automated Excel report generation
- Professional portfolio dashboard
- Publication-quality charts
- Processed portfolio data export

---

## Technology Stack

### Programming

- Python 3.13

### Data Analysis

- NumPy
- Pandas

### Scientific Computing

- SciPy

### Data Visualization

- Matplotlib

### Reporting

- OpenPyXL

### Market Data

- Yahoo Finance API (`yfinance`)

### Development

- Git
- Virtual Environments (`venv`)

---


## Example Outputs
---

### Portfolio Optimization Report

The Excel report compares the current portfolio with the optimized Maximum Sharpe and Minimum Volatility portfolios, while also summarizing the Monte Carlo forecast.

![Portfolio Optimization Report](images/optimization_sheet.png)

### Efficient Frontier

The efficient frontier visualizes thousands of feasible portfolio allocations and highlights the current portfolio, the constrained Maximum Sharpe portfolio, and the Minimum Volatility portfolio.

![Efficient Frontier](images/efficient_frontier.png)

### Monte Carlo Forecast

The Monte Carlo forecast simulates 10,000 possible future portfolio paths using Geometric Brownian Motion. The chart highlights the median simulated path and the 5th–95th percentile range.

![Monte Carlo Forecast](images/monte_carlo_forecast.png)

---

## Financial Methodology

This project implements several widely used portfolio management and quantitative finance techniques.

### Portfolio Performance Analysis

The platform calculates:

- Total portfolio return
- Annualized return
- Annualized volatility
- Sharpe ratio
- Maximum drawdown
- Asset contribution analysis
- Correlation matrix

These metrics provide a comprehensive view of portfolio performance and risk.

---

### Mean-Variance Optimization

Portfolio optimization is based on Modern Portfolio Theory (MPT), introduced by Harry Markowitz.

The optimizer constructs portfolios that maximize expected risk-adjusted return while respecting practical investment constraints, including:

- Full portfolio investment (weights sum to 100%)
- Long-only portfolios (no short selling)
- Maximum position size limits

The project identifies both the:

- Maximum Sharpe Portfolio
- Minimum Volatility Portfolio

and compares them against the current portfolio allocation.

---

### Efficient Frontier

Thousands of feasible portfolios are simulated to visualize the efficient frontier.

Each simulated portfolio is evaluated using:

- Expected annual return
- Expected annual volatility
- Sharpe ratio

The visualization highlights:

- Current portfolio
- Maximum Sharpe portfolio
- Minimum Volatility portfolio

to demonstrate the trade-offs between expected return and portfolio risk.

---

### Monte Carlo Simulation

Future portfolio performance is estimated using Geometric Brownian Motion (GBM).

The simulation generates 10,000 possible one-year portfolio paths based on the portfolio's expected return and volatility.

The Monte Carlo engine reports:

- Expected ending portfolio value
- Median ending value
- 5th and 95th percentile outcomes
- Probability of loss
- Expected gain
- Downside risk

These simulations help estimate the range of potential future outcomes rather than relying on a single expected return estimate.

---
## Project Architecture

The project is organized into modular components, with each module responsible for a specific part of the analytics pipeline.

| Module | Purpose |
|----------|---------|
| `download_data.py` | Downloads historical market data and risk-free rates using Yahoo Finance. |
| `portfolio.py` | Calculates portfolio returns, cumulative performance, drawdowns, contribution analysis, and correlation statistics. |
| `analytics.py` | Computes portfolio performance metrics including annualized return, volatility, Sharpe ratio, and other summary statistics. |
| `optimization.py` | Implements Modern Portfolio Theory, efficient frontier generation, and constrained portfolio optimization. |
| `monte_carlo.py` | Simulates future portfolio performance using Geometric Brownian Motion and summarizes forecast statistics. |
| `visualization.py` | Generates publication-quality charts for portfolio analytics, optimization, and forecasting. |
| `excel_report.py` | Creates a professionally formatted Excel workbook containing portfolio analytics, optimization results, charts, and Monte Carlo forecasts. |
| `utils.py` | Shared helper functions used throughout the project. |
| `run_analysis.py` | End-to-end execution of the complete analytics pipeline using a sample portfolio. |
---

## Workflow

```text
Download Market Data
          │
          ▼
Portfolio Return Calculation
          │
          ▼
Risk & Performance Analytics
          │
          ├──────────────┐
          ▼              ▼
Portfolio        Monte Carlo
Optimization     Simulation
          │              │
          └──────┬───────┘
                 ▼
       Charts & Excel Report
```

The modular design keeps the analytics engine maintainable, reusable, and easy to extend with additional portfolio analysis features.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/portfolio-analytics-platform.git
cd portfolio-analytics-platform
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the complete analytics pipeline:

```bash
python src/run_analysis.py
```
The program will:

1. Download historical market data.
2. Calculate portfolio performance statistics.
3. Optimize the portfolio using Modern Portfolio Theory.
4. Generate the Efficient Frontier.
5. Run Monte Carlo simulations.
6. Produce publication-quality charts.
7. Generate a professional Excel report.

All generated outputs are saved automatically in the appropriate project folders.

---

## Repository Structure

```text
Portfolio-Analytics-Optimization-Platform/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── images/
│   ├── efficient_frontier.png
│   ├── monte_carlo_forecast.png
│   └── optimization_sheet.png
│
├── outputs/
│   ├── charts/
│   └── reports/
│
├── src/
│   ├── analytics.py
│   ├── download_data.py
│   ├── excel_report.py
│   ├── monte_carlo.py
│   ├── optimization.py
│   ├── portfolio.py
│   ├── run_analysis.py
│   ├── utils.py
│   └── visualization.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Future Enhancements

Planned future improvements include:

- Interactive Streamlit dashboard
- Portfolio strategy backtesting
- Portfolio rebalancing simulator
- Historical stress testing
- Portfolio comparison engine
- Performance attribution analysis
- Command-line interface (CLI)
- Configuration file support
- Enhanced logging and error handling

These enhancements are intended to improve usability, realism, and software engineering quality while remaining focused on practical portfolio analytics.

---

## Skills Demonstrated

This project demonstrates practical experience with:

### Finance

- Portfolio Analytics
- Modern Portfolio Theory
- Mean-Variance Optimization
- Efficient Frontier Analysis
- Monte Carlo Simulation
- Risk Measurement
- Performance Attribution

### Programming

- Python
- Object-Oriented Programming
- Data Analysis
- Scientific Computing
- Financial Data Processing
- Data Visualization
- Excel Automation
- Modular Software Design

---

## Author

**Ali Sayli**

Economics (Finance) & Political Science  
University of Toronto

This project was developed as part of my technical portfolio for investment analysis, portfolio management, capital markets, and financial analytics opportunities.

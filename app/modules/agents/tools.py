import yfinance
from agents import function_tool
from tavily import TavilyClient

from app.core.settings import settings

tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)


@function_tool
def search_web(query: str):
    """Search the web for the given query and return a summary of the results."""

    results = tavily_client.search(query, max_results=3)
    return results

@function_tool
def get_stock_info(ticker: str):
    """Get stock and financial information for a company using its stock ticker symbol.
    Example tickers: AAPL (Apple), GOOGL (Google), TSLA (Tesla), MSFT (Microsoft).
    Returns company profile, financial metrics, and current stock price."""

    stock = yfinance.Ticker(ticker)
    info = stock.info

    return {
        "company_name": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "country": info.get("country"),
        "website": info.get("website"),
        "summary": info.get("longBusinessSummary"),
        "current_price": info.get("currentPrice"),
        "currency": info.get("currency"),
        "market_cap": info.get("marketCap"),
        "revenue": info.get("totalRevenue"),
        "net_income": info.get("netIncomeToCommon"),
        "profit_margin": info.get("profitMargins"),
        "pe_ratio": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "eps": info.get("trailingEps"),
        "dividend_yield": info.get("dividendYield"),
        "52_week_high": info.get("fiftyTwoWeekHigh"),
        "52_week_low": info.get("fiftyTwoWeekLow"),
        "50_day_average": info.get("fiftyDayAverage"),
        "200_day_average": info.get("twoHundredDayAverage"),
        "total_employees": info.get("fullTimeEmployees"),
    }

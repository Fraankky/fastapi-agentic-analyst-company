# Guide: Improve ke Research Analyst Agent

Mengubah chatbot sederhana menjadi **Research Analyst Agent** dengan menambahkan tool `get_stock_info` menggunakan `yfinance`.

---

## Step 1: Tambah Dependency `yfinance`

```bash
uv add yfinance
```

---

## Step 2: Buat Tool `get_stock_info`

Edit file `app/modules/agents/tools.py`, tambahkan di bawah function `search_web`:

```python
import yfinance as yf


@function_tool
def get_stock_info(ticker: str):
    """Get stock and financial information for a company using its stock ticker symbol.
    Example tickers: AAPL (Apple), GOOGL (Google), TSLA (Tesla), MSFT (Microsoft).
    Returns company profile, financial metrics, and current stock price."""

    stock = yf.Ticker(ticker)
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
```

File lengkapnya akan jadi seperti ini:

```python
import yfinance as yf
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

    stock = yf.Ticker(ticker)
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
```

---

## Step 3: Register Tool ke Agent

Edit file `app/modules/chats/router.py`.

**Ubah import:**

```python
# Sebelum
from app.modules.agents.tools import search_web

# Sesudah
from app.modules.agents.tools import search_web, get_stock_info
```

**Ubah tools di Agent:**

```python
# Sebelum
agent = Agent(
    "Assistant",
    instructions=SYSTEM_PROMPT,
    model=llm_model,
    tools=[search_web],
)

# Sesudah
agent = Agent(
    "Assistant",
    instructions=SYSTEM_PROMPT,
    model=llm_model,
    tools=[search_web, get_stock_info],
)
```

---

## Step 4: Update System Prompt

Edit file `app/modules/agents/prompt.py`, ganti seluruh isinya:

```python
SYSTEM_PROMPT = """
You are a professional Research Analyst AI assistant specializing in company and stock market analysis.

You have access to the following tools:
- **search_web**: Search the internet for news, articles, and general information about companies
- **get_stock_info**: Get real-time stock data and financial metrics using a company's ticker symbol

<guidelines>
- When a user asks about a company, use BOTH tools to provide comprehensive analysis:
  1. Use `get_stock_info` with the company's ticker to get financial data
  2. Use `search_web` to find recent news and developments
- When asked specifically about stock prices or financial metrics, use `get_stock_info`
- When asked about news or general company info, use `search_web`
- Always structure your research response with clear sections:
  - Company Overview
  - Financial Metrics (price, market cap, P/E ratio, etc.)
  - Recent News & Developments
  - Summary/Key Takeaways
- Be thorough and analytical in your responses
- Present numbers in a readable format (e.g., $2.5T for market cap)
- Always mention the currency and that stock data may be delayed
</guidelines>
"""
```

---

## Step 5: Update Frontend (Optional)

Edit file `chat.html`, ubah bagian tool_call display agar lebih informatif.

Ganti bagian ini:

```javascript
} else if (json.type === "tool_call") {
  const el = document.createElement("span");
  el.className = "tool-call";
  el.textContent = `\n[tool: ${json.tool_name}]\n`;
  responseDiv.appendChild(el);
}
```

Menjadi:

```javascript
} else if (json.type === "tool_call") {
  const el = document.createElement("span");
  el.className = "tool-call";
  el.textContent = `\n[🔧 ${json.tool_name}(${json.argument})]\n`;
  responseDiv.appendChild(el);
}
```

---

## Step 6: Jalankan & Test

```bash
# Sync dependencies
uv sync

# Jalankan server
make dev
```

### Test Cases

Buka `chat.html` di browser, lalu coba:

1. **"Analisis perusahaan Apple"**
   → Agent akan pakai `get_stock_info("AAPL")` + `search_web("Apple company news")`

2. **"Berapa harga saham Tesla sekarang?"**
   → Agent akan pakai `get_stock_info("TSLA")`

3. **"Berita terbaru tentang Microsoft"**
   → Agent akan pakai `search_web("Microsoft latest news")`

4. **"Bandingkan GOOGL dan MSFT"**
   → Agent akan pakai `get_stock_info` dua kali + `search_web`

---

## Struktur File yang Berubah

```
app/
├── modules/
│   ├── agents/
│   │   ├── tools.py      ← tambah get_stock_info
│   │   └── prompt.py     ← update system prompt
│   └── chats/
│       └── router.py     ← register tool baru
├── chat.html              ← improve tool call display
└── pyproject.toml         ← tambah yfinance
```

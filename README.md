

# FinSight
LLM-Powered Stock Market Intelligence Platform.



## 🚀 Overview

FinSight simplifies financial research by integrating intelligent AI agents with live market data.

Instead of manually browsing financial reports and financial websites, users can simply ask questions like:

- *"Analyze Apple's financial health."*
- *"Compare NVIDIA and AMD fundamentals."*
- *"Show Tesla's latest analyst recommendations."*
- *"Summarize Microsoft's quarterly revenue growth."*

The AI agent retrieves relevant financial information, reasons over the data, and generates concise, human-readable insights.


## ✨ Features

### 📊 Real-Time Market Data

- Live stock price tracking
- Historical market data
- Company profiles
- Market capitalization
- Key valuation metrics

### 📈 Financial Analysis

- Income Statement
- Balance Sheet
- Cash Flow Statement
- Financial ratios
- Earnings analysis

### 🤖 AI-Powered Assistant

- Natural language financial queries
- Intelligent multi-step reasoning
- Company comparison
- Investment research assistance
- Context-aware conversations

### 📑 Market Intelligence

- Analyst recommendations
- Insider transactions
- Institutional holdings
- Dividend history
- Stock split history
- Company ticker lookup

### ⚡ Interactive Experience

- Real-time streaming AI responses
- Modern React-based interface
- FastAPI backend for high performance
- Responsive design across devices


## 🛠 Tech Stack

### Backend
- Python
- FastAPI
- LangChain
- LangGraph
- OpenAI GPT
- Yahoo Finance API

### Frontend
- React
- Vite
- Tailwind CSS

### AI & Data
- Large Language Models (LLMs)
- AI Agents
- Financial Data Processing

### Development Tools
- Git
- GitHub
- VS Code


## 🏗️ System Architecture

```text
                        +----------------------+
                        |        User          |
                        +----------+-----------+
                                   |
                                   v
                    +-----------------------------+
                    |      React Frontend         |
                    +-------------+---------------+
                                  |
                                  v
                    +-----------------------------+
                    |      FastAPI Backend        |
                    +-------------+---------------+
                                  |
                    +-------------+-------------+
                    |                           |
                    v                           v
          +------------------+      +----------------------+
          |   LangGraph AI   |      |   Financial Tools    |
          |      Agent        |      | (Yahoo Finance API) |
          +---------+---------+      +----------+----------+
                    |                           |
                    +-------------+-------------+
                                  |
                                  v
                        +----------------------+
                        |   OpenAI GPT Model   |
                        +----------+-----------+
                                   |
                                   v
                    +-----------------------------+
                    | AI-Powered Financial Insights|
                    +-----------------------------+
```



## Project Structure

```text
FinSight/
├── .agents/             # AI agent configurations
├── config/              # Configuration files
├── frontend/            # React frontend application
├── logs/                # Application logs
├── backend/       # Core AI workflows & business logic
├── .env                 # Environment variables (not committed)
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project configuration
├── package.json         # Frontend dependencies
├── render.yaml          # Deployment configuration
└── README.md
```


## AI Capabilities

FinSight provides AI-powered tools for stock market research and financial analysis, including:

- Stock price tracking
- Historical market data
- Company information
- Financial statements
- Balance Sheet analysis
- Income Statement analysis
- Cash Flow analysis
- Financial ratios
- Dividend history
- Stock split history
- Institutional holdings
- Insider transactions
- Analyst recommendations
- Company comparison
- Natural language financial queries
- Company ticker lookup


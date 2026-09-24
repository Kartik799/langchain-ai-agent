# LangChain AI Agent
A simple AI Agent built with **LangChain** to practice agents, tools, LLM integration, and external APIs.
## 🚀 Features
- LangChain ReAct Agent
- OpenRouter LLM integration
- Tavily web search
- WeatherStack weather tool
- Streamlit interface
- Custom LangChain tool
## 🛠️ Tech Stack
- Python
- LangChain
- OpenRouter
- Tavily
- WeatherStack
- Streamlit
## 🔄 Workflow
```text
User Query
    ↓
LangChain ReAct Agent
    ↓
Tools (Tavily / Weather)
    ↓
OpenRouter LLM
    ↓
Final Response
````

## 📁 Project Structure

```text
LangChain-AI-Agent/
├── research/
│   ├── app.py
│   └── main.py
├── .gitignore
├── README.md
└── requirements.txt
```

## ⚙️ Setup

Clone the repository:

```bash
git clone https://github.com/Kartik799/langchain-ai-agent.git
cd langchain-ai-agent
```

Create and activate a virtual environment:

```bash
python -m venv langagent
.\langagent\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add:

```env
OPENROUTER_API_KEY=your_api_key
Tavily_API_KEY=your_api_key
WEATHERSTACK_API_KEY=your_api_key
```

Run the Streamlit app:

```bash
streamlit run research/app.py
```

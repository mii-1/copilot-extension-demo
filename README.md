# Copilot Extension Demo (Graph/Power Platform Connector Mock)

This project demonstrates how a Copilot-style agent could answer domain-specific questions by fetching enterprise data (mock Graph/Power Platform connector) and synthesizing responses with an LLM.

## Goals
- Show ecosystem thinking: M365 Graph/Power Platform integration (mock)
- Demonstrate product thinking with a simple UX (Streamlit)
- Keep secrets safe via `.env`

## Stack
- Python 3.10+
- Streamlit
- OpenAI (or Azure OpenAI) via API
- dotenv

## Use Case
> Legal/ Sales teams ask: “When does the **Contoso** contract renew?”

The mock connector loads contracts; the app retrieves and summarizes the relevant one.

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env  # add your keys
streamlit run app.py


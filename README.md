AI Finance Assistant

An intelligent, multimodal finance assistant that allows users to ask questions about a company's stock and receive real-time data, news, document insights, and voice responses. Built with FastAPI (backend) and Streamlit (frontend), this project integrates multiple AI agents and natural language models.

Features

Component

Description

📈 Stock Data Agent

Fetches live stock prices and trading data using Yahoo Finance API.

📰 News Agent

Scrapes recent news headlines related to the company using web scraping.

📄 Document Agent

Extracts insights from SEC filings using sentence embeddings + retrieval.

🧠 Language Agent

Summarizes stock, news, and document data using a local LLM.

🎤 Voice Agent

Supports both speech-to-text input and voice output using TTS.

🌐 Multinational Support

Supports US and Indian stocks via ticker selection.

📊 Streamlit UI

Intuitive dashboard with charts, voice control, and dynamic summaries.

Architecture:
User ➝ Streamlit Frontend ➝ FastAPI Backend ➝ AI Agents
                                               │
                                               ├─ APIFinanceAgent (Stock Data)
                                               ├─ ScrapingAgent (News)
                                               ├─ RetrieverAgent (Document QA)
                                               ├─ LanguageAgent (LLM Summary)
                                               └─ VoiceAgent (Speech I/O)

Tech Stack

Backend: FastAPI

Frontend: Streamlit

AI/NLP: SentenceTransformers, LangChain-style modular agents

Speech: SpeechRecognition, pyttsx3

Data APIs: yFinance, Yahoo Finance Scraper

 File Structure:
finance_assistance/
├── agents/
│   ├── api_agent.py
│   ├── scraping_agent.py
│   ├── retriever_agent.py
│   ├── language_agent.py
│   └── voice_agent.py
├── orchestrator.py      
├── streamlit_app/
│   └── app.py           
├── docs_data/           
└── requirements.txt


Acknowledgements

Inspired by modular AI agent design (LangChain-style)

Uses open-source data via yFinance, Yahoo News

Built as part of a generative AI application project

 Project by: Mummidivarapu Sri Sai Nikshith | Built with ❤️ using AI tools

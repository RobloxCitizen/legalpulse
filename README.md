# LegalPulse

LegalPulse is a Streamlit-based application designed to provide legal information from Belarusian sources, specifically pravo.by and president.gov.by. It allows users to query legal documents and news, leveraging a Retrieval-Augmented Generation (RAG) pipeline for accurate responses. The app is built as a template that works out-of-the-box with placeholder data and supports integration with DeepSearch (via xAI API) or OpenAI API for advanced search capabilities when API keys are provided.

## Features
- Search Legal Documents: Retrieves legal news and presidential decrees from pravo.by and president.gov.by.
- RAG Pipeline: Uses embeddings and a vector store to find relevant documents and generate precise answers.
- Placeholder Mode: Operates without API keys using mock data (e.g., "Decree No. 196" and "Amnesty Bill 2025").
- DeepSearch Integration: Supports xAI's DeepSearch or OpenAI for enhanced search when API keys are added to .env.
- User-Friendly Interface: Simple Streamlit UI with no manual API key input required.
- Rate Limiting: Limits queries to 80 per 3 hours for fair usage.

## Setup
1. Clone the Repository:
   ```bash
   git clone https://github.com/your-repo/legalpulse.git
   cd legalpulse

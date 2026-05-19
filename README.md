# 🛍️ Smart E-Commerce AI Support Agent

## Project Overview
This project is an **Autonomous Agentic AI Support System** designed to bridge the gap between static FAQ documents and active user assistance. Built as a Capstone Project for the **Boston Institute of Analytics (BIA)**, this assistant uses an LLM brain to read data live, make real-time analytical decisions, and execute programmatic backend tools.

---

## 🚀 Core Features & Architecture

### 1. Retrieval-Augmented Generation (RAG)
Instead of relying on static training data, the agent reads local knowledge bases live to answer user queries with 100% precision:
- `Products.json`: Live database for stock availability, pricing, and product descriptions.
- `Policies.md`: Contextual store rules covering shipping updates, returns, and exchanges.

### 2. Agentic Tool Execution (Function Calling)
The AI agent autonomously decides when to run Python code. It connects to the following mock tools:
- `get_order_status`: Searches tracking systems for delivery details.
- `create_return_request`: Validates and initiates a product return flow.

### 3. Safety Guardrails & Human Escalation
If a user submits an out-of-scope prompt, tries to bypass system instructions, or uses abusive language, the agent automatically intercepts the text and invokes a fallback mechanism to route the customer seamlessly to a live human agent.

---

## 🛠️ Tech Stack
- **Backend Framework:** Python 3.9+
- **AI Core:** Google Gemini 2.5 Flash (`google-genai` SDK)
- **User Interface:** Streamlit (Web-based application)

---

## 💻 How to Setup and Run This Project

Follow these steps to deploy and run the interface locally:

### 1. Install Dependencies
Ensure you have Python installed, then install the required libraries:
```bash
pip install streamlit google-genai

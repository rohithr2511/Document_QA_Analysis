# 💼 Financial Document Q&A Assistant

## 📖 Overview
The **Financial Document Q&A Assistant** is a Streamlit-based application that helps users **upload financial documents (PDF or Excel)**, automatically extract key information, and ask **questions about the data**.  

The app uses:
- **PyPDF2** → Extract text from PDF documents  
- **Pandas** → Handle Excel data  
- **Regex** → Detect common financial metrics (revenue, expenses, profit, etc.)  
- **Ollama (LLaMA2)** → Answer natural language questions based on extracted data  

---

## ⚙️ Features
- Upload **PDF** or **Excel** financial documents  
- Automatic extraction of text or tabular data  
- Detection of key metrics like **Revenue, Expenses, Profit, Assets, Liabilities**  
- Ask **natural language questions** about your data with **Ollama-powered Q&A**  
- View full conversation history  

---

## 📂 Repository Structure
document/
├── trail.py # Main Streamlit application
├── venv/ # Virtual environment (not recommended for GitHub)

---
## create a environment
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows

---
## Install dependencies
pip install -r requirements.txt

---

## Run the Streamlit app:
streamlit run trail.py

---

##Insights

Detects and displays core financial metrics (Revenue, Expenses, Profit, Assets, Liabilities).

Provides an interactive Q&A system for financial data exploration.

Can be extended with additional regex patterns or new LLM models for deeper analysis.

import streamlit as st
import pandas as pd
import PyPDF2
import re
import tempfile
import os
from typing import Dict, List, Any
import json

# Ollama configuration
try:
    import ollama
except ImportError:
    st.warning("Ollama package not found. Please install it with: pip install ollama")

class FinancialDocumentProcessor:
    """Process financial documents (PDF and Excel) and extract data"""
    
    def __init__(self):
        self.extracted_data = {}
        
    def process_excel(self, file) -> Dict[str, Any]:
        """Extract data from Excel files"""
        try:
            df = pd.read_excel(file)
            # Converting DataFrame to a readable string format
            data_str = df.to_string()
            self.extracted_data['excel_data'] = data_str
            return {"success": True, "data": data_str}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def process_pdf(self, file) -> Dict[str, Any]:
        """Extract text from PDF files"""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            self.extracted_data['pdf_text'] = text
            return {"success": True, "data": text}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def extract_financial_metrics(self, text: str) -> Dict[str, str]:
        """Extract common financial metrics from text"""
        metrics = {}
        
        # Patterns for common financial metrics
        patterns = {
            'revenue': r'revenue\s*[:$]?\s*[\$]?(\d+(?:,\d+)*(?:\.\d+)?)',
            'expenses': r'expenses?\s*[:$]?\s*[\$]?(\d+(?:,\d+)*(?:\.\d+)?)',
            'profit': r'profit\s*[:$]?\s*[\$]?(\d+(?:,\d+)*(?:\.\d+)?)',
            'net_income': r'net income\s*[:$]?\s*[\$]?(\d+(?:,\d+)*(?:\.\d+)?)',
            'gross_profit': r'gross profit\s*[:$]?\s*[\$]?(\d+(?:,\d+)*(?:\.\d+)?)',
            'assets': r'assets\s*[:$]?\s*[\$]?(\d+(?:,\d+)*(?:\.\d+)?)',
            'liabilities': r'liabilities?\s*[:$]?\s*[\$]?(\d+(?:,\d+)*(?:\.\d+)?)',
            'equity': r'equity\s*[:$]?\s*[\$]?(\d+(?:,\d+)*(?:\.\d+)?)',
        }
        
        for metric, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                metrics[metric] = match.group(1)
        
        return metrics

class FinancialQASystem:
    """Question-answering system for financial data"""
    
    def __init__(self):
        self.conversation_history = []
    
    def ask_question(self, question: str, context: str) -> str:
        """Use Ollama to answer questions based on the provided context"""
        try:
            # Prompt with context and question
            prompt = f"""
            Based on the following financial data:
            {context}
            
            Answer this question: {question}
            
            Provide a concise and accurate response. If the information is not available in the data, say so.
            """
            
            # Calling Ollama
            response = ollama.chat(model='llama2', messages=[{'role': 'user', 'content': prompt}])
            answer = response['message']['content']
            
            # Store conversation history
            self.conversation_history.append({"question": question, "answer": answer})
            
            return answer
        except Exception as e:
            return f"Error processing question: {str(e)}. Please ensure Ollama is installed and running."

def main():
    st.set_page_config(page_title="Financial Document Q&A Assistant", page_icon="💼")
    st.title("Financial Document Q&A Assistant")
    st.write("Upload financial documents (PDF or Excel) and ask questions about the data.")
    
    # Initialize session state
    if 'processor' not in st.session_state:
        st.session_state.processor = FinancialDocumentProcessor()
    if 'qa_system' not in st.session_state:
        st.session_state.qa_system = FinancialQASystem()
    if 'processed' not in st.session_state:
        st.session_state.processed = False
    if 'extracted_text' not in st.session_state:
        st.session_state.extracted_text = ""
    
    # File upload section
    uploaded_file = st.file_uploader("Choose a financial document", type=['pdf', 'xlsx', 'xls'])
    
    if uploaded_file is not None:
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
        st.write(file_details)
        
        # Processing the file based on type
        if uploaded_file.type == "application/pdf":
            result = st.session_state.processor.process_pdf(uploaded_file)
            if result["success"]:
                st.session_state.extracted_text = result["data"]
                st.session_state.processed = True
            else:
                st.error(f"Error processing PDF: {result['error']}")
                
        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
            result = st.session_state.processor.process_excel(uploaded_file)
            if result["success"]:
                st.session_state.extracted_text = result["data"]
                st.session_state.processed = True
            else:
                st.error(f"Error processing Excel: {result['error']}")
        
        # Display extracted data if processing was successful
        if st.session_state.processed:
            st.subheader("Extracted Data Preview")
            st.text_area("Document Content", st.session_state.extracted_text, height=200)
            
            # Extracting and displaying financial metrics
            metrics = st.session_state.processor.extract_financial_metrics(st.session_state.extracted_text)
            if metrics:
                st.subheader("Detected Financial Metrics")
                for metric, value in metrics.items():
                    st.write(f"{metric.replace('_', ' ').title()}: ${value}")
            
            # Question-answering section
            st.subheader("Ask Questions About the Financial Data")
            question = st.text_input("Enter your question:")
            
            if question:
                with st.spinner("Thinking..."):
                    answer = st.session_state.qa_system.ask_question(
                        question, st.session_state.extracted_text
                    )
                    st.write("**Answer:**", answer)
            
            # Displaying conversation history
            if st.session_state.qa_system.conversation_history:
                st.subheader("Conversation History")
                for i, exchange in enumerate(st.session_state.qa_system.conversation_history):
                    st.write(f"**Q{i+1}:** {exchange['question']}")
                    st.write(f"**A{i+1}:** {exchange['answer']}")
                    st.write("---")
    else:
        st.info("Please upload a financial document to get started.")

if __name__ == "__main__":
    main()

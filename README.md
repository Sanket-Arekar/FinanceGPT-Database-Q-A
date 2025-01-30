# FinanceGPT-Database-Q&A

## Overview
FinanceGPT-Database-Q&A is an AI-powered tool designed to perform natural language question answering over MySQL databases. It enables financial analysts and professionals to extract meaningful insights from structured financial data using conversational AI. This project integrates LangChain with OpenAI's language models and Chroma DB for vector storage to enhance SQL query generation and retrieval.

---

## Features

- **Natural Language Query Processing**: Converts user queries into MySQL queries and executes them.
- **Few-Shot Learning**: Utilizes example-based learning to improve SQL generation.
- **Vector Storage with Chroma DB**: Stores embeddings for efficient retrieval.
- **Financial Insights Extraction**: Retrieves key financial data, such as revenue trends, expense analysis, and product performance.
- **Interactive Streamlit Interface**: User-friendly UI for entering queries and viewing results.

---

## Architecture

### 1. **User Input**
   - Users input financial questions via the Streamlit web interface.
   
### 2. **Query Processing**
   - The question is processed by LangChain's SQL generation pipeline.
   - A few-shot learning approach improves accuracy by leveraging example queries.

### 3. **Database Interaction**
   - SQL queries are executed against a MySQL database containing financial records.
   - The SQLDatabaseChain module from LangChain handles structured data interactions.

### 4. **Vector Storage**
   - Chroma DB stores embeddings of past queries and their results for similarity-based retrieval.
   - HuggingFace Embeddings are used for text-to-vector conversion.

### 5. **Answer Generation**
   - Query results are processed and formatted into a natural language response.
   - The response is displayed to the user via Streamlit.

---

## Technologies Used
![image](https://github.com/user-attachments/assets/2fed7b39-f8cb-45bd-ab3d-5b4bff9831f9) ![image](https://github.com/user-attachments/assets/0c2e484a-6ebf-4c75-9313-ef8db4a65f21) ![image](https://github.com/user-attachments/assets/13ddc582-08f1-46bb-8fd0-39bf4c1fa2ef) ![image](https://github.com/user-attachments/assets/7d0dc970-7a45-4647-8b7f-8016c143f9f2) 




- **Programming Language**: Python
- **LLM Framework**: LangChain
- **Database**: MySQL
- **Vector Database**: Chroma DB
- **Embeddings**: HuggingFace Embeddings
- **Frontend**: Streamlit
- **Environment Management**: dotenv
- **Other Libraries**: OpenAI, pymysql, sentence-transformers

---

## Installation

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd FinanceGPT-Database-Q-A
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables:**
   - Add your OpenAI API key in `.env`:
     ```env
     OPENAI_API_KEY='your_openai_api_key'
     ```

4. **Run the Application:**
   ```bash
   streamlit run main.py
   ```

---

## Usage Examples

### Example 1: Retrieve Top Revenue-Generating Product
1. Enter the question:
   ```
   What is the top-performing product category in 2023?
   ```
2. System generates an SQL query:
   ```sql
   SELECT r.product_category, SUM(r.revenue_amount) - COALESCE(SUM(e.expense_amount), 0) AS net_revenue
   FROM revenue r LEFT JOIN expenses e ON r.product_category = e.expense_type
   AND YEAR(r.revenue_date) = YEAR(e.expense_date) WHERE YEAR(r.revenue_date) = 2023
   GROUP BY r.product_category
   ORDER BY net_revenue DESC
   LIMIT 1;
   ```
3. Displays the result in natural language format.

### Example 2: Monthly Expense Breakdown
1. Enter the question:
   ```
   What are the top 3 expense categories by total amount for each month in 2023?
   ```
2. System retrieves and ranks expense data for each month.

---

## Screenshots

### 1. Home Page
![image](https://github.com/user-attachments/assets/55c42686-2558-4be4-9188-0eebccbc340e)

### 2. Query Input/Output

### Input
![image](https://github.com/user-attachments/assets/ecbf13e4-69a0-4a37-a2bc-4f67d3436c10)
### Internal Query generation of the LLM
![Screenshot (496)](https://github.com/user-attachments/assets/ae818b11-b21a-4ae5-ba80-661a8757ddc3)

### Input
![image](https://github.com/user-attachments/assets/e4379ba4-8c62-4d00-9162-02930f2b2d9a)
### Internal Query generation of the LLM
![Screenshot (498)](https://github.com/user-attachments/assets/746f434c-38c1-4e90-b536-d74d3c9c3756)

---

## Future Enhancements

- **Support for Additional Databases**: PostgreSQL, MongoDB, etc.
- **More Advanced Query Optimization**: Using contextual learning.
- **Financial Forecasting Features**: AI-based revenue prediction.

---

## Contributing

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Submit a pull request.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.


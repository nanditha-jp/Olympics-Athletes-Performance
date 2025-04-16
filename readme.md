# 🏅 Olympic Athlete Performance Analysis Dashboard

An interactive Streamlit dashboard that enables exploration and analysis of Olympic athlete performance across countries, sports, and years. The application combines data visualization with natural language Q&A powered by a Large Language Model (LLM) for intuitive data exploration.

---

## ✨ Main Features

| | Feature | Description |
|--|---------|-------------|
| 🤖 | **LLM-Powered Q&A Assistant** | Ask natural language questions and get answers derived from Olympic athlete data. |
| 📊 | **Interactive Visual Analytics** | Dynamic visualizations using Plotly and Streamlit for performance trends, medal counts, and more. |
| 🔥 | **Modular Code Architecture** | Scalable project layout with reusable components for data processing and visualization. |

---

## 🧠 Technologies Used

- **Python**
- **Streamlit**
- **Pandas, NumPy**
- **Plotly**
- **Groq API / (LLM integration for Q&A)**
- **BeautifulSoup / Requests** – for data scraping

---

## 📄 Data Source

The dataset is scraped from [Olympedia](https://www.olympedia.org/athletes/), an open database of Olympic athlete data.

---

## 🗂️ Project Architecture
![Architecture](assets/architecture.svg)

---

## ⚙️ How to Run Locally

1. **Clone the repo**  
   ```bash
   git clone https://github.com/pxxthik/Olympics-Athletes-Performance.git
   cd Olympics-Athletes-Performance
   ```

2. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

3. Run the Streamlit app
    ```bash
    streamlit run app.py
    ```

---

## 📌 Disclaimer

This project is for educational and analytical purposes, using data scraped from https://www.olympedia.org/athletes/.

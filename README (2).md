# 🛍️ CustomerLens — E-Commerce Customer Segmentation & Revenue Intelligence

> End-to-end data science project that segments 99K+ customers using RFM Analysis & K-Means Clustering, predicts Customer Lifetime Value, and delivers insights via interactive dashboards.

---

## 📊 Live Dashboards
| Dashboard | Link |
|---|---|
| 🚀 Streamlit App | [Add your Streamlit link here] |
| 📊 Tableau Public | [Add your Tableau Public link here] |

---

## 🎯 Business Problem
E-commerce businesses struggle to identify which customers are most valuable, at risk of leaving, or likely to generate future revenue. This project answers:
- **Who are our best customers?**
- **Which customers are about to churn?**
- **How much is each customer worth in the future?**

---

## 🔍 Key Results
- Identified **5 distinct customer segments** from 99,441 customers
- Top **18% of customers (Champions)** contribute **70%+ of total revenue**
- CLV prediction model reveals high-value segments for targeted retention
- Interactive dashboard enabling real-time segment filtering for business teams

---

## 🏗️ Project Architecture
```
Raw Data (MySQL)
      ↓
Data Extraction (SQL Joins)
      ↓
EDA & Data Cleaning (Pandas)
      ↓
RFM Feature Engineering
      ↓
K-Means Clustering (Elbow + Silhouette)
      ↓
CLV Prediction (Random Forest)
      ↓
Streamlit Dashboard + Tableau Dashboard
```

---

## 🛠️ Tech Stack
| Category | Tools |
|---|---|
| Language | Python 3.x |
| Database | MySQL, MySQL Workbench |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn (K-Means, Random Forest) |
| Visualization | Plotly, Seaborn, Matplotlib |
| Dashboard | Streamlit, Tableau Public |
| Environment | VS Code |

---

## 📁 Project Structure
```
CustomerLens/
├── data/
│   ├── raw_data.csv               # Extracted from MySQL
│   ├── rfm_data.csv               # RFM engineered features
│   ├── clustered_data.csv         # K-Means cluster results
│   ├── final_data.csv             # Final dataset with CLV
│   ├── elbow_plot.png             # Elbow method chart
│   └── silhouette_plot.png        # Silhouette score chart
├── notebooks/
│   ├── 01_EDA.py                  # Exploratory Data Analysis
│   ├── 02_RFM.py                  # RFM Feature Engineering
│   ├── 03_clustering.py           # K-Means Clustering
│   └── 04_CLV.py                  # CLV Prediction Model
├── sql/
│   └── extract_data.sql           # SQL extraction query
├── app.py                         # Streamlit Dashboard
├── load_data.py                   # MySQL data loader
└── requirements.txt               # Dependencies
```

---

## 📦 Dataset
**Brazilian E-Commerce Public Dataset by Olist**
- Source: [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- 99,441 orders from 2016–2018
- Tables used: customers, orders, order_items, payments

---

## ⚙️ How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/CustomerLens.git
cd CustomerLens
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup MySQL
- Create database `customerlens` in MySQL Workbench
- Run `sql/extract_data.sql` to create tables
- Run `load_data.py` to load CSV data into MySQL

```bash
python load_data.py
```

### 4. Run notebooks in order
```bash
python notebooks/01_EDA.py
python notebooks/02_RFM.py
python notebooks/03_clustering.py
python notebooks/04_CLV.py
```

### 5. Launch Streamlit dashboard
```bash
streamlit run app.py
```

---

## 🔬 Methodology

### RFM Analysis
| Metric | Description |
|---|---|
| **Recency** | Days since last purchase |
| **Frequency** | Total number of orders |
| **Monetary** | Total amount spent |

### Customer Segments
| Segment | Description |
|---|---|
| 🏆 Champions | Bought recently, buy often, spend the most |
| 💛 Loyal Customers | Buy regularly with good spend |
| ⚠️ At Risk | Used to buy often but haven't recently |
| 😴 Hibernating | Low recency, frequency and monetary |
| ❌ Lost | Lowest scores across all RFM metrics |

### K-Means Clustering
- Optimal K selected using **Elbow Method** + **Silhouette Score**
- Features scaled using **StandardScaler**
- 3D RFM scatter plot for visual validation

### CLV Prediction
- Target: `Monetary × log(1 + Frequency)`
- Model: **Random Forest Regressor**
- Evaluated using MAE and R² score

---

## 📈 Streamlit Dashboard Features
- 📊 KPI metrics (Total Customers, Revenue, Avg CLV, Segments)
- 🔍 Real-time segment filter (sidebar)
- 💰 Revenue by segment (bar chart)
- 📈 Revenue share (pie chart)
- 🎯 RFM scatter plot
- 📦 CLV by segment
- 🔁 Purchase frequency analysis
- 📋 Raw data viewer

---

## 📊 Tableau Dashboard Features
- Revenue by segment (bar chart)
- Customer count treemap
- CLV distribution by segment
- Recency vs Monetary scatter
- Drill-through filters by segment/state/city

---

## 📋 Requirements
```
pandas
numpy
matplotlib
seaborn
plotly
scikit-learn
streamlit
mysql-connector-python
```

---

## 👤 Author
**Your Name**
- LinkedIn: [your linkedin]
- GitHub: [your github]
- Email: [your email]

---

## 📄 License
MIT License — free to use for learning and portfolio purposes.

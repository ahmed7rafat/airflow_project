# Airflow Project – Sales Data Pipeline  

This project is a simple ETL pipeline using **Apache Airflow**.  
It extracts sales data from a PostgreSQL database, processes it with Pandas, and generates a daily revenue **Time Series Line Plot**.  

---

## 📂 Project Files  
- `airflow_project.py` → Airflow DAG (main workflow)  
- `daily_sales_data.csv` → extracted sales data  
- `daily_revenue.csv` → calculated revenue  
- `daily_revenue_plot.png` → revenue time series line plot  

---

## ⚙️ Workflow  
1. Extract sales data from PostgreSQL (via Airflow PostgresHook) → save as CSV.  
2. Transform with Pandas → calculate daily revenue.  
3. Save the processed revenue data → `daily_revenue.csv`.  
4. Visualize revenue with a **time series line plot** → `daily_revenue_plot.png`.  

---

## 🛠️ Technologies  
- Apache Airflow  
- PostgreSQL  
- Pandas  
- Matplotlib  

---

## 🚀 Usage  
1. Clone the repo:  
   ```bash
   git clone https://github.com/ahmed7rafat/airflow_project.git

2. Place `airflow_project.py` inside your Airflow `dags/` folder.  
3. Run Airflow and trigger the DAG to generate the output files (CSV + plot).

---

## 📌 Notes  
- Database connection (PostgreSQL) is not included — update with your own DB details in the DAG.
   

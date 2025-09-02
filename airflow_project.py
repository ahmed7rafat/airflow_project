from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.hooks.postgres_hook import PostgresHook
from datetime import timedelta
import pandas as pd
import matplotlib.pyplot as plt

PG_CONN_ID = 'postgres_conn'

default_args = {
    'owner': 'kiwilytics',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}


# Task 1: Fetch order data including prices from products
def fetch_order_data():
    # Connect to PostgreSQL using Airflow connection
    hook = PostgresHook(postgres_conn_id=PG_CONN_ID)
    conn = hook.get_conn()


    query = """
    SELECT
        o.OrderDate::date AS sale_date,
        od.ProductID,
        p.ProductName,
        od.Quantity,
        p.Price
    FROM orders o
    JOIN order_details od ON o.OrderID = od.OrderID
    JOIN products p ON od.ProductID = p.ProductID
    """
    
    # Read query result into pandas DataFrame
    df = pd.read_sql(query, conn)
    
    # Save result as CSV for next tasks
    df.to_csv('/home/kiwilytics/airflow_output/daily_sales_data.csv', index=False)




    # Task 2: Process total daily revenue
def process_daily_revenue():
    
    df = pd.read_csv('/home/kiwilytics/airflow_output/daily_sales_data.csv')
    
    # Calculate revenue per row
    df['total_revenue'] = df['quantity'] * df['price']

    # Aggregate revenue per day
    revenue_per_day = df.groupby('sale_date').agg(total_revenue=('total_revenue', 'sum')).reset_index()
    
    # Save aggregated result
    revenue_per_day.to_csv('/home/kiwilytics/airflow_output/daily_revenue.csv', index=False)



# Task 3: Plot daily revenue
def plot_daily_revenue():
    # Load the daily revenue data from Task 2
    df = pd.read_csv('/home/kiwilytics/airflow_output/daily_revenue.csv')
    df['sale_date'] = pd.to_datetime(df['sale_date'])  # Convert date column to datetime format

    # Create a line chart of revenue per day
    plt.figure(figsize=(12, 6))
    plt.plot(df['sale_date'], df['total_revenue'], marker='o', linestyle='-')
    plt.title("Daily Total Sales Revenue")
    plt.xlabel("Date")
    plt.ylabel("Total Revenue")
    plt.xticks(rotation=45)  # Rotate x-axis labels for readability
    plt.grid(True)
    plt.tight_layout()

    # Save the chart as PNG image
    output_path = '/home/kiwilytics/airflow_output/daily_revenue_plot.png'
    plt.savefig(output_path)
    print(f"Revenue chart saved to {output_path}")



# Define the DAG
with DAG(
    dag_id='daily_sales_revenue_analysis',   
    default_args=default_args,           
    start_date=days_ago(1),                  
    schedule_interval='@daily',          
    catchup=False,                           # Do not backfill for past dates
    description='Compute and visualize daily revenue using Pandas and Matplotlib in Airflow',
) as dag:

    # Task to fetch raw order data from Postgres
    task_fetch_data = PythonOperator(
        task_id='fetch_order_data',
        python_callable=fetch_order_data,
    )

    # Task to process daily revenue
    task_process_revenue = PythonOperator(
        task_id='process_daily_revenue',
        python_callable=process_daily_revenue,
    )

    # Task to plot daily revenue
    task_plot_revenue = PythonOperator(
        task_id='plot_daily_revenue',
        python_callable=plot_daily_revenue,
    )

    # Define task dependencies (order of execution)
    task_fetch_data >> task_process_revenue >> task_plot_revenue

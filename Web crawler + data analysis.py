import urllib.request
import io
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# ==========================================
# 0. Global Settings
# ==========================================
plt.style.use('seaborn-v0_8-whitegrid')

# ==========================================
# 1. REAL Data Acquisition from the Internet
# ==========================================
def get_real_employment_data():
    print(">>> Connecting to real data source (FiveThirtyEight GitHub Repository)...")
    
    # This is a real, live URL containing actual graduate employment data
    real_url = "https://raw.githubusercontent.com/fivethirtyeight/data/master/college-majors/recent-grads.csv"
    
    try:
        # Using urllib instead of requests to bypass Python 3.13 crash
        response = urllib.request.urlopen(real_url)
        # Read and decode the real data
        real_csv_data = response.read().decode('utf-8')
        print(">>> Successfully downloaded real data from the internet!")
        
        # Load the real data into Pandas
        df = pd.read_csv(io.StringIO(real_csv_data))
        
        # Clean the real data (Drop rows with missing salary or employment info)
        df = df.dropna(subset=['Median', 'Unemployment_rate', 'Total'])
        
        # Rename columns to match our project perfectly
        df = df.rename(columns={
            'Major': 'Major',
            'Major_category': 'Industry',
            'Median': 'Avg_Salary', # This is actual median salary in USD
            'Unemployment_rate': 'Unemployment_Rate'
        })
        
        # Calculate Real Employment Rate (100 - Unemployment Rate)
        df['Employment_Rate'] = 100 - (df['Unemployment_Rate'] * 100)
        
        # Keep only the columns we need for the report
        df_final = df[['Major', 'Industry', 'Avg_Salary', 'Employment_Rate']].copy()
        
        print(f">>> Data processing complete. Loaded {len(df_final)} real majors.")
        return df_final

    except Exception as e:
        print(f">>> Network Error: {e}")
        print(">>> Please check your internet connection and run again.")
        return None

# ==========================================
# 2. Data Processing & Saving
# ==========================================
def process_data(df):
    print("\n>>> Saving real data to CSV...")
    df.to_csv('real_graduates_data.csv', index=False, encoding='utf-8-sig')
    print(">>> Saved as 'real_graduates_data.csv'")
    return df

# ==========================================
# 3. Data Analysis & Visualization
# ==========================================
def visualize_data(df):
    print("\n>>> Generating professional charts from real data...")
    
    # --- Chart 1: Top 15 Highest-Paying Majors (Real Data) ---
    df_top = df.sort_values(by='Avg_Salary', ascending=True).tail(15)
    plt.figure(figsize=(12, 8))
    bars = plt.barh(df_top['Major'], df_top['Avg_Salary'], color=plt.cm.viridis(df_top['Avg_Salary'] / df_top['Avg_Salary'].max()))
    plt.xlabel('Real Median Salary (USD)', fontsize=12)
    plt.title('Chart 1: Top 15 Real Majors by Median Salary', fontsize=14, fontweight='bold')
    for bar in bars:
        plt.text(bar.get_width() + 200, bar.get_y() + bar.get_height()/2, f"${int(bar.get_width())}", va='center', fontsize=9)
    plt.tight_layout()
    plt.savefig('chart1_real_top_salary.png', dpi=150)

    # --- Chart 2: Average Salary by Industry Category (Real Data) ---
    # Grouping real data by Industry (e.g., Engineering, Arts, Business)
    industry_salary = df.groupby('Industry')['Avg_Salary'].mean().sort_values(ascending=True).tail(10)
    plt.figure(figsize=(12, 7))
    bars = plt.barh(industry_salary.index, industry_salary.values, color='#4C72B0', edgecolor='black')
    plt.xlabel('Average Median Salary (USD)', fontsize=12)
    plt.title('Chart 2: Real Salary Comparison by Industry Category', fontsize=14, fontweight='bold')
    for bar in bars:
        plt.text(bar.get_width() + 200, bar.get_y() + bar.get_height()/2, f"${int(bar.get_width())}", va='center', fontsize=9)
    plt.tight_layout()
    plt.savefig('chart2_real_industry_salary.png', dpi=150)

    # --- Chart 3: Distribution of Majors by Industry (Real Data) ---
    industry_counts = df['Industry'].value_counts().head(8)
    plt.figure(figsize=(9, 9))
    plt.pie(industry_counts, labels=industry_counts.index, autopct='%1.1f%%', startangle=140, 
            colors=plt.cm.Set3.colors, textprops={'fontsize': 9})
    plt.title('Chart 3: Distribution of Real Majors by Industry', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('chart3_real_industry_pie.png', dpi=150)

    # --- Chart 4: The Real "Golden Major" Matrix ---
    avg_salary = df['Avg_Salary'].mean()
    avg_rate = df['Employment_Rate'].mean()
    
    plt.figure(figsize=(13, 8))
    scatter = plt.scatter(df['Employment_Rate'], df['Avg_Salary'], s=80, c=df['Avg_Salary'], cmap='plasma', edgecolors='black', alpha=0.8)
    
    # Only label top outliers to keep the chart clean
    for i, row in df.nlargest(10, 'Avg_Salary').iterrows():
        plt.text(row['Employment_Rate'] + 0.1, row['Avg_Salary'] + 500, row['Major'], fontsize=8, fontweight='bold', color='red')
        
    plt.axhline(y=avg_salary, color='blue', linestyle='--', linewidth=1.5, label=f'Avg Salary (${avg_salary:.0f})')
    plt.axvline(x=avg_rate, color='green', linestyle='--', linewidth=1.5, label=f'Avg Emp Rate ({avg_rate:.1f}%)')
    
    plt.colorbar(scatter, label='Salary Level (Color)')
    plt.xlabel('Real Employment Rate (%)', fontsize=12)
    plt.ylabel('Real Median Salary (USD)', fontsize=12)
    plt.title('Chart 4: Real "Golden Major" Matrix Analysis', fontsize=13, fontweight='bold')
    plt.legend(loc='lower right', fontsize=10)
    plt.tight_layout()
    plt.savefig('chart4_real_golden_matrix.png', dpi=150)
    
    print(">>> 4 real-data charts generated successfully!")

# ==========================================
# 4. Real Database Management (SQLite)
# ==========================================
def database_management(df):
    print("\n>>> Starting Database Management with REAL data...")
    conn = sqlite3.connect('real_graduates.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS real_salary_data (id INTEGER PRIMARY KEY AUTOINCREMENT, major TEXT, industry TEXT, salary REAL, rate REAL)''')
    
    print("\n[CREATE] Inserting real data into database...")
    # Clear old data if any
    cursor.execute('DELETE FROM real_salary_data')
    for index, row in df.iterrows():
        cursor.execute('INSERT INTO real_salary_data (major, industry, salary, rate) VALUES (?, ?, ?, ?)',
                       (row['Major'], row['Industry'], row['Avg_Salary'], row['Employment_Rate']))
    conn.commit()
    
    print("\n[READ] Querying real high-paying Engineering majors:")
    cursor.execute('SELECT major, salary FROM real_salary_data WHERE industry LIKE "%Engineering%" AND salary > 60000 ORDER BY salary DESC LIMIT 5')
    for row in cursor.fetchall():
        print(f" - {row[0]}: ${row[1]}")
        
    print("\n[UPDATE] Simulating inflation: Adding 5% to all salaries...")
    cursor.execute('UPDATE real_salary_data SET salary = salary * 1.05')
    conn.commit()

    print("\n[DELETE] Deleting a dummy entry to demonstrate DELETE operation...")
    cursor.execute('INSERT INTO real_salary_data (major, industry, salary, rate) VALUES (?, ?, ?, ?)', ('Dummy', 'None', 0, 0))
    cursor.execute('DELETE FROM real_salary_data WHERE major = "Dummy"')
    conn.commit()

    conn.close()
    print("\n>>> Real Database CRUD completed.")

# ==========================================
# Main Execution
# ==========================================
if __name__ == "__main__":
    # Step 1: Get REAL data
    df_real = get_real_employment_data()
    
    # Only proceed if the internet connection worked
    if df_real is not None:
        print("\n[Real Data Preview - First 5 Rows]")
        print(df_real.head())
        
        df_processed = process_data(df_real)
        visualize_data(df_processed)
        database_management(df_processed)
        
        print("\n" + "="*60)
        print("SUCCESS! You just processed REAL international data.")
        print("Check your folder for the real CSV, PNG charts, and DB file.")
        print("="*60)
    else:
        print("\nProgram stopped. Please connect to the internet and try again.")

🎓 Graduate Employment & Salary Data Analysis
Python VersionStatusDB

A robust, end-to-end Python data pipeline designed to acquire, clean, analyze, and visualize real-world employment statistics for college graduates. The core objective of this project is to identify "Golden Majors" — academic fields that offer the perfect balance of high financial returns and strong job security.

🔄 Project Pipeline
🌐 Data Acquisition ➡️ 🧹 Data Cleaning ➡️ 📈 Data Visualization ➡️ 🗄️ Database Management

📸 Key Visualizations
The script generates 4 distinct, high-quality charts to uncover hidden economic trends:

1. Top 15 Highest-Paying Majors
A horizontal bar chart revealing the steep financial hierarchy among top-tier majors, led by Petroleum Engineering.Top 15 Salaries

2. Industry Category Macro Comparison
Grouping majors into broader sectors to observe macro-economic trends (e.g., Engineering vs. Business vs. Arts).Industry Salary

3. Labor Supply Distribution
A pie chart illustrating the proportion of graduates produced by each field, revealing potential oversupply issues in certain sectors.Labor Distribution

4. The "Golden Major" Matrix (Core Analysis)
A scatter plot mapping Employment Rate (X-axis) against Median Salary (Y-axis) to classify majors into risk/reward quadrants.Golden Matrix

🛠️ Tech Stack
Category	Technology	Purpose
Language	Python 3.13	Core programming environment
Data Fetching	urllib.request	Bypassed Python 3.13 requests crash using built-in libs
Data Processing	pandas, io	Data cleaning, NaN handling, and memory-stream parsing
Visualization	matplotlib	Professional chart generation with seaborn styling
Database	sqlite3	Localized DB implementation with full CRUD operations
🚀 How to Run
Clone the repository:
git clone https://github.com/Achraf-Kreit/Graduate-Employment-Data-Analysis.git
Navigate to the folder:
bash

cd Graduate-Employment-Data-Analysis
Install required dependencies: (urllib and sqlite are built-in)
bash

pip install pandas matplotlib
Execute the pipeline:
bash

python "Web crawler + data analysis.py"
📁 Project Structure
text

├── "Web crawler + data analysis.py"   # Main Python script
├── real_graduates_data.csv            # Extracted raw dataset
├── real_graduates.db                  # SQLite Database (CRUD demo)
├── Charts/                            # Generated Visualizations
│   ├── chart1_real_top_salary.png
│   ├── chart2_real_industry_salary.png
│   ├── chart3_real_industry_pie.png
│   └── chart4_real_golden_matrix.png
└── README.md                          # You are here :)
👤 Author
Achraf Kreit

Dataset Source: FiveThirtyEight GitHub Repository

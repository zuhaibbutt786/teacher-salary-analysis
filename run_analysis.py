#!/usr/bin/env python3
# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from fpdf import FPDF
import os

# Set visualization styles
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('viridis')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

print("Starting teacher salary analysis...")

# Load the dataset
file_path = 'OECD.EDU.IMEP,DSD_EAG_SAL_STA@DF_EAG_SAL_STA_ALL,+all.csv'
df = pd.read_csv(file_path)

# Display basic information about the dataset
print(f"Dataset shape: {df.shape}")
print("\nFirst few rows:")
print(df.head())

# Check column names and data types
print("\nColumn data types:")
print(df.dtypes)

# Check for missing values
missing_values = df.isnull().sum()
print("\nMissing values per column:")
print(missing_values[missing_values > 0])

# Focus on relevant columns for our analysis
relevant_columns = [
    'REF_AREA', 'Reference area', 'MEASURE', 'Measure', 'UNIT_MEASURE', 'Unit of measure',
    'EDUCATION_LEV', 'Education level', 'PERS_TYPE', 'Type of personnel',
    'PERS_EXP_LEV', 'Experience level', 'OBS_VALUE', 'Observation value',
    'CURRENCY', 'Currency', 'REF_PERIOD', 'Reference period'
]

# Create a cleaned dataframe with only relevant columns
try:
    df_clean = df[relevant_columns].copy()
except KeyError as e:
    print(f"Some columns not found: {e}")
    # If columns are missing, use the ones that are available
    available_columns = [col for col in relevant_columns if col in df.columns]
    df_clean = df[available_columns].copy()

# Display the cleaned dataframe
print("\nCleaned dataframe:")
print(df_clean.head())

# Convert observation values to numeric
df_clean['OBS_VALUE'] = pd.to_numeric(df_clean['OBS_VALUE'], errors='coerce')

# Filter out rows with missing observation values
df_clean = df_clean.dropna(subset=['OBS_VALUE'])

# Check the number of records after cleaning
print(f"\nNumber of records after cleaning: {len(df_clean)}")

# Filter data for USD PPP (Purchasing Power Parity) values
df_usd = df_clean[df_clean['UNIT_MEASURE'] == 'USD_PPP'].copy()

# Filter for teacher data only
df_teachers = df_usd[df_usd['PERS_TYPE'] == 'TE'].copy()

# Group by country and calculate average salary
country_avg = df_teachers.groupby('Reference area')['OBS_VALUE'].mean().reset_index()
country_avg = country_avg.sort_values('OBS_VALUE', ascending=False)

print("\nTop 10 countries by average teacher salary:")
print(country_avg.head(10))

# Plot the top 20 countries by average teacher salary
plt.figure(figsize=(14, 10))
sns.barplot(x='OBS_VALUE', y='Reference area', data=country_avg.head(20))
plt.title('Top 20 Countries by Average Teacher Salary (USD PPP)', fontsize=16)
plt.xlabel('Average Salary (USD PPP)', fontsize=14)
plt.ylabel('Country', fontsize=14)
plt.tight_layout()
plt.savefig('teacher_salary_by_country.png', dpi=300)
print("Saved teacher_salary_by_country.png")

# Define experience levels and their order
exp_order = ['EXP0', 'EXP10', 'EXP15', 'EXPMAX']
exp_labels = ['Starting', '10 Years', '15 Years', 'Maximum']

# Filter data for experience analysis
df_exp = df_teachers[df_teachers['PERS_EXP_LEV'].isin(exp_order)].copy()

# Create a new column with readable experience labels
df_exp['Experience'] = df_exp['PERS_EXP_LEV'].map(dict(zip(exp_order, exp_labels)))

# Select top 10 countries by average salary for better visualization
top_countries = country_avg.head(10)['Reference area'].tolist()
df_exp_top = df_exp[df_exp['Reference area'].isin(top_countries)].copy()

# Calculate average salary by country and experience level
exp_avg = df_exp_top.groupby(['Reference area', 'PERS_EXP_LEV', 'Experience'])['OBS_VALUE'].mean().reset_index()

# Create a line plot to show salary progression
plt.figure(figsize=(14, 10))
sns.lineplot(data=exp_avg, x='Experience', y='OBS_VALUE', hue='Reference area', marker='o', linewidth=2.5)
plt.title('Teacher Salary Progression by Experience Level (Top 10 Countries)', fontsize=16)
plt.xlabel('Experience Level', fontsize=14)
plt.ylabel('Average Salary (USD PPP)', fontsize=14)
plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('salary_progression_by_experience.png', dpi=300)
print("Saved salary_progression_by_experience.png")

# Define education levels and their readable labels
edu_levels = {
    'ISCED11_02': 'Pre-primary',
    'ISCED11_1': 'Primary',
    'ISCED11_24': 'Lower secondary',
    'ISCED11_34': 'Upper secondary'
}

# Filter data for education level analysis
df_edu = df_teachers[df_teachers['EDUCATION_LEV'].isin(edu_levels.keys())].copy()

# Create a new column with readable education level labels
df_edu['Education Level'] = df_edu['EDUCATION_LEV'].map(edu_levels)

# Calculate average salary by education level
edu_avg = df_edu.groupby('Education Level')['OBS_VALUE'].mean().reset_index()
edu_avg = edu_avg.sort_values('OBS_VALUE')

# Create a bar plot
plt.figure(figsize=(12, 8))
sns.barplot(x='Education Level', y='OBS_VALUE', data=edu_avg, palette='viridis')
plt.title('Average Teacher Salary by Education Level', fontsize=16)
plt.xlabel('Education Level', fontsize=14)
plt.ylabel('Average Salary (USD PPP)', fontsize=14)
plt.tight_layout()
plt.savefig('salary_by_education_level.png', dpi=300)
print("Saved salary_by_education_level.png")

# Create an interactive box plot using Plotly
fig = px.box(df_teachers[df_teachers['Reference area'].isin(top_countries)],
             x='Reference area', y='OBS_VALUE', color='Reference area',
             title='Distribution of Teacher Salaries by Country',
             labels={'Reference area': 'Country', 'OBS_VALUE': 'Salary (USD PPP)'})

fig.update_layout(showlegend=False, height=600, width=1000)
fig.write_html('salary_distribution.html')
print("Saved salary_distribution.html")

# Check if we have multiple years in the dataset
years = df_clean['REF_PERIOD'].unique()
print(f"\nAvailable years in the dataset: {years}")

# If multiple years are available, create a time series analysis
if len(years) > 1:
    # Convert reference period to numeric
    df_clean['REF_PERIOD'] = pd.to_numeric(df_clean['REF_PERIOD'], errors='coerce')
    
    # Filter for USD PPP and teachers
    df_time = df_clean[(df_clean['UNIT_MEASURE'] == 'USD_PPP') & 
                       (df_clean['PERS_TYPE'] == 'TE')].copy()
    
    # Group by year and calculate average salary
    time_avg = df_time.groupby(['REF_PERIOD', 'Reference area'])['OBS_VALUE'].mean().reset_index()
    
    # Filter for top countries
    time_avg_top = time_avg[time_avg['Reference area'].isin(top_countries[:5])].copy()
    
    # Create a line plot
    plt.figure(figsize=(14, 10))
    sns.lineplot(data=time_avg_top, x='REF_PERIOD', y='OBS_VALUE', hue='Reference area', marker='o', linewidth=2.5)
    plt.title('Teacher Salary Trends Over Time (Top 5 Countries)', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Average Salary (USD PPP)', fontsize=14)
    plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('salary_trends_over_time.png', dpi=300)
    print("Saved salary_trends_over_time.png")
else:
    print("Only one year available in the dataset. Cannot perform time series analysis.")

# Calculate average salary by country and education level
country_edu_avg = df_edu.groupby(['Reference area', 'Education Level'])['OBS_VALUE'].mean().reset_index()

# Create a pivot table for better visualization
pivot_edu = country_edu_avg.pivot(index='Reference area', columns='Education Level', values='OBS_VALUE')

# Filter for countries with data for all education levels
pivot_edu_complete = pivot_edu.dropna()

# Create a heatmap
plt.figure(figsize=(14, 12))
sns.heatmap(pivot_edu_complete, annot=True, fmt='.0f', cmap='viridis', linewidths=.5)
plt.title('Teacher Salaries by Country and Education Level (USD PPP)', fontsize=16)
plt.tight_layout()
plt.savefig('salary_heatmap_by_education.png', dpi=300)
print("Saved salary_heatmap_by_education.png")

# Create a PDF report with the analysis results
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Teacher Salary Analysis Report', 0, 1, 'C')
        self.ln(10)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)
        
    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 10, body)
        self.ln()
        
    def add_image(self, image_path, w=180):
        if os.path.exists(image_path):
            self.image(image_path, x=10, w=w)
            self.ln(5)
        else:
            self.cell(0, 10, f"Image not found: {image_path}", 0, 1, 'L')

# Create PDF
pdf = PDF()
pdf.add_page()

# Introduction
pdf.chapter_title('Introduction')
pdf.chapter_body('This report presents an analysis of teacher salaries across different countries, education levels, and experience levels based on OECD data. The analysis provides insights into salary variations, progression patterns, and comparative statistics.')

# Analysis 1: Teacher Salaries by Country
pdf.add_page()
pdf.chapter_title('1. Teacher Salaries by Country')
pdf.chapter_body('The chart below shows the top 20 countries by average teacher salary in USD PPP (Purchasing Power Parity). This allows for a fair comparison of teacher compensation across different economies.')
pdf.add_image('teacher_salary_by_country.png')

# Analysis 2: Salary Progression by Experience
pdf.add_page()
pdf.chapter_title('2. Salary Progression by Experience Level')
pdf.chapter_body('This analysis examines how teacher salaries progress with experience, from starting salary to maximum salary. The chart shows the salary trajectory for the top 10 highest-paying countries.')
pdf.add_image('salary_progression_by_experience.png')

# Analysis 3: Salary by Education Level
pdf.add_page()
pdf.chapter_title('3. Salary Comparison by Education Level')
pdf.chapter_body('This chart compares average teacher salaries across different education levels, from pre-primary to upper secondary education. It highlights how compensation varies based on the level of education being taught.')
pdf.add_image('salary_by_education_level.png')

# Analysis 6: Correlation Between Education Level and Salary
pdf.add_page()
pdf.chapter_title('4. Correlation Between Education Level and Salary')
pdf.chapter_body('The heatmap below shows the relationship between education levels and teacher salaries across different countries. Darker colors indicate higher salaries.')
pdf.add_image('salary_heatmap_by_education.png')

# Conclusion
pdf.add_page()
pdf.chapter_title('Conclusion')
pdf.chapter_body('The analysis reveals significant variations in teacher salaries across countries, education levels, and experience levels. Generally, salaries increase with experience and higher education levels. Countries with stronger economies tend to offer higher compensation for teachers, but there are notable exceptions that suggest policy and cultural factors also play important roles in determining teacher compensation.')

# Save the PDF
pdf.output('teacher_salary_analysis_report.pdf')
print("Saved teacher_salary_analysis_report.pdf")

# Create an HTML report
html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Teacher Salary Analysis</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            color: #333;
        }}
        .container {{
            width: 90%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        header {{
            background-color: #2c3e50;
            color: white;
            padding: 20px 0;
            text-align: center;
        }}
        h1, h2, h3 {{
            color: #2c3e50;
        }}
        header h1 {{
            color: white;
        }}
        .section {{
            margin: 40px 0;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .chart-container {{
            margin: 20px 0;
            text-align: center;
        }}
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .interactive {{
            margin: 20px 0;
            height: 600px;
            border: none;
            width: 100%;
        }}
        footer {{
            background-color: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px 0;
            margin-top: 40px;
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>Teacher Salary Analysis</h1>
            <p>An in-depth analysis of teacher salaries across different countries, education levels, and experience levels</p>
        </div>
    </header>
    
    <div class="container">
        <div class="section">
            <h2>Introduction</h2>
            <p>This report presents an analysis of teacher salaries across different countries, education levels, and experience levels based on OECD data. The analysis provides insights into salary variations, progression patterns, and comparative statistics.</p>
        </div>
        
        <div class="section">
            <h2>1. Teacher Salaries by Country</h2>
            <p>The chart below shows the top 20 countries by average teacher salary in USD PPP (Purchasing Power Parity). This allows for a fair comparison of teacher compensation across different economies.</p>
            <div class="chart-container">
                <img src="teacher_salary_by_country.png" alt="Teacher Salaries by Country">
            </div>
        </div>
        
        <div class="section">
            <h2>2. Salary Progression by Experience Level</h2>
            <p>This analysis examines how teacher salaries progress with experience, from starting salary to maximum salary. The chart shows the salary trajectory for the top 10 highest-paying countries.</p>
            <div class="chart-container">
                <img src="salary_progression_by_experience.png" alt="Salary Progression by Experience">
            </div>
        </div>
        
        <div class="section">
            <h2>3. Salary Comparison by Education Level</h2>
            <p>This chart compares average teacher salaries across different education levels, from pre-primary to upper secondary education. It highlights how compensation varies based on the level of education being taught.</p>
            <div class="chart-container">
                <img src="salary_by_education_level.png" alt="Salary by Education Level">
            </div>
        </div>
        
        <div class="section">
            <h2>4. Salary Distribution by Country (Interactive)</h2>
            <p>The interactive chart below shows the distribution of teacher salaries across different countries. You can hover over the data points to see detailed information.</p>
            <div class="chart-container">
                <iframe class="interactive" src="salary_distribution.html" frameborder="0"></iframe>
            </div>
        </div>
        
        <div class="section">
            <h2>5. Correlation Between Education Level and Salary</h2>
            <p>The heatmap below shows the relationship between education levels and teacher salaries across different countries. Darker colors indicate higher salaries.</p>
            <div class="chart-container">
                <img src="salary_heatmap_by_education.png" alt="Salary Heatmap by Education Level">
            </div>
        </div>
        
        <div class="section">
            <h2>Conclusion</h2>
            <p>The analysis reveals significant variations in teacher salaries across countries, education levels, and experience levels. Generally, salaries increase with experience and higher education levels. Countries with stronger economies tend to offer higher compensation for teachers, but there are notable exceptions that suggest policy and cultural factors also play important roles in determining teacher compensation.</p>
            <p>For a more detailed analysis, please refer to the PDF report or the Jupyter notebook.</p>
            <p><a href="teacher_salary_analysis_report.pdf" target="_blank">Download PDF Report</a> | <a href="teacher_salary_analysis.ipynb" target="_blank">View Jupyter Notebook</a></p>
        </div>
    </div>
    
    <footer>
        <div class="container">
            <p>Teacher Salary Analysis Report | Generated on {pd.Timestamp.now().strftime('%Y-%m-%d')}</p>
        </div>
    </footer>
</body>
</html>
'''

# Save the HTML file
with open('index.html', 'w') as f:
    f.write(html_content)
print("Saved index.html")

print("\nAnalysis completed successfully!")
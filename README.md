# Teacher Salary Analysis

## Overview
This project provides an in-depth analysis of teacher salaries across different countries, education levels, and experience levels based on OECD data. The analysis offers valuable insights into global teacher compensation patterns and trends.

## Features
- **Comprehensive Data Analysis**: Examines teacher salaries across multiple dimensions including country, education level, and experience.
- **Interactive Visualizations**: Includes both static and interactive charts for better data exploration.
- **Multiple Output Formats**: Provides results in HTML dashboard, PDF report, and Jupyter notebook formats.

## Dataset
The analysis uses the OECD dataset on statutory salaries of teachers and school heads. The dataset includes information on:
- Teacher salaries across different countries
- Salaries at different education levels (pre-primary, primary, lower secondary, upper secondary)
- Salary progression based on experience (starting, 10 years, 15 years, maximum)
- Salaries in both national currencies and USD PPP (Purchasing Power Parity)

## Key Findings
1. **Salary Variations by Country**: Significant differences exist in teacher compensation across countries, even when adjusted for purchasing power parity.
2. **Experience Premium**: Most countries show clear salary progression with experience, though the rate of increase varies substantially.
3. **Education Level Impact**: Generally, teachers at higher education levels earn more than those at lower levels.
4. **Policy Implications**: Teacher compensation strategies vary widely, reflecting different approaches to attracting and retaining teaching talent.

## Files in this Repository
- `run_analysis.py`: Python script that performs the complete analysis
- `teacher_salary_analysis.ipynb`: Jupyter notebook with the analysis code and explanations
- `teacher_salary_analysis_report.pdf`: Comprehensive PDF report with findings and visualizations
- `index.html`: Interactive web dashboard presenting the analysis results
- Various visualization files (PNG and HTML)

## Visualizations
- **Teacher Salaries by Country**: Bar chart showing top 20 countries by average teacher salary
- **Salary Progression by Experience**: Line chart showing how salaries increase with experience
- **Salary by Education Level**: Bar chart comparing salaries across education levels
- **Salary Distribution by Country**: Interactive box plot showing salary distributions
- **Correlation Between Education Level and Salary**: Heatmap showing the relationship between education levels and salaries

## How to Run
1. Clone this repository
2. Install required packages:
   ```
   pip install pandas matplotlib seaborn plotly fpdf2
   ```
3. Run the analysis script:
   ```
   python run_analysis.py
   ```
4. View the results in the generated HTML dashboard (`index.html`) or PDF report (`teacher_salary_analysis_report.pdf`)

## Future Work
- Time series analysis with more historical data
- Correlation analysis with economic indicators
- Regional comparisons and clustering analysis
- Gender-based salary comparison (if data becomes available)

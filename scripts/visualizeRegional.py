import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data exported from Navicat (Output 1)
# Using sep='\t' because Navicat usually exports text files as tab-separated
try:
    df = pd.read_csv('Output1.txt', sep='\t')
except FileNotFoundError:
    print("Please make sure Output1.txt is saved in the same folder as this script!")
    exit()

# Clean up column names just in case Navicat left quotes
df.columns = df.columns.str.replace('"', '').str.strip()

# Chart 3: Regional Averages (Bar Chart)
plt.figure(figsize=(10, 6))
regional_stats = df.groupby('Region')['Avg_Annual_Homicides'].mean().sort_values(ascending=False).reset_index()

sns.barplot(data=regional_stats, x='Region', y='Avg_Annual_Homicides', palette='viridis')
plt.title('Average Annual Homicides by Global Region', fontsize=14, fontweight='bold')
plt.xlabel('Region', fontsize=12)
plt.ylabel('Average Annual Homicides (per Country)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('Regional_Averages.png', dpi=300)
print("Saved Regional_Averages.png")

# Chart 4: Global Scatter with Log Scale (Wealth vs. Crime by Region)
plt.figure(figsize=(12, 7))
sns.scatterplot(data=df, x='Avg_GDP', y='Avg_Annual_Homicides', hue='Region', 
                s=100, alpha=0.7, edgecolor='black', palette='Set1')

# Apply a logarithmic scale to the Y-axis because countries like USA and Brazil skew it heavily
plt.yscale('log')
plt.title('Global Wealth vs. Crime (Logarithmic Scale)', fontsize=14, fontweight='bold')
plt.xlabel('Average GDP Per Capita ($)', fontsize=12)
plt.ylabel('Average Annual Homicides (Log Scale)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)

# Highlight a few notable countries
notable_countries = ['United States', 'Brazil', 'Luxembourg', 'South Africa', 'Qatar']
for i, row in df.iterrows():
    if row['Country_Name'] in notable_countries:
        plt.text(row['Avg_GDP'], row['Avg_Annual_Homicides'], 
                 f" {row['Country_Name']}", fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('Global_Scatter_Log.png', dpi=300)
print("Saved Global_Scatter_Log.png")
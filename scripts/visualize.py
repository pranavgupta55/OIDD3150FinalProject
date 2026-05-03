import pandas as pd
import matplotlib.pyplot as plt
import io

# 1. Output 2 Data (Wealth Tiers)
tier_data = """Wealth_Tier,Num_Countries_In_Tier,Tier_Avg_GDP,Tier_Avg_Homicides
1,35,64188.9,708
2,35,29657.63,1096
3,35,15725.77,15933
4,35,8351.46,2743
5,35,2988.33,2696"""

df_tiers = pd.read_csv(io.StringIO(tier_data))

# Plot 1: Wealth Tiers vs Crime
plt.figure(figsize=(10, 6))
bars = plt.bar(df_tiers['Wealth_Tier'], df_tiers['Tier_Avg_Homicides'], color='skyblue', edgecolor='black')
plt.title('Average Homicides by Global Wealth Tier', fontsize=14, fontweight='bold')
plt.xlabel('Wealth Tier (1 = Richest, 5 = Poorest)', fontsize=12)
plt.ylabel('Average Annual Homicides', fontsize=12)
plt.xticks(df_tiers['Wealth_Tier'])
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add data labels
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 200, int(yval), ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('Tier_Analysis.png', dpi=300)
print("Saved Tier_Analysis.png")

# 2. Output 3 Data (Outliers)
outlier_data = """Country_Name,Region,Avg_GDP,Avg_Homicides
United States,North America,58268.61,18448
Germany,Europe,53445.9,1061
France,Europe,47429.02,978
Puerto Rico,North America,38318.79,774
United Kingdom,Europe,44221.47,772
Italy,Europe,48293.72,711
Canada,North America,50300.12,631
Japan,Asia,40670.09,542"""

df_outliers = pd.read_csv(io.StringIO(outlier_data))

# Plot 2: Outliers Bubble Chart
plt.figure(figsize=(10, 6))
colors = {'North America':'red', 'Europe':'blue', 'Asia':'green'}
for i in range(len(df_outliers)):
    plt.scatter(df_outliers['Avg_GDP'][i], df_outliers['Avg_Homicides'][i], 
                s=df_outliers['Avg_Homicides'][i]/10, alpha=0.6, 
                c=colors[df_outliers['Region'][i]], edgecolors='black')
    
    # Label the USA distinctly
    if df_outliers['Country_Name'][i] == 'United States':
        plt.text(df_outliers['Avg_GDP'][i] - 1000, df_outliers['Avg_Homicides'][i] + 500, 
                 df_outliers['Country_Name'][i], fontweight='bold', ha='center')

plt.title('High-GDP Outliers: >$30k GDP and >500 Homicides', fontsize=14, fontweight='bold')
plt.xlabel('Average GDP Per Capita ($)', fontsize=12)
plt.ylabel('Average Annual Homicides', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Create a custom legend
handles = [plt.Line2D([0],[0], marker='o', color='w', markerfacecolor=c, markersize=10, label=r) for r, c in colors.items()]
plt.legend(handles=handles, title="Region")

plt.tight_layout()
plt.savefig('Outliers_Analysis.png', dpi=300)
print("Saved Outliers_Analysis.png")
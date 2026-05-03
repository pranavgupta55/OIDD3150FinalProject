import pandas as pd

print("Fetching data from Our World in Data...")
# Fetch the data
df_gdp = pd.read_csv("https://ourworldindata.org/grapher/gdp-per-capita-worldbank.csv?v=1&csvType=full&useColumnShortNames=true", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})
df_crime = pd.read_csv("https://ourworldindata.org/grapher/homicides-unodc.csv?v=1&csvType=full&useColumnShortNames=true", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

print("Cleaning and normalizing into 3NF...")

# 1. Create Dim_Country (Dimension Table)
# We drop rows without a country code (like regional aggregates) to ensure clean joins
countries_gdp = df_gdp[['code', 'entity', 'owid_region']].dropna(subset=['code'])
countries_crime = df_crime[['code', 'entity', 'owid_region']].dropna(subset=['code'])
dim_country = pd.concat([countries_gdp, countries_crime]).drop_duplicates(subset=['code'])
dim_country.rename(columns={'code': 'Country_Code', 'entity': 'Country_Name', 'owid_region': 'Region'}, inplace=True)

# 2. Create Fact_Economics
fact_econ = df_gdp[['code', 'year', 'ny_gdp_pcap_pp_kd']].dropna(subset=['code', 'ny_gdp_pcap_pp_kd']).copy()
fact_econ.rename(columns={'code': 'Country_Code', 'year': 'Year', 'ny_gdp_pcap_pp_kd': 'GDP_Per_Capita'}, inplace=True)

# 3. Create Fact_Crime
crime_col = 'value__category_total__sex_total__age_total__unit_of_measurement_counts'
fact_crime = df_crime[['code', 'year', crime_col]].dropna(subset=['code', crime_col]).copy()
fact_crime.rename(columns={'code': 'Country_Code', 'year': 'Year', crime_col: 'Crime_Count'}, inplace=True)
fact_crime['Crime_Type'] = 'Homicide'

# 4. Filter for Intersecting Data (Inner Join Concept)
# We only want to keep rows where a country has BOTH GDP and Crime data for that specific year
valid_pairs = pd.merge(fact_econ[['Country_Code', 'Year']], fact_crime[['Country_Code', 'Year']], on=['Country_Code', 'Year'], how='inner')

fact_econ = pd.merge(fact_econ, valid_pairs, on=['Country_Code', 'Year'], how='inner')
fact_crime = pd.merge(fact_crime, valid_pairs, on=['Country_Code', 'Year'], how='inner')

# 5. Export to CSV locally
dim_country.to_csv('data/Dim_Country.csv', index=False)
fact_econ.to_csv('data/Fact_Economics.csv', index=False)
fact_crime.to_csv('data/Fact_Crime.csv', index=False)

print(f"Success! Created Dim_Country.csv ({len(dim_country)} rows)")
print(f"Success! Created Fact_Economics.csv ({len(fact_econ)} rows)")
print(f"Success! Created Fact_Crime.csv ({len(fact_crime)} rows)")
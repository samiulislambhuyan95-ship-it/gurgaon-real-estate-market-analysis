import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data.csv')
#print(df.head())
#print(df.info())

# data cleaning
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')  # Remove leading/trailing whitespace from column names
#print(df.columns.tolist())
df= df.drop_duplicates()  # Remove duplicate rows

# numerical column cleaning
# Numerical Columns Cleaning
df['price'] = df['price'].astype(str).str.replace(',', '').astype(float)
df['area'] = df['area'].astype(str).str.replace(',', '').astype(int)
df['rate_per_sqft'] = df['rate_per_sqft'].astype(str).str.replace(',', '').astype(int)

#print(df['rate_per_sqft'])

# categorical column cleaning
df['status'] = df['status'].str.strip().str.lower()  # Remove leading/trailing whitespace and convert to lowercase
df['rera_approval'] = df['rera_approval'].str.strip().str.lower().map({'approved by rera': True, 'not approved by rera': False})  # Remove leading/trailing whitespace and convert to lowercase
df['flat_type'] = df['flat_type'].str.strip().str.lower()  # Remove leading/trailing whitespace and convert to lowercase
df = df.drop_duplicates()  # Remove duplicate rows
#print(df)


# question 1: which is the costliest flat  in the dataset?
costliest_flat = df.loc[df['price'].idxmax()]
#print("Costliest Flat Details:")
#print(costliest_flat)
'''
lets write this in a more readable format
Costliest Flat Details:
price                                1226300000.0
status                              ready to move
area                                        16500
rate_per_sqft                               74323
property_type    6 BHK Apartment in DLF Camellias
locality                                Sector 42
builder_name                    Provident Capital
rera_approval                               False
bhk_count                                       6
society                             DLF Camellias
company_name                                  DLF
flat_type                               apartment
'''
#print(f"the Costliest Flat is a  {costliest_flat['bhk_count']} BHK {costliest_flat['flat_type']} in {costliest_flat['locality']} with a price of {costliest_flat['price']} and an area of {costliest_flat['area']} sqft. The rate per sqft is {costliest_flat['rate_per_sqft']}. The builder is {costliest_flat['builder_name']} and the RERA approval status is {costliest_flat['rera_approval']}.")

# question 2: which locality has the highest average price?
highest_avg_price_locality = df.groupby('locality')['price'].mean().idxmax()
highest_avg_price = df.groupby('locality')['price'].mean().max()
#print(f"The locality with the highest average price is {highest_avg_price_locality} with an average price of {highest_avg_price}.")

# question 3: which locality has the highest rate per sqft?
highest_avg_rate_locality = df.groupby('locality')['rate_per_sqft'].mean().idxmax()
highest_avg_rate = df.groupby('locality')['rate_per_sqft'].mean().max()
#print(f"The locality with the highest average rate per sqft is {highest_avg_rate_locality} with an average rate of {highest_avg_rate}.")


# question 4: Do ready to move properties cost more than under construction properties?
ready_to_move_avg_price = df[df['status'] == 'ready to move']['price'].mean()
under_construction_avg_price = df[df['status'] == 'under construction']['price'].mean()
if ready_to_move_avg_price > under_construction_avg_price:
    result = "Yes, ready to move properties cost more than under construction properties."
else:
    result = "No, under construction properties cost more than ready to move properties."
#print(result)


# question 5: Do RERA-approved properties command a price premium?
rera_approved_avg_price = df[df['rera_approval'] == True]['price'].mean()
non_rera_approved_avg_price = df[df['rera_approval'] == False]['price'].mean()
if rera_approved_avg_price > non_rera_approved_avg_price:
    result = "Yes, RERA-approved properties cost more than non-RERA-approved properties."
else:
    result = "No, non-RERA-approved properties cost more than RERA-approved properties."
#print(result)


# question 6: how does area impact price?
sns.scatterplot(data=df, x='area', y='price')
plt.title('Area vs Price')
plt.xlabel('Area (sqft)')
plt.ylabel('Price (INR)')
#plt.show()


# question 7: which BHK configuration is the most expensive based on per sqft rate?
most_expensive_bhk = df.groupby('bhk_count')['rate_per_sqft'].mean().idxmax()
most_expensive_bhk_rate = df.groupby('bhk_count')['rate_per_sqft'].mean().max()
#print(f"The most expensive BHK configuration is {most_expensive_bhk} BHK with an average rate per sqft of {most_expensive_bhk_rate}.")

# question 8: which property type is the costliest based on rate per sqft?
costliest_property_type = df.groupby('property_type')['rate_per_sqft'].mean().idxmax()
costliest_property_type_rate = df.groupby('property_type')['rate_per_sqft'].mean().max()
#print(f"The costliest property type is {costliest_property_type} with an average rate per sqft of {costliest_property_type_rate}.")

# question 9: Do certain builders price higher print the name of top 5 builders?
print(df.groupby('builder_name')['price'].mean().sort_values(ascending=False).head(5))
print("The top 5 builders with the highest average price are:")
top_5_builders = df.groupby('builder_name')['price'].mean().sort_values(ascending=False).head(5)
#print(top_5_builders)

# question 10: Are larger homes more expensive based on per sqft rate?

df['area_category'] = pd.cut(
    df['area'],
    bins=[0, 1000, 2000, 3000, 5000, float('inf')],
    labels=['Below 1000', '1000-2000', '2000-3000', '3000-5000', 'Above 5000']
)

area_rate_analysis = df.groupby('area_category', observed=True)['rate_per_sqft'].mean()

print("Average rate per sqft by property area:")
print(area_rate_analysis)
print("Conclusion: In this dataset, larger properties generally have a higher average rate per sqft.")
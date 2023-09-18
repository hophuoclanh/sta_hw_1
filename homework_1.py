import csv
import statistics
import pandas as pd

## What is the proportion (probability) of individuals who had PhD degrees?

# Define your filtering condition for the 3rd column (modify this function as needed)
def filter_condition(row):
    # Replace this condition with your specific criteria for the 3rd column
    return row[2] == 'PhD'

def proportion(condition, total):
    phd_proportion = condition/total
    return phd_proportion

# Open the input CSV file
with open('marketing_campaign.csv', 'r') as input_file:
    # Specify the delimiter as a semicolon
    csv_reader = csv.reader(input_file, delimiter=';')

    # Initialize a variable to count the rows
    row_count = 0

    # Initialize a variable to count matching rows
    filtered_count = 0

    # Iterate through the rows and apply your filtering criteria
    for row in csv_reader:
        row_count += 1  # Increment the row count for each row

        if filter_condition(row):
            filtered_count += 1

row_count = row_count -1
# Print the count of rows that fit the conditions
# print(f"Number of rows that fit the conditions: {filtered_count}")
# Print the total number of rows
# print(f"Total number of rows in the CSV file: {row_count}")
# Print the proportion
print(f"The proportion of individuals who had PhD degrees is: ", proportion(filtered_count, row_count))

## What is the proportion (probability) of individuals with PhD degrees that have incomes less than the sample mean/median incomes?

data = []  # Create an empty list to store the values for the incomes

# Open the input CSV file
with open('marketing_campaign.csv', 'r') as input_file:
    # Specify the delimiter as a semicolon
    csv_reader = csv.reader(input_file, delimiter=';')

    # Iterate through the rows and apply your filtering criteria
    for row in csv_reader:
        try:
            value = float(row[4])  # Assuming the 5th column contains numeric values
            data.append(value)
        except (ValueError, IndexError):
            pass  # Handle non-numeric values or index errors, if needed

sample_mean = statistics.mean(data)
sample_median = statistics.median(data)

# Create a subset of individuals with PhD degrees
phd_subset = []

with open('marketing_campaign.csv', 'r') as file:
    csv_reader = csv.reader(file, delimiter=';')

    for row in csv_reader:
        if row[2] == 'PhD':  # Assuming the 3rd column indicates the degree
            try:
                income = float(row[4])  # Assuming the 5th column contains income values
                phd_subset.append(income)
            except (ValueError, IndexError):
                pass  # Handle non-numeric values or index errors, if needed

# Calculate the proportion (probability) for mean
mean_count = sum(1 for income in phd_subset if income < sample_mean)
mean_proportion = mean_count / row_count

# Calculate the proportion (probability) for median
median_count = sum(1 for income in phd_subset if income < sample_median)
median_proportion = median_count / row_count

print(f"Proportion of individuals with PhD degrees with incomes less than sample mean: {mean_proportion}")
print(f"Proportion of individuals with PhD degrees with incomes less than sample median: {median_proportion}")

## Find the crosstabulation for the Education and Marital Status features. Then make up your own interpretation about these matters.

# Load your data into a DataFrame
df = pd.read_csv('marketing_campaign.csv', delimiter=';')

# Create the crosstabulation between 'Degree' and 'Income'
crosstab = pd.crosstab(df['Education'], df['Marital_Status'])

# Print the crosstabulation table
print(crosstab)

## Compare the average spending on wine products of the two group of customers based on the marital status: Divorced and Single.

# Create a subset of individuals who divorced
divorced_subset = []
# Create a subset of individuals who single
single_subset = []

with open('marketing_campaign.csv', 'r') as file:
    csv_reader = csv.reader(file, delimiter=';')

    for row in csv_reader:
        if row[3] == 'Divorced':  # Assuming the 4th column indicates the marital status
            try:
                wine = float(row[9])  # Assuming the 9th column contains the amount spent on wine products
                divorced_subset.append(wine)
            except (ValueError, IndexError):
                pass  # Handle non-numeric values or index errors, if needed

        if row[3] == 'Single':  # Assuming the 4th column indicates the marital status
            try:
                wine = float(row[9])  # Assuming the 9th column contains the amount spent on wine products
                single_subset.append(wine)
            except (ValueError, IndexError):
                pass  # Handle non-numeric values or index errors, if needed

total_wine_divorced = sum(divorced_subset)
total_wine_single = sum(single_subset)

divorced_totals = crosstab['Divorced'].sum()
single_totals = crosstab['Single'].sum()

average_wine_divorced = total_wine_divorced/divorced_totals
average_wine_single = total_wine_single/single_totals

# Determine which one is greater using an if-else statement
if average_wine_single < average_wine_divorced:
    print("The average spending on wine products of the divorced customers are greater than the single customers.")
elif average_wine_single > average_wine_divorced:
    print("The average spending on wine products of the single customers are greater than the divorced customers.")
else:
    print("The average spending on wine products of the divorced customers and the single customers are equal in quantity.")

# print(f"The average spending on wine products of the divorced customers: {average_wine_divorced}")
# print(f"The average spending on wine products of the single customers: {average_wine_single}")

##  In terms of Education, which group of customers spend most on wine products? on sweet products?
# Group the data by the 'Education' column
grouped = df.groupby('Education')

# Calculate the total wine for each group
total_wine_per_degree = grouped['MntWines'].sum()

# Print the results
# print(total_wine_per_degree)

# Find the degree with the maximum total wine
degree_with_max_wine = total_wine_per_degree.idxmax()

# Find the maximum total wine
max_total_wine = total_wine_per_degree.max()

# Print the degree and maximum total wine
print(f"The degree with the maximum total income is: {degree_with_max_wine}")
print(f"The maximum total income among degree categories is: {max_total_wine}")

# Calculate the total income for each group
total_sweet_per_degree = grouped['MntSweetProducts'].sum()

# Print the results
# print(total_sweet_per_degree)

# Find the degree with the maximum total sweet
degree_with_max_sweet = total_sweet_per_degree.idxmax()

# Find the maximum total sweet
max_total_sweet = total_sweet_per_degree.max()

# Print the degree and maximum total sweet
print(f"The degree with the maximum total income is: {degree_with_max_sweet}")
print(f"The maximum total income among degree categories is: {max_total_sweet}")

import matplotlib.pyplot as plt
import seaborn as sns

# Create a bar plot for the categorical variable 'Education'
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='Education', order=df['Education'].value_counts().index)
plt.xlabel('Education')
plt.ylabel('Count')
plt.title('Distribution of Education Levels')
plt.xticks(rotation=45)
plt.show()

# Create a histogram for the quantitative variable 'Income'
plt.figure(figsize=(10, 6))
plt.hist(df['Income'], bins=100, edgecolor='k')
plt.xlabel('Income')
plt.ylabel('Frequency')
plt.title('Income Distribution')
plt.show()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV
df = pd.read_csv("data.csv")

# Show first 5 rows
print("Data:")
print(df.head())

# Show basic information
print("\nInfo:")
print(df.info())

# Show summary statistics
print("\nSummary Statistics:")
print(df.describe())

# Average Age
print("\nAverage Age:", df["Age"].mean())

# Bar Chart - Age Distribution
df["Age"].value_counts().plot(kind="bar")
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Count")
plt.show()

# Scatter Plot - Age vs Salary
plt.scatter(df["Age"], df["Salary"])
plt.title("Age vs Salary")
plt.xlabel("Age")
plt.ylabel("Salary")
plt.show()

# Heatmap - Correlation (only numeric columns)
numeric_df = df.select_dtypes(include=["number"])
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()


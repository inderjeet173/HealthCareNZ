import pandas as pd
import numpy as np

num_records = 50000
np.random.seed(42)

ages = np.random.randint(0, 90, num_records)
genders = np.random.choice(['Male', 'Female'], num_records)
regions = np.random.choice(['Auckland', 'Wellington', 'Canterbury', 'Otago', 'Bay of Plenty'], num_records)
diseases = np.random.choice(['Diabetes', 'Heart Disease', 'Flu', 'Asthma'], num_records)
years = np.random.choice([2024, 2025], num_records)

df = pd.DataFrame({
    'Patient_ID': range(10001, 10001 + num_records),
    'Age': ages,
    'Gender': genders,
    'Region': regions,
    'Disease': diseases,
    'Cases': 1,
    'Year': years
})

df.to_csv("data/NZ_Health_Dataset.csv", index=False)
print("Dummy dataset created!")
print(df.head())
import pandas as pd

# Load datasets
resumes = pd.read_csv("data/resumes.csv")
jobs = pd.read_csv("data/jobs.csv")
matches = pd.read_csv("data/matches.csv")


print("\n==============================")
print("RESUMES DATASET")
print("==============================")

print("Shape:", resumes.shape)

print("\nColumns:")
print(resumes.columns.tolist())

print("\nFirst 2 rows:")
print(resumes.head(2).to_string())

print("\nMissing values:")
print(resumes.isnull().sum())


print("\n==============================")
print("JOBS DATASET")
print("==============================")

print("Shape:", jobs.shape)

print("\nColumns:")
print(jobs.columns.tolist())

print("\nFirst 2 rows:")
print(jobs.head(2).to_string())

print("\nMissing values:")
print(jobs.isnull().sum())


print("\n==============================")
print("MATCHES DATASET")
print("==============================")

print("Shape:", matches.shape)

print("\nColumns:")
print(matches.columns.tolist())

print("\nFirst 2 rows:")
print(matches.head(2).to_string())

print("\nMissing values:")
print(matches.isnull().sum())
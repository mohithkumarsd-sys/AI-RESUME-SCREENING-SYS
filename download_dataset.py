import pandas as pd
import os

os.makedirs("data", exist_ok=True)

print("Downloading resumes...")

resumes_url = (
    "https://huggingface.co/datasets/"
    "michaelozon/candidate-matching-synthetic/"
    "resolve/main/resumes/train-00000-of-00001.parquet"
)

resumes = pd.read_parquet(resumes_url)

print("Downloading jobs...")

jobs_url = (
    "https://huggingface.co/datasets/"
    "michaelozon/candidate-matching-synthetic/"
    "resolve/main/jobs/train-00000-of-00001.parquet"
)

jobs = pd.read_parquet(jobs_url)

print("Downloading matches...")

matches_url = (
    "https://huggingface.co/datasets/"
    "michaelozon/candidate-matching-synthetic/"
    "resolve/main/matches/train-00000-of-00001.parquet"
)

matches = pd.read_parquet(matches_url)

resumes.to_csv("data/resumes.csv", index=False)
jobs.to_csv("data/jobs.csv", index=False)
matches.to_csv("data/matches.csv", index=False)

print("\n==============================")
print("DOWNLOAD COMPLETE")
print("==============================")

print("Resumes :", len(resumes))
print("Jobs    :", len(jobs))
print("Matches :", len(matches))

print("\nFiles created:")
print("data/resumes.csv")
print("data/jobs.csv")
print("data/matches.csv")
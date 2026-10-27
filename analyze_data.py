import pandas as pd

# Load datasets
resumes = pd.read_csv("data/resumes.csv")
jobs = pd.read_csv("data/jobs.csv")


print("\n==============================")
print("RESUME ANALYSIS")
print("==============================")

print("\nRoles:")
print(resumes["role"].value_counts())

print("\nSeniorities:")
print(resumes["seniority"].value_counts())

print("\nIndustries:")
print(resumes["industry"].value_counts())

print("\nEducation:")
print(resumes["education"].value_counts())


print("\n==============================")
print("JOB ANALYSIS")
print("==============================")

print("\nJob titles:")
print(jobs["job_title"].value_counts())

print("\nSeniorities:")
print(jobs["seniority"].value_counts())

print("\nIndustries:")
print(jobs["industry"].value_counts())


print("\n==============================")
print("SAMPLE SKILLS")
print("==============================")

print("\nResume skills:")
for i in range(5):
    print(resumes.loc[i, "skills"])

print("\nJob must-have skills:")
for i in range(5):
    print(jobs.loc[i, "must_have_skills"])

print("\nJob nice-to-have skills:")
for i in range(5):
    print(jobs.loc[i, "nice_to_have_skills"])
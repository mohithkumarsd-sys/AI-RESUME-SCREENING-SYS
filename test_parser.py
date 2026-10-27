from services.data_processor import parse_list_field

job_skills = "['Timeline Management' 'Process Improvement' 'Stakeholder Communication']"
resume_skills = "['OOP' 'Databases' 'Git' 'Docker' 'Python' 'Unit Testing' 'Java']"

print("Job skills:")
print(parse_list_field(job_skills))

print("\nResume skills:")
print(parse_list_field(resume_skills))
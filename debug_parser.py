import inspect
from services.data_processor import parse_list_field

print("===== FUNCTION PYTHON IS LOADING =====")
print(inspect.getsource(parse_list_field))

job_skills = "['Timeline Management' 'Process Improvement' 'Stakeholder Communication']"

print("\n===== TEST RESULT =====")
print(parse_list_field(job_skills))
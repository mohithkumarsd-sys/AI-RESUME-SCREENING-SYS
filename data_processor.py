import re
import ast
import numpy as np



def parse_list_field(value):
    import ast
    import re

    if value is None:
        return []

    if isinstance(value, (list, tuple, set)):
        return [str(item).strip() for item in value if str(item).strip()]

    if not isinstance(value, str) or not value.strip():
        return []

    value = value.strip()

    # Parse a valid Python list first
    try:
        parsed = ast.literal_eval(value)
        if isinstance(parsed, (list, tuple, set)):
            return [str(item).strip() for item in parsed if str(item).strip()]
    except (ValueError, SyntaxError):
        pass

    # Parse resume IDs
    if "R_" in value:
        return re.findall(r"R_\d{6}", value)

    # Extract each quoted item separately
    items = re.findall(r"""['"]([^'"]*)['"]""", value)

    if items:
        return [item.strip() for item in items if item.strip()]

    # Fallback for comma-separated values
    return [
        item.strip().strip("'\"")
        for item in value.strip("[]").split(",")
        if item.strip()
    ]


def normalize_skill(skill):
    """
    Standardize a skill for comparison.
    Example: ' Python ' becomes 'python'.
    """

    return skill.strip().lower()


def calculate_skill_match(
    resume_skills,
    must_have_skills,
    nice_to_have_skills
):
    """
    Compare a candidate's skills with a job's requirements.
    """

    # Normalize skills so comparisons ignore capitalization and spaces.
    candidate_skills = {
        normalize_skill(skill) for skill in resume_skills
    }

    required_skills = {
        normalize_skill(skill) for skill in must_have_skills
    }

    optional_skills = {
        normalize_skill(skill) for skill in nice_to_have_skills
    }

    # Find matching and missing skills.
    matched_required = candidate_skills & required_skills
    missing_required = required_skills - candidate_skills
    matched_optional = candidate_skills & optional_skills

    # Calculate the must-have skill-match percentage.
    if required_skills:
        match_percentage = (
            len(matched_required) / len(required_skills)
        ) * 100
    else:
        match_percentage = 0.0

    return {
        "matched_must_have": sorted(matched_required),
        "missing_must_have": sorted(missing_required),
        "matched_nice_to_have": sorted(matched_optional),
        "skill_match_percentage": round(match_percentage, 2)
    }

    

def calculate_seniority_fit(candidate_seniority, job_seniority):
    """
    Compare candidate seniority with the job's seniority.

    Same level: 100
    One level apart: 50
    Two levels apart: 0
    """
    seniority_levels = {
        "junior": 0,
        "mid": 1,
        "senior": 2
    }

    candidate_level = seniority_levels.get(
        str(candidate_seniority).strip().lower()
    )
    job_level = seniority_levels.get(
        str(job_seniority).strip().lower()
    )

    # Unknown seniority should not receive an invented score.
    if candidate_level is None or job_level is None:
        return None

    difference = abs(candidate_level - job_level)

    if difference == 0:
        return 100.0
    elif difference == 1:
        return 50.0
    else:
        return 0.0




def rank_candidates(resumes, job, top_n=10):
    """
    Rank candidates using skills, role, seniority,
    and industry relevance.
    """
    results = []

    for _, resume in resumes.iterrows():

        # 1. Calculate required skill match.
        match = calculate_skill_match(
            resume["skills"],
            job["must_have_skills"],
            job["nice_to_have_skills"]
        )

        skill_score = match["skill_match_percentage"]

        # 2. Calculate role match.
        candidate_role = normalize_skill(resume["role"])
        job_title = normalize_skill(job["job_title"])

        role_score = (
            100.0 if candidate_role == job_title else 0.0
        )

        # 3. Calculate seniority match.
        seniority_score = calculate_seniority_fit(
            resume["seniority"],
            job["seniority"]
        )

        # 4. Calculate industry match.
        candidate_industry = normalize_skill(resume["industry"])
        job_industry = normalize_skill(job["industry"])

        industry_score = (
            100.0
            if candidate_industry == job_industry
            else 0.0
        )

        # 5. Calculate weighted overall score.
        # Weights: Skills 50%, Role 20%,
        # Seniority 15%, Industry 15%.

        weighted_score = (
            skill_score * 0.50
            + role_score * 0.20
            + industry_score * 0.15
        )

        total_weight = 0.85

        if seniority_score is not None:
            weighted_score += seniority_score * 0.15
            total_weight = 1.00

        overall_score = weighted_score / total_weight

        # 6. Store candidate results.
        results.append({
            "resume_id": resume["resume_id"],
            "role": resume["role"],
            "seniority": resume["seniority"],
            "years_experience": resume["years_experience"],
            "matched_skills": match["matched_must_have"],
            "missing_skills": match["missing_must_have"],
            "skill_score": round(skill_score, 2),
            "role_score": round(role_score, 2),
            "seniority_score": (
                round(seniority_score, 2)
                if seniority_score is not None
                else None
            ),
            "industry_score": round(industry_score, 2),
            "score": round(overall_score, 2)
        })

    # 7. Sort by overall score, then use
    # individual factors to break ties.
    results.sort(
        key=lambda candidate: (
            candidate["score"],
            candidate["industry_score"],
            candidate["skill_score"],
            candidate["role_score"],
            candidate["seniority_score"]
            if candidate["seniority_score"] is not None
            else -1
        ),
        reverse=True
    )

    return results[:top_n]


if __name__ == "__main__":
    import pandas as pd

    # Load the datasets
    resumes = pd.read_csv("data/resumes.csv")
    jobs = pd.read_csv("data/jobs.csv")

    # Convert skill fields from text into Python lists
    resumes["skills"] = resumes["skills"].apply(parse_list_field)
    jobs["must_have_skills"] = jobs["must_have_skills"].apply(parse_list_field)
    jobs["nice_to_have_skills"] = jobs["nice_to_have_skills"].apply(parse_list_field)

    # Select the first job and rank candidates
    job = jobs.iloc[0]
    ranked_candidates = rank_candidates(
        resumes, job, top_n=10
    )

    print("Total resumes loaded:", len(resumes))
    print("Candidates returned:", len(ranked_candidates))


    # Display the results
    print("\n==============================")
    print("TOP 10 CANDIDATES")
    print("==============================")
    print("Job:", job["job_id"], "-", job["job_title"])
    print("Required skills:", job["must_have_skills"])

    for rank, candidate in enumerate(ranked_candidates, start=1):
        print(f"\nRank: {rank}")
        print("Resume ID:", candidate["resume_id"])
        print("Current role:", candidate["role"])
        print("Seniority:", candidate["seniority"])
        print("Experience:", candidate["years_experience"], "years")
        print("Matched skills:", candidate["matched_skills"])
        print("Missing skills:", candidate["missing_skills"])
        print("Skill score:", candidate["skill_score"], "%")
        print("Role score:", candidate["role_score"], "%")
        print("Seniority score:", candidate["seniority_score"])
        print("Overall score:", candidate["score"], "%")
import pandas as pd

# Your existing data
data = {
    "ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "neuroticism_scores": [78, 45, 59, 36, 80, 47, 62, 51, 68, 39, 74, 53],
    "extroversion_scores": [34, 67, 71, 50, 45, 68, 55, 79, 46, 59, 42, 75],
    "openness_scores": [69, 33, 62, 58, 49, 54, 60, 35, 73, 64, 48, 57],
    "agreeableness_scores": [42, 56, 47, 61, 39, 72, 41, 67, 53, 49, 62, 55],
    "conscientiousness_scores": [55, 48, 30, 40, 66, 37, 57, 44, 31, 52, 69, 38],
    "major": ['ISE', 'SWE', 'ICS', 'ISE', 'SWE', 'ICS', 'ISE', 'SWE', 'ICS', 'ISE', 'SWE', 'ICS'],
    "GPA": [3.5, 3.2, 2.9, 3.7, 3.1, 3.4, 3.0, 3.6, 2.8, 3.8, 3.3, 3.5],
    "role_in_project": ['executor', 'innovator', 'collaborator', 'executor', 'innovator', 'collaborator', 'executor', 'innovator', 'collaborator', 'executor', 'innovator', 'collaborator']
}

# Assuming this is your team assignment
team_assignments = [1, 2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 3]

# Create DataFrame
students_df = pd.DataFrame(data)

# Add the team assignments
students_df['Team_Number'] = team_assignments

# Save to CSV
students_df.to_csv("students_with_teams.csv", index=False)

import random
import csv

def generate_scores(mean, std_dev, num_samples=100):
    return [round(random.gauss(mean, std_dev), 2) for _ in range(num_samples)]

def generate_majors(majors, num_samples=100):
    return [random.choice(majors) for _ in range(num_samples)]

def generate_gpas(min_gpa, max_gpa, num_samples=100):
    return [round(random.uniform(min_gpa, max_gpa), 2) for _ in range(num_samples)]

def generate_roles(roles, num_samples=100):
    return [random.choice(roles) for _ in range(num_samples)]

# Number of individuals
num_individuals = 100

# List of majors and roles
majors_list = ["ICS", "SWE", "ISE"]
roles_list = ["executor", "innovator", "collaborator"]

# Generating scores, majors, GPAs, and roles
neuroticism_scores = generate_scores(21.65, 7.06, num_individuals)
extroversion_scores = generate_scores(51.02, 7.69, num_individuals)
openness_scores = generate_scores(44.24, 5.86, num_individuals)
agreeableness_scores = generate_scores(50.63, 8.51, num_individuals)
conscientiousness_scores = generate_scores(41.37, 5.80, num_individuals)
majors = generate_majors(majors_list, num_individuals)
gpas = generate_gpas(2.0, 4.0, num_individuals)
roles = generate_roles(roles_list, num_individuals)

# Writing data to a CSV file
filename = 'generated_data_GPA_role.csv'
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['ID', 'neuroticism_scores', 'extroversion_scores', 'openness_scores', 
                     'agreeableness_scores', 'conscientiousness_scores', 'major', 'GPA', 'role_in_project'])
    
    # Write the data rows
    for i in range(num_individuals):
        writer.writerow([i+1, neuroticism_scores[i], extroversion_scores[i], openness_scores[i], 
                         agreeableness_scores[i], conscientiousness_scores[i], majors[i], gpas[i], roles[i]])

print(f"Data successfully written to {filename}")


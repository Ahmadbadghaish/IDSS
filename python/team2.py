import numpy as np
import pandas as pd
import random
from collections import Counter

def initialize_population(pop_size, student_count, team_count):
    """Initialize a population with random team assignments."""
    return [np.random.choice(range(team_count), student_count) for _ in range(pop_size)]

def team_composition(individual, students_df):
    """Evaluate the team composition based on roles, majors, and GPA."""
    team_roles = {team: Counter() for team in range(6)}
    team_majors = {team: Counter() for team in range(6)}
    team_gpa = {team: [] for team in range(6)}

    for student_idx, team in enumerate(individual):
        student = students_df.iloc[student_idx]
        team_roles[team][student['role_in_project']] += 1
        team_majors[team][student['major']] += 1
        team_gpa[team].append(student['GPA'])

    # Evaluate team balance
    balance_score = 0
    for team in team_roles:
        balance_score += len(set(team_roles[team].values())) - 1  # More unique counts, less balance
        balance_score += len(set(team_majors[team].values())) - 1
        balance_score += abs(np.mean(team_gpa[team]) - students_df['GPA'].mean())

    return balance_score

def fitness(individual, students_df):
    """Calculate the fitness of an individual. Lower is better (more balanced teams)."""
    return team_composition(individual, students_df)

def evolve(population, students_df, retain=0.2, random_select=0.05, mutate=0.01):
    graded = [(fitness(x, students_df), x) for x in population]
    graded = [x[1] for x in sorted(graded, key=lambda x: x[0])]
    retain_length = int(len(graded)*retain)
    parents = graded[:retain_length]

    # Randomly add other individuals to promote genetic diversity
    for individual in graded[retain_length:]:
        if random_select > random.random():
            parents.append(individual)

    # Crossover parents to create children
    desired_length = len(population) - len(parents)
    children = []
    while len(children) < desired_length:
        male_idx, female_idx = random.sample(range(len(parents)), 2)
        male = parents[male_idx]
        female = parents[female_idx]
        half = len(male) // 2
        child = np.concatenate((male[:half], female[half:]))
        children.append(child)

    # Mutate some individuals
    for individual in children:
        if mutate > random.random():
            pos_to_mutate = random.randint(0, len(individual)-1)
            individual[pos_to_mutate] = random.randint(0, 5)

    parents.extend(children)
    return parents

# Read CSV file into DataFrame
students_df = pd.read_csv('generated_data_GPA_role.csv')

# Assuming your CSV file is correctly formatted, you can use the DataFrame directly
student_count = len(students_df)  # Total number of students
team_count = 6                   # Number of teams
pop_size = 100                   # Population size

# Initialize population
population = initialize_population(pop_size, student_count, team_count)

# Evolve the population
for i in range(100):
    population = evolve(population, students_df)
    best_individual = min(population, key=lambda ind: fitness(ind, students_df))
    best_fitness = fitness(best_individual, students_df)
    print(f"Generation {i+1}: Best Fitness = {best_fitness}")

# Identify and print the best team distribution after the final evolution
best_individual = min(population, key=lambda ind: fitness(ind, students_df))
best_teams = Counter(best_individual)
print("Best Team Distribution:", best_teams)

# Optionally, print detailed information about each team
for team in range(team_count):
    team_members = students_df.iloc[np.where(np.array(best_individual) == team)]
    print(f"\nTeam {team + 1} Members:")
    print(team_members)

# Add the team number to the DataFrame
best_teams = np.array(best_individual) + 1  # Adding 1 to make team numbers start from 1
students_df['Team_Number'] = best_teams

# Save the updated DataFrame to a new CSV file
students_df.to_csv('updated_student_data_with_teams.csv', index=False)
print("Updated data saved to 'updated_student_data_with_teams.csv'")

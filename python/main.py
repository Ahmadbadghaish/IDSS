import numpy as np
import pandas as pd
import random
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

# GA:

def initialize_population(pop_size, student_count, team_count, min_team_size, max_team_size):
    """Initialize a population with team assignments within size constraints."""
    population = []
    for _ in range(pop_size):
        individual = []
        for team in range(team_count):
            team_size = random.randint(min_team_size, max_team_size)
            individual.extend([team] * team_size)
        individual = individual[:student_count]  # Trim if exceeds student count
        random.shuffle(individual)
        population.append(individual)
    return population


def team_composition(individual, students_df):
    """Evaluate the team composition based on roles, majors, and GPA."""
    team_roles = {team: Counter() for team in range(20)}
    team_majors = {team: Counter() for team in range(20)}
    team_gpa = {team: [] for team in range(20)}

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
        if team_gpa[team]:
            balance_score += abs(np.mean(team_gpa[team]) - students_df['GPA'].mean())
    return balance_score

def fitness(individual, students_df, min_team_size, max_team_size):
    """Calculate the fitness of an individual with penalty for size constraint violation."""
    team_sizes = Counter(individual)
    size_penalty = sum(abs(min_team_size - size) + abs(size - max_team_size) for size in team_sizes.values() if not (min_team_size <= size <= max_team_size))
    
    balance_score = team_composition(individual, students_df)
    return balance_score + size_penalty


def evolve(population, students_df, team_count, min_team_size, max_team_size, retain=0.2, random_select=0.05, mutate=0.01):
    graded = [(fitness(x, students_df, min_team_size, max_team_size), x) for x in population]
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

    # Mutation with team size check
    for individual in children:
        if mutate > random.random():
            team_counts = Counter(individual)
            team_to_reduce = random.choice([team for team in team_counts if team_counts[team] > min_team_size])
            team_to_increase = random.choice([team for team in team_counts if team_counts[team] < max_team_size])
            for i, team in enumerate(individual):
                if team == team_to_reduce:
                    individual[i] = team_to_increase
                    break

    parents.extend(children)
    return parents

























# main

# Read CSV file into DataFrame
df = pd.read_csv('data_scores_GPA_major.csv', delimiter=',')

# Assign each of 5 people in a team randomly
num_teams = 20
team_numbers = np.random.randint(1, num_teams + 1, size=len(df))
df['Team number'] = team_numbers

# Drop the first column
# df = df.drop(df.columns[0], axis=1)

# Define target average and function to generate team scores
target_average = 70  # Desired average score

def generate_team_score(target_average, team_size):
    total = target_average * team_size
    min_score = max(0, total - 100 * (team_size - 1))
    max_score = min(100, total)
    return random.randint(min_score, max_score)

# Create a new column with team scores
team_scores = {}
for team_number, team_data in df.groupby('Team number'):
    team_size = len(team_data)
    team_scores[team_number] = generate_team_score(target_average, team_size)

df['Team Score'] = df['Team number'].map(team_scores)

# Calculate mean and standard deviation for each BIG 5 score
stats_cols = ['neuroticism_scores', 'extroversion_scores', 'openness_scores', 'agreeableness_scores', 'conscientiousness_scores']
means = df[stats_cols].mean()
std_devs = df[stats_cols].std()

# Print the statistics
print("Mean and Standard Deviation for each score:")
print(means)
print(std_devs)


# Determine the optimal number of clusters using Silhouette and Davies-Bouldin indices
k_vals = range(2, 15)
sShil_max = np.empty([len(k_vals), 1])
sDaBo_min = np.empty_like(sShil_max)

for i, n in enumerate(k_vals):
    kmeans = KMeans(n_clusters=n, max_iter=1000, n_init=10, random_state=0).fit(df[stats_cols])
    sShil_max[i] = metrics.silhouette_score(df[stats_cols], kmeans.labels_)
    sDaBo_min[i] = metrics.davies_bouldin_score(df[stats_cols], kmeans.labels_)

# Perform KMeans clustering with the selected number of clusters (e.g., 3)
kmeans = KMeans(n_clusters=3, random_state=100)
kmeans.fit(df[stats_cols])
df['cluster'] = kmeans.labels_

# Assign roles based on clusters
role_assignment = {0: 'Executor', 1: 'Collaborator', 2: 'Innovator'}
df['role_in_project'] = df['cluster'].map(role_assignment)

# Decision Tree Classifier for Role prediction
X = df[stats_cols]
y = df['role_in_project']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

dt_classifier = DecisionTreeClassifier(random_state=0, criterion='entropy')
dt_classifier.fit(X_train, y_train)
y_pred = dt_classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)
print(f'Accuracy: {accuracy}')
print('Classification Report:\n', classification_rep)

# Save the processed DataFrame to an CSV file
# df.to_excel('adjusted_results.xlsx', index=False)
# df.to_csv('generated_data_GPA_role.csv', index=False)







# GA main:
# df = pd.read_csv('generated_data_GPA_role.csv')

# Assuming your CSV file is correctly formatted, you can use the DataFrame directly
student_count = len(df)  # Total number of students
team_count = 20                   # Number of teams
pop_size = 100                   # Population size

min_team_size = 4  # Example minimum team size
max_team_size = 6  # Example maximum team size

# Initialize population with the specified team size range
population = initialize_population(pop_size, student_count, team_count, min_team_size, max_team_size)

fitness_over_generations = []

# Evolve the population
for i in range(50):
    population = evolve(population, df, team_count, min_team_size, max_team_size)
    best_individual = min(population, key=lambda ind: fitness(ind, df, min_team_size, max_team_size))
    best_fitness = fitness(best_individual, df, min_team_size, max_team_size)
    print(f"Generation {i+1}: Best Fitness = {best_fitness}")
    fitness_over_generations.append(best_fitness)

# Identify and print the best team distribution after the final evolution
best_individual = min(population, key=lambda ind: fitness(ind, df, min_team_size, max_team_size))
best_teams = Counter(best_individual)
print("Best Team Distribution:", best_teams)

# Optionally, print detailed information about each team
for team in range(team_count):
    team_members = df.iloc[np.where(np.array(best_individual) == team)]
    print(f"\nTeam {team + 1} Members:")
    print(team_members)


if len(best_individual) == len(df):
    best_teams = np.array(best_individual) + 1  # Teams start from 1
else:
    print("Mismatch in team assignments. Assigning remaining students randomly.")
    best_teams = np.array(best_individual[:len(df)]) + 1
    for _ in range(len(df) - len(best_individual)):
        best_teams = np.append(best_teams, random.randint(1, team_count))

df['Team_Number'] = best_teams

# Save the updated DataFrame to a new CSV file
df.to_csv('updated_student_data_with_teams.csv', index=False)
print("Updated data saved to 'updated_student_data_with_teams.csv'")


# Plotting the fitness over generations
plt.plot(fitness_over_generations)
plt.title('Fitness Over Generations')
plt.xlabel('Generation')
plt.ylabel('Best Fitness')
plt.show()
import pandas as pd
import random
from deap import base, creator, tools, algorithms
# from scipy.stats import variance
import numpy as np


# Person class
class Person:
    def __init__(self, identifier, scores):
        self.id = identifier
        self.scores = scores  # scores is a dictionary of trait scores

# Fitness Function
def evaluate(individual, all_people, num_teams):
    team_scores = {i: 0 for i in range(num_teams)}
    team_counts = {i: 0 for i in range(num_teams)}

    # Aggregate scores for each team
    for person_idx, team in enumerate(individual):
        team_scores[team] += all_people[person_idx].scores['Extroversion']
        team_counts[team] += 1

    # Calculate variance of average scores
    avg_scores = [team_scores[i] / team_counts[i] if team_counts[i] > 0 else 0 for i in range(num_teams)]
    score_variance = np.var(avg_scores)

    # Minimize the variance
    return -score_variance,

# Reading data from Excel file
def load_data_from_excel(file_path):
    df = pd.read_excel(file_path)
    all_people = []
    for _, row in df.iterrows():
        identifier = row['ID']
        scores = {'Extroversion': row['Extroversion']}  # Add more traits if available
        all_people.append(Person(identifier, scores))
    return all_people

file_path = 'adjusted_results.xlsx'  # Replace with your file path
all_people = load_data_from_excel(file_path)

# GA parameters
num_individuals = len(all_people)
num_teams = 5  # Adjust as needed

# Genetic Algorithm Setup
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
toolbox.register("attr_team", random.randint, 0, num_teams - 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_team, n=num_individuals)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate, all_people=all_people, num_teams=num_teams)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

# Running the Genetic Algorithm
def run_ga():
    pop = toolbox.population(n=50)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=50, stats=stats, halloffame=hof)
    return pop, log, hof

pop, log, hof = run_ga()

# Best solution
best_team_assignment = hof[0]

# Assign individuals to teams based on the best solution
teams = {i: [] for i in range(num_teams)}
for person_idx, team in enumerate(best_team_assignment):
    teams[team].append(all_people[person_idx])

# Output the team assignments
for team, members in teams.items():
    print(f"Team {team}: {[person.id for person in members]}")

from constraint import Problem

# Define a simple CSP for team assignments

# Assuming you have a list of all people called all_people and a specified number of teams
team_count = 5  # Change as needed
teams = range(1, team_count + 1)

# Initialize problem
problem = Problem()

# Variables: For each person, we set their domain to be any of the teams
for person in all_people:
    problem.addVariable(person.id, teams)

# Constraints
# 1. No two persons with High on a given trait can be in the same team
for trait in ['Neuroticism', 'Extroversion', 'Openness', 'Agreeableness', 'Conscientiousness']:
    high_trait_persons = [person for person in all_people if person.levels[trait] == 'High']
    
    for i in range(len(high_trait_persons)):
        for j in range(i+1, len(high_trait_persons)):
            problem.addConstraint(lambda i, j: i != j, (high_trait_persons[i].id, high_trait_persons[j].id))

# You can add more constraints as needed

# Solve
solutions = problem.getSolutions()

# Note: The above will give all possible solutions. If you want only one solution, you can simply use:
# solution = problem.getSolution()

if solutions:
    print("One of the possible team assignments:")
    for person_id, team in solutions[0].items():
        print(f"Person ID {person_id} is in Team {team}")
else:
    print("No solutions found!")


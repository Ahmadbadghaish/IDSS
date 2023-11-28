import csv
from constraint import Problem
from statistics import mean, stdev

class Person:
    def __init__(self, identifier, neuroticism, extroversion, openness, agreeableness, conscientiousness, major):
        self.id = identifier
        # self.name = name
        self.scores = {
            'Neuroticism': neuroticism,
            'Extroversion': extroversion,
            'Openness': openness,
            'Agreeableness': agreeableness,
            'Conscientiousness': conscientiousness
        }
        self.major = major  # Add this line

        self.levels = {
            'Neuroticism': None,
            'Extroversion': None,
            'Openness': None,
            'Agreeableness': None,
            'Conscientiousness': None
        }

    def classify_trait(self, trait, µ, σ):
        # Classify trait based on mean and standard deviation
        score = self.scores[trait]
        if score > (µ + σ):
            self.levels[trait] = 'High'
        elif score < (µ - σ):
            self.levels[trait] = 'Low'
        else:
            self.levels[trait] = 'Medium'
    
    def classify_all_traits(self, means, stdevs):
        # Classify all traits
        for trait in self.scores.keys():
            self.classify_trait(trait, means[trait], stdevs[trait])

class Team:
    # Team class to group persons into teams
    def __init__(self, team_name):
        self.team_name = team_name
        self.members = []

    def add_member(self, person):
        # Add a person to the team
        if isinstance(person, Person):
            self.members.append(person)
        else:
            raise TypeError("Must add an instance of Person.")

    def calculate_team_scores(self):
        # Calculate team scores and standard deviations
        total_scores = {
            'Neuroticism': [],
            'Extroversion': [],
            'Openness': [],
            'Agreeableness': [],
            'Conscientiousness': []
        }
        for member in self.members:
            for trait, score in member.scores.items():
                total_scores[trait].append(score)
        
        avg_scores = {trait: mean(scores) for trait, scores in total_scores.items()}
        stdev_scores = {trait: stdev(scores) for trait, scores in total_scores.items()}
        
        return avg_scores, stdev_scores

    def get_team_info(self):
        # Print team information
        print(f"Team Name: {self.team_name}")
        print("Members:")
        for member in self.members:
            print(f" - {member.name} (ID: {member.id})")
            for trait in member.scores:
                print(f"   {trait} Score: {member.scores[trait]}, Level: {member.levels[trait]}")

# Function to set up and solve the CSP
def solve_csp(all_people, team_count=5):
    problem = Problem()
    teams = range(1, team_count + 1)

    # Assign each person to a team
    for person in all_people:
        problem.addVariable(person.id, teams)

    # Constraint: No two persons with 'High' on the same trait in the same team
    for trait in ['Neuroticism', 'Extroversion', 'Openness', 'Agreeableness', 'Conscientiousness']:
        high_trait_people = [person for person in all_people if person.levels[trait] == 'High']
        
        for i in range(len(high_trait_people)):
            for j in range(i + 1, len(high_trait_people)):
                problem.addConstraint(lambda x, y: x != y, (high_trait_people[i].id, high_trait_people[j].id))

    # Get one solution
    solution = problem.getSolution()

    if solution:
        return solution
    else:
        return "No solutions found!"

# Example: Reading data and classifying people
all_people = []

with open('C:\\Users\\badgh\\Desktop\\IDSS\\generated_data.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        person = Person(
            identifier=row['ID'],  # Make sure this matches the parameter in the __init__ method
            neuroticism=float(row['neuroticism_scores']),
            extroversion=float(row['extroversion_scores']),
            openness=float(row['openness_scores']),
            agreeableness=float(row['agreeableness_scores']),
            conscientiousness=float(row['conscientiousness_scores']),
            major=row['major']
        )
        all_people.append(person)


traits = ['Neuroticism', 'Extroversion', 'Openness', 'Agreeableness', 'Conscientiousness']
trait_scores = {trait: [] for trait in traits}

for person in all_people:
    for trait in traits:
        trait_scores[trait].append(person.scores[trait])

means = {trait: mean(scores) for trait, scores in trait_scores.items()}
stdevs = {trait: stdev(scores) for trait, scores in trait_scores.items()}

# Classify all traits for all people
for person in all_people:
    person.classify_all_traits(means, stdevs)

# Solve CSP to assign teams
team_assignments = solve_csp(all_people)

# Create Team objects and add members
if isinstance(team_assignments, dict):
    teams = {i: Team(f"Team {i}") for i in range(1, 6)}
    for person_id, team_number in team_assignments.items():
        person = next(p for p in all_people if p.id == person_id)
        teams[team_number].add_member(person)

    # Output team information
    for team in teams.values():
        team.get_team_info()
else:
    print(team_assignments)

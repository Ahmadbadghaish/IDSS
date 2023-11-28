from constraint import Problem


class Person:
    def __init__(self, id, neuroticism, extroversion, openness, agreeableness, conscientiousness, major):
        self.id = id
        self.scores = {
            'Neuroticism': neuroticism,
            'Extroversion': extroversion,
            'Openness': openness,
            'Agreeableness': agreeableness,
            'Conscientiousness': conscientiousness
        }
        # Add logic to determine the level based on scores
        self.levels = {trait: self.determine_level(score) for trait, score in self.scores.items()}
        self.major = major

    def determine_level(self, score):
        # Dummy implementation, replace with your own logic
        if score > 60:
            return 'High'
        elif score > 40:
            return 'Medium'
        else:
            return 'Low'


# Function to set up and solve the CSP
def solve_csp(all_people, group_size=5):
    problem = Problem()

    # Calculate the number of groups needed
    num_students = len(all_people)
    group_count = -(-num_students // group_size)  # Ceiling division

    # Assign groups (1 to group_count)
    groups = range(1, group_count + 1)

    # Set each student's domain to be any of the groups
    for person in all_people:
        problem.addVariable(person.id, groups)

    # Constraint: No two students with 'High' on the same trait in the same group
    for trait in ['Neuroticism', 'Extroversion', 'Openness', 'Agreeableness', 'Conscientiousness']:
        high_trait_students = [person for person in all_people if person.levels[trait] == 'High']
        
        for i in range(len(high_trait_students)):
            for j in range(i+1, len(high_trait_students)):
                problem.addConstraint(lambda x, y: x != y, (high_trait_students[i].id, high_trait_students[j].id))

    # Get one solution
    solution = problem.getSolution()

    if solution:
        print(solution)
        return solution
    else:
        return "No solutions found!"




import csv

all_people = []

with open('C:\\Users\\badgh\\Desktop\\IDSS\\generated_data.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        person = Person(
            id=row['ID'],
            neuroticism=float(row['neuroticism_scores']),
            extroversion=float(row['extroversion_scores']),
            openness=float(row['openness_scores']),
            agreeableness=float(row['agreeableness_scores']),
            conscientiousness=float(row['conscientiousness_scores']),
            major=row['major']
        )
        all_people.append(person)


group_assignment = solve_csp(all_people)

if group_assignment != "No solutions found!":
    # Output the group assignments in a more readable format
    for person_id, group in group_assignment.items():
        print(f"Person ID {person_id} is in Group {group}")
else:
    print(group_assignment)

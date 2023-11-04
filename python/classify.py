from statistics import mean, stdev

class Person:
    def __init__(self, identifier, name, scores=None):
        self.id = identifier
        self.name = name
        
        self.scores = scores or {
            'Neuroticism': 0,
            'Extroversion': 0,
            'Openness': 0,
            'Agreeableness': 0,
            'Conscientiousness': 0
        }
        
        self.levels = {
            'Neuroticism': None,
            'Extroversion': None,
            'Openness': None,
            'Agreeableness': None,
            'Conscientiousness': None
        }

    def classify_trait(self, trait, µ, σ):
        score = self.scores[trait]
        if score > (µ + σ):
            self.levels[trait] = 'High'
        elif score < (µ - σ):
            self.levels[trait] = 'Low'
        else:
            self.levels[trait] = 'Medium'
    
    def classify_all_traits(self, means, stdevs):
        for trait in self.scores.keys():
            self.classify_trait(trait, means[trait], stdevs[trait])



class Team:
    def __init__(self, team_name):
        self.team_name = team_name
        self.members = []

    def add_member(self, person):
        if isinstance(person, Person):
            self.members.append(person)
        else:
            raise TypeError("Must add an instance of Person.")

    def calculate_team_scores(self):
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
        print(f"Team Name: {self.team_name}")
        print("Members:")
        for member in self.members:
            print(f" - {member.name} (ID: {member.id})")
            for trait in member.scores:
                print(f"   {trait} Score: {member.scores[trait]}, Level: {member.levels[trait]}")



# person1 = Person(1, "Alice", {'Neuroticism': 10, 'Extroversion': 8, 'Openness': 9, 'Agreeableness': 7, 'Conscientiousness': 8})
# person2 = Person(2, "Bob", {'Neuroticism': 7, 'Extroversion': 9, 'Openness': 8, 'Agreeableness': 6, 'Conscientiousness': 9})

# person2.classify_trait('Openness')


# team = Team("Innovators")
# team.add_member(person1)
# team.add_member(person2)

# team.get_team_info()

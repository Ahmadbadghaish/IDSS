import random

# Generate random scores for a trait
def generate_scores(mean, std_dev, num_samples=100):
    return [round(random.gauss(mean, std_dev), 2) for _ in range(num_samples)]

# Number of individuals
num_individuals = 100

neuroticism_scores = generate_scores(21.65, 7.06, num_individuals)
extroversion_scores = generate_scores(51.02, 7.69, num_individuals)
openness_scores = generate_scores(44.24, 5.86, num_individuals)
agreeableness_scores = generate_scores(50.63, 8.51, num_individuals)
conscientiousness_scores = generate_scores(41.37, 5.80, num_individuals)

# Print the data in CSV format
print(f"{0},{'neuroticism_scores'},{'extroversion_scores'},{'openness_scores'},{'agreeableness_scores'},{'conscientiousness_scores'}")

for i in range(num_individuals):
    print(f"{i+1},{neuroticism_scores[i]},{extroversion_scores[i]},{openness_scores[i]},{agreeableness_scores[i]},{conscientiousness_scores[i]}")

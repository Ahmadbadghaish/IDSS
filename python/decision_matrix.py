import pandas as pd

# Step 1: Load the CSV data
# Replace 'path/to/your/file.csv' with the actual path to your CSV file
data = pd.read_csv('path/to/your/file.csv', delimiter='\t')  # assuming the data is tab-separated

# Step 2: Define the weights for each trait
weights = {
    'neuroticism_scores': 2,
    'extroversion_scores': 1,
    'openness_scores': 1,
    'agreeableness_scores': -1,
    'conscientiousness_scores': 4
}

# Step 3: Apply the weights to the scores and calculate a total weighted score
# Create a new DataFrame to store the weighted scores
weighted_scores = data.copy()

for trait, weight in weights.items():
    if trait in weighted_scores.columns:  # Check if the trait exists in the dataframe
        weighted_scores[trait] = data[trait] * weight

# Add a new column for the total score
weighted_scores['total_score'] = weighted_scores[list(weights.keys())].sum(axis=1)

# Step 4: Identify the potential leader
# Find the index of the individual with the highest total score
leader_index = weighted_scores['total_score'].idxmax()

# Get the ID of the potential leader from the original data
leader_id = data.iloc[leader_index]['ID']

# Print out the ID of the selected leader and their scores for review
print("Selected Leader ID:", leader_id)
print("Scores of the selected leader:")
print(data.iloc[leader_index])

# If you want to view the entire DataFrame with weighted scores and total scores, you can do so:
print("\nData with weighted scores:")
print(weighted_scores)

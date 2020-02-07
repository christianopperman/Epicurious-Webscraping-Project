import numpy as np
import pandas as pd

# Import scraped raw data
recipes = pd.read_csv("epicurious_final.csv")


##################################################
# Data Processing for Recipe Recommender App
##################################################

# Parse list of ingredients, which in the raw file is a single string, into a list of individual ingredients.
# Create a new column to show the number of ingredients used in the recipe, which will be used as a measure of recipe complexity.
recipes['ingredients'] = recipes['ingredients'].str.split('\t')
recipes['ingredients_length'] = recipes['ingredients'].str.len()

# Calculate the length of the recipe name, to generate a rough measure of how "complex" a recipe sounds
recipes['name_length'] = recipes['recipe'].str.len()

# Write datafile back to a .csv for use in the Shiny Recipe Recommender app
recipes.to_csv("epicurious_final_processed.csv")

############################################################
# Further Data Processing for Data Analysis & Visualization
############################################################

# Create a subset of the dataframe for correlation analysis
recipes_correlation = recipes[['calories', 'carbs', 'fat', 'protein', 'make_again',
    'rating', 'reviews', 'ingredients_length', 'keywords_length', 'name_length']]

# Remove rows where there reviews, ratings, and make again percentage were zero.
# Any recipe that was reviewed and strongly disliked would have had reviews present but a low score 
# for rating/make again percentage, so made sure not to exclude recipes that fell into that category.
recipes_correlation = recipes_correlation[(recipes_correlation['reviews'] != 0)
    & (recipes_correlation['rating'] != 0)
    & (recipes_correlation['make_again'] != 0)]

# Calculate the Pearson Correlation values between various discreet variables and recipe rating, make again 
# percentage, and review score
recipes_correlation.corr()[['rating', 'reviews', 'make_again']]
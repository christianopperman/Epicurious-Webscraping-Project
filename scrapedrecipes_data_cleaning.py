import numpy as np
import pandas as pd
import seaborn as sns
import re
from matplotlib import pyplot as plt
plt.style.use('ggplot')

# Import raw data
recipes = pd.read_csv("epicurious_final.csv")
inspections = pd.read_csv("DOHMH_New_York_City_Restaurant_Inspection_Results.csv")

##################################################
# Data Processing for Recipe Recommender App
##################################################

# Parse ingredients and keywords, which in the raw file are single strings, into lists.
# Create a new column to show the number of ingredients used in the recipe, which will be used as a measure of recipe complexity
recipes['ingredients'] = recipes['ingredients'].str.split('\t')
recipes['ingredients_length'] = recipes['ingredients'].str.len()
recipes['keywords'] = recipes['keywords'].str.split(',')

# Add the Italian keyword to recipes where Pasta is present as a keyword
for i in recipes['keywords']:
    if 'Pasta' in i:
        i.append("Italian")

# Remove any recipes with no ingredients or no keywords to eliminate junk data
recipes = recipes[np.logical_and(pd.notnull(recipes["ingredients_length"]), pd.notnull(recipes['keywords']))]

# Calculate the length of the recipe name, to generate a rough measure of how "complex" a recipe sounds
recipes['name_length'] = recipes['recipe'].str.len()

# Rename some unwieldy cuisine types in inspections dataset for more aesthetic visualization
inspections.replace('Latin (Cuban, Dominican, Puerto Rican, South & Central American)', 'Latin', inplace = True)
inspections.replace('Ice Cream, Gelato, Yogurt, Ices', 'Dessert', inplace = True)

# Generate list of unique cuisines from NYC Restaurant Inspection dataset.
cuisines = inspections["CUISINE DESCRIPTION"].str.strip().unique().tolist()

# Helper function to classify each recipe according to cuisine type.
# Create a new column with each recipe's cuisine type
def define_cuisine(x):
    for i in cuisines:
        if re.search(i , ''.join(x)):
            return i
    return "Unknown"

recipes['cuisine'] = recipes['keywords'].apply(define_cuisine)

# Generate list of unique keywords
keywords = recipes['keywords'].tolist()
keywords = list(set([item for sublist in keywords for item in sublist]))

# Write datafile back to a .csv for use in the Shiny Recipe Recommender app
recipes.to_csv("epicurious_final_processed.csv")




############################################################
# Further Data Processing for Data Analysis & Visualization
############################################################

# Create a subset of the dataframe for correlation analysis and remove rows with no reviews.
# Any recipe that was reviewed and strongly disliked would have had reviews present but a low score 
# for rating/make again percentage, so made sure not to exclude recipes that fell into that category.
recipes_correlation = recipes[['calories', 'carbs', 'fat', 'protein', 'make_again',
    'rating', 'reviews', 'ingredients_length', 'name_length']]
recipes_correlation = recipes_correlation[(recipes_correlation['reviews'] != 0)]

# Calculate the Pearson Correlation values between various discreet variables and recipe rating, make again 
# percentage, and review score
recipes_correlation.corr()[['rating', 'reviews', 'make_again']]

### Calculate frequency count of cuisines in both recipe and inspections dataset for visualizations
# Subset the recipe dataset by cuisine type and calculate frequency
# Dropped "Unknown" cuisines because it is of little interest to our question
recipe_cuisines = pd.DataFrame(recipes[recipes['cuisine'] != "Unknown"]['cuisine'].value_counts().reset_index())
recipe_cuisines = recipe_cuisines.rename(columns={"index": "Cuisine", "cuisine": "Count"})
recipe_cuisines['Percentage'] = recipe_cuisines['Count']/sum(recipe_cuisines['Count'])

# Subset the inspections dataset by cuisine type and calculate frequency
rest_cuisines = pd.DataFrame(inspections['CUISINE DESCRIPTION'].value_counts().reset_index())
rest_cuisines = rest_cuisines.rename(columns={"index": "Cuisine", "CUISINE DESCRIPTION": "Count"})
rest_cuisines['Percentage Restaurants'] = rest_cuisines['Count']/sum(rest_cuisines['Count'])
rest_cuisines = rest_cuisines[rest_cuisines['Cuisine'].isin(recipe_cuisines['Cuisine'].unique())].sort_values('Cuisine')

### Calculate summary statistics
# Subset the recipe dataset by cuisine type and calculate summary statistics for various variables
recipes_by_cuisine = recipes.groupby('cuisine')
summary_stats = recipes_by_cuisine[['rating', 'reviews', 'make_again', 'ingredients_length']].agg(['mean', 'std'])




############################################################
# Data Visualization
############################################################


# Visualize average recipe rating by cuisine type
ratings_by_cuisine = recipes_by_cuisine.mean()['rating'].reset_index().sort_values(
    'rating', ascending = False)
ratines_by_cuisine = ratings_by_cuisine.loc[ratings_by_cuisine['cuisine'] != 'Unknown']
plt.subplots(figsize = (8, 10))
sns.barplot(data = ratings_by_cuisine, y = 'cuisine', x = 'rating', color = "#cf625d")
plt.savefig('graphs/ratingbycuisine.pdf', bbox_inches='tight')

# Remove cuisines with too few recipes (less than 50) and re-graph the remaining cuisines' average rating
filtered_recipe_cuisines = pd.DataFrame(
    recipes_by_cuisine['cuisine'].count()[lambda x: x>50]).rename(
    {'cuisine': 'count'}, axis = 'columns').reset_index()
filtered_recipe_cuisines = filtered_recipe_cuisines.merge(
    ratings_by_cuisine, on = "cuisine", how = 'left').sort_values('rating', ascending = False).loc[filtered_recipe_cuisines['cuisine'] != 'Unknown']
plt.subplots(figsize = (8, 10))
sns.barplot(data = filtered_recipe_cuisines , y = 'cuisine', x = 'rating', color = "#cf625d")
plt.savefig('graphs/ratingbycuisine_filtered.pdf', bbox_inches='tight')


# Visualize distribution of recipes and restaurants by cuisine in the same chart
restaurant_and_recipe_cuisinecount = recipe_cuisines.merge(rest_cuisines, on = "Cuisine").drop(['Count_x', 'Count_y'], axis = 1)
plt.subplots(figsize = (8, 15))
tidy = restaurant_and_recipe_cuisinecount.melt(id_vars='Cuisine').rename(columns=str.title).sort_values('Value', ascending = False)
sns.barplot(data = tidy, x = "Value", y = "Cuisine", hue = "Variable").set(
	title = "Cuisine Breakdown: Recipes & Restaurants", xlabel = "Percentage")
plt.savefig('graphs/reciperestaurantcuisines.pdf', bbox_inches='tight')

# Visualize distribution of number of ingredients
sns.distplot(recipes["ingredients_length"], kde = False, hist_kws=dict(alpha=0.8)).set(
	xlabel="Number of Ingredients", title = "Distribution of Ingredient Number")
plt.savefig('graphs/ingredientnumberdist.pdf', bbox_inches='tight')

# Visualize distribution of number of ingredients by rating
sns.boxplot(y = 'ingredients_length', x = 'rating', data = recipes_correlation2, color = "#cf625f").set(
    title = "Distrubtion of Ingredients by Rating", xlabel = "Rating", ylabel = "Number of Ingredients")
plt.savefig('graphs/ingredientnumberdistbyrating.pdf', bbox_inches='tight')

# Visualize correlation between rating - all recipes
sns.lmplot("rating", "ingredients_length", recipes_correlation).set(
	title = "Rating vs. Number of Ingredients", xlabel = "Rating", ylabel = "Number of Ingredients")
plt.savefig('graphs/ratingvsingredientsnumber.pdf', bbox_inches='tight')



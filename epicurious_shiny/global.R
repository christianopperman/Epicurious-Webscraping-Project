library(shiny)
library(shinydashboard)
library(data.table)
library(dplyr)

#Import database
recipes = fread(file = "./data/recipes.csv", stringsAsFactors = F)

library(shiny)
library(shinydashboard)
library(data.table)
library(dplyr)

#Import database
recipes = fread(file = "../epicurious_final_processed.csv", stringsAsFactors = F)

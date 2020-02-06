function(input, output) {
  
  ########Data Processing########
  #Filter dataset by ingredients and keyword as supplied by the user
  recipe_df = reactive({
    if(input$mealtype == "All"){
      mealtype = ""}
    else{
      mealtype = input$mealtype
    }
    
    if(input$numingredients == ""){
      numingredients = ""}
    else{
      numingredients = input$numingredients
    }
    
    print(numingredients)
    
    if(input$ingredient1 == ""){
      ingredient1 = ""}
    else{
      ingredient1 = input$ingredient1
    }
    
    if(input$ingredient2 == ""){
      ingredient2 = ""}
    else{
      ingredient2 = input$ingredient2
    }

    if(input$ingredient3 == ""){
      ingredient3 = ""}
    else{
      ingredient3 = input$ingredient3
    }
    
    recipe_df = recipes %>% 
      filter(., grepl(mealtype, keywords, ignore.case = T)) %>%
      filter(., grepl(ingredient1, ingredients, ignore.case = T)) %>%
      filter(., grepl(ingredient2, ingredients, ignore.case = T)) %>%
      filter(., grepl(ingredient3, ingredients, ignore.case = T)) %>% 
      filter(., ingredients_length <= round(as.numeric(numingredients, digits = 0))) %>% 
      mutate(., Recipe = paste0("<a href =",url,">",recipe,"</a>"), `Number of Ingredients` = as.character(ingredients_length)) %>% 
      select(., Recipe, Rating = rating, `Make Again Percentage` = make_again, `Number of Ingredients`) %>% 
      arrange(., desc(Rating), desc(`Make Again Percentage`)) %>% 
      head(., n = as.integer(input$recipenumber))
  })
 
  output$table = renderTable({recipe_df()},  align = 'c', sanitize.text.function = function(x) x)
  
}
  
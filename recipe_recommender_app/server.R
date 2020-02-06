function(input, output) {
  
  ########Data Processing########
  #Filter dataset by ingredients and keyword as supplied by the user
  recipe_df = reactive({
    if(input$mealtype == "All"){
      mealtype = ""}
    else{
      mealtype = input$mealtype
    }
    
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
      select(., Recipe = recipe, Link = url, Rating = rating) %>% 
      arrange(., desc(Rating)) %>% 
      head(., n = as.integer(input$recipenumber))
  })
 
  output$table = renderTable({recipe_df()}, sanitize.text.function = function(x) x)
  
}
  
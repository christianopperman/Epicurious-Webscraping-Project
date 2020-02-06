dashboardPage(skin = "red",
  
  # Define header with app title, author name, and links to GitHub and LinkedIn accounts
  dashboardHeader(
    title="Your Recipe Finder",
    tags$li("Christian Opperman", 
            style = "padding-right: 15px; padding-top: 15px; font-weight: bold; font-size: 13px",
            class = "dropdown"),
    tags$li(a(href="https://github.com/christianopperman", icon("github-square")),
            style = "font-size: 20px",
            class = "dropdown"),
    tags$li(a(href="https://www.linkedin.com/in/christian-opperman/", icon("linkedin")),
            style = "font-size: 20px",
            class = "dropdown")
  ),
  
  
  # Define sidebar with relevant tab options for navigation
  dashboardSidebar(
    sidebarUserPanel("Christian Opperman",
                     subtitle = "Fellow @ NYCDSA",
                     image = "Me.jpg"),
    
    sidebarMenu(id = "sidebar",
      menuItem("Recipe Recommender", tabName = "recipes", icon = icon("list")),
      menuItem("About", tabName = "about", icon = icon("info"))
      
    )
  ),
  
  
  # Define body with tabs to be selected in the sidebar
  dashboardBody(
    
    tabItems(
      #Define tab that contains spots for user input the recipe recommender
      tabItem(tabName = "recipes",
              #Row that contains summary info boxes displaying most murderous state and the average murders (both in murders/1000 people)
              fluidRow(
                box(width = 5,
                  column(12,
                       selectizeInput("mealtype", label = "Which Meal Are You Making?", choices = c("All", "Breakfast", "Lunch", "Dinner")),
                       textInput("recipenumber", label = "How Many Choices Would You Like?", value = 0),
                       textInput("ingredient1", label = "First Ingredient?"),
                       textInput("ingredient2", label = "Second Ingredient?"),
                       textInput("ingredient3", label = "Third Ingredient?"))),
                box(width = 7,
                column(12,
                       tableOutput("table")))
              )),
      
      #Define tab that contains information about the data set and myself
      tabItem(tabName = "about",
              box(width = 12,
              fluidRow(
                #Column describing the underlying myself
                column(6, offset = 3, align = "center",
                       tagList(tags$img(src = "Me.jpg",
                                        width = "50%",
                                        style="border-radius: 50%"),
                               tags$br(),
                               tags$h4("About the Creator"),
                               tags$br(),
                               "Christian Opperman is a data scientist and analyst based in New York City. 
                               Originally from South Africa, he was raised in the Bay Area, California, and after
                               college lived in Tokyo, Japan, working in the energy sector, for a number of years
                               before moving back to the U.S.", 
                               tags$br(),
                               tags$br(),
                               "Please feel free to explore Christian's ",
                               tags$a("GitHub Account", href = "https://github.com/christianopperman"), 
                              "or ", 
                              tags$a("LinkedIn Profile", href = "https://www.linkedin.com/in/christian-opperman/"), 
                              ".")
                       )
                )
              )
      ))
    )
  )

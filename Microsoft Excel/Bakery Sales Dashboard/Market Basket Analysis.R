
#install.packages("arules")
#install.packages("arulesViz")
# install.packages("tidyverse")
# install.packages("lubridate")

library(arules)
library(arulesViz)
library(lubridate)
library(tidyverse)
library(readxl)

# Read Data from Excel 
bakery_sales <- read_excel("Dashboard.xlsx", sheet = "Bakery Sales Data" )
print(bakery_sales)

# Dropping the specified columns
bakery_sales_basket <- subset(bakery_sales, select = -c(datetime, time, `day of week`, `total sales`))
print(bakery_sales_basket)

# Convert to binary
bakery_sales_basket_binary <- as.data.frame(lapply(bakery_sales_basket, function(x) ifelse(!is.na(x) & x > 0, 1, 0)))
print(bakery_sales_basket_binary)

# Convert to transactions
transactions <- as(as.matrix(bakery_sales_basket_binary), "transactions")
print(transactions)

itemFrequencyPlot(transactions, topN = 10, type = "absolute")

# Apply the apriori algorithm
rules <- apriori(transactions, parameter = list(supp = 0.01, conf = 0.8))
inspect(rules)

# # Graph plot
# plot(rules, method = "graph", control = list(type = "items"))
# 
# # Grouped matrix plot
# plot(rules, method = "grouped")
# 
# # Matrix plot
# plot(rules, method = "matrix", control = list(reorder = TRUE))





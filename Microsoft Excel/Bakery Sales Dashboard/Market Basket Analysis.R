
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

# Item Frequency
# x <- bakery_sales_basket
# y <-
# barplot()



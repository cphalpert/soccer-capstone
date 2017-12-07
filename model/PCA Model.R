##main source: https://www.r-bloggers.com/performing-principal-components-regression-pcr-in-r/

setwd("~/Documents/MH/Columbia/CAPSTONE/soccer")

library(tidyverse)
library(modelr)
library(pls)

# read data
data <- read_csv('pca_data.csv')

data.train <- data %>% select(-X1) %>% filter(season!=2015)
data.test <- data %>% select(-X1) %>% filter(season==2015)

pcr_model <- pcr(market_val~., data = data.train, scale = TRUE, validation = "CV")

summary(pcr_model)

# Plot the RMSE
validationplot(pcr_model)

# Plot the R2
validationplot(pcr_model, val.type = "R2")

#test set
y_test = data.test$market_val
x_test = data.test %>% select(-market_val)

#set number of principal components to 30
pcr_pred <- predict(pcr_model, x_test, ncomp = 30)

#RMSE
sqrt(mean((pcr_pred - y_test)^2))



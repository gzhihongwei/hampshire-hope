## SCRIPT FOR SCARPING THE OPIOD DEATH PDF ##

# Number of Opioid-Related Overdose Deaths, All Intents by City/Town 2015-2019 #

rm(list = ls())

# libraries needed
library(pdftools)
library(tidyverse)
library(usmap)

## Loading the Data ## 

# extracting the pdf
opiodData <- pdf_text("Opioid-related-Overdose-Deaths-by-City-Town-June-2020.pdf")
head(opiodData)

# we can remove the last rows because the last page doesn't have the data we want
opiodData <- opiodData[-length(opiodData)]

# then we want to separate the data based on newlines, so
lineOpiodData <- unlist(strsplit(opiodData, "\n"))
head(lineOpiodData)

## isolating the data ##

lineData <- lineOpiodData[grep("[123456789]", lineOpiodData, invert = F)]
# this isolates all data lines with numbers
lineData1 <- lineData[-c(1:8)]
lineData2 <- lineData1[grep("          ", lineData1)] 
# when converting from pdf to lines, the values in the table have large 
# spaces in between them, so this identifies those lines
# this could probably be done more smoothly but
lineData3 <- lineData2[grep("2015", lineData2, invert = T)] 
# gets rid of the year headers
lineData4 <- str_replace(lineData3, "^ *", "")
# gets rid of spaces in front of the lines
lineData5 <-lineData4[grep("^[123456789]", lineData4, invert = T)]
# this gets rid of page number lines

## Converting into a data frame ##

# splitting the data
dataList <- str_split(lineData5, "\\s{2,}")
allData <- unlist(dataList)

# creating an empty data frame
dataFrame <- as.data.frame(matrix(rep(NA, length(allData)), nrow = length(lineData5)))

# iterating over to fill the data frame
for(i in 1:length(dataList)) {
  dataFrame[i, ] <-dataList[[i]]
}

colnames(dataFrame) <- c("City/Town Name", "2015", "2016", "2017", "2018", "2019")

# Now we want to split the data into the two tables
(totals <- which(dataFrame$`City/Town Name` == "Total"))
# so, after the 2nd table starts at row 322

table1 <- dataFrame[1:totals[1], 1:6]
tot <- totals[1] + 1
table2 <- dataFrame[tot:totals[2], 1:6]

# we need to fix table 2 a little bit
rownames(table2) <- c(1:nrow(table2))

## Time to Convert to .csv files ##
write.csv(table1, "table1.csv")
write.csv(table2, "table2.csv")

# to consider: 
  # https://stackoverflow.com/questions/36685805/how-to-find-the-county-for-each-city-in-a-vector-of-city-names-using-r




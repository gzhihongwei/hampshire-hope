# parsing Bus Route Data

# potential libraries
library(dbplyr)
library(RSQLite)
library(tidyverse)


routesData <- readLines("getvisibleroutes.xml", warn = FALSE)
routesData[1]

# creating list of variables to extract
route.vars <- c("Color", "GoogleDescription", "IncludeInGoogle", 
                "IsHeadway", "IsVisible", "LongName", "RouteAbbreviation", 
                "RouteRecordId", "ShortName", "SortOrder")
  # did NOT include: Group i:nil, IvrDescription, Messages, RouteTraceFilename, 
    # RouteTraceHash64 i:nil, Stops 1:nil, or TextColor because they seem unnecessary
  # did NOT include RouteId in this sequence, because there are some other 
    # complications later

# function to extract this info from routes
getRouteFilled <- function(field, dat) {
  
  # extracting nec lines
  str.pattern <- paste("<", field, ">", "(.*?)", "</", field, ">", sep ="")
  matches <- gregexpr(text = dat, pattern = str.pattern)
  matches.lines <- unlist(regmatches(dat, matches))
  
  # splitting the lines 
  str.pattern <- paste("<", field, ">", sep = "")
  first.sep <- unlist(strsplit(matches.lines, str.pattern))
  str.pattern2 <- paste("</", field, ">", sep = "")
  second.sep <- unlist(strsplit(first.sep, str.pattern2))
  
  # getting rid of unwanted lines
  ext.field <- second.sep[grep("<", second.sep, invert = T)]
  
  return(ext.field)
}

# checking what the length is for the data frame
N1 <- length(getRouteFilled(route.vars[3], routesData))

# creating an empty data frame
routes.df <- as.data.frame(matrix(NA, ncol = length(route.vars), nrow = N1))
colnames(routes.df) <- route.vars

# iterating over variables
for(i in 1:length(route.vars)){
  routes.df[,i] <- getRouteFilled(route.vars[i], routesData)
}

head(routes.df)

# now, to join the RouteID

# first, splitting the original data by route
route.matches <- gregexpr(text = routesData, pattern = "<Route>(.*?)</Route>")
route.lines <- unlist(regmatches(x = routesData, m = route.matches))
head(route.lines)

# extracting RouteId
RouteIds <- getRouteFilled(field = "RouteId", dat = route.lines)
head(RouteIds) # this just checking it for me
length(RouteIds) 

# extracting the unique ones because there are duplicates
RouteId <- unique(RouteIds)

# binding them 
routes.df <- cbind(RouteId, routes.df)

### Now, to deal with the vehicle data ###

# extracting the vehicle data from the route list data
vehicle.matches <- gregexpr(text = route.lines, pattern = "<Vehicles>(.*?)</Vehicles>")
vehicle.lines <- regmatches(x = route.lines, m = vehicle.matches)
head(vehicle.lines)

vehicle.vars <- c("BlockFareboxId", "Destination", "Deviation", "Direction", 
                  "DirectionLong", "Heading", "LastStop", "LastUpdated", 
                  "Latitude", "Longitude", 
                  "Name", "RouteId", "TripId", "VehicleId")
  # did NOT include: CommStatus, DisplayStatus, DriverName, GPSStatus, 
    # OnBoard, OpStatus, or Speed

# checking what the length is for the data frame
N2 <- length(getRouteFilled(vehicle.vars[1], vehicle.lines))

# creating an empty data frame
vehicles.df <- as.data.frame(matrix(NA, ncol = length(vehicle.vars), nrow = N2))
colnames(vehicles.df) <- vehicle.vars

# iterating over variables
for(i in 1:length(vehicle.vars)){
  vehicles.df[,i] <- getRouteFilled(vehicle.vars[i], vehicle.lines)
}

## Now, we join the data frames ##

# this matches all the data in the vehicles.df to the data in routes.df by their 
  # unique RouteId
PVTA_Route_df <- inner_join(routes.df, vehicles.df, by = "RouteId")

# turning the main Route Info into a csv
write.csv(PVTA_Route_df, "PVTA_Route_Data.csv")

       
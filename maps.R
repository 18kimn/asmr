library(sf)
library(tidyverse)

queryable_points <- read_csv("outputs/filtered_queryable_points.csv") |> 
  st_as_sf(coords = c("lon", "lat"))

ggplot(queryable_points) + 
  geom_sf(size = 0.2) + 
  theme_void() 
  theme(axis.text = element_blank(),
        axis.ticks = element_blank()
        )

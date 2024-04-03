library(sf)
library(tidyverse)
library(mapboxapi)
library(ggspatial)

main_outline <- st_read("inputs/Detroit_Boxes.geojson")
madheights <- st_read("inputs/madison_heights_strip_mall.geojson")

filtered_queryable_points <- read_csv("outputs/filtered_queryable_points.csv") |> 
  st_as_sf(coords = c("lon", "lat")) |> 
  st_set_crs(st_crs(madheights))
queryable_points <- read_csv("outputs/queryable_points.csv") |> 
  st_as_sf(coords = c("lon", "lat")) |> 
  st_set_crs(st_crs(madheights))

make_map <- function(input, zoom = 15, buffer_dist = 100, ...){
  tiles <- get_static_tiles(
    location = st_bbox(input),
    zoom = zoom,
    buffer_dist = buffer_dist,
    style_url = "mapbox://styles/18kimn/cluc3xqxi02bg01qq6wm55qq4"
  )
  
  ggplot(input) + 
    layer_spatial(tiles) + 
    geom_sf(...) + 
    theme_void() 
}

outline_plot <- make_map(main_outline, 11)
ggsave("figures/figure_1.png", outline_plot)

madheights_plot <- make_map(madheights, fill = NA)
ggsave("figures/figure_1a.png", madheights_plot)

madheights_points_plot <- make_map(madheights, fill = NA) + 
  geom_sf(data = filtered_queryable_points, size = 0.1)
ggsave("figures/figure_1b.png", madheights_points_plot)


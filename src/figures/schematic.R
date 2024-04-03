library(tidyverse)
library(magick)
library(sf)
library(ggrepel)

madheights <- st_read("inputs/madison_heights_strip_mall.geojson")
queryable_points <- read_csv("outputs/filtered_queryable_points.csv") |> 
  st_as_sf(coords = c("lon", "lat")) |> 
  st_set_crs(st_crs(madheights))
market_168 <- st_point(x = c(-83.108841, 42.5307229)) |> 
  st_geometry() |> 
  st_set_crs(st_crs(queryable_points))
images_168 <- queryable_points |> 
  select(panoid) |> 
  distinct() |> 
  mutate(dist_168 = st_distance(geometry, market_168)) |> 
  arrange(dist_168) |> 
  slice_head(n = 20)

scraped <- list.files("outputs/csvs", full.names = TRUE) 
  map_dfr(~read_csv(., col_types = cols(.default = "c"))) |> 
  filter(str_detect(text, "168")) |> 
  pull(filename) |> 
  unique() |> 
  str_remove("\\.jpg")

dta_168 <- c(images_168$panoid, basename(scraped)) |> 
  unique() |> 
  map_dfr(\(panoid){
    img_filename <- paste0("outputs/stitched/", panoid, ".jpg")
    data_filenames <- list.files("outputs/csvs", full.names = TRUE, pattern = panoid)
    if(length(data_filenames) == 0) return()
    message("Processing ", panoid)
    dta <- map_dfr(data_filenames, 
                   ~read_csv(., col_types = cols(
                     left = col_number(),
                     top = col_number(),
                     width = col_number(),
                     height = col_number(),
                     .default = "c"))) |> 
      filter(!is.na(text), nchar(text) > 3, width > 50, text != "Google", lang != "urd") 
    if(nrow(dta) == 0){
      return()
    }
    
    image <- image_read(img_filename)
    info <- image_info(image)
    
    plot_168 <- plot <- ggplot() + 
      annotation_raster(image, xmin = 0, xmax = info$width, ymin = 0, ymax = info$height) +
      geom_rect(data = dta, aes(xmin = left, xmax = left + width,
                                ymin = info$height - top - height, ymax = info$height - top),
                color = "red", size = 0.2) +
      geom_label_repel(data = dta,
                       max.overlaps = 20,
                       segment.size = 2,
                       min.segment.length = Inf,
                       force_pull = 0.5, aes(
        x = left, y = info$height - top - height/2, label = text
      )) + 
      coord_cartesian(xlim = c(0, info$width), ylim = c(0, info$height)) +
      theme_void()
    ggsave(paste0("figures/examples/", panoid, ".png"),
           plot_168)
    return(dta)
  })

# Just copying over unmarked images into a separate directory
walk(c(images_168$panoid, basename(scraped)), \(panoid){
  file.copy(paste0("outputs/stitched/", panoid, ".jpg"),
            paste0("figures/168/", panoid, ".jpg"))
})


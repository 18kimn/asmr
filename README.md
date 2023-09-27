# ASMR Displacement and Movement Metric Gathering

This repository contains the in-progress codebase for gathering data
and metrics for displacement of Asian businesses in Southeast
Michigan.

To get started, you will need a working knowledge and the installation
of [Git](https://git-scm.com), [Poetry](https://python-poetry.org/),
[DVC](https://dvc.org). It also helps to have understandings of OCR,
color analysis, and web scraping. You can look any and all of these
things up on Google, or just contact Nathan at ncyk[at]umich.edu and
he will gladly go over the project with you.

## Data storage

The
[Google Drive folder](https://drive.google.com/drive/u/1/folders/1-3OHZZUUuHfRH3hZ9sIPORwP9NINbrMI)
is now mainly used as a backend for data storage, since data files and
especially the relatively large number of non-newline-delimited files
(JPGs and shapefiles) in this project are best stored outside of Git.
Git is best for storing files where code is written and collaborators
can compare different (human) edits to code, not for comparing machine
output of complicated binary formats like images. And hosts like Github
place limits on file storage that are quite conservative for any data
project, at 50MB for a single file and about 5GB for the entire
project. For reference, our outputs folder at the time of writing is
about 50GB in total size.

So instead, this project uses [DVC](https://dvc.org), or "data version
control", which creates tiny hashes of your data and then checks those
hashes into Git. When the data changes, the hashes change too, and
checking the hashes into Git again allows you to document when your
data has changed alongside the code changes that resulted in changes
to data. The data itself still exists on your computer, but is not
uploaded to any Git-based repository; instead, it is uploaded onto
"backends" that store data, which in our case is our
[Google Drive folder](https://drive.google.com/drive/u/1/folders/1-3OHZZUUuHfRH3hZ9sIPORwP9NINbrMI)
(see the "files" folder within). DVC manages that pretty much entirely
on its own, so to minimize the chance for error, please do not touch
that folder manually or handle any data storage besides through DVC.

To get started with DVC:

1. Run through steps 1-3 for Poetry below to install DVC.
2. Run `dvc pull` to get everything, or (if you know what you are looking for)
    you can specify the filename as an argument (like `dvc pull inputs/area_of_interest_zctas.csv`).

## Poetry

I've scaffolded this project using Poetry, which I find the least
frustrating out of the numerous Python package and environment
management tools. A package maangement tool is indeed necessary for a
somewhat sane and reproducible development environment when working
with a project like this; you need to ensure you have the same tools
as a collaborator or the code will not run.

To get started with Poetry:

1. [Install Poetry.](https://python-poetry.org/docs/#installation)
2. Open a terminal at the root of the project and run
   `poetry install`.
3. Open a shell with `poetry shell`, which should now have the correct
   versions of Python, Python packages, and dvc made available to you.
4. Add new packages with `poetry add <package-name>`. For anything
   more complicated, refer to
   [the docs](https://python-poetry.org/docs/basic-usage/).

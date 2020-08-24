# Movieman
Movieman is a **D**jango **R**est **F**ramework based simple movie app. Feature of this app inlcudes :
- Scapres the imdb website urls for movie information. Example: https://www.imdb.com/chart/top/
- Maintains the scraped movie information in a lightweight sqlite database.
- Users can mantain the list of movies they have watched or going to watch.

## Setup Instructions
1. Setup the conda environment using `environment.yml`.

        conda env create -f environment.yml

2. Activate the conda environment.

        conda activate DRF

3. Run the app in development mode.

        python manage.py runserver

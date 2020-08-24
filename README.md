# Movieman
Movieman is a **D**jango **R**est **F**ramework based simple movie app. Features of this app inlcudes:
- Scrapes the IMDB website pages for movie information. URL example: https://www.imdb.com/chart/top/.
- Maintains the scraped movie information in a lightweight sqlite database.
- Users can mantain the list of movies they have watched or going to watch.

## Setup Instructions
1. Setup the conda environment using `environment.yml`.

        conda env create -f environment.yml

2. Activate the conda environment.

        conda activate DRF

3. Make the database migrations.

        python manage.py makemigrations
        python manage.py migrate

4. Create an admin user.

        python manage.py createsuperuser

    On creating an admin user, a token will be generated automatically. This token is required for subsequent API requests.

5. Run the server in development mode.

        python manage.py runserver

## Swagger API Docs
- *URL :* http://127.0.0.1:8000/api-docs/
- *Admin URL :* http://127.0.0.1:8000/admin/

## Contact
- [Rishabh Jain](mailto:rj8130950@gmail.com)
import os
from pathlib import Path
from dagster_dbt import DbtProject

# Especifica la ruta al directorio que contiene profiles.yml
#os.environ["DBT_PROFILES_DIR"] = "/Users/andresjaromezuk/.dbt/"

RELATIVE_PATH_TO_MY_DBT_PROJECT = "../../../dbt/db_postgres"

my_project = DbtProject(
    project_dir=Path(__file__).joinpath("..", RELATIVE_PATH_TO_MY_DBT_PROJECT).resolve(),
)
my_project.prepare_if_dev()
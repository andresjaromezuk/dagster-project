from dagster import Definitions, load_assets_from_modules, load_assets_from_package_module, define_asset_job, AssetSelection, AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets
from dagster import EnvVar,AssetKey
from dagster_airbyte import AirbyteCloudResource,build_airbyte_assets
from pathlib import Path
from recommender_system.project import my_project


airbyte_instance = AirbyteCloudResource(
    client_id=EnvVar("AIRBYTE_CLIENT_ID"),
    client_secret=EnvVar("AIRBYTE_CLIENT_SECRET") 
)

from recommender_system.configs import job_data_config, job_training_config

from recommender_system.assets import (
 airbyte_assets, core_assets, recommender_assets, dbt_assets
)
all_assets = [ *core_assets, *recommender_assets, *airbyte_assets, *dbt_assets]

elt_job = define_asset_job(
    name="my_airbyte_dbt_job",
    #selection=['recommmender_system_raw/movies', 'recommmender_system_raw/users', 'recommmender_system_raw/scores', 'movies', 'users', 'scores'],  # Selecciona todos los assets
    # O selecciona assets específicos:
    selection=AssetSelection.groups("airbyte") | AssetSelection.groups("dbt"),
)

data_job = define_asset_job(
    name='get_data',
    selection=['transformed_data'],
    config=job_data_config
)

defs = Definitions(
    assets=all_assets,
    resources={"airbyte": airbyte_instance, "dbt": DbtCliResource(project_dir=my_project) },
    jobs=[
        elt_job,
        data_job,
        #run_everything_job,
        define_asset_job(
            "only_training",
            # selection=['preprocessed_training_data', 'user2Idx', 'movie2Idx'],
            selection=AssetSelection.groups('recommender'),
            config=job_training_config
        )
    ]
)
from dagster import load_assets_from_package_module
from . import core
from . import recommender
from . import dbt
from . import airbyte

airbyte_assets = load_assets_from_package_module(
    package_module=airbyte, group_name='airbyte',
    
)

dbt_assets = load_assets_from_package_module(
    package_module=dbt, group_name='dbt',
    
)

core_assets = load_assets_from_package_module(
    package_module=core, group_name='core',
    
)
recommender_assets = load_assets_from_package_module(
    package_module=recommender, group_name='recommender'
)
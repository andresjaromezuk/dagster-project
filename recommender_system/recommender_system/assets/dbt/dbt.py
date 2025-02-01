from dagster import AssetExecutionContext, OpExecutionContext, AssetIn
from dagster_dbt import DbtCliResource, dbt_assets
from recommender_system.project import my_project

@dbt_assets(manifest=my_project.manifest_path)
def my_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

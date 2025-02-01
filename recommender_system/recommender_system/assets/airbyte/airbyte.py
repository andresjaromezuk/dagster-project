from dagster import asset, Output, String, AssetIn, FreshnessPolicy, MetadataValue
from dagster_airbyte import AirbyteCloudResource,build_airbyte_assets

movies = build_airbyte_assets(
    connection_id="bf0ae1cf-1f33-4dca-a2b9-67a015fa7314",
    destination_tables=["movies"],
    asset_key_prefix=["recommmender_system_raw"]   
)

scores = build_airbyte_assets(
    connection_id="9b0705ef-b286-491a-a937-7a9b8278aa3e",
    destination_tables=["scores"],
    asset_key_prefix=["recommmender_system_raw"]
)

users = build_airbyte_assets(
    connection_id="3d065da9-14fa-4b68-81ce-36ab5ac580b0",
    destination_tables=["users"],
    asset_key_prefix=["recommmender_system_raw"]
)


from dagster import asset, Output, String, AssetIn, FreshnessPolicy, MetadataValue,AssetDep
from dagster_mlflow import mlflow_tracking
import pandas as pd
from sqlalchemy import create_engine

DATABASE_URI = "postgresql://postgres.wemhlooqasajgnjxcsui:L6fsyu$n4VRjV.K@aws-0-us-east-1.pooler.supabase.com:6543/postgres?options=-c%20search_path=target"  # Ejemplo: "postgresql://user:password@host:port/database"
engine = create_engine(DATABASE_URI)

movies_categories_columns = [
    'unknown', 'action', 'adventure', 'animation',
    "childrens", 'comedy', 'crime', 'documentary', 'drama',
    'fantasy', 'film_noir', 'horror', 'musical', 'mystery',
    'romance', 'sci_fi', 'thriller', 'war', 'western']



# @asset(
#     freshness_policy=FreshnessPolicy(maximum_lag_minutes=5),
#     # group_name='csv_data',
#     code_version="2",
#     config_schema={
#         'table_name': String
#     },
# )
# def movies_processed(context) -> Output[pd.DataFrame]: 
#     table_name = context.op_config["table_name"]
#     query = f"SELECT * FROM target.{table_name}"
#     result = pd.read_sql(query, engine)
#     # uri = context.op_config["uri"]
#     # result = pd.read_csv(uri)
#     return Output(
#         result,
#         metadata={
#             "Total rows": len(result),
#             **result[movies_categories_columns].sum().to_dict(),
#             "preview": MetadataValue.md(result.head().to_markdown()),
#         },
#     )


# @asset(
#     # group_name='csv_data',
#     # io_manager_key="parquet_io_manager",
#     # partitions_def=hourly_partitions,
#     # key_prefix=["s3", "core"],
#      config_schema={
#         'table_name': String
#     },
# )
# def users_processed(context) -> Output[pd.DataFrame]:
#     table_name = context.op_config["table_name"]
#     query = f"SELECT * FROM target.{table_name}"
#     result = pd.read_sql(query, engine)
#     return Output(
#         result,
#         metadata={
#             "Total rows": len(result),
#             **result.groupby('Occupation').count()['id'].to_dict()
#         },
#     )


@asset(
    deps=[AssetDep("scores_movies_users")],
    resource_defs={'mlflow': mlflow_tracking},
    # io_manager_key="parquet_io_manager",
    # partitions_def=hourly_partitions,
    # key_prefix=["s3", "core"],
     config_schema={
        'table_name': String
    },
)
def transformed_data(context) -> Output[pd.DataFrame]:
    mlflow = context.resources.mlflow
    table_name = context.op_config["table_name"]
    query = f"SELECT * FROM target.{table_name}"
    result = pd.read_sql(query, engine)
    metrics = {
        "Total rows": len(result),
        "scores_mean": float(result['rating'].mean()),
        "scores_std": float(result['rating'].std()),
        "unique_movies": len(result['movie_id'].unique()),
        "unique_users": len(result['user_id'].unique())
    }
    mlflow.log_metrics(metrics)

    return Output(
        result,
        metadata=metrics,
    )

# @asset(ins={
#     "transformed_data": AssetIn(
#         # key_prefix=["snowflake", "core"],
#         # metadata={"columns": ["id"]}
#     ),
#     # "movies_processed": AssetIn(
#     #     # key_prefix=["snowflake", "core"],
#     #     # metadata={"columns": ["id"]}
#     # ),
#     # "users_processed": AssetIn(
#     #     # key_prefix=["snowflake", "core"],
#     #     # metadata={"columns": ["id", "user_id", "parent"]}
#     # ),
# })
# def training_data(transformed_data: pd.DataFrame) -> Output[pd.DataFrame]:
#     # scores_users = pd.merge(scores_processed, users_processed, left_on='user_id', right_on='id')
#     # all_joined = pd.merge(scores_users, movies_processed, left_on='movie_id', right_on='id')

#     return Output(
#         transformed_data,
#         metadata={
#             "Total rows": len(transformed_data)
#         },
#     )

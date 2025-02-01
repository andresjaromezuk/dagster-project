mlflow_resources = {
    'mlflow': {
        'config': {
            'experiment_name': 'recommender_system',
        }            
    },
}

data_ops_config = {
    'transformed_data': {
        'config': {
            'table_name': 'scores_movies_users'
            }
    },
    # 'users_processed': {
    #     'config': {
    #         'table_name': 'scores_movies_users'
    #         }
    # },
    # 'scores_processed': {
    #     'config': {
    #         'table_name': 'scores_movies_users'
    #         }
    # }
}

job_data_config = {
    'resources': {
        **mlflow_resources
    },
    'ops': {
        **data_ops_config,
    }
}

training_config = {
    'model_trained': {
        'config': {
            'batch_size': 128,
            'epochs': 10,
            'learning_rate': 1e-3,
            'embeddings_dim': 5
        }
    }
}

job_training_config = {
    'resources': {
        **mlflow_resources
    },
    'ops': {
        **training_config
    }
}
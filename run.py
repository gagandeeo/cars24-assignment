import mlflow

experiment_name = "SGDClassifier"
entry_point = "Training"

mlflow.set_tracking_uri("http://mlflowserver.centralindia.cloudapp.azure.com:5000")

mlflow.projects.run(
    uri=".",
    entry_point=entry_point,
    experiment_name=experiment_name,
    env_manager="conda"
)
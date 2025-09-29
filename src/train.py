import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.sklearn
import pickle

# Set the tracking URI to a local directory
mlflow.set_tracking_uri("http://127.0.0.1:5000")

print("Starting training script...")

# Load the dataset
df = pd.read_csv('data/dataset.csv')
X = df[['sepal.length', 'sepal.width', 'petal.length', 'petal.width']]
y = df['variety']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Start an MLflow run
with mlflow.start_run():
    # Model parameters
    C = 1.0
    solver = 'lbfgs'

    # Log parameters
    mlflow.log_param("C", C)
    mlflow.log_param("solver", solver)

    # Create and train the model
    model = LogisticRegression(C=C, solver=solver, max_iter=200)
    model.fit(X_train, y_train)

    # Make predictions
    predictions = model.predict(X_test)

    # Log metrics
    accuracy = accuracy_score(y_test, predictions)
    mlflow.log_metric("accuracy", accuracy)

    print(f"Model Accuracy: {accuracy}")

    # Save the model as a pickle file for the FastAPI app
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)

    # Log the model artifact
    mlflow.log_artifact("model.pkl", artifact_path="model")

    print("Model trained and logged successfully.")
import pickle
import os
import pandas as pd

# Paths to your pickle files
model_path = "models/churn_model.pkl"
preprocess_path = "models/preprocessing.pkl"
metrics_path = "models/metrics.pkl"

def load_pickle(file_path):
    """Load a pickle file and return the object."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    with open(file_path, "rb") as f:
        obj = pickle.load(f)
    return obj

def inspect_model(model):
    """Inspect a scikit-learn model."""
    print(f"\n=== Model Info ===")
    print(f"Type: {type(model)}")
    if hasattr(model, "feature_importances_") and hasattr(model, "n_features_in_"):
        print(f"Number of features: {model.n_features_in_}")
        df = pd.DataFrame({
            "Feature": getattr(model, "feature_names_in_", [f"Feature {i}" for i in range(model.n_features_in_)]),
            "Importance": model.feature_importances_
        }).sort_values(by="Importance", ascending=False)
        print("\nFeature Importances:")
        print(df.to_string(index=False))
    if hasattr(model, "classes_"):
        print(f"\nClasses: {model.classes_}")

def inspect_preprocessing(preproc):
    """Inspect a preprocessing object (dictionary)."""
    print(f"\n=== Preprocessing Info ===")
    print(f"Type: {type(preproc)}")
    if isinstance(preproc, dict):
        print("Keys in preprocessing object:")
        for key, value in preproc.items():
            print(f"  {key}: {type(value)}")
    else:
        print(preproc)

def inspect_metrics(metrics):
    """Inspect model metrics."""
    print(f"\n=== Metrics Info ===")
    if isinstance(metrics, dict):
        for key, value in metrics.items():
            print(f"{key.capitalize()}: {value}")
    else:
        print(metrics)

# Load and inspect model
model = load_pickle(model_path)
if model:
    inspect_model(model)

# Load and inspect preprocessing
preproc = load_pickle(preprocess_path)
if preproc:
    inspect_preprocessing(preproc)

# Load and inspect metrics
metrics = load_pickle(metrics_path)
if metrics:
    inspect_metrics(metrics)
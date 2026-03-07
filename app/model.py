import numpy as np


class DummyModel:
    """
    Simple dummy model.
    Replace with:
    - MLflow model loader
    - Pickle loader
    - Torch model
    - TensorFlow model
    """

    def predict(self, X):
        return np.sum(X, axis=1)


def load_model():
    """
    Load and return the ML model.
    This function is called during app startup.
    """
    print("📦 Loading model...")
    return DummyModel()
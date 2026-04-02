import os
import sys

# Add ml directory to sys.path so we can import from it
ml_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ml"))
if ml_dir not in sys.path:
    sys.path.append(ml_dir)

from predict import load_model, predict  # noqa: E402

ml_models = {}


def load_ml_models():
    """Load the ML components directly and store in our global dictionary"""
    model_dir = os.path.join(ml_dir, "model")
    model, scaler = load_model(model_dir)
    ml_models["model"] = model
    ml_models["scaler"] = scaler


def clear_ml_models():
    """Clear memory used by ML components"""
    print("Clearing ML models from memory...")
    ml_models.clear()


class PredictService:
    def __init__(self, model, scaler):
        self.model = model
        self.scaler = scaler

    def get_prediction(self, jumlah_penjualan: int, harga: int, diskon: int) -> str:
        """
        Takes input features and returns the prediction result using the loaded ML model.
        """
        result = predict(self.model, self.scaler, jumlah_penjualan, harga, diskon)
        return result


def get_predict_service() -> PredictService:
    return PredictService(ml_models.get("model"), ml_models.get("scaler"))

import os
import sys

# Add ml directory to sys.path so we can import from it
ml_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ml"))
if ml_dir not in sys.path:
    sys.path.append(ml_dir)

from predict import load_model, predict  # noqa: E402


class PredictService:
    def __init__(self):
        # Load the model and scaler when the service is instantiated
        self.model_dir = os.path.join(ml_dir, "model")
        self.model, self.scaler = load_model(self.model_dir)

    def get_prediction(self, jumlah_penjualan: int, harga: int, diskon: int) -> str:
        """
        Takes input features and returns the prediction result using the loaded ML model.
        """
        # Call the predict function from ml/predict.py
        result = predict(self.model, self.scaler, jumlah_penjualan, harga, diskon)
        return result


# Singleton instance to be used across requests
predict_service = PredictService()

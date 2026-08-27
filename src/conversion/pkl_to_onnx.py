import os
import joblib

from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType


MODEL_PATH = "models/model.pkl"
ONNX_PATH = "models/model.onnx"

model_data = joblib.load(MODEL_PATH)

model = model_data["model"]
features = model_data["features"]

initial_type = [
    ("float_input", FloatTensorType([None, len(features)]))
]

onnx_model = convert_sklearn(
    model,
    initial_types=initial_type,
    options={
        id(model): {
            "zipmap": False
        }
    }
)

os.makedirs("models", exist_ok=True)

with open(ONNX_PATH, "wb") as f:
    f.write(onnx_model.SerializeToString())


print(f"Converted {MODEL_PATH} -> {ONNX_PATH}")
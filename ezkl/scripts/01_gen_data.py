import torch
import onnx
import json
from ezkl_config import *

def infer_input_shape(onnx_path):
    model = onnx.load(str(onnx_path))
    input_tensor = model.graph.input[0]
    shape = []
    for d in input_tensor.type.tensor_type.shape.dim:
        if d.dim_value > 0:
            shape.append(d.dim_value)
        else:
            shape.append(1)
    return shape

def main():
    logger.info("--- Step 1: Calibration Data ---")
    shape = infer_input_shape(MODEL_PATH)
    logger.info(f"Inferred Shape: {shape}")
    
    dummy_input = torch.randn(*shape)
    data = dict(input_data=[dummy_input.flatten().tolist()])
    
    with open(INPUT_PATH, "w") as f:
        json.dump(data, f)
    logger.info(f"Saved to {INPUT_PATH}")

if __name__ == "__main__":
    main()

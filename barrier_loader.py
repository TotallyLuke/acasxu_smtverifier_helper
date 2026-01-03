import torch
import onnx
import onnx2torch


def load_onnx_as_sequential(path: str) -> torch.nn.Sequential:
    """
    Loads an ONNX model, converts it to Torch, and flattens linear/ReLU
    layers into a Sequential container.
    """
    onnx_model = onnx.load(path)
    torch_model = onnx2torch.convert(onnx_model)
    torch_model.eval()

    try:
        from torch.fx import symbolic_trace
        graph_module = symbolic_trace(torch_model)
    except Exception as e:
        # fallback: if tracing fails, extract from named_modules directly
        graph_module = torch_model

    layers = []
    for _, module in graph_module.named_modules():
        if isinstance(module, (torch.nn.Linear, torch.nn.ReLU)):
            layers.append(module)

    return torch.nn.Sequential(*layers)
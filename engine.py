import torch
from pathlib import Path

class Qwen3ASREngine:
    def __init__(self, model_dir="./models"):
        self.model_dir = Path(model_dir)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.dtype = self._select_precision()
        self.loaded_models = {}
        self.aligner = None

    def _select_precision(self):
        if self.device != "cuda":
            return torch.float32
        capability = torch.cuda.get_device_capability(0)
        return torch.bfloat16 if capability[0] >= 8 else torch.float16

    def load_model(self, name, timestamps=False):
        if name in self.loaded_models:
            return True
        path = self.model_dir / name
        if not path.exists():
            return False
        from qwen_asr import Qwen3ASRModel
        
        kwargs = {
            "dtype": self.dtype,
            "device_map": "cuda:0" if self.device == "cuda" else "cpu",
            "max_new_tokens": 4096,
        }
        
        if timestamps:
            kwargs["forced_aligner"] = str(self.model_dir / "Qwen3-ForcedAligner-0.6B")
            kwargs["forced_aligner_kwargs"] = {
                "dtype": self.dtype,
                "device_map": "cuda:0" if self.device == "cuda" else "cpu",
            }
        
        self.loaded_models[name] = Qwen3ASRModel.from_pretrained(str(path), **kwargs)
        return True

    def transcribe(self, audio, model="Qwen3-ASR-1.7B", lang=None, timestamps=False):
        if not self.load_model(model, timestamps):
            return {"error": f"无法加载模型 {model}"}
        
        kwargs = {}
        if timestamps:
            kwargs["return_time_stamps"] = True
        
        result = self.loaded_models[model].transcribe(
            audio=audio, language=lang, **kwargs
        )
        return {
            "text": result[0].text,
            "language": result[0].language,
            "timestamps": getattr(result[0], "time_stamps", None)
        }

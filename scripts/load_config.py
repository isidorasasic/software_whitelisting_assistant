import yaml
from pathlib import Path



from software_whitelisting_assistant.config import AppConfig


def load_config(path: str | Path) -> AppConfig:
    
    path = Path(__file__).parent.parent / "config" / "config.yaml"
    print(path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    if path.suffix in {".yaml", ".yml"}:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    else:
        raise ValueError("Config must be .yaml or .yml")

    return AppConfig.model_validate(raw)

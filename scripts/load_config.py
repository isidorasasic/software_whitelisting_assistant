import yaml
from pathlib import Path
from software_whitelisting_assistant.config import AppConfig


def load_configuration() -> AppConfig:
    """
    Load application configuration from a YAML file and validate it.

    Returns:
        AppConfig: The validated application configuration.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        ValueError: If the file is not a `.yaml` or `.yml` file.
    """
    
    path = Path(__file__).parent.parent / "config" / "config.yaml"

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    if path.suffix in {".yaml", ".yml"}:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    else:
        raise ValueError("Config must be .yaml or .yml")

    return AppConfig.model_validate(raw)

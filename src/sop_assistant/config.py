"""Settings from environment variables (.env is loaded automatically)."""
import os
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

_env = ROOT / ".env"
if _env.exists():
    for line in _env.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


@dataclass(frozen=True)
class Settings:
    pdf_dir: Path = Path(os.getenv("PDF_DIR", ROOT / "data" / "pdfs"))
    qdrant_url: str = os.getenv("QDRANT_URL", "")  # empty = embedded storage in qdrant_path
    qdrant_path: str = os.getenv("QDRANT_PATH", str(ROOT / ".qdrant"))
    collection: str = "sop_chunks"
    embed_backend: str = os.getenv("EMBED_BACKEND", "fastembed")  # or "hash" (offline)
    embed_model: str = os.getenv("EMBED_MODEL", "intfloat/multilingual-e5-large")
    llm_base_url: str = os.getenv("LLM_BASE_URL", "")  # any OpenAI-compatible endpoint
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "")
    top_k: int = int(os.getenv("TOP_K", 6))
    gate_hard: float = float(os.getenv("GATE_HARD", 0.20))  # below: refuse before the LLM
    gate_extractive: float = float(os.getenv("GATE_EXTRACTIVE", 0.60))  # below: refuse without LLM

    @property
    def llm_enabled(self) -> bool:
        return bool(self.llm_base_url and self.llm_model)
import logging
import os
from pathlib import Path


LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "pipeline.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
    filemode='a'
)

logger = logging.getLogger(__name__)

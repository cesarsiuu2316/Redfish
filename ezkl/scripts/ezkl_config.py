import logging
import resource
import time
import os
from pathlib import Path
from datetime import datetime

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
EZKL_DIR = PROJECT_ROOT / "ezkl"
ARTIFACTS_DIR = EZKL_DIR / "artifacts"
MODEL_PATH = ARTIFACTS_DIR / "network.onnx"
CONTRACTS_SRC = PROJECT_ROOT / "src"

# Use a fixed 'latest' log dir for current run, or timestamped
# For sequential scripts, we want them to share the same output folder.
# Let's use a 'current_run' symlink concept or just a fixed build dir.
BUILD_DIR = EZKL_DIR / "build"
BUILD_DIR.mkdir(parents=True, exist_ok=True)

INPUT_PATH = BUILD_DIR / "input.json"
SETTINGS_PATH = BUILD_DIR / "settings.json"
COMPILED_PATH = BUILD_DIR / "network.ezkl"
PK_PATH = BUILD_DIR / "pk.key"
VK_PATH = BUILD_DIR / "vk.key"
SRS_PATH = BUILD_DIR / "kzg.srs"
VERIFIER_PATH = BUILD_DIR / "Verifier.sol"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def log_resource_usage(stage_name):
    usage = resource.getrusage(resource.RUSAGE_SELF)
    max_rss_mb = usage.ru_maxrss / 1024
    if 'darwin' in os.sys.platform:
        max_rss_mb /= 1024
    logger.info(f"[{stage_name}] Max Memory: {max_rss_mb:.2f} MB")

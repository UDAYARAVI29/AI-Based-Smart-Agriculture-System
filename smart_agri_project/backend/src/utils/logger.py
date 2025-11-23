import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "data", "logs", "app.log")

# Ensure logs folder exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Logging configuration
logging.basicConfig(
    filename=LOG_FILE,
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("smart_agri_logger")

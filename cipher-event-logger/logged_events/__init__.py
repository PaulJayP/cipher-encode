
import os
from pathlib import Path

BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent

EVENT_STORAGE_PATH = Path(BASE_DIR, 'logged_events')

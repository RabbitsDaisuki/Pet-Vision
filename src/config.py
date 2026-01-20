import logging
from pathlib import Path
# --- 

yolo_model_index = "yolov8n.pt"
train_data = "pet.yaml"
project_name = "pet_vision"
whisper_model_index = "base"
sound_input = "input.wav"
camera_index = 0
verbose = False
confidence_threshold = 0.5
chunk_size = 1024
threshold = 50
silence = 2.0
pet_yaml_name = "pat.yaml"


# --- Path Settings ---
BASE_DIR = Path( __file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"


# --- Ensure directories exist ---
DATA_DIR.mkdir(parents = True, exist_ok = True)
(DATA_DIR / "raw").mkdir(parents = True, exist_ok = True)
(DATA_DIR / "result").mkdir(parents = True, exist_ok = True)
LOGS_DIR.mkdir(parents = True, exist_ok = True)
(DATA_DIR / "yaml").mkdir(parents = True, exist_ok = True)
(DATA_DIR / "weights").mkdir(parents = True, exist_ok = True)
(DATA_DIR / "user_sound").mkdir(parents = True, exist_ok = True)

# --- Model Setting ---
YOLO_MODEL_NAME = yolo_model_index
MODEL_PATH = MODELS_DIR / YOLO_MODEL_NAME

WHISPER_MODEL_NAME = whisper_model_index

# ---BOX Settings ---
CONFIDENCE_THRESHOLD = confidence_threshold

# --- Camera Settings ---
CAMERA_INDEX = camera_index
VERBOSE_STATUS = verbose

# --- Logging Settings ---
LOG_FILE = LOGS_DIR / "app.log"
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_LEVEL = logging.INFO

# --- train Setup ---
YAML_PATH = DATA_DIR / "yaml"
TRAIN_DATA = YAML_PATH / train_data
PROJECT_TRAIN_DIR = YAML_PATH / project_name
PROJECT_TRAIN_DIR.mkdir(parents = True, exist_ok = True)
TRAIN_LABELS_DIR = PROJECT_TRAIN_DIR / "train/labels"
TRAIN_LABELS_DIR.mkdir(parents = True, exist_ok = True)
TRAIN_IMAGES_DIR = PROJECT_TRAIN_DIR / "train/images"
TRAIN_IMAGES_DIR.mkdir(parents = True, exist_ok = True)
VAL_LABELS_DIR = PROJECT_TRAIN_DIR / "val/labels"
VAL_LABELS_DIR.mkdir(parents = True, exist_ok = True)
VAL_IMAGES_DIR = PROJECT_TRAIN_DIR / "val/images"
VAL_IMAGES_DIR.mkdir(parents = True, exist_ok = True)
WEIGHTS_PATH = DATA_DIR / "weights"
INPUT_YAML_SMT = YAML_PATH
TRAIN_EPOCHS = 100
IMG_SIZE = 640

# --- COCO2017 train Setup ---
COCO_TRAIN_IMG_PATH = DATA_DIR / "yaml/coco2017/train/data"
COCO_TRAIN_JSON_PATH = DATA_DIR / "yaml/coco2017/annotations/instances_train2017.json"
COCO_VAL_IMG_PATH = DATA_DIR / "yaml/coco2017/validation/data"
COCO_VAL_JSON_PATH = DATA_DIR / "yaml/coco2017/annotations/instances_val2017.json"

# --- pet train setup ---
PET_OUT_PATH = YAML_PATH / project_name
PET_OUT_PATH.mkdir(parents = True, exist_ok = True)
PET_YAML_PATH = YAML_PATH / "pet.yaml"



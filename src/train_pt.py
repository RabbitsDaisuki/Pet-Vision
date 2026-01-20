from ultralytics import YOLO
from src import config
import logging
import config

def train_custom_model():
    # --- Log Loading ---
    logging.basicConfig(
        level = config.LOG_LEVEL,
        format = config.LOG_FORMAT,
        filename = config.LOG_FILE,
        filemode = 'a'
    )

    try:
    # --- Model Loading ---
        logging.info(f"Training process initialized with {str(config.YOLO_MODEL_NAME)}.")
        model = YOLO(str(config.MODEL_PATH))

        results = model.train(
            # data: path to your dataset .yaml file
            data = config.TRAIN_DATA,
            
            # epochs: How many times the model sees the entire dataset
            epochs = config.TRAIN_EPOCHS,
            
            # imgsz: Input image size (standard is 640) 
            imgsz = config.IMG_SIZE,

            # device: 'mps' leverages Apple Silicon GPU power if use Nvidia with '0'
            device = "mps",
            conf = 0.5,
            iou = 0.6,
            )
        
        print("Training finished successfully.")

    except Exception as e:
        print(f"Error during training: {e}")
        logging.error(f"Training failed: {e}")

if __name__ == "__main__":
    train_custom_model()
from ultralytics import YOLO
import time
import logging
import cv2
from src import config

class PCBDetection():
    def __init__(self):
        # ----- Load and check Model -----
        try:
            self.model = YOLO(str(config.MODEL_PATH))
        except Exception as e:
            print(f"Critical Error: Could not load model: {e}")
            logging.error(f"Could not loaded model with {config.YOLO_MODEL_NAME}")
            self.model = None

    def take_inference(self, frame):
        if self.model is None:
            return frame, None
        
        results = self.model.predict(frame, 
                                    conf = config.CONFIDENCE_THRESHOLD,
                                    stream = False,
                                    verbose = config.VERBOSE_STATUS,
                                    )
        annotated_frame = results[0].plot()

        return annotated_frame, results[0]

    def _img_save(self, frame):
        datetime = time.strftime("%Y%m%d_%H%M%S")
        img_name = f"pcb_snap_{datetime}.png"
        save_path = config.DATA_DIR / "result" / img_name
        img_save = cv2.imwrite(str(save_path), frame)
        if not img_save:
            print("Warning: Failing to save")
            logging.warning(f"Could not save to {save_path}, please check path or memory")
        else:
            print("Image save start :Successfully ")
            logging.info(f"The image {img_name} was saved to {save_path}")

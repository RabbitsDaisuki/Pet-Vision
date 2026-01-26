from ultralytics import YOLO
import time
import logging
from src import config

class PETDetection():
    def __init__(self):
        # --- Status Setting ---
        self.prev_frame = None
        self.start_time = 0
        self.last_detection_time = 0
        self.current_duration = 0


        self.class_name = {
            0: "Person",
            15: "Cat",
            16: "Dog",
        }


        # ----- Load and check Model -----
        try:
            self.model = YOLO(str(config.MODEL_PATH))
        except Exception as e:
            print(f"Critical Error: Could not load model: {e}")
            logging.error(f"Could not loaded model with {config.YOLO_MODEL_NAME}")
            self.model = None

    def take_inference(self, frame, camera_status = None):
        # Confidence threshold for image capture
        import cv2
        annotated_frame = frame
        results_return = None
        detected_classes = []

        if self.model is None:
            logging.info("No frame input")
            return frame, None, camera_status, 0, []
        
            
        if camera_status == 1:
            self.detected_time = time.time()
            results_yolo = self.model.predict(frame, 
                                        # take person, cat and dog from class setting
                                        classes = config.YOLO_CLASS,
                                        conf = config.CONFIDENCE_THRESHOLD,
                                        stream = False,
                                        verbose = config.VERBOSE_STATUS,
                                        iou = 0.65,
                                        imgsz = 480,
                                        device = "mps"
                                        )
            
            current_result = results_yolo[0]
            item_count = len(current_result.boxes)
            if self.start_time == 0:
                self.start_time = time.time()
                camera_status = 1
            else:
                if item_count == 0:
                    self.last_detection_time = time.time() - self.start_time
                    time_end_1 = time.time() - self.last_detection_time
                    if time_end_1 > config.COOL_DOWN_TIME:
                        camera_status = 2
                        annotated_frame = current_result.plot()
                        

                else:
                    camera_status = 1
                    annotated_frame = current_result.plot()
                    class_tensor = current_result.boxes.cls
                    if class_tensor is not None:
                        detected_classes = list(set(class_tensor.cpu().numpy().astype(int)))
        
            results_return = current_result

        elif camera_status == 2:
            # --- Preprocessing ---
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_gray_gaussian = cv2.GaussianBlur(frame_gray, (21, 21), 0)
            
            # --- Binarization ---
            if self.prev_frame is None:
                self.prev_frame = frame_gray_gaussian
                return frame, None, 2, 0, []
            
            frame_delta = cv2.absdiff(self.prev_frame, frame_gray_gaussian)
            
            _, frame_threshold = cv2.threshold(frame_delta, 127, 255, cv2.THRESH_BINARY)
            
            white_count = cv2.countNonZero(frame_threshold)

            self.prev_frame = frame_gray_gaussian
            
            if white_count > config.APPROACH_THRESHOLD:
                self.last_detection_time = time.time()
                time_end_2 = config.COOL_DOWN_TIME - self.last_detection_time
                if time_end_2 > config.COOL_DOWN_TIME:
                    camera_status = 1
                    annotated_frame = cv2.cvtColor(frame_threshold, cv2.COLOR_GRAY2BGR)
            else:
                camera_status = 2
                annotated_frame = cv2.cvtColor(frame_threshold, cv2.COLOR_GRAY2BGR)

            results_return = None
            detected_classes = []
        
        else:
            camera_status = 1
            annotated_frame = None
            detected_classes = []
        

        return annotated_frame, results_return, camera_status, detected_classes

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

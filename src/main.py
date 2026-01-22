import cv2
from vision_module import PETDetection as PETs
import logging
import time
from src import config
from kivy.app import App
from kivy.lang import Builder
from gui import WindowManager
import threading

class SharedContext:
    def __init__ (self):
        self.visual_info = "Nothing detected yet"
        self.current_frame = None
        self.is_running = True
        self.is_listening = False

# --- GUI loop --- 
def main():

    # ----- Initialize Logging -----
    logging.basicConfig(
        level = config.LOG_LEVEL,
        format = config.LOG_FORMAT,
        filename = str(config.LOG_FILE),
    )

    try:
        # --- Take Vision system ---
        pet_system = PETs() 
        # --- Take LLM System ---
    except Exception as e:
        print(f"Initialization Error: {e}")
        logging.error(f"Error: System can not take:{e}")
        return

    # --- Camera Loading ---
    Mac_cap = cv2.VideoCapture(config.CAMERA_INDEX)

    if not Mac_cap.isOpened():
        logging.error("System could not opened camera.")
        print("Error: No camera input, please check...")
        return
    else:
        print("System Running... Press 's' to get image , 'q' to exit.")
        logging.info("System status: Running")

    try:
        while True:
            start = time.time()
            ret, frame = Mac_cap.read()

            if not ret:
                print("Failed to receive frame, exiting...")
                logging.error("Could not generate frame, please check camera")
                break
            
            # --- Vision Loading ---
            annotated_frame, results = pet_system.take_inference(frame)

            # -----show fps-----
            fps = 1/(time.time() - start)
            
            cv2.putText(annotated_frame,
                        f"FPS: {fps:.2f}, Status: AI Idle",
                        (10,60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (255, 0, 0),
                        2,
                        cv2.LINE_AA
            )

            
            # --- Show GUI ---
            cv2.imshow("Read_PET", annotated_frame)

            input_key = cv2.waitKey(1) & 0xFF
            if input_key == ord('q'):
                print("System shutdown safely")
                logging.info("System shutdown safely")
                break
            
            elif input_key == ord('s'):
                pet_system._img_save(annotated_frame)

    except KeyboardInterrupt:
        logging.info("System by pass")
        pass

    except Exception as e:
        print(f"An unexpected error occurred {e}")
        logging.error(f"System Error for {e}")
    
    finally:
        if Mac_cap.isOpened():
            Mac_cap.release()
        cv2.destroyAllWindows()
        print("System closed.")
        logging.info("Camera Status: Release successfully")

if __name__ == "__main__":
    main().run()




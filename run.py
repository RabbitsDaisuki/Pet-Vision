import sys
import os
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from coco_to_yolo import Coco_to_yolo
    import train_pt
    import main as vision_l
    import config


    logging.basicConfig(
        level = config.LOG_LEVEL,
        format = config.LOG_FORMAT,
        filename = str(config.LOG_FILE),
    )
    # from src import



except ImportError as e:
    print(f"Import Error: {e}")
    logging.error(f"Import Error: {e}")
    sys.exit(1)

def print_menu():

    # ---Display an interactive menu for the user.---
    print("\n" + "="*30)
    print("   AI PROJECT MASTER CONTROL")
    print("="*30)
    print("1. Data Conversion (COCO to YOLO)")
    print("2. Start Model Training")
    print("3. Run Vision System (PCB Detection)")
    print("4. Exit")
    print("="*30)



def main():
    while True:
        print_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            print("\n[Action] Starting Data Conversion...")
            # Principle: Instantiate the converter class and execute processing logic.
            converter = Coco_to_yolo()
            converter.run(
                config.COCO_TRAIN_JSON_PATH,
                config.COCO_TRAIN_IMG_PATH,
                config.TRAIN_IMAGES_DIR,
                config.TRAIN_LABELS_DIR,
                )
    
            converter.run(
                        config.COCO_VAL_JSON_PATH,
                        config.COCO_VAL_IMG_PATH,
                        config.VAL_IMAGES_DIR,
                        config.VAL_LABELS_DIR,
                        )

        elif choice == '2':
            print("\n[Action] Starting Model Training...")
            # Principle: Call the encapsulated training function.
            # Ensure you have a start_training function defined in src/train.py
            try:
                # Replace with your actual YAML config path
                train_pt.train_custom_model() 
            except AttributeError:
                print("Error: 'start_training' function not found in train.py")

        elif choice == '3':
            print("\n[Action] Launching Vision System GUI...")
            # Principle: Run the main function from your vision_app (main.py).
            vision_l.main()

        elif choice == '4':
            print("Exiting system. Goodbye!")
            break

        else:
            print("Invalid selection, please try again.")

if __name__ == "__main__":
    main()
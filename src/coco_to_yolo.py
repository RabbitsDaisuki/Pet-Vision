import json
import os
import shutil
import config
import yaml
import logging

class Coco_to_yolo():
    def __init__(self):
        self.target_classes = ['cat', 'dog', 'person']

        logging.basicConfig(
            level = config.LOG_LEVEL,
            format = config.LOG_FORMAT,
            filename = config.LOG_FILE,
            filemode = 'a',
        )

    def _normalize_bbox(self, bbox, img_w, img_h):
        x_min, y_min, w, h = bbox
        x_center = (x_min + w / 2.0) / img_w
        y_center = (y_min + h / 2.0) / img_h
        norm_w = w / img_w
        norm_h = h / img_h
        return x_center, y_center, norm_w, norm_h
    
    def _generate_yaml(self):
            try:
                data_config = {
                    'path' : str(config.PET_OUT_PATH),
                    'train' : str(config.TRAIN_IMAGES_DIR),
                    'val' : str(config.VAL_IMAGES_DIR),
                    'names' : {i: name for i, name in enumerate(self.target_classes)}
                }

                yaml_path = config.PET_YAML_PATH

                with open(yaml_path, 'w') as f:
                    yaml.dump(data_config, f, default_flow_style = False)
                
                print(f'Success: YAML configuration generation at {yaml_path}')
                logging.info("Yaml Save Status: Save successfully.")
            except Exception as e:
                print(f"Error: Could not save to {yaml_path}")
                logging.error("Yaml Save Status: Fail")

    def run(self, input_json, input_images, out_image, out_lab):
        # Load COCO JSON
        with open(input_json, 'r') as f:
            data = json.load(f)
            if not data:
                print('Could not found file')
                logging.error(f'json load fail')
                return

        # Map category IDs to names and filter target IDs
        cat_id_map = {cat['id']: cat['name'] for cat in data['categories']}
        target_ids = [cat['id'] for cat in data['categories'] if cat['name'] in self.target_classes]
        
        # Create a mapping for YOLO class indices (e.g., cat=0, dog=1)
        class_to_idx = {name: i 
                        for i, name in enumerate(self.target_classes)}
        id_to_idx = {
            cat['id']: class_to_idx[cat['name']] 
            for cat in data['categories'] 
            if cat['name'] in self.target_classes
            }

        # Index annotations by image_id
        img_id_to_ann = {}
        for ann in data['annotations']:
            if ann['category_id'] in target_ids:
                img_id = ann['image_id']
                if img_id not in img_id_to_ann:
                    img_id_to_ann[img_id] = []
                img_id_to_ann[img_id].append(ann)

        # Process images
        for img_info in data['images']:
            img_id = img_info['id']
            if img_id in img_id_to_ann:
                file_name = img_info['file_name']
                img_w = img_info['width']
                img_h = img_info['height']

                # Copy image to new directory
                try:
                    src_img_path = os.path.join(input_images, file_name)
                    dst_img_path = os.path.join(out_image, file_name)
                    if os.path.exists(src_img_path):
                        shutil.copy(src_img_path, dst_img_path)
                
                    # Create YOLO label file
                    base_name = os.path.splitext(file_name)[0]
                    label_file = os.path.join(out_lab, f"{base_name}.txt")

                    with open(label_file, 'w') as f_label:
                        for ann in img_id_to_ann[img_id]:
                            # COCO bbox: [xmin, ymin, width, height]
                            x_center, y_center, w, h = self._normalize_bbox(ann['bbox'], img_w, img_h)
                            
                            class_idx = id_to_idx[ann['category_id']]
                            f_label.write(f"{class_idx} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n")
                            
                except Exception as e:
                    print("Output Save Status: Fail! please check path")
                    logging.error(f"Image Output Status: Fail! ")
        
        print(f"Extraction completed. Data saved to: {config.PET_OUT_PATH}")
        self._generate_yaml()

if __name__ == "__main__":
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


# Example usage:
# convert_coco_to_yolo('annotations/instances_train2017.json', 'train2017', 'pet_dataset/train')
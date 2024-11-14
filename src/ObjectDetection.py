import os
import cv2
import  logging
import json
from ultralytics import YOLO

logger = logging.getLogger(__name__)


class YOLOv8Detector:
    def __init__(self, model_path='yolov8n.pt'):
        logger.info(f'Loading YOLOv8 model from {model_path}')
        self.model = YOLO(model_path)

    def detect_objects(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            logger.error(f"Image at path '{image_path}' could not be loaded.")
            raise ValueError(f"Image at path '{image_path}' could not be loaded.")

        results = self.model(image)

        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]

                detections.append({
                    'class_id': class_id,
                    'class_name': class_name,
                    'confidence': confidence,
                    'bounding_box': {
                        'x1': x1,
                        'y1': y1,
                        'x2': x2,
                        'y2': y2
                    }
                })

                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f'{class_name} {confidence:.2f}'
                cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        base_name = os.path.splitext(image_path)[0]
        output_image_path = f'{base_name}_output.jpg'
        output_json_path = f'{base_name}_output.json'

        cv2.imwrite(output_image_path, image)

        with open(output_json_path, 'w') as f:
            json.dump(detections, f, indent=4)

        logger.info(f'Annotated image saved to {output_image_path}')
        logger.info(f'JSON output saved to {output_json_path}')

        return detections


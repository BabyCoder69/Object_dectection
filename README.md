

***Object Detection API***
===

This API allows you to perform object detection on images.  


***Thought Process:***
===

- A simple and user-friendly UI is provided for uploading images and visualizing object detection results.
- The UI allows users to:
  - Upload an image.
  - Call the API for processing.
  - View the processed image with bounding boxes.
  - Receive a structured JSON response of detected objects.

- The API utilizes the YOLOv8 model for object detection.
- YOLOv8 implementation is based on the official documentation: https://docs.ultralytics.com/modes/predict/#inference-sources


***How to run:***
===
1. Build the docker image with the following command:

    ```docker build -t aimonk_object_detection .```

2. Run the docker image with the following command:

    ```docker run --rm -it -p 8000:8000 aimonk_object_detection```

3. Click on the url `http://0.0.0.0:8000` to open the UI.
4. The UI allows you to upload images and view the results.
5. Click on the choose file button and select an image to upload (test images are provided named test1.jpg and test2.jpg).
6. Click on the process button to process the image.
7. The processed image with bounding boxes will be displayed.
8. The JSON response of detected objects will be displayed. 
9. A healthcheck endpoint is available at `/health`, this is used to check the health of the API for deployment purposes.


# API Documentation


### 1. POST: /process_image

Performs object detection on an image and returns the results.


***Returns:***
===
Returns a JSON object containing the relevant results that match the search query.


***Example:***
===

### *Response:*
```json
{
  "processed_image_url": "static url of the output image",
  "detection_results": [
  {
    "class_id": 1,
    "class_name": "bicycle",
    "confidence": 0.9231963753700256,
    "bounding_box": {
      "x1": 258,
      "y1": 88,
      "x2": 1331,
      "y2": 977
    }
  },
  {
    "class_id": 16,
    "class_name": "dog",
    "confidence": 0.8430494070053101,
    "bounding_box": {
      "x1": 1279,
      "y1": 476,
      "x2": 1567,
      "y2": 984
    }
  },
  {
    "class_id": 0,
    "class_name": "person",
    "confidence": 0.5951238870620728,
    "bounding_box": {
      "x1": 11,
      "y1": 318,
      "x2": 50,
      "y2": 412
    }
  },
  {
    "class_id": 2,
    "class_name": "car",
    "confidence": 0.31421637535095215,
    "bounding_box": {
      "x1": 1704,
      "y1": 325,
      "x2": 1796,
      "y2": 361
    }
  }
]
          
}

```

### 2. GET: /health

Checks the health of the API.

***Returns:***
===
Returns a JSON object containing the status of the API.

### *Response:*
```json
{
  "status_code": "200",
  "health": "healthy"
}
```

---
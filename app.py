import logging
import os
from fastapi import FastAPI, status, HTTPException, Request, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from src.ObjectDetection import YOLOv8Detector


# Configuring logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(filename)s:%(lineno)d] - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

upload_folder = "uploads"

if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

app = FastAPI(
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    docs_url="/aimonk/docs",
    openapi_url="/aimonk/openapi.json",
)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

templates = Jinja2Templates(directory="templates")

detector_inst = YOLOv8Detector()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process_image")
async def process_image(file: UploadFile = File(...)):
    try:
        logger.info(f"Received image for processing: {file.filename}")
        input_path = os.path.join(upload_folder, file.filename)

        with open(input_path, "wb") as f:
            content = await file.read()
            f.write(content)

        detections = detector_inst.detect_objects(input_path)

        output_image_path = f"{os.path.splitext(input_path)[0]}_output.jpg"

        return {
            "processed_image_url": f"/uploads/{os.path.basename(output_image_path)}",
            "detection_results": detections
        }
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)



@app.get("/health")
def health() -> dict:
    """
    Health check API endpoint.

    Returns:
    - dict: Status of the service.
    """
    return {"status_code": "200", "health": "healthy"}

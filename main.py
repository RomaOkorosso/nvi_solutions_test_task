import json
import os
import dotenv

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from torchvision import models, transforms
from PIL import Image
import torch
from logger import logger

app = FastAPI()
templates = Jinja2Templates(directory="templates")
# include static
app.mount("/static", app=StaticFiles(directory="static"), name="static")

# Загружаем предобученную модель
model = models.resnet50(pretrained=True)
model.eval()
with open("imagenet-simple-labels.json") as f:
    labels = json.load(f)

# Определяем преобразования для изображения
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.get("/result/")
async def get_result(request: Request, filename: str, content_type: str,
                     prediction: str, width: int, height: int, img: str = None):
    return templates.TemplateResponse("result.html",
                                      {"request": request, "filename": filename, "content_type": content_type,
                                       "prediction": prediction, "width": width, "height": height, "img": None})


@app.post("/result/")
async def get_result(request: Request, filename: str, content_type: str,
                     prediction: str, width: int, height: int, img: str = None):
    logger.log(f"")
    return templates.TemplateResponse("result.html",
                                      {"request": request, "filename": filename, "content_type": content_type,
                                       "prediction": prediction, "width": width, "height": height, "img": None})


@app.post("/predict/")
async def predict(request: Request, file: UploadFile = File(...)):
    # check if no file
    logger.log(f"Got file: '{file.filename}'")
    if not file or not file.filename:
        return templates.TemplateResponse("error.html", {"request": request, "error": "No file"})
    image = Image.open(file.file)
    # save img into static/uploads
    image.save(f"static/uploads/{file.filename}")
    # get real wight and height of image
    r_weight, r_height = image.size
    logger.log(f"Image size: {r_weight}x{r_height}")
    image_transformed = transform(image).unsqueeze(0)
    outputs = model(image_transformed)
    _, predicted = torch.max(outputs, 1)
    predicted_label = labels[predicted.item()]
    logger.log(f"Predicted: {predicted_label}")

    return RedirectResponse(url=f"/result?filename={file.filename}&content_type={file.content_type}"
                                f"&prediction={predicted_label}&width={r_weight}"
                                f"&height={r_height}")


def main():
    import uvicorn
    # get port and host from env

    dotenv.load_dotenv()
    port = os.getenv("APP_PORT")
    host = os.getenv("APP_HOST")
    if port and host:
        logger.log(f"Start app at {host}:{port}")
        uvicorn.run(app, host=host, port=int(port))


if __name__ == "__main__":
    logger.log(f"Start app")
    main()

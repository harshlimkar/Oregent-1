from fastapi import FastAPI, UploadFile, File, Form
from conversation_agent import conversation_agent
import uuid
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/chat")
async def chat(
    user_input: str = Form(...),
    session_id: str = Form("default"),
    image: UploadFile | None = File(None)
):
    image_path = None

    if image:
        filename = f"{uuid.uuid4()}_{image.filename}"
        image_path = os.path.join(UPLOAD_DIR, filename)

        with open(image_path, "wb") as f:
            f.write(await image.read())

    response = conversation_agent(
        user_input=user_input,
        image_path=image_path
    )

    response["session_id"] = session_id
    return response

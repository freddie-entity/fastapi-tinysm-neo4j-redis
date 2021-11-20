from config import settings
import secrets
from PIL import Image

async def upload_image(file):
    filename = file.filename
    extension = filename.split(".")[-1]    

    if extension not in ["jpg", "png"]:
        return {"status" : "error", "detail" : "file extension not allowed"}

    token_name = secrets.token_hex(10)+"."+extension
    generated_name = settings.FILE_PATH + token_name
    file_content = await file.read()
    with open(generated_name, "wb") as file:
        file.write(file_content)

    img = Image.open(generated_name)
    # img = img.resize(size = (200,200))
    img.save(generated_name)
    file.close()
    return generated_name[1:]
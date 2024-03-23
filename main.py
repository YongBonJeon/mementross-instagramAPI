from fastapi import FastAPI
from instagrapi import Client

app = FastAPI()

cl = Client()
cl.login("mementross", "qwer1234!")


@app.get("/images")
async def login(tag: str, count: int):
    user_id = cl.user_id_from_username(tag)
    medias = cl.user_medias(user_id, count)

    images = {}
    for idx, media in enumerate(medias):
        images[idx] = media.thumbnail_url

    return images;


@app.get("/get_user_info")
async def get_user_info():
    return cl.user_info

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
    idx = 1
    for media in medias:
        for res in media.resources:
            images[idx] = res.thumbnail_url
            idx += 1
            print(idx)
            if idx == count:
                break
        if idx == count:
            break

    return images

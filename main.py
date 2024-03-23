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
        print(media.resources)
        if not media.resources:
            images[idx] = media.thumbnail_url
            idx += 1
        else:
            for res in media.resources:
                images[idx] = res.thumbnail_url
                idx += 1
                if idx > count:
                    break
        if idx > count:
            break

    return images

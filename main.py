from fastapi import FastAPI
from instagrapi import Client

app = FastAPI()

cl = Client()
cl.login("mementross", "qwer1234!")

@app.get("/images")
async def getImages(tag: str, count: int):
    user_id = cl.user_id_from_username(tag)
    medias = cl.user_medias(user_id, count)

    images = {}
    idx = 1
    for media in medias:
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

@app.get("/postings")
async def getPostings(tag: str, count: int):
    user_id = cl.user_id_from_username(tag)
    medias = cl.user_medias(user_id, count)

    postings = {}
    posting_idx = 1
    for media in medias:
        posting = {}
        posting["caption"] = media.caption_text
        posting["date"] = media.taken_at
        images = {}
        if not media.resources:
            images[1] = media.thumbnail_url
        else:
            idx = 1
            for res in media.resources:
                images[idx] = res.thumbnail_url
                idx += 1
        posting["images"] = images
        postings[posting_idx] = posting
        posting_idx += 1

    return postings
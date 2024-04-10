from fastapi import FastAPI
from instagrapi import Client
import datetime

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

@app.get("/posts")
async def getPosts(tag: str, count: int):
    user_id = cl.user_id_from_username(tag)
    medias = cl.user_medias(user_id, count)

    posts = {}
    post_idx = 1
    for media in medias:
        post = {}
        post["caption"] = media.caption_text
        post["date"] = media.taken_at
        images = {}
        if not media.resources:
            images[1] = media.thumbnail_url
        else:
            idx = 1
            for res in media.resources:
                images[idx] = res.thumbnail_url
                idx += 1
        post["images"] = images
        posts[post_idx] = post
        post_idx += 1

    return posts

@app.get("/posts/date")
async def getPosts(tag: str, date: str, count: int):
    user_id = cl.user_id_from_username(tag)
    medias = cl.user_medias(user_id, 20)

    criterion_date = datetime.datetime.strptime(date, "%Y-%m-%d")

    posts = {}
    post_idx = 1
    for media in medias:
        post = {}
        post_date = media.taken_at.replace(tzinfo=None)

        if post_date > criterion_date:
            continue
        post["caption"] = media.caption_text
        post["date"] = media.taken_at
        images = {}
        if not media.resources:
            images[1] = media.thumbnail_url
        else:
            idx = 1
            for res in media.resources:
                images[idx] = res.thumbnail_url
                idx += 1
        post["images"] = images
        posts[post_idx] = post
        post_idx += 1
        if post_idx > count:
            break

    return posts
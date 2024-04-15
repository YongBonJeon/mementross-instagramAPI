import json
from fastapi import FastAPI, Depends, HTTPException
from instagrapi import Client
import datetime

from sqlalchemy.orm import Session

import crud
from database import SessionLocal, engine

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/members/{member_insta_username}")
def read_member(member_insta_username: str, db: Session = Depends(get_db)):
    db_member = crud.get_member(db, member_insta_username=member_insta_username)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member


def update_member(db: Session, member_insta_username: str, member_insta_posting: str):
    db_member = crud.get_member(db, member_insta_username=member_insta_username)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    db_member.member_insta_posting = member_insta_posting
    db.commit()
    return db_member


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
async def getPosts(tag: str, count: int, db: Session = Depends(get_db)):
    user_info = cl.user_info_by_username_v1(tag)
    user_id = user_info.pk
    medias = cl.user_medias(user_id, count)

    posts = {}
    totalimages = {}
    post_idx = 1
    image_idx = 1
    for media in medias:
        post = {}
        post["caption"] = media.caption_text
        post["date"] = media.taken_at
        images = {}
        if not media.resources:
            images[1] = media.thumbnail_url
            totalimages[image_idx] = media.thumbnail_url
            image_idx += 1
        else:
            for res in media.resources:
                images[image_idx] = res.thumbnail_url
                totalimages[image_idx] = res.thumbnail_url
                image_idx += 1
        post["images"] = images
        posts[post_idx] = post
        post_idx += 1

    urls_str = {k: str(v) for k, v in totalimages.items()}
    JSON = json.dumps(urls_str)
    db_member = crud.get_member(db, member_insta_username=tag)
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    db_member.member_insta_posting = JSON
    db.commit()
    print(db_member.member_insta_posting)

    return posts


@app.get("/posts/date")
async def getPosts(tag: str, date: str, count: int):
    user_info = cl.user_info_by_username_v1(tag)
    user_id = user_info.pk
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

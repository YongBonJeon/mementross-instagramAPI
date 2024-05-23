import json
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException
from instagrapi import Client
import datetime
import openai

from sqlalchemy.orm import Session

import crud
from database import SessionLocal, engine
from pydantic import BaseModel

from const import openai_api_key

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Item(BaseModel):
    keywords: List[str]


@app.post("/gpt")
def generate(keywords: Item):
    openai.api_key = openai_api_key()

    query = ""
    for keyword in keywords.keywords:
        query += keyword + " "
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": "#Context#"
                        + "I want to write a diary in korean based on a Instagram post I uploaded"

                        + "#Objective#"
                        + "Act as a diary writer, that will write a diary based on the description of the photo and additional information provided by me."

                        + "#Style#"
                        + "It should be brief, its content only based on the description of the photo provided and additional information I provide. do not describe photo in the diary nor mention taking/uploading of the photo. diary should be written in past tense. "

                        + "#Tone#"
                        + "Do not exaggerate, write as if you are a blunt person, explaining to a friend. each phrases should be connected so that they form a long sentence, starting new sentence only if necessary. Do not end phrases with '습니다'or'한다'or'했다'or'었다'. if it does, convert to '어'"

                        + "#Audience#"
                        + "Only I will be the one to read it."

                        + "#Response#"
                        + "A short diary in korean."

                        + "#description of the photo#"
                        + query
             }
        ]
    )


    return response.choices[0].message.content


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
    user_info = cl.user_info_by_username_v1(tag)
    user_id = user_info.pk
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
    for media in medias:
        post = {}
        post["caption"] = media.caption_text
        post["date"] = media.taken_at
        images = {}
        image_idx = 1
        if not media.resources:
            images[1] = media.thumbnail_url
            totalimages[image_idx] = media.thumbnail_url
        else:
            for res in media.resources:
                images[image_idx] = res.thumbnail_url
                totalimages[image_idx] = res.thumbnail_url
                image_idx += 1
        post["images"] = images
        posts[post_idx] = post
        post_idx += 1

    urls_str = {k: str(v) for k, v in totalimages.items()}
    #JSON = json.dumps(urls_str)
    #db_member = crud.get_member(db, member_insta_username=tag)
    #if db_member is None:
    #    raise HTTPException(status_code=404, detail="Member not found")
    #db_member.member_insta_posting = JSON
    #db.commit()
    #print(db_member.member_insta_posting)

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

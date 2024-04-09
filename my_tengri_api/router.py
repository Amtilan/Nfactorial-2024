from fastapi import APIRouter
import aiofiles
import json
import datetime
import def_text 
router = APIRouter()

file_path = 'tengrinews.json'
date1 = datetime.datetime.now()

@router.get("/allpages")
async def get_all_articles():
    async with aiofiles.open(file_path, mode='r', encoding='utf-8') as json_file:
        data = await json_file.read()
    articles = json.loads(data)
    return articles

@router.get("/allpages/{name}")
async def get_articles(name):
    async with aiofiles.open(file_path, mode='r', encoding='utf-8') as json_file:
        data = await json_file.read()
    articles = json.loads(data)
    json1 = []
    for i in articles:
        if f"{i['id']}" == f"{name}":
            json1 = i['data']
    return json1

@router.get('/{name}')
async def det_find(name):
    return await def_text.search_news(name=name)

@router.get('/tags/{name}')
async def get_tags(name):
    return await def_text.search_by_tags(name=name)
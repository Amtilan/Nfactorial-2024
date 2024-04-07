from fastapi import APIRouter
import aiofiles
import json
import datetime
import def_text 
router = APIRouter(
    prefix="/news",
    tags=["News"],
)

file_path = 'tengrinews.json'
date1 = datetime.datetime.now()

@router.get("")
async def get_all_articles():
    if date1.hour == 22 and date1.minute == 12:
        await def_text.news_parsing()
    async with aiofiles.open(file_path, mode='r', encoding='utf-8') as json_file:
        data = await json_file.read()
    articles = json.loads(data)
    return articles
import json
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import json
import asyncio
import aiohttp
# import os

GOOGLE_API_KEY = "AIzaSyCPzEJyZAJ2QsIZ-FPBLPKJiVJg2bX77dg"
genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
  "temperature": 0.5,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "HIGH"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "HIGH"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "HIGH"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "HIGH"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

HEADERS = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36"
}

DOMEN = "http://tengrinews.kz"

URL = "https://tengrinews.kz/tag/алматы"
async def get_ai(full_text):
    response = f"Твоя задача заключается в том чтобы полностью обьяснит всю важную информацию в новостной статье очень кратко и ясно.  {full_text}"
    text = await model.generate_content(response)
    return text.text

async def get_response(url_def, headers_def=HEADERS):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url_def, headers=headers_def) as response:
            if response.status == 200:
                return await response.read()
            else:
                return f"Bad response {response.status}"

async def get_text(response):
    soup = BeautifulSoup(response, 'html.parser') 
    all_text = soup.find("div", class_="content_main_text")
    paragraphs = all_text.find_all('p') if all_text else [] 
    tags_div = soup.find("div", class_="content_main_text_tags")
    tags = [span.get_text() for span in tags_div.find_all('span')] if tags_div else []
    full_text = ' '.join(paragraph.get_text() for paragraph in paragraphs)
    ai_text = get_ai(full_text)
    return [full_text, ai_text, tags]    

async def get_soup(response):
    parse_news = []
    soup = BeautifulSoup(response, 'html.parser')
    all_news = soup.find_all("div", class_="content_main_item")
    for item in all_news:
        try:
            title = item.find("span", class_="content_main_item_title").text
            description = item.find(class_="content_main_item_announce").text
            date_time = item.find(class_="content_main_item_meta").text.strip()
            news_url = DOMEN + item.find("a").get("href")
            image_url = DOMEN + item.find('picture').find_all('source')[0].get('srcset') if item.find('picture') else ""
            text_response = await get_response(url_def=news_url) 
            text1, ai_text, tags = await get_text(text_response)
        except Exception as e:
            print(e)
        try:
            all_to_json = {
                "title": title.text if title else "N/A",
                "description": description.text if description else "N/A",
                "date_time": date_time.text.strip() if date_time else "N/A",
                "image": f"{image_url}",
                "url": news_url,
                "text": text1,
                "ai_text": ai_text,
                "tags": tags if tags else "N/A",
            }
        except:
            all_to_json = {
                "title": title.text if title else "N/A",
                "description": description.text if description else "N/A",
                "date_time": date_time.text.strip() if date_time else "N/A",
                "image": f"{image_url}",
                "url": news_url,
                "text": text1,
                "tags": tags
            }
        parse_news.append(all_to_json)
    return parse_news

async def news_parsing():
    soup = []
    for i in range(1, 2):
        response = await get_response(url_def=URL + "/page/" + str(i) + '/')
        soup.append({
            'id': i,
            'data': await get_soup(response)
        })
        
    with open("tengrinews.json", "w", encoding="UTF-8") as file:
        json.dump(soup, file, indent=4, ensure_ascii=False)
    
if __name__ == "__main__":
    news_parsing()
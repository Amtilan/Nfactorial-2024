import json
import requests
from bs4 import BeautifulSoup
import json
import asyncio
import aiohttp
# import def_ai_text

HEADERS = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36"
}

DOMEN = "http://tengrinews.kz"

URL = "https://tengrinews.kz/tag/алматы"

SEARCH_URL = "https://tengrinews.kz/search/?text="

async def get_response(url_def, headers_def=HEADERS):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url_def, headers=headers_def) as response:
            if response.status == 200:
                return await response.text() 
            else:
                return f"Bad response {response.status}"

async def get_text(url_def):
    response = await get_response(url_def)
    if not isinstance(response, str) or response.startswith("Bad response"):
        return response
    
    soup = BeautifulSoup(response, 'html.parser')
    all_text_div = soup.find("div", class_="content_main_text")
    paragraphs = all_text_div.find_all('p') if all_text_div else []
    tags_div = soup.find("div", class_="content_main_text_tags")
    tags = [span.get_text() for span in tags_div.find_all('span')] if tags_div else []
    full_text = ' '.join(paragraph.get_text() for paragraph in paragraphs)
    # ai_text = def_ai_text.get_ai(full_text)
    return [full_text, tags]    

async def get_soup(response):
    parse_news = []
    text1 = ""
    tags = []
    soup = BeautifulSoup(response, 'html.parser')
    all_news = soup.find_all("div", class_="content_main_item")
    for item in all_news:
        try:
            title = item.find("span", class_="content_main_item_title").text
            description = item.find(class_="content_main_item_announce").text
            date_time = item.find(class_="content_main_item_meta").text.strip()
            news_url = DOMEN + item.find("a").get("href")
            image_url = "https://tengrinews.kz" + item.find('picture').find_all('source')[0].get('srcset') if item.find('picture') else ""
            text1, tags = await get_text(url_def=news_url)
        except Exception as e:
            print(e)
        try:
            all_to_json = {
                "title": title if title else "N/A",
                "description": description if description else "N/A",
                "date_time": date_time if date_time else "N/A",
                "image": f"{image_url}",
                "url": news_url,
                "text": text1,
                # "ai_text": ai_text,
                "tags": tags if tags else "N/A",
            }
            parse_news.append(all_to_json)
        except:
            pass
    return parse_news

async def search_by_tags(name):
    soup = []
    response = await(get_response(url_def = "https://tengrinews.kz/tag/" + name))
    soup.append(
        {
         "data" : await get_soup(response)
         }
    )
    return soup

async def search_news(name):
    soup = []
    response = await(get_response(url_def=SEARCH_URL+name))
    soup.append(
        {
            "data" : await get_soup(response)
        }
    )
    return soup

async def news_parsing():
    soup = []
    for i in range(1, 6):
        response = await get_response(url_def=URL + "/page/" + str(i) + '/')
        soup.append({
            'id': i,
            'data': await get_soup(response)
        })
    
    with open("tengrinews.json", "w", encoding="UTF-8") as file:
        json.dump(soup, file, indent=4, ensure_ascii=False)
    
if __name__ == "__main__":
    asyncio.run(news_parsing())
import json
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import json
import requests
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

URL = "https://tengrinews.kz/tag/алматы/"

def get_response(url_def, headers_def = HEADERS):      
    response = requests.get(url = url_def, headers = headers_def) 
    if response.status_code == 200: 
        src = response.content      
        return src                  
    else:
        return f"Bad response {response.status_code}"
    
def get_text(response):
    soup = BeautifulSoup(response, 'html.parser') 
    
    all_text = soup.find("div", class_="content_main_text")
    paragraphs = all_text.find_all('p') if all_text else [] 
    tags_div = soup.find("div", class_="content_main_text_tags")
    tags = [span.get_text() for span in tags_div.find_all('span')] if tags_div else []
    full_text = ' '.join(paragraph.get_text() for paragraph in paragraphs)
    ai_text = get_ai(full_text)
    
    return [full_text, ai_text, tags]
    
# def get_bad_or_good(full_text) -> bool:
    
def get_ai(full_text):
    response = f"Твоя задача заключается в том чтобы полностью обьяснит всю важную информацию в новостной статье очень кратко и ясно.  {full_text}"
    text = model.generate_content(response)
    # print(text)
    return text.text
    
def get_soup(response):
    soup = BeautifulSoup(response, 'html.parser')
    all_news = soup.find_all("div", class_="content_main_item")
    
    parse_news = []
    for item in all_news:
        news_url = ""
        text1 = []
        image_url = ""
        tags = []
        try:
            title = item.find("span", class_="content_main_item_title")
            description = item.find(class_="content_main_item_announce")
            date_time = item.find(class_="content_main_item_meta")
            news_url = DOMEN + item.find("a").get("href")
            image = item.find('picture')
            if image:
                source_tags = image.find_all('source')
                if source_tags:
                    image_url = source_tags[0].get('srcset') 
            text_response = get_response(url_def=news_url) 
            text1 = get_text(text_response)
            tags = [text1[text] for text in range(2, len(text1))] if len(text1) > 1 else []

            # print(tags) 
        except Exception as e:
            print(e)
        try:
            all_to_json = {
                "title": title.text if title else "N/A",
                "description": description.text if description else "N/A",
                "date_time": date_time.text.strip() if date_time else "N/A",
                "image": f"{image_url}",
                "url": news_url,
                "text": text1[0],
                "ai_text": text1[1],
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


def news_parsing():
    soup = []
    for i in range(1, 2):
        response = get_response(url_def=URL+"/page/"f'{i}/')
        soup.append(get_soup(response))
        
    with open(f"core//json//tengrinews.json", "w", encoding="UTF-8") as file:
        json.dump(soup, file, indent=5, ensure_ascii=False)

    
if __name__ == "__main__":
    news_parsing()
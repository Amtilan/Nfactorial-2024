from fastapi import FastAPI
from router import router as tasks_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# import def_text

app = FastAPI()
# scheduler = AsyncIOScheduler()

# scheduler.add_job(def_text.news_parsing, 'cron', hour=22, minute=10)

# scheduler.start()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает все источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешает все методы
    allow_headers=["*"],  # Разрешает все заголовки
)



app.include_router(tasks_router)


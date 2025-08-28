from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram.webhook import Webhook
from .config import TELEGRAM_BOT_TOKEN, BASE_WEBHOOK_URL, WEBHOOK_SECRET
from .database import Base, engine
from .handlers import router
from .admin import admin_router

Base.metadata.create_all(bind=engine)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)
dp.include_router(admin_router)

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    webhook_url = f"{BASE_WEBHOOK_URL}/webhook/{WEBHOOK_SECRET}"
    await bot.set_webhook(webhook_url)

@app.post("/webhook/{secret}")
async def telegram_webhook(secret: str, request: Request):
    if secret != WEBHOOK_SECRET:
        return {"error": "invalid secret"}
    data = await request.json()
    await dp.feed_update(bot, data)
    return {"ok": True}

import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_WEBHOOK_URL = os.getenv("BASE_WEBHOOK_URL")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
SMM_API_URL = os.getenv("SMM_API_URL")
SMM_API_KEY = os.getenv("SMM_API_KEY")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))

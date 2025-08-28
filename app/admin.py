from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Topup, User
from .config import ADMIN_IDS

admin_router = Router()

@admin_router.message(Command("approve"))
async def approve_topup(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Usage: /approve <topup_id>")
        return
    topup_id = int(args[1])
    session = SessionLocal()
    topup = session.query(Topup).filter(Topup.id == topup_id).first()
    if not topup:
        await message.answer("❌ Topup not found")
        session.close()
        return
    if topup.approved:
        await message.answer("⚠️ Already approved")
        session.close()
        return
    user = session.query(User).filter(User.id == topup.user_id).first()
    user.balance += topup.amount
    topup.approved = True
    session.commit()
    await message.answer(f"✅ Topup #{topup.id} approved. User {user.id} credited {topup.amount} INR.")
    await message.bot.send_message(user.id, f"🎉 Your topup of {topup.amount} INR has been approved!")
    session.close()

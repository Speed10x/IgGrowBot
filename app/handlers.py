from aiogram import Router, types, F
from aiogram.filters import Command
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import User, Order, Topup
from .smm_api import get_services, create_order
from .config import ADMIN_IDS

router = Router()

def get_user(session: Session, user_id: int, username: str):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(id=user_id, username=username, balance=0.0)
        session.add(user)
        session.commit()
    return user

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    session = SessionLocal()
    user = get_user(session, message.from_user.id, message.from_user.username or "")
    await message.answer("👋 Welcome to SMM Bot!\n\nUse menu:\n- /services\n- /order\n- /balance\n- /add_balance")
    session.close()

@router.message(Command("balance"))
async def cmd_balance(message: types.Message):
    session = SessionLocal()
    user = get_user(session, message.from_user.id, message.from_user.username or "")
    await message.answer(f"💰 Your balance: {user.balance} INR")
    session.close()

@router.message(Command("services"))
async def cmd_services(message: types.Message):
    services = await get_services()
    reply = "\n".join([f"{s['service']} - {s['name']} ({s['rate']} per 1000)" for s in services[:10]])
    await message.answer(f"📋 Available services:\n{reply}")

@router.message(Command("order"))
async def cmd_order(message: types.Message):
    await message.answer("Send me in format:\n/order <service_id> <link> <quantity>")

@router.message(F.text.startswith("/order "))
async def handle_order(message: types.Message):
    session = SessionLocal()
    args = message.text.split(" ", 3)
    if len(args) < 4:
        await message.answer("⚠️ Usage: /order <service_id> <link> <quantity>")
        return
    service_id, link, qty = int(args[1]), args[2], int(args[3])
    user = get_user(session, message.from_user.id, message.from_user.username or "")
    cost = qty / 1000 * 10  # Example pricing
    if user.balance < cost:
        await message.answer("❌ Not enough balance!")
        return
    user.balance -= cost
    order = Order(user_id=user.id, service_id=service_id, link=link, quantity=qty, status="created")
    session.add(order)
    session.commit()
    res = await create_order(service_id, link, qty)
    await message.answer(f"✅ Order placed: {res}")
    session.close()

@router.message(Command("add_balance"))
async def cmd_add_balance(message: types.Message):
    await message.answer("Send /topup <amount> to request balance topup")

@router.message(F.text.startswith("/topup "))
async def handle_topup(message: types.Message):
    session = SessionLocal()
    try:
        amount = float(message.text.split(" ")[1])
    except:
        await message.answer("⚠️ Usage: /topup <amount>")
        return
    topup = Topup(user_id=message.from_user.id, amount=amount, approved=False)
    session.add(topup)
    session.commit()
    await message.answer(f"✅ Topup request created: {amount} INR. Please send payment proof to admin.")
    for admin_id in ADMIN_IDS:
        await message.bot.send_message(admin_id, f"🔔 New topup request #{topup.id} from {message.from_user.id}: {amount} INR")
    session.close()

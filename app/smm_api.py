import httpx
from .config import SMM_API_URL, SMM_API_KEY

async def get_services():
    async with httpx.AsyncClient() as client:
        resp = await client.post(SMM_API_URL, data={"key": SMM_API_KEY, "action": "services"})
        return resp.json()

async def create_order(service, link, quantity):
    async with httpx.AsyncClient() as client:
        resp = await client.post(SMM_API_URL, data={
            "key": SMM_API_KEY,
            "action": "add",
            "service": service,
            "link": link,
            "quantity": quantity
        })
        return resp.json()

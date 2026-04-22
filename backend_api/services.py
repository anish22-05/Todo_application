import httpx
import time
from datetime import datetime
"""This file contains async function which fetch weather and location details"""
context_cache = {}
CACHE_EXPIRE_SECONDS = 1800

async def fetch_context_data(lat:float, lon:float):
    try:
        lat = float(lat)
        lon = float(lon)
    except (TypeError, ValueError):
        return {"location_name": "Unknown","temperature": 0, "weather_condition":"Unknown","local_time_str":"N/A","local_date":"N/A"}
    # Check if we have a valid cache hit, rounding the coordinates to avoid tiny gps drifts
    cache_key = (round(lat,3), round(lon,3))
    now_ts = time.time()
    if cache_key in context_cache:
        cached_item = context_cache[cache_key]
        if now_ts < cached_item['expires']:
            data = cached_item['data'].copy()
            current_now = datetime.now()
            data["local_time_str"] = current_now.strftime("%A, %I:%M %p")
            data['local_date'] = current_now.strftime("%Y-%m-%d")

            # return cached_item["data"]
            return data
        
    # If no cache fetch from external API's
    # Nominatim requires a User-Agent
    headers = {"User-Agent": "TodoApp Backend/1.0"}
    async with httpx.AsyncClient(headers=headers,timeout=10.0) as client:
        try:
            # Reverse Geocoding
            geo_response = await client.get(f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}")
            geo_res = geo_response.json()
            address = geo_res.get('address',{})
            loc_name = address.get('city') or address.get('town') or address.get('suburb') or 'Unknown'
            # Weather-----------------
            w_response = await client.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&timezone=auto")
            w_res = w_response.json()
            weather = w_res.get('current_weather',{})
            # # it will take care of local time
            # local_iso_time = weather.get('time',"")
            # # formatting the string 
            # formatted_time = "Unknown Time"
            # local_date = "Unknown Date"
            # if local_iso_time:
            #     dt_obj = datetime.fromisoformat(local_iso_time)
            #     formatted_time = dt_obj.strftime("%A, %I:%M %p")
            #     local_date = dt_obj.strftime("%Y-%m-%d")
            # Virtual clock: Capture systems time now instead of using open-meteo.
            system_now = datetime.now()
            result ={
                "location_name": loc_name,
                "temperature": weather.get('temperature'),
                "weather_condition": "Clear" if weather.get('weathercode',0) < 3 else "Cloudy/Rainy",
                "local_time_str": system_now.strftime("%A, %I:%M %p"),
                "local_date": system_now.strftime("%Y-%m-%d")
            }
            # store in cache before return
            context_cache[cache_key] = {
                "data": result,
                "expires": now_ts + CACHE_EXPIRE_SECONDS
            }
            return result
        except Exception as e:
            import traceback
            print(f"SERVICE ERROR: {e}")
            # return fallback data so the app doesn't crash
            traceback.print_exc()

            return {
                "location_name": "Bengaluru",
                "temperature":25,
                "weather_condition":"Clear",
                "local_time_str": datetime.now().strftime("%A, %I:%M %p"),
                "local_date": datetime.now().strftime("%Y-%m-%d")
            } 


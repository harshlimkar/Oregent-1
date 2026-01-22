import json, os, time

CACHE = "review_cache.json"
TTL_HOURS = 72

def _load():
    if os.path.exists(CACHE):
        return json.load(open(CACHE, "r", encoding="utf-8"))
    return {}

def _save(d): json.dump(d, open(CACHE,"w",encoding="utf-8"), indent=2)

def get(url):
    d=_load(); x=d.get(url)
    if not x: return None
    if time.time()-x["ts"] > TTL_HOURS*3600: return None
    return x["data"]

def put(url, data):
    d=_load(); d[url]={"ts":time.time(),"data":data}; _save(d)

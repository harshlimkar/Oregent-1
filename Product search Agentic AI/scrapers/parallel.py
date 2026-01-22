from concurrent.futures import ThreadPoolExecutor, as_completed
from scrapers.base import make_driver

class DriverPool:
    def __init__(self, size=5):
        self.size = size
        self.pool = [make_driver() for _ in range(size)]

    def acquire(self):
        return self.pool.pop()

    def release(self, d):
        self.pool.append(d)

    def close(self):
        for d in self.pool:
            try: d.quit()
            except: pass

def parallel_map(func, items, pool_size=5):
    results = []
    with ThreadPoolExecutor(max_workers=pool_size) as ex:
        futures = [ex.submit(func, it) for it in items]
        for f in as_completed(futures):
            try: results.append(f.result())
            except: pass
    return results

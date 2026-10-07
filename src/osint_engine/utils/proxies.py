import random
from typing import List, Optional

class ProxyManager:
    def __init__(self, proxy_list: Optional[List[str]] = None):
        self.proxies = proxy_list or []

    def get_random_proxy(self) -> Optional[str]:
        if not self.proxies:
            return None
        return random.choice(self.proxies)
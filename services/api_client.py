import time
import aiohttp
from aiohttp import ClientError, ClientTimeout

class ExplanationClient:
    def __init__(self: str, cache_ttl: int = 30000000000000, timeout: int = 10):
        self.base_url = "https://api.dictionaryapi.dev/api/v2/entries/en"
        self.timeout = timeout  # Таймаут запроса в секундах

        self.cache: dict[str, tuple[float, dict]] = {}  # word -> (timestamp, data)
        self.cache_ttl = cache_ttl  # Время жизни кэша в секундах

    async def get_explanation(self, word: str) -> dict:
        now = time.time()

        # Проверка кэша
        if word in self.cache:
            ts, data = self.cache[word]
            if now - ts < self.cache_ttl:
                return data

        try:
            # Создаем клиент с таймаутом
            timeout = ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                try:
                    async with session.get(
                        f"{self.base_url}/{word}"
                    ) as response:
                        data = await response.json()
                        # Сохраняем в кэш, если ответ корректный
                        self.cache[word] = (now, data)
                        return data
                        
                except ClientError as e:
                    # исключения соединения или таймаута
                    raise Exception(f"Failed to get data: {str(e)}")
                    
        except Exception as e:
            # другие ошибки
            raise Exception(f"Unexpected error occurred: {str(e)}")

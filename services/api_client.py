import time
import aiohttp
from aiohttp import ClientError, ClientTimeout

class WeatherClient:
    def __init__(self: str, cache_ttl: int = 30000000000000, timeout: int = 10):
        self.base_url = "https://api.dictionaryapi.dev/api/v2/entries/en"
        self.timeout = timeout  # Таймаут запроса в секундах

        self._wheater_cache: dict[str, tuple[float, dict]] = {}  # word -> (timestamp, data)
        self.cache_ttl = cache_ttl  # Время жизни кэша в секундах

    async def get_weather(self, word: str) -> dict:
        now = time.time()

        # Проверка кэша
        if word in self._wheater_cache:
            ts, data = self._wheater_cache[word]
            if now - ts < self.cache_ttl:
                return data

        #try:
        if 1:
            # Создаем клиент с таймаутом
            timeout = ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                #try:
                if 1:
                    async with session.get(
                        f"{self.base_url}/{word}"
                    ) as response:
                        data = await response.json()
                        # Сохраняем в кэш, если ответ корректный
                        self._wheater_cache[word] = (now, data)
                        return data
                        
                #except ClientError as e:
                    # Обработка ошибок соединения/таймаута
                    #raise Exception(f"Failed to get weather data: {str(e)}")
                    
        #except Exception as e:
            # Обработка других исключений
            #raise Exception(f"Unexpected error occurred: {str(e)}")

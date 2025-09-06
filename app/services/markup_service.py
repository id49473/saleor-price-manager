from decimal import Decimal
from typing import Dict, Optional
import json
from app.core.config import settings
from app.saleor.api import get_channel, update_channel_metadata

class MarkupService:
    def __init__(self):
        # Временно отключаем Redis для demo-режима
        self._cache = {}  # Простой in-memory кэш
        try:
            import redis.asyncio as redis
            self.redis = redis.from_url(settings.REDIS_URL)
        except:
            print("Redis not available, using in-memory cache")
            self.redis = None
        
    async def get_channel_markup(self, channel_id: str) -> Optional[Decimal]:
        """Получить процент наценки для канала"""
        cache_key = f"channel_markup:{channel_id}"
        
        # Пробуем получить из кэша
        if self.redis:
            try:
                cached = await self.redis.get(cache_key)
                if cached:
                    return Decimal(cached.decode())
            except:
                pass
        else:
            # Используем in-memory кэш
            if cache_key in self._cache:
                return Decimal(self._cache[cache_key])
            
        # Если нет в кэше, получаем из Saleor
        channel = await get_channel(channel_id)
        if channel and "metadata" in channel:
            for item in channel["metadata"]:
                if item["key"] == "price_markup_percent":
                    markup = Decimal(item["value"])
                    # Кэшируем результат
                    if self.redis:
                        try:
                            await self.redis.set(cache_key, str(markup), ex=3600)
                        except:
                            pass
                    else:
                        self._cache[cache_key] = str(markup)
                    return markup
                    
        return Decimal('0')
        
    async def set_channel_markup(self, channel_id: str, markup_percent: Decimal) -> bool:
        """Установить процент наценки для канала"""
        # Обновляем в Saleor
        success = await update_channel_metadata(
            channel_id, 
            [{"key": "price_markup_percent", "value": str(markup_percent)}]
        )
        
        if success:
            # Обновляем кэш
            cache_key = f"channel_markup:{channel_id}"
            if self.redis:
                try:
                    await self.redis.set(cache_key, str(markup_percent), ex=3600)
                except:
                    pass
            else:
                self._cache[cache_key] = str(markup_percent)
            
        return success
        
    async def invalidate_cache(self, channel_id: str):
        """Инвалидировать кэш для канала"""
        cache_key = f"channel_markup:{channel_id}"
        if self.redis:
            try:
                await self.redis.delete(cache_key)
            except:
                pass
        else:
            self._cache.pop(cache_key, None)

markup_service = MarkupService()

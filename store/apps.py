from django.apps import AppConfig

class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    def ready(self):
        # Importamos aquí para evitar problemas de importación circular
        import store.signals
        from .redis_cache import ProductCache
        
        try:
            cache = ProductCache()
            cache.cache_all_products()
        except Exception as e:
            print("Failed to cache products:", e)
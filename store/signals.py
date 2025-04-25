from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django_redis import get_redis_connection
import json
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Card
from .redis_cache import ProductCache


@receiver(user_logged_in)
def load_cart_from_redis(sender, user, request, **kwargs):
    redis = get_redis_connection("default")
    cart_data = redis.get(f"user_cart:{user.id}")
    if cart_data:
        try:
            request.session['cart'] = json.loads(cart_data)
            request.session.modified = True
        except Exception as e:
            print("Error loading cart from Redis:", e)


@receiver(user_logged_in)
def load_recent_cards_from_redis(sender, user, request, **kwargs):
    redis = get_redis_connection("default")
    data = redis.get(f"user_recent_cards:{user.id}")
    if data:
        try:   
            request.session['recent_cards'] = json.loads(data)
            request.session.modified = True
        except Exception as e:
            print("Failed to load recent cards:", e)

@receiver(post_save, sender=Card)
@receiver(post_delete, sender=Card)
def update_product_cache(sender, instance, **kwargs):
    cache = ProductCache()
    cache.invalidate_product(instance.id)
    cache.cache_all_products()
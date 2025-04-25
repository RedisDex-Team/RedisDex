from django_redis import get_redis_connection
import json
from .models import Card, Order, OrderItem
from django.utils import timezone
import datetime

class ProductCache:
    def __init__(self):
        self.redis = get_redis_connection("default")
    
    def cache_all_products(self):
        """Almacena todos los productos en Redis"""
        products = Card.objects.all()
        for product in products:
            key = f"product:{product.id}"
            product_data = {
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'image_url': product.image_url,
                'description': product.description,
                'unique_visits': 0,  # Inicialmente 0 visitas
                'sales_count': 0,    # Inicialmente 0 ventas
                'last_updated': timezone.now().isoformat()
            }
            self.redis.set(key, json.dumps(product_data))
    
    def get_product(self, product_id, user_id=None):
        """Obtiene un producto de Redis y actualiza visitas únicas"""
        key = f"product:{product_id}"
        product_data = self.redis.get(key)
        
        if product_data:
            product_data = json.loads(product_data)
            
            # Si hay un user_id, actualizamos la visita única
            if user_id:
                visit_key = f"product_visits:{product_id}"
                visits = self.redis.sadd(visit_key, user_id)
                if visits == 1:  # Si es una nueva visita única
                    product_data['unique_visits'] += 1
                    self.redis.set(key, json.dumps(product_data))
            
            return product_data
        return None
    
    def record_sale(self, product_id, quantity):
        """Registra una venta y actualiza el contador"""
        key = f"product:{product_id}"
        product_data = self.redis.get(key)
        
        if product_data:
            product_data = json.loads(product_data)
            product_data['sales_count'] += int(quantity)
            product_data['last_updated'] = timezone.now().isoformat()
            self.redis.set(key, json.dumps(product_data))
            
            # También guardamos la venta en un conjunto para estadísticas
            sale_key = f"product_sales:{product_id}"
            timestamp = int(timezone.now().timestamp())  # Timestamp Unix
            self.redis.zadd(sale_key, {
                str(quantity): timestamp  # Usamos el timestamp como score
            })
    
    def get_product_stats(self, product_id):
        """Obtiene estadísticas de una carta"""
        key = f"product:{product_id}"
        product_data = self.redis.get(key)
        
        if product_data:
            data = json.loads(product_data)
            visits = self.redis.scard(f"product_visits:{product_id}")
            sales_key = f"product_sales:{product_id}"
            
            # Obtener ventas por día
            sales_by_day = {}
            today = timezone.now().date()
            for i in range(7):  # Últimos 7 días
                date = today - datetime.timedelta(days=i)
                start_timestamp = int(datetime.datetime.combine(date, datetime.time.min).timestamp())
                end_timestamp = int(datetime.datetime.combine(date, datetime.time.max).timestamp())
                
                # Obtener todas las ventas del día usando los timestamps
                sales = self.redis.zrangebyscore(
                    sales_key,
                    start_timestamp,
                    end_timestamp
                )
                
                # Convertir los valores a float y sumarlos
                sales_by_day[date.isoformat()] = sum(float(sale) for sale in sales)
            
            return {
                'visits': visits,
                'sales': data['sales_count'],
                'sales_by_day': sales_by_day,
                'last_updated': data['last_updated']
            }
        return None
    
    def get_top_products(self, metric='sales', limit=10):
        """Obtiene los productos más populares por ventas o visitas"""
        products = []
        for key in self.redis.keys('product:*'):
            product_data = json.loads(self.redis.get(key))
            product_id = product_data['id']
            
            if metric == 'sales':
                score = product_data['sales_count']
            else:  # 'visits'
                score = self.redis.scard(f"product_visits:{product_id}")
            
            products.append((product_id, score, product_data['name']))
        
        # Ordenar por el score en orden descendente
        products.sort(key=lambda x: x[1], reverse=True)
        return products[:limit]

    def get_all_products(self):
        """Obtiene todos los productos de Redis"""
        products = []
        for key in self.redis.keys('product:*'):
            product_data = self.redis.get(key)
            if product_data:
                products.append(json.loads(product_data))
        return products

    def invalidate_product(self, product_id):
        """Invalidates the cache for a specific product"""
        key = f"product:{product_id}"
        self.redis.delete(key)
        # Also invalidate the visits set
        visit_key = f"product_visits:{product_id}"
        self.redis.delete(visit_key)
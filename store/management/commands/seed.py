# myapp/management/commands/seed.py
from django.core.management.base import BaseCommand
from store.models import Card
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Inserta usuarios y productos predeterminados'

    def handle(self, *args, **kwargs):
        # Create regular user if it doesn't exist
        self.stdout.write(self.style.MIGRATE_HEADING('=== SEEDING USUARIOS ==='))
        try:
            user = User.objects.get(username='user1')
            self.stdout.write(self.style.WARNING('🟡 Usuario ya existe: user1'))
        except User.DoesNotExist:
            user = User.objects.create_user('user1', password='1234')
            self.stdout.write(self.style.SUCCESS('🟢 Usuario creado: user1'))

        # Create admin user if it doesn't exist
        try:
            admin_user = User.objects.get(username='admin')
            self.stdout.write(self.style.WARNING('🟡 Usuario admin ya existe'))
        except User.DoesNotExist:
            admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('🟢 Usuario admin creado'))

        # Create products
        self.stdout.write('\n' + self.style.MIGRATE_HEADING('=== SEEDING PRODUCTOS ==='))
        productos = [
            {"name": "Pikachu VMax", "price": 10.0, "image_url": "https://www.cardtrader.com/uploads/blueprints/image/201792/show_pikachu-vmax-006-s8a-g-25th-anniversary-golden-box.jpg", "description": "A nice pikachu card."},
            {"name": "Kingdra Ex Special Ilustration", "price": 20.27, "image_url": "https://www.cardtrader.com/uploads/blueprints/image/295844/show_kingdra-ex-special-illustration-rare-131-sv-black-star-promos.png", "description": "The Pokémon Trading Card Game (Japanese: ポケモンカードゲーム) is a tabletop game that involves collecting, trading and playing with Pokémon themed playing cards."},
            {"name": "Salamence ex", "price": 3.51, "image_url": "https://www.cardtrader.com/uploads/blueprints/image/326091/show_salamence-ex-full-art-177-159-journey-together.jpg", "description": "The Pokémon Trading Card Game (Japanese: ポケモンカードゲーム) is a tabletop game that involves collecting, trading and playing with Pokémon themed playing cards."},
            {"name": "Jolteon ex", "price": 4.18, "image_url": "https://www.cardtrader.com/uploads/blueprints/image/316634/show_jolteon-ex-ultra-rare-030-131-prismatic-evolutions.jpg", "description": "The Pokémon Trading Card Game (Japanese: ポケモンカードゲーム) is a tabletop game that involves collecting, trading and playing with Pokémon themed playing cards."},
            {"name": "Miraidon ex", "price": 5.63, "image_url": "https://www.cardtrader.com/uploads/blueprints/image/241958/show_miraidon-ex-secret-rare-253-198-scarlet-violet.png", "description": "The Pokémon Trading Card Game (Japanese: ポケモンカードゲーム) is a tabletop game that involves collecting, trading and playing with Pokémon themed playing cards."},
        ]

        for prod in productos:
            obj, created = Card.objects.get_or_create(name=prod["name"], defaults=prod)
            if created:
                self.stdout.write(self.style.SUCCESS(f'🟢 Producto creado: {obj.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'🟡 Ya existe: {obj.name}'))

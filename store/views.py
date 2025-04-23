from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from .models import Card, Order, OrderItem
from .forms import EditProfileForm
from django_redis import get_redis_connection
import json

# Create your views here.


def home(request):
    return render(request, 'store/home.html')


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # inicia sesión automáticamente
            return redirect('home')  # redirige donde quieras
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def shop(request):
    query = request.GET.get('q', '').strip()
    cards = Card.objects.all()

    if query:
        cards = cards.filter(name__icontains=query)

        # Guardar término en historial Redis por usuario
        if request.user.is_authenticated:
            redis = get_redis_connection("default")
            key = f"user_searches:{request.user.id}"
            searches = redis.lrange(key, 0, -1)
            decoded = [term.decode('utf-8') for term in searches]
            if query not in decoded:
                redis.lpush(key, query)
                redis.ltrim(key, 0, 9)  # máx 10 búsquedas

    return render(request, 'store/shop.html', {'cards': cards})


@login_required
def add_to_cart(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    cart = request.session.get('cart', {})

    if str(card_id) in cart:
        cart[str(card_id)]['qty'] += 1
    else:
        cart[str(card_id)] = {
            'name': card.name,
            'price': float(card.price),
            'qty': 1,
            'image_url': card.image_url
        }

    request.session['cart'] = cart
    request.session.modified = True

    if request.user.is_authenticated:
        redis = get_redis_connection("default")
        redis.set(f"user_cart:{request.user.id}", json.dumps(cart), ex=86400)
    return redirect('cart')


@login_required
def cart(request):
    cart = request.session.get('cart', {})
    total = 0

    for item in cart.values():
        item['subtotal'] = round(item['qty'] * item['price'], 2)
        total += item['subtotal']

    return render(request, 'store/cart.html', {
        'cart': cart,
        'total': round(total, 2),
    })


def test_session_view(request):
    counter = request.session.get('counter', 0)
    counter += 1
    request.session['counter'] = counter
    return HttpResponse(f"Sesión activa. Has visitado esta página {counter} veces.")


@login_required
def increase_qty(request, card_id):
    if request.method == "POST":
        cart = request.session.get('cart', {})
        if card_id in cart:
            cart[card_id]['qty'] += 1
            request.session.modified = True
    return redirect('cart')


@login_required
def decrease_qty(request, card_id):
    if request.method == "POST":
        cart = request.session.get('cart', {})
        if card_id in cart:
            if cart[card_id]['qty'] > 1:
                cart[card_id]['qty'] -= 1
            else:
                del cart[card_id]
            request.session.modified = True
    return redirect('cart')


@login_required
def place_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    total = sum(item['qty'] * item['price'] for item in cart.values())
    order = Order.objects.create(user=request.user, total=total)

    for item in cart.values():
        OrderItem.objects.create(
            order=order,
            name=item['name'],
            quantity=item['qty'],
            price=item['price'],
            subtotal=item['qty'] * item['price']
        )

    request.session['cart'] = {}
    request.session.modified = True

    return render(request, 'store/order_success.html', {'order': order})


@login_required
def profile_view(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')

    recent_ids = request.session.get('recent_cards', [])
    recent_cards = Card.objects.filter(id__in=recent_ids)

    recent_cards = sorted(recent_cards, key=lambda x: recent_ids.index(x.id))

    redis = get_redis_connection("default")
    search_history = []
    if request.user.is_authenticated:
        key = f"user_searches:{request.user.id}"
        raw = redis.lrange(key, 0, -1)
        search_history = [term.decode('utf-8') for term in raw]

    return render(request, 'store/profile.html', {
        'user': request.user,
        'orders': orders,
        'recent_cards': recent_cards,
        'search_history': search_history
    })


@login_required
def clear_search_history(request):
    if request.method == "POST":
        redis = get_redis_connection("default")
        redis.delete(f"user_searches:{request.user.id}")
    return redirect('profile')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'store/edit_profile.html', {'form': form})


def card_detail(request, card_id):
    card = get_object_or_404(Card, id=card_id)

    recent = request.session.get('recent_cards', [])
    if card_id in recent:
        recent.remove(card_id)
    recent.insert(0, card_id)
    request.session['recent_cards'] = recent[:5]

    if request.user.is_authenticated:
        redis = get_redis_connection("default")
        redis.set(f"user_recent_cards:{request.user.id}", json.dumps(recent), ex=86400)

    return render(request, 'store/card_detail.html', {'card': card})
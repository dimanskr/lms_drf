import stripe
from config.settings import STRIPE_API_KEY


stripe.api_key = STRIPE_API_KEY


def create_stripe_product(instance):
    """Создаем stripe продукт"""
    title_product = (
        f"{instance.course}" if instance.course else f"{instance.lesson}"
    )
    stripe_product = stripe.Product.create(name=f"{title_product}")
    return stripe_product.get("id")


def create_stripe_price(stripe_product_id, amount):
    """Создаём stripe цену"""
    return stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),
        product=stripe_product_id,
    )


def create_stripe_session(price):
    """Создаём stripe сессию"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/users/payments",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")

def get_status_payment(session_id):
    """ Получаем статус платежа в stripe """
    return stripe.checkout.Session.retrieve(session_id)
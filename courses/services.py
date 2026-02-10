import stripe
import os

def create_product(product_name, description):
    stripe.api_key = os.getenv('STRIPE_API_KEY')

    return stripe.Product.create(name=product_name, description=description)

def create_price(product_id, product_price: int):
    stripe.api_key = os.getenv('STRIPE_API_KEY')

    return stripe.Price.create(
        currency="rub",
        unit_amount=product_price*100,
        product=product_id,
    )

def create_checkout_session(price_id):
    stripe.api_key = os.getenv('STRIPE_API_KEY')

    return stripe.checkout.Session.create(
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
        success_url='http://127.0.0.1:8000/api/payments/success/',
        cancel_url='http://127.0.0.1:8000/api/payments/cancel/'
    )

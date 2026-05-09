import os
from flask import Blueprint, render_template, flash, request, redirect, jsonify
from .models import Product, Cart, Order, ProductImage
from flask_login import current_user, login_required
from . import db
from intasend import APIService
import traceback
from werkzeug.utils import secure_filename
from sqlalchemy import or_

views = Blueprint('views', __name__)

API_PUBLISHABLE_KEY = 'ISPubKey_test_75a58408-dabd-4de7-80fe-1c2b8c5694c1'
API_TOKEN = 'ISSecretKey_test_16b75fd1-2407-4b03-bd6c-d1041df160af'


@views.route('/')
def home():
    items = Product.query.filter_by(flash_sale=True).all()
    return render_template('home.html', items=items, cart=Cart.query.filter_by( customer_link=current_user.id).all()
                           if current_user.is_authenticated else[])


@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html", customer=current_user)


@views.route('/upload_profile', methods=['POST'])
@login_required
def upload_profile():
    file = request.files.get('profile_photo')

    if not file or file.filename == "":
        flash("Please select an image")
        return redirect('/profile')

    try:
        # 🔥 delete old photo (if exists)
        if current_user.profile_photo:
            old_path = current_user.profile_photo.lstrip('/')
            if os.path.exists(old_path):
                os.remove(old_path)
        file_name = secure_filename(file.filename)
        file_path = f'media/{file_name}'
        file.save(file_path)

        current_user.profile_photo = '/' + file_path
        db.session.commit()

        flash("Profile photo updated successfully!")
    except Exception as e:
        db.session.rollback()
        print(e)
        flash("Upload failed!")

    return redirect('/profile')


@views.route('/item/<int:id>')
def item_page(id):
    product = Product.query.get_or_404(id)
    return render_template("item.html", product=product)


@views.route('/add_to_cart/<int:item_id>', methods=['GET', 'POST'])
@login_required
def add_to_cart(item_id):
    item_to_add = Product.query.get(item_id)
    item_exits = Cart.query.filter_by(product_link=item_id, customer_link=current_user.id).first()
    if item_exits:
        try:
            item_exits.quantity = item_exits.quantity + 1
            db.session.add()
            flash('Successfully added item to cart.')
            return redirect(request.referrer)
        except Exception as e:
            print(e)
            flash('Error adding item to cart.')
            return redirect(request.referrer)

    new_cart_item = Cart()
    new_cart_item.quantity = 1
    new_cart_item.product_link = item_to_add.id
    new_cart_item.customer_link = current_user.id

    try:
        db.session.add(new_cart_item)
        db.session.commit()
        flash('Successfully added item to cart.')
        return redirect(request.referrer)
    except Exception as e:
        print(e)
        flash('Error adding item to cart.')
        return redirect(request.referrer)


@views.route('/cart', methods=['GET', 'POST'])
@login_required
def show_cart():
    cart = Cart.query.filter_by(customer_link=current_user.id).all()
    amount = 0
    for item in cart:
        amount += item.product.current_price * item.quantity

    return render_template('cart.html', cart=cart, amount=amount, total=amount+3500)


@views.route('/pluscart')
@login_required
def plus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        cart_item.quantity = cart_item.quantity + 1
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()
        amount = 0
        for item in cart:
            amount += item.product.current_price * item.quantity

        data = {
            'quantity' : cart_item.quantity,
            'amount' : amount,
            'total' : amount+3500
        }

        return jsonify(data)
    return None


@views.route('/minuscart')
@login_required
def minus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        if cart_item.quantity > 1:
            cart_item.quantity = cart_item.quantity - 1
        else:
            db.session.delete(cart_item)

        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()
        amount = 0
        for item in cart:
            amount += item.product.current_price * item.quantity

        data = {
            'quantity' : cart_item.quantity,
            'amount' : amount,
            'total' : amount+3500
        }

        return jsonify(data)
    return None


@views.route('/remove_cart')
@login_required
def remove_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        cart_item = Cart.query.get(cart_id)
        db.session.delete(cart_item)
        db.session.commit()

        cart = Cart.query.filter_by(customer_link=current_user.id).all()
        amount = 0
        for item in cart:
            amount += item.product.current_price * item.quantity

        data = {
            'amount' : amount,
            'total' : amount+3500
        }

        return jsonify(data)
    return None


@views.route('/place_order')
@login_required
def place_order():
    customer_cart = Cart.query.filter_by(customer_link=current_user.id).all()
    if customer_cart:
        try:
            total = 0
            for item in customer_cart:
                total += item.product.current_price * item.quantity

            service = APIService(token=API_TOKEN, publishable_key=API_PUBLISHABLE_KEY, test=True)
            create_order_response = service.collect.mpesa_stk_push(phone_number="254708374149", email=current_user.email, amount=total+3500,
                                                         narrative='Purchase of goods')

            for item in customer_cart:
                new_order = Order()
                new_order.quantity = item.quantity
                new_order.price = item.product.current_price
                new_order.status = create_order_response['invoice']['state'].capitalize()
                new_order.payment_id = create_order_response['id']
                new_order.product_link = item.product_link
                new_order.customer_link = item.customer_link
                db.session.add(new_order)

                product = Product.query.get(item.product_link)
                product.in_stock -= item.quantity
                db.session.delete(item)

            db.session.commit()

            flash('Order Placed Successfully')
            return redirect('/order')

        except Exception as e:
            print("ERROR:", e)
            traceback.print_exc()
            flash('Order not successful')
            return redirect('/')

    else:
        flash('Your Cart is Empty')
        return None


@views.route('/order')
@login_required
def order():
    orders= Order.query.filter_by(customer_link=current_user.id).all()
    return render_template("order.html", orders=orders)


@views.route('/search', methods=['GET', 'POST'])
def search():
    items = []

    # handle GET (from clicking category)
    search_query = request.args.get('query')

    # handle POST (from search form)
    if request.method == 'POST':
        search_query = request.form.get('search')

    if search_query:
        search_query = search_query.strip()
        items = Product.query.filter(
            or_(
                Product.product_name.ilike(f'%{search_query}%'),Product.hashtags.ilike(f'%{search_query}%'))).all()

    return render_template(
        "search.html",items=items,cart=Cart.query.filter_by(customer_link=current_user.id).all()
        if current_user.is_authenticated else [])


@views.route('/about_us')
def about_us():
    return render_template('about_us.html')

@views.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')
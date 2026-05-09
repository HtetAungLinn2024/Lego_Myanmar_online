from flask import Blueprint, render_template, flash, send_from_directory, redirect
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import Product, Order, Customer, ProductImage
from .forms import ShopItemForm, OrderForm
from . import db

admin = Blueprint('admin', __name__)

@admin.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory('../media/', filename)

@admin.route('/add_shop_items', methods=['GET', 'POST'])
@login_required
def add_shop_item():
    if current_user.id == 1:
        form = ShopItemForm()
        if form.validate_on_submit():

            files = form.product_images.data
            # check if no images uploaded
            if not files or files[0].filename == "":
                flash("Please upload at least one image!")
                return render_template('add_shop_items.html', form=form)

            try:
                #  create product
                new_product = Product(
                    product_name=form.product_name.data,
                    current_price=form.current_price.data,
                    previous_price=form.previous_price.data,
                    in_stock=form.in_stock.data,
                    flash_sale=form.flash_sale.data,
                    hashtags=form.hashtags.data
                )
                db.session.add(new_product)
                db.session.commit()

                # save images
                for file in files:
                    if file:
                        file_name = secure_filename(file.filename)
                        file_path = f'media/{file_name}'
                        file.save(file_path)

                        new_image = ProductImage(
                            image_url='/' + file_path,
                            product_id=new_product.id
                        )
                        db.session.add(new_image)

                db.session.commit()

                flash('Product added successfully!')
                return redirect('/shop_items')
            except Exception as e:
                print(e)
                db.session.rollback()
                flash('Error adding product!')

        return render_template('add_shop_items.html', form=form)


@admin.route('/shop_items', methods=['GET', 'POST'])
@login_required
def shop_items():
    if current_user.id == 1:
        items = Product.query.order_by(Product.date_added).all()
        return render_template('shop_items.html', items=items)

    return render_template('404.html')


@admin.route('/update_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    if current_user.id == 1:
        form = ShopItemForm()

        item_to_update = Product.query.get(item_id)

        form.product_name.render_kw = {'placeholder': item_to_update.product_name}
        form.previous_price.render_kw = {'placeholder': item_to_update.previous_price}
        form.current_price.render_kw = {'placeholder': item_to_update.current_price}
        form.in_stock.render_kw = {'placeholder': item_to_update.in_stock}
        form.flash_sale.render_kw = {'placeholder': item_to_update.flash_sale}

        if form.validate_on_submit():

            files = form.product_images.data

            try:
                item_to_update.product_name = form.product_name.data
                item_to_update.current_price = form.current_price.data
                item_to_update.previous_price = form.previous_price.data
                item_to_update.in_stock = form.in_stock.data
                item_to_update.flash_sale = form.flash_sale.data
                item_to_update.hashtags = form.hashtags.data


                #  delete old images first
                ProductImage.query.filter_by(product_id=item_id).delete()
                # then add new ones
                for file in files:
                    if file:
                        file_name = secure_filename(file.filename)
                        file_path = f'media/{file_name}'
                        file.save(file_path)

                        new_image = ProductImage(
                            image_url='/' + file_path,
                            product_id=item_id
                        )
                        db.session.add(new_image)
                db.session.commit()
                flash('Product updated successfully!')
                return redirect('/shop_items')
            except Exception as e:
                db.session.rollback()
                print("ERROR:",e)
                flash('Item not updated!')

        return render_template('update_item.html', form=form)
    return render_template('404.html')


@admin.route('/delete_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    if current_user.id == 1:
        try:
            item_to_delete = Product.query.get(item_id)
            db.session.delete(item_to_delete)
            db.session.commit()
            flash('item deleted successfully!')
            return redirect('/shop_items')
        except Exception as e:
            print(e)
            flash('cannot be deleted!')
            return redirect('/shop_items')
    return render_template('404.html')


@admin.route('/view_orders')
@login_required
def order_view():
    if current_user.id == 1:
        orders = Order.query.all()
        return render_template('/view_orders.html', orders=orders)
    return render_template('404.html')


@admin.route('/order_update/<int:order_id>', methods=['GET', 'POST'])
@login_required
def order_update(order_id):
    if current_user.id == 1:
        form = OrderForm()

        order = Order.query.get(order_id)
        if form.validate_on_submit():
            status = form.order_status.data
            order.status = status

            try:
                db.session.commit()
                flash(f'Order ID{order.id} updated successfully!')
                return redirect('/view_orders')
            except Exception as e:
                print(e)
                flash('Order not Update')
                return redirect('/view_orders')

        return render_template('order_update.html', form=form)
    else:
        return render_template('404.html')


@admin.route('/customers')
@login_required
def customer_view():
    if current_user.id == 1:
        customers = Customer.query.all()
        return render_template('/customers.html', customers=customers)
    else:
        return render_template('404.html')


@admin.route('/admin_page')
@login_required
def admin_page():
    if current_user.id == 1:
        return render_template('admin_page.html')
    else:
        return render_template('404.html')
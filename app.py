import os
import random
import datetime
from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'streetbites_and_dine_ultra_secure_key_2026'

# SQLite Database Setup
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'streetbites.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ============================================================================
# Database Models
# ============================================================================

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    role = db.Column(db.String(20), default='customer') # 'customer', 'vendor', 'admin'
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone or '',
            'address': self.address or '',
            'role': self.role,
            'vendor_id': self.vendor_id
        }

class Vendor(db.Model):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    vendor_type = db.Column(db.String(50), default='street_vendor') # 'street_vendor', 'restaurant', 'food_truck', 'cafe'
    tagline = db.Column(db.String(255))
    category = db.Column(db.String(100), nullable=False) # e.g. "Chaat & Street Food", "Biryani & Tandoor", "South Indian"
    landmark = db.Column(db.String(255), nullable=False) # e.g. "Opposite Metro Pillar 42, Karol Bagh"
    city = db.Column(db.String(100), default='Delhi NCR')
    phone = db.Column(db.String(30), nullable=False)
    rating = db.Column(db.Float, default=4.8)
    reviews_count = db.Column(db.Integer, default=120)
    image_url = db.Column(db.String(500))
    is_open = db.Column(db.Boolean, default=True)
    rush_level = db.Column(db.String(30), default='low') # 'low', 'medium', 'high'
    current_token_serving = db.Column(db.Integer, default=10)
    has_hygiene_badge = db.Column(db.Boolean, default=True) # FSSAI / Clean Street Food Hub Certified
    upi_id = db.Column(db.String(100), default='vendor@upi')
    zero_commission_enabled = db.Column(db.Boolean, default=True)
    min_price = db.Column(db.Float, default=40.0)
    opening_hours = db.Column(db.String(100), default='12:00 PM - 10:30 PM')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    items = db.relationship('MenuItem', backref='vendor', lazy=True, cascade="all, delete-orphan")
    orders = db.relationship('Order', backref='vendor', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'vendor_type': self.vendor_type,
            'tagline': self.tagline or '',
            'category': self.category,
            'landmark': self.landmark,
            'city': self.city,
            'phone': self.phone,
            'rating': self.rating,
            'reviews_count': self.reviews_count,
            'image_url': self.image_url,
            'is_open': self.is_open,
            'rush_level': self.rush_level,
            'current_token_serving': self.current_token_serving,
            'has_hygiene_badge': self.has_hygiene_badge,
            'upi_id': self.upi_id,
            'zero_commission_enabled': self.zero_commission_enabled,
            'min_price': self.min_price,
            'opening_hours': self.opening_hours,
            'items_count': len(self.items) if self.items else 0
        }

class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, default=4.8)
    image_url = db.Column(db.String(500))
    is_veg = db.Column(db.Boolean, default=True)
    is_bestseller = db.Column(db.Boolean, default=False)
    is_available = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'vendor_id': self.vendor_id,
            'name': self.name,
            'category': self.category,
            'description': self.description or '',
            'price': self.price,
            'rating': self.rating,
            'image_url': self.image_url,
            'is_veg': self.is_veg,
            'is_bestseller': self.is_bestseller,
            'is_available': self.is_available
        }

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    token_number = db.Column(db.String(30), nullable=False) # e.g. "TK-42"
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    order_type = db.Column(db.String(30), default='takeaway_token') # 'takeaway_token', 'dine_in', 'delivery'
    delivery_address = db.Column(db.Text)
    payment_method = db.Column(db.String(30), default='UPI') # 'UPI', 'Cash at Stall', 'Card'
    payment_status = db.Column(db.String(20), default='Paid')
    status = db.Column(db.String(30), default='Preparing') # 'Order Placed', 'Preparing', 'Ready for Pickup', 'Completed', 'Cancelled'
    subtotal = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, default=0.0)
    tax = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, nullable=False)
    coupon_code = db.Column(db.String(30))
    notes = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'token_number': self.token_number,
            'vendor_id': self.vendor_id,
            'vendor_name': self.vendor.name if self.vendor else 'Food Spot',
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'order_type': self.order_type,
            'delivery_address': self.delivery_address or 'Self-Pickup at Counter',
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'status': self.status,
            'subtotal': self.subtotal,
            'discount': self.discount,
            'tax': self.tax,
            'total_amount': self.total_amount,
            'coupon_code': self.coupon_code or '',
            'created_at': self.created_at.strftime('%d %b %Y, %I:%M %p'),
            'items': [item.to_dict() for item in self.items]
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    item_name = db.Column(db.String(150), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'item_name': self.item_name,
            'quantity': self.quantity,
            'price': self.price
        }

class Reservation(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    booking_ref = db.Column(db.String(50), unique=True, nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    res_date = db.Column(db.String(20), nullable=False)
    res_time = db.Column(db.String(20), nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    seating_area = db.Column(db.String(50), default='Main Dining')
    special_request = db.Column(db.Text)
    status = db.Column(db.String(20), default='Confirmed')
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'booking_ref': self.booking_ref,
            'vendor_id': self.vendor_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'res_date': self.res_date,
            'res_time': self.res_time,
            'guests': self.guests,
            'seating_area': self.seating_area,
            'special_request': self.special_request or '',
            'status': self.status,
            'created_at': self.created_at.strftime('%d %b %Y')
        }

class Coupon(db.Model):
    __tablename__ = 'coupons'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30), unique=True, nullable=False)
    discount_percent = db.Column(db.Float, default=0)
    flat_discount = db.Column(db.Float, default=0)
    min_order = db.Column(db.Float, default=0)

    def to_dict(self):
        return {
            'code': self.code,
            'discount_percent': self.discount_percent,
            'flat_discount': self.flat_discount,
            'min_order': self.min_order
        }

# ============================================================================
# Seed Data Initializer
# ============================================================================

def seed_database():
    db.create_all()

    # Seed Admin User
    if not User.query.filter_by(email='admin@streetbites.com').first():
        admin = User(
            name='Platform Master',
            email='admin@streetbites.com',
            password_hash=generate_password_hash('admin123'),
            phone='+91 99999 00000',
            role='admin'
        )
        db.session.add(admin)

    # Seed Demo Customer
    if not User.query.filter_by(email='customer@example.com').first():
        customer = User(
            name='Aarav Sharma',
            email='customer@example.com',
            password_hash=generate_password_hash('customer123'),
            phone='+91 98765 43210',
            address='Flat 302, Green Avenue, Delhi NCR',
            role='customer'
        )
        db.session.add(customer)

    # Seed Coupons
    if not Coupon.query.filter_by(code='STREETLOVE').first():
        db.session.add(Coupon(code='STREETLOVE', discount_percent=15.0, min_order=150.0))
        db.session.add(Coupon(code='FIRSTBITE', flat_discount=30.0, min_order=100.0))
        db.session.add(Coupon(code='DINER20', discount_percent=20.0, min_order=400.0))

    # Seed Vendors (Street Vendors + Restaurants + Food Trucks)
    if Vendor.query.count() == 0:
        vendors = [
            Vendor(
                name='Gupta Ji Chaat & Pani Puri Bhandar',
                vendor_type='street_vendor',
                tagline='Crunchy Suji & Atta Golgappe with 5 Types of Flavored Spicy Pudina Water',
                category='Chaat & Street Food',
                landmark='Corner of Block B, Near Metro Pillar 142, Karol Bagh',
                city='Delhi NCR',
                phone='+91 98112 34567',
                rating=4.9,
                reviews_count=340,
                image_url='https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=800&q=80',
                is_open=True,
                rush_level='medium',
                current_token_serving=18,
                has_hygiene_badge=True,
                upi_id='guptachaat@oksbi',
                zero_commission_enabled=True,
                min_price=30.0,
                opening_hours='03:00 PM - 10:30 PM'
            ),
            Vendor(
                name='Sharma Sweets & Chole Bhature Express',
                vendor_type='street_vendor',
                tagline='Fluffy Golden Bhature with Pindi Chole, Amla Achar & Sweet Lassi',
                category='North Indian Snacks',
                landmark='Shop 4, Main Market, Chandni Chowk',
                city='Delhi NCR',
                phone='+91 98114 55667',
                rating=4.8,
                reviews_count=510,
                image_url='https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?auto=format&fit=crop&w=800&q=80',
                is_open=True,
                rush_level='high',
                current_token_serving=34,
                has_hygiene_badge=True,
                upi_id='sharmachole@paytm',
                zero_commission_enabled=True,
                min_price=60.0,
                opening_hours='08:00 AM - 04:00 PM'
            ),
            Vendor(
                name='Al-Noor Kathi Rolls & Shawarma Hub',
                vendor_type='street_vendor',
                tagline='Charcoal Grilled Chicken Kathi Rolls, Paneer Tikka Rolls & Rumali Wraps',
                category='Rolls & Wraps',
                landmark='Opposite City Center Mall, Sector 18',
                city='Noida',
                phone='+91 99887 11223',
                rating=4.9,
                reviews_count=290,
                image_url='https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=800&q=80',
                is_open=True,
                rush_level='low',
                current_token_serving=12,
                has_hygiene_badge=True,
                upi_id='alnoorkathi@icici',
                zero_commission_enabled=True,
                min_price=50.0,
                opening_hours='05:00 PM - 11:30 PM'
            ),
            Vendor(
                name="Anna's 99 Variety Dosa Cart",
                vendor_type='food_truck',
                tagline='Crispy Butter Mysore Masala, Cheese Burst & Ghee Roast Dosas on Wheels',
                category='South Indian',
                landmark='Tech Park Gate 3, Cyber Hub Road',
                city='Gurugram',
                phone='+91 97766 54321',
                rating=4.9,
                reviews_count=420,
                image_url='https://images.unsplash.com/photo-1668236543090-82eba5ee5976?auto=format&fit=crop&w=800&q=80',
                is_open=True,
                rush_level='medium',
                current_token_serving=26,
                has_hygiene_badge=True,
                upi_id='annadosa@axl',
                zero_commission_enabled=True,
                min_price=70.0,
                opening_hours='07:30 AM - 10:00 PM'
            ),
            Vendor(
                name='Tibetan Momo Corner & Thukpa Bar',
                vendor_type='street_vendor',
                tagline='Steamed, Pan-Fried Kurkure Momos with Fiery Red Dalle Chili Sauce',
                category='Momos & Street Fast Food',
                landmark='Kalyan Nagar, Outer Ring Road, Near Bus Stand',
                city='Bangalore',
                phone='+91 96543 21098',
                rating=4.7,
                reviews_count=180,
                image_url='https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?auto=format&fit=crop&w=800&q=80',
                is_open=True,
                rush_level='low',
                current_token_serving=8,
                has_hygiene_badge=True,
                upi_id='tibetanmomos@ybl',
                zero_commission_enabled=True,
                min_price=60.0,
                opening_hours='04:00 PM - 10:30 PM'
            ),
            Vendor(
                name='The Urban Tandoor & Royal Biryani',
                vendor_type='restaurant',
                tagline='Fine Indian Dining, Dum Biryani Handis, Tandoori Platters & Luxury Ambience',
                category='Biryani & Mughlai',
                landmark='Building 24, Outer Circle, Connaught Place',
                city='Delhi NCR',
                phone='+91 99112 23344',
                rating=4.9,
                reviews_count=780,
                image_url='https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=800&q=80',
                is_open=True,
                rush_level='medium',
                current_token_serving=45,
                has_hygiene_badge=True,
                upi_id='urbantandoor@hdfcbank',
                zero_commission_enabled=False,
                min_price=220.0,
                opening_hours='12:00 PM - 11:30 PM'
            ),
            Vendor(
                name='Crust & Flame Artisanal Pizzeria',
                vendor_type='cafe',
                tagline='Wood-fired Neapolitan Pizzas, Truffle Pastas & Handcrafted Cold Brews',
                category='Italian & Cafe',
                landmark='12th Main Road, Indiranagar',
                city='Bangalore',
                phone='+91 98450 12345',
                rating=4.8,
                reviews_count=460,
                image_url='https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=800&q=80',
                is_open=True,
                rush_level='low',
                current_token_serving=14,
                has_hygiene_badge=True,
                upi_id='crustandflame@icici',
                zero_commission_enabled=False,
                min_price=180.0,
                opening_hours='11:00 AM - 11:00 PM'
            )
        ]

        for v in vendors:
            db.session.add(v)
        db.session.flush()

        # Seed Menu Items for each Vendor
        menu_data = [
            # Gupta Ji Chaat
            (vendors[0].id, 'Signature Suji Golgappe (6 Pcs)', 'Chaat', 'Crispy suji puris served with boiled potato-chickpea filling and 5 chilled waters: Hing, Mint, Khatta Meetha, Pudina & Garlic.', 40.0, 4.9, 'https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=400&q=80', True, True),
            (vendors[0].id, 'Dahi Papdi Chaat Royale', 'Chaat', 'Crisp papdis layered with creamy spiced curd, tamarind chutney, mint drizzle, pomegranate pearls and crunchy sev.', 60.0, 4.8, 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?auto=format&fit=crop&w=400&q=80', True, True),
            (vendors[0].id, 'Kurkuri Aloo Tikki Burger Pav', 'Snacks', 'Double deep fried golden potato cutlet served in butter toasted pav with zesty green chutney.', 50.0, 4.7, 'https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?auto=format&fit=crop&w=400&q=80', True, False),
            (vendors[0].id, 'Sev Puri Mumbai Chowpatty Style', 'Chaat', 'Flat crisp puris topped with potatoes, raw onions, tangy raw mango slivers, sweet and spicy chutneys.', 50.0, 4.8, 'https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=400&q=80', True, False),

            # Sharma Sweets & Chole Bhature
            (vendors[1].id, 'Special Pindi Chole Bhature (2 pcs)', 'Main Course', 'Giant balloon bhaturas cooked in fresh oil, slow simmered pindi chana, onion pickle and fried green chili.', 120.0, 5.0, 'https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?auto=format&fit=crop&w=400&q=80', True, True),
            (vendors[1].id, 'Paneer Stuffed Bhature Platter', 'Main Course', 'Bhaturas stuffed with spiced cottage cheese and herbs, served with rich spicy chole and raita.', 150.0, 4.9, 'https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?auto=format&fit=crop&w=400&q=80', True, True),
            (vendors[1].id, 'Thandi Malai Sweet Lassi in Kulhad', 'Beverages', 'Thick creamy Punjabi sweet curd churned with saffron strands, crushed pistachios and clotted malai layer.', 60.0, 4.9, 'https://images.unsplash.com/photo-1571091718767-18b5b1457add?auto=format&fit=crop&w=400&q=80', True, False),

            # Al-Noor Kathi Rolls
            (vendors[2].id, 'Double Egg Double Chicken Kathi Roll', 'Rolls', 'Flaky paratha layered with two beaten farm eggs, tender charcoal tandoori chicken tikka, onions and mint mayo.', 140.0, 4.9, 'https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=400&q=80', False, True),
            (vendors[2].id, 'Paneer Tikka Mayo Roll', 'Rolls', 'Charred cottage cheese cubes marinated in tandoori spices, rolled with crunchy bell peppers and secret spice blend.', 110.0, 4.8, 'https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=400&q=80', True, False),
            (vendors[2].id, 'Authentic Arabian Chicken Shawarma', 'Wraps', 'Thin pita bread stuffed with thinly sliced rotisserie spiced chicken, garlic toum sauce, fries and pickled cucumbers.', 120.0, 4.9, 'https://images.unsplash.com/photo-1529006557810-274b9b2fc783?auto=format&fit=crop&w=400&q=80', False, True),

            # Anna's 99 Dosa
            (vendors[3].id, 'Butter Mysore Masala Dosa', 'South Indian', 'Golden crispy rice crepe smeared with fiery red garlic chutney, filled with mashed spiced potato masala.', 90.0, 4.9, 'https://images.unsplash.com/photo-1668236543090-82eba5ee5976?auto=format&fit=crop&w=400&q=80', True, True),
            (vendors[3].id, 'Cheese Burst Sweet Corn Dosa', 'South Indian', 'Loaded with molten mozzarella and cheddar, sweet corn kernels, Italian herbs and hot chili flakes.', 130.0, 4.8, 'https://images.unsplash.com/photo-1668236543090-82eba5ee5976?auto=format&fit=crop&w=400&q=80', True, False),
            (vendors[3].id, 'Authentic Ghee Podi Roast', 'South Indian', 'Drizzled generously with pure desi ghee and Gunpowder (idli podi), served with 3 homemade chutneys.', 100.0, 4.9, 'https://images.unsplash.com/photo-1668236543090-82eba5ee5976?auto=format&fit=crop&w=400&q=80', True, True),

            # Tibetan Momo Corner
            (vendors[4].id, 'Steamed Chicken Darjeeling Momos (8 pcs)', 'Momos', 'Paper thin translucent dumplings stuffed with minced juicy spiced chicken and spring onions.', 100.0, 4.8, 'https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?auto=format&fit=crop&w=400&q=80', False, True),
            (vendors[4].id, 'Crispy Kurkure Veg Paneer Momos', 'Momos', 'Crunchy cornflake coated fried momos with cheesy paneer stuffing, served with hot garlic dipping sauce.', 90.0, 4.9, 'https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?auto=format&fit=crop&w=400&q=80', True, True),
            (vendors[4].id, 'Tibetan Vegetable Thukpa Noodle Soup', 'Soup', 'Comforting aromatic broth with flat noodles, bok choy, carrots, wild mushrooms and spicy chili oil.', 110.0, 4.7, 'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=400&q=80', True, False),

            # The Urban Tandoor & Biryani (Restaurant)
            (vendors[5].id, 'Dum Pukht Lucknowi Chicken Biryani Handi', 'Biryani', 'Aged long-grain basmati rice layered with chicken infused in saffron, kewra and caramelised onions cooked in sealed clay handi.', 380.0, 5.0, 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=400&q=80', False, True),
            (vendors[5].id, 'Dal Makhani Bukhara Style', 'Curry', 'Whole black lentils slow simmered for 24 hours with vine tomatoes, churned white butter and fenugreek.', 290.0, 4.9, 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?auto=format&fit=crop&w=400&q=80', True, True),
            (vendors[5].id, 'Murgh Tikka Angara', 'Starters', 'Boneless chicken chunks marinated in hung curd, deggi mirch and roasted gram flour char-grilled over coal.', 340.0, 4.8, 'https://images.unsplash.com/photo-1599488615731-7e5c2823ff28?auto=format&fit=crop&w=400&q=80', False, False),

            # Crust & Flame Pizzeria (Cafe/Resto)
            (vendors[6].id, 'Margherita Burrata Truffle Pizza', 'Pizza', 'San Marzano tomato base, artisanal fresh burrata ball, fresh basil, extra virgin olive oil and truffle drizzle.', 450.0, 4.9, 'https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=400&q=80', True, True),
            (vendors[6].id, 'Smoked Pepperoni Blaze Sourdough Pizza', 'Pizza', 'Slow fermented sourdough crust topped with spicy pepperoni slices, mozzarella and hot honey drizzle.', 490.0, 4.8, 'https://images.unsplash.com/photo-1534308983496-4fabb1a015ee?auto=format&fit=crop&w=400&q=80', False, True),
            (vendors[6].id, 'Creamy Wild Mushroom Penne', 'Pasta', 'Al dente penne tossed with porcini and button mushrooms in rich roasted garlic parmesan cream sauce.', 380.0, 4.7, 'https://images.unsplash.com/photo-1621996346565-e3d5d6281745?auto=format&fit=crop&w=400&q=80', True, False)
        ]

        for v_id, name, cat, desc, price, rating, img, veg, best in menu_data:
            item = MenuItem(
                vendor_id=v_id,
                name=name,
                category=cat,
                description=desc,
                price=price,
                rating=rating,
                image_url=img,
                is_veg=veg,
                is_bestseller=best,
                is_available=True
            )
            db.session.add(item)

        # Seed Sample Orders with Digital Tokens
        sample_order = Order(
            order_number='SB-2026-1042',
            token_number='TK-19',
            vendor_id=vendors[0].id,
            user_id=2,
            customer_name='Aarav Sharma',
            customer_phone='+91 98765 43210',
            order_type='takeaway_token',
            delivery_address='Self-Pickup at Stall Counter',
            payment_method='UPI',
            payment_status='Paid',
            status='Ready for Pickup',
            subtotal=100.0,
            discount=15.0,
            tax=0.0,
            total_amount=85.0,
            coupon_code='STREETLOVE'
        )
        db.session.add(sample_order)
        db.session.flush()

        db.session.add(OrderItem(order_id=sample_order.id, item_name='Signature Suji Golgappe (6 Pcs)', quantity=1, price=40.0))
        db.session.add(OrderItem(order_id=sample_order.id, item_name='Dahi Papdi Chaat Royale', quantity=1, price=60.0))

    db.session.commit()

# ============================================================================
# API Endpoints
# ============================================================================

@app.route('/')
def index():
    return render_template('index.html')

# 1. Vendors API
@app.route('/api/vendors', methods=['GET'])
def get_vendors():
    v_type = request.args.get('type', 'all') # 'all', 'street_vendor', 'restaurant', 'food_truck', 'cafe'
    category = request.args.get('category', 'all')
    search = request.args.get('search', '').lower().strip()
    city = request.args.get('city', 'all')

    query = Vendor.query

    if v_type != 'all':
        query = query.filter_by(vendor_type=v_type)

    if category != 'all':
        query = query.filter(Vendor.category.ilike(f'%{category}%'))

    if city != 'all':
        query = query.filter_by(city=city)

    vendors = query.all()

    if search:
        vendors = [
            v for v in vendors
            if search in v.name.lower() or
               search in (v.tagline or '').lower() or
               search in v.landmark.lower() or
               search in v.category.lower() or
               any(search in item.name.lower() for item in v.items)
        ]

    return jsonify([v.to_dict() for v in vendors])

@app.route('/api/vendors/<int:vendor_id>', methods=['GET'])
def get_vendor_detail(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    v_data = vendor.to_dict()
    v_data['menu'] = [item.to_dict() for item in vendor.items]
    return jsonify(v_data)

# Register New Vendor (Street Vendor or Restaurant)
@app.route('/api/vendors', methods=['POST'])
def register_vendor():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Stall/Restaurant Name is required'}), 400

    vendor = Vendor(
        name=name,
        vendor_type=data.get('vendor_type', 'street_vendor'),
        tagline=data.get('tagline', 'Fresh and authentic local food served with passion.'),
        category=data.get('category', 'Street Food'),
        landmark=data.get('landmark', 'Main Street Market'),
        city=data.get('city', 'Delhi NCR'),
        phone=data.get('phone', '+91 99999 99999'),
        rating=5.0,
        reviews_count=1,
        image_url=data.get('image_url') or 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=80',
        is_open=True,
        rush_level='low',
        current_token_serving=1,
        has_hygiene_badge=bool(data.get('has_hygiene_badge', True)),
        upi_id=data.get('upi_id', 'vendor@upi'),
        zero_commission_enabled=(data.get('vendor_type') in ['street_vendor', 'food_truck']),
        min_price=float(data.get('min_price', 40.0)),
        opening_hours=data.get('opening_hours', '11:00 AM - 10:00 PM')
    )
    db.session.add(vendor)
    db.session.flush()

    # Add default welcome menu item if provided
    initial_dish = data.get('initial_dish')
    if initial_dish:
        db.session.add(MenuItem(
            vendor_id=vendor.id,
            name=initial_dish,
            category='Specialty',
            description='House special prepared fresh on order.',
            price=float(data.get('initial_price', 50.0)),
            rating=5.0,
            image_url=vendor.image_url,
            is_veg=True,
            is_bestseller=True
        ))

    db.session.commit()
    return jsonify({'message': 'Vendor registered successfully!', 'vendor': vendor.to_dict()})

# Update Vendor Live Status, Rush Meter & Token Counter
@app.route('/api/vendors/<int:vendor_id>/status', methods=['PUT'])
def update_vendor_status(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    data = request.json

    if 'is_open' in data:
        vendor.is_open = bool(data['is_open'])
    if 'rush_level' in data:
        vendor.rush_level = data['rush_level'] # 'low', 'medium', 'high'
    if 'next_token' in data:
        vendor.current_token_serving += 1
    elif 'current_token_serving' in data:
        vendor.current_token_serving = int(data['current_token_serving'])

    db.session.commit()
    return jsonify({'message': 'Vendor status updated', 'vendor': vendor.to_dict()})

# 2. Menu Items API
@app.route('/api/menu', methods=['GET'])
def get_all_menu():
    vendor_id = request.args.get('vendor_id')
    category = request.args.get('category')
    search = request.args.get('search', '').lower()

    query = MenuItem.query.filter_by(is_available=True)
    if vendor_id:
        query = query.filter_by(vendor_id=vendor_id)
    if category and category != 'all':
        query = query.filter_by(category=category)

    items = query.all()
    if search:
        items = [i for i in items if search in i.name.lower() or search in (i.description or '').lower()]

    return jsonify([i.to_dict() for i in items])

@app.route('/api/menu', methods=['POST'])
def add_menu_item():
    data = request.json
    vendor_id = data.get('vendor_id')
    if not vendor_id:
        return jsonify({'error': 'Vendor ID is required'}), 400

    item = MenuItem(
        vendor_id=vendor_id,
        name=data.get('name'),
        category=data.get('category', 'Specials'),
        description=data.get('description', ''),
        price=float(data.get('price', 50.0)),
        rating=5.0,
        image_url=data.get('image_url') or 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=400&q=80',
        is_veg=bool(data.get('is_veg', True)),
        is_bestseller=bool(data.get('is_bestseller', False)),
        is_available=True
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({'message': 'Menu item added successfully', 'item': item.to_dict()})

@app.route('/api/menu/<int:item_id>', methods=['PUT', 'DELETE'])
def manage_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)

    if request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'})

    data = request.json
    if 'is_available' in data:
        item.is_available = bool(data['is_available'])
    if 'price' in data:
        item.price = float(data['price'])
    if 'name' in data:
        item.name = data['name']

    db.session.commit()
    return jsonify({'message': 'Item updated successfully', 'item': item.to_dict()})

# 3. Orders & Digital Token API
@app.route('/api/orders', methods=['POST', 'GET'])
def handle_orders():
    if request.method == 'GET':
        vendor_id = request.args.get('vendor_id')
        user_id = session.get('user_id')

        if vendor_id:
            orders = Order.query.filter_by(vendor_id=vendor_id).order_by(Order.created_at.desc()).all()
        elif user_id:
            orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
        else:
            orders = Order.query.order_by(Order.created_at.desc()).limit(20).all()

        return jsonify([order.to_dict() for order in orders])

    if request.method == 'POST':
        data = request.json
        items = data.get('items', [])
        if not items:
            return jsonify({'error': 'Cart is empty'}), 400

        vendor_id = data.get('vendor_id', 1)
        vendor = Vendor.query.get(vendor_id)

        subtotal = sum(float(item['price']) * int(item['quantity']) for item in items)
        discount = float(data.get('discount', 0))
        # 0% tax for street vendors! 5% for fine dine
        tax = 0.0 if (vendor and vendor.zero_commission_enabled) else round(subtotal * 0.05, 2)
        total = round(max(0.0, (subtotal - discount) + tax), 2)

        # Generate Digital Token & Order Number
        rand_token = random.randint(20, 99)
        token_num = f"TK-{rand_token}"
        order_num = f"SB-{random.randint(1000, 9999)}"

        order = Order(
            order_number=order_num,
            token_number=token_num,
            vendor_id=vendor_id,
            user_id=session.get('user_id'),
            customer_name=data.get('name', 'Food Lover'),
            customer_phone=data.get('phone', '+91 98765 00000'),
            order_type=data.get('order_type', 'takeaway_token'),
            delivery_address=data.get('address') or 'Pickup at Stall Counter',
            payment_method=data.get('payment_method', 'UPI'),
            payment_status='Paid' if data.get('payment_method') == 'UPI' else 'Cash at Counter',
            status='Order Placed',
            subtotal=subtotal,
            discount=discount,
            tax=tax,
            total_amount=total,
            coupon_code=data.get('coupon_code')
        )
        db.session.add(order)
        db.session.flush()

        for it in items:
            db.session.add(OrderItem(
                order_id=order.id,
                item_name=it['name'],
                quantity=it['quantity'],
                price=float(it['price'])
            ))

        db.session.commit()
        return jsonify({
            'message': 'Order placed successfully! Your live token has been generated.',
            'order': order.to_dict(),
            'token_number': token_num
        })

@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.json.get('status')
    if new_status:
        order.status = new_status
        db.session.commit()
    return jsonify({'message': 'Order status updated', 'order': order.to_dict()})

# 4. Live Token Status Query API
@app.route('/api/tokens/<token_num>', methods=['GET'])
def get_token_status(token_num):
    order = Order.query.filter_by(token_number=token_num).order_by(Order.created_at.desc()).first()
    if not order:
        return jsonify({'error': 'Token not found'}), 404

    vendor = Vendor.query.get(order.vendor_id)
    return jsonify({
        'token_number': order.token_number,
        'order_number': order.order_number,
        'vendor_name': vendor.name if vendor else 'Food Stall',
        'status': order.status,
        'now_serving': vendor.current_token_serving if vendor else 10,
        'customer_name': order.customer_name,
        'items': [item.to_dict() for item in order.items],
        'total_amount': order.total_amount
    })

# 5. Table Reservations (For Restaurants)
@app.route('/api/reservations', methods=['POST', 'GET'])
def handle_reservations():
    if request.method == 'GET':
        res_list = Reservation.query.order_by(Reservation.created_at.desc()).all()
        return jsonify([r.to_dict() for r in res_list])

    data = request.json
    booking_ref = f"#SB-RES-{random.randint(1000, 9999)}"
    res = Reservation(
        booking_ref=booking_ref,
        vendor_id=data.get('vendor_id'),
        user_id=session.get('user_id'),
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone'),
        res_date=data.get('date'),
        res_time=data.get('time'),
        guests=int(data.get('guests', 2)),
        seating_area=data.get('seating_area', 'Main Dining'),
        special_request=data.get('special_request')
    )
    db.session.add(res)
    db.session.commit()
    return jsonify({'message': 'Reservation confirmed successfully!', 'reservation': res.to_dict()})

# 6. Street Vendor Resource Center & Government Schemes
@app.route('/api/schemes', methods=['GET'])
def get_vendor_schemes():
    schemes = [
        {
            'title': 'PM SVANidhi Micro-Credit Scheme',
            'badge': 'Government of India Support',
            'summary': 'Collateral-free working capital micro-loans designed specifically for urban & rural street food vendors.',
            'loan_amount': '₹10,000 to ₹50,000',
            'interest_subsidy': '7% interest subsidy per year credited directly to your bank account',
            'cashback': 'Up to ₹1,200 annual cashback on digital transactions (UPI / QR code)',
            'eligibility': 'Street vendors with Certificate of Vending (CoV) or Identity Card issued by ULB/Municipality.',
            'portal_url': 'https://pmsvanidhi.mohua.gov.in'
        },
        {
            'title': 'FSSAI Clean Street Food Hub Certification',
            'badge': 'Hygiene & Customer Trust',
            'summary': 'Get your street cart certified with FSSAI Street Food Vendor registration (₹100/year fee). Boost customer footfall by 3x.',
            'checklist': [
                'Potable drinking water for cooking and washing',
                'Clean stainless steel / covered food preparation counter',
                'Hand hygiene: food safety gloves & aprons',
                'Proper waste segregation bin near cart',
                'Display of FSSAI QR badge at stall'
            ],
            'portal_url': 'https://foscos.fssai.gov.in'
        },
        {
            'title': 'Digital India 0% MDR UPI QR Integration',
            'badge': 'Instant Direct Settlement',
            'summary': 'Receive 100% money directly into your savings account with zero commission, instant soundbox notifications, and no daily deduction.',
            'features': ['100% Zero platform fees for carts', 'Auto settlement at 11 PM', 'No card machine rent']
        }
    ]
    return jsonify(schemes)

# 7. Mandi Wholesale Ingredient Benchmark Rates
@app.route('/api/mandi-rates', methods=['GET'])
def get_mandi_rates():
    rates = [
        {'item': 'Potato (Aloo - Pahadi/Jyoti)', 'mandi_rate': '₹18 - ₹22 / kg', 'trend': 'stable', 'source': 'Azadpur Wholesale Mandi'},
        {'item': 'Onion (Pyaaz - Nasik Red)', 'mandi_rate': '₹24 - ₹28 / kg', 'trend': 'down', 'source': 'Lasalgaon / APMC'},
        {'item': 'Tomatoes (Hybrid Red)', 'mandi_rate': '₹22 - ₹26 / kg', 'trend': 'stable', 'source': 'Kolar / Regional APMC'},
        {'item': 'Refined Cooking Oil (Soybean/Mustard)', 'mandi_rate': '₹115 - ₹125 / Ltr', 'trend': 'up', 'source': 'Bulk 15L Tin Index'},
        {'item': 'Fresh Paneer (Malai Bulk)', 'mandi_rate': '₹260 - ₹280 / kg', 'trend': 'stable', 'source': 'Local Dairy Cooperative'},
        {'item': 'Maida / Atta (Chakki Fresh)', 'mandi_rate': '₹32 - ₹36 / kg', 'trend': 'stable', 'source': 'Flour Mill Direct'}
    ]
    return jsonify(rates)

# 8. Coupon Validation API
@app.route('/api/coupons/validate', methods=['POST'])
def validate_coupon():
    code = request.json.get('code', '').upper().strip()
    coupon = Coupon.query.filter_by(code=code).first()
    if not coupon:
        return jsonify({'valid': False, 'message': 'Invalid coupon code'}), 404
    return jsonify({'valid': True, 'coupon': coupon.to_dict()})

# 9. Auth API
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email is already registered'}), 400

    user = User(
        name=data.get('name'),
        email=email,
        password_hash=generate_password_hash(data.get('password')),
        phone=data.get('phone'),
        address=data.get('address'),
        role=data.get('role', 'customer')
    )
    db.session.add(user)
    db.session.commit()

    session['user_id'] = user.id
    session['role'] = user.role
    session['name'] = user.name

    return jsonify({'message': 'Registration successful', 'user': user.to_dict()})

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid email or password'}), 401

    session['user_id'] = user.id
    session['role'] = user.role
    session['name'] = user.name

    return jsonify({'message': 'Login successful', 'user': user.to_dict()})

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/api/auth/user', methods=['GET'])
def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'user': None})
    user = User.query.get(user_id)
    return jsonify({'user': user.to_dict() if user else None})

# Initialize Database & Seed
with app.app_context():
    seed_database()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

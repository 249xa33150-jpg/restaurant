# 🍲 StreetBites & Dine
### Empowering Street Food Vendors & Premier Restaurants

**StreetBites & Dine** is a modern full-stack web platform built specifically to support and uplift **street food vendors (thelas, food carts, kiosks, food trucks)** alongside **dine-in restaurants and cafes**.

---

## 🌟 Why StreetBites & Dine is Revolutionary

Traditional food aggregators charge **25% to 35% commission**, which is devastating for local street carts selling ₹30 - ₹100 snacks. StreetBites & Dine solves this with a **zero-commission model** and tailor-made features for street food vendors:

### 1. 🛒 Street Vendor Empowerment
- **0% Platform Commission**: Street food vendors keep 100% of their earnings.
- **Smart Digital Token Queuing (e.g. #TK-18)**: Customers receive real-time digital tokens on their phone. No crowded chaos, pushing, or shouting around the stall!
- **Direct UPI QR Integration**: Customers pay straight to the vendor's UPI ID (Google Pay, PhonePe, Paytm, BHIM) with zero middleman deductions. Cash at stall is also supported.
- **Live Stall Status & Rush Meter**: Vendors can toggle `🟢 OPEN / 🔴 SOLD OUT` in 1 tap, and display live wait times (`Low <5m`, `Moderate 10m`, `High Rush 20m`).
- **Landmark-Based Geo Location**: Street stalls can specify easy landmarks (*"Opposite Metro Pillar 142, Karol Bagh"*).
- **Printable Cart QR Code**: Vendors can generate and print a QR flyer for their stall counter so customers can scan, order, and get a token.

### 2. 🏛️ Vendor Support Hub & Government Schemes
- **PM SVANidhi Micro-Credit Loan Guide**: Direct guidance on ₹10,000 to ₹50,000 collateral-free working capital loans with 7% interest subsidy & ₹1,200 digital cashback.
- **FSSAI Clean Street Food Hub Guide**: 10-point street food hygiene checklist to earn the verified hygiene badge.
- **Daily Mandi Wholesale Price Index**: Live wholesale benchmark rates (potatoes, onions, tomatoes, cooking oil, paneer, flour) to help vendors budget and negotiate fair bulk prices.

### 3. 🍽️ Premier Restaurant & Cafe Features
- **Table Reservation System**: Online booking with guest count, date, time slots, and seating preference (Main Dining, Rooftop, Booth).
- **Comprehensive Gourmet Menus**: Multi-course offerings with veg/non-veg tags, chef specials, and ratings.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+
- Installed packages: `Flask`, `Flask-SQLAlchemy`, `Werkzeug`

### 2. Run the Web Server
In PowerShell or Terminal:
```powershell
python app.py
```
The server will start on: **`http://127.0.0.1:5000`**

### 3. Open in Browser
Visit `http://127.0.0.1:5000` to access the full application with the live SQLite database, or open `index.html` directly for offline preview with mock data fallback.

---

## 📂 Project Architecture

```
restaurant/
├── app.py                     # Flask application with REST API & SQLite models
├── streetbites.db             # Auto-generated SQLite database
├── test_api.py                # Automated backend test suite
├── requirements.txt           # Python dependencies
├── index.html                 # Root index (static & local compatible)
├── styles.css                 # Root stylesheet
├── app.js                     # Root client-side application script
├── templates/
│   └── index.html             # Flask Jinja2 frontend template
├── static/
│   ├── css/
│   │   └── style.css          # Master responsive styles & dark/light theme
│   └── js/
│       └── main.js            # Client-side dynamic interaction & API logic
└── assets/                    # Culinary imagery & dish photos
```

---

## 🧪 Testing the API
Run the automated verification suite:
```powershell
python test_api.py
```
All endpoints (vendors, menu, orders, tokens, schemes, reservations, and mandi rates) are fully verified and passing.

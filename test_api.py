import json
from app import app

client = app.test_client()

# 1. Test Home
r = client.get('/')
assert r.status_code == 200, f'Home failed: {r.status_code}'

# 2. Test Vendors
r = client.get('/api/vendors')
assert r.status_code == 200
vendors = r.get_json()
assert len(vendors) >= 7, f'Expected 7+ vendors, got {len(vendors)}'
print(f'[PASS] /api/vendors returned {len(vendors)} vendors')

# 3. Test Vendor detail & menu
v1_id = vendors[0]['id']
r = client.get(f'/api/vendors/{v1_id}')
assert r.status_code == 200
v1 = r.get_json()
menu_count = len(v1.get('menu', []))
assert menu_count > 0
print(f'[PASS] /api/vendors/{v1_id} returned {menu_count} menu items')

# 4. Test Place Order & Token Generation
order_payload = {
    'vendor_id': v1_id,
    'name': 'Pooja Verma',
    'phone': '+91 98765 11111',
    'order_type': 'takeaway_token',
    'payment_method': 'UPI',
    'items': [{'name': 'Signature Suji Golgappe (6 Pcs)', 'price': 40.0, 'quantity': 2}]
}
r = client.post('/api/orders', data=json.dumps(order_payload), content_type='application/json')
assert r.status_code == 200
order_res = r.get_json()
token_num = order_res['token_number']
print(f'[PASS] /api/orders placed order successfully, Generated Token: {token_num}')

# 5. Test Live Token Query
r = client.get(f'/api/tokens/{token_num}')
assert r.status_code == 200
token_res = r.get_json()
print(f'[PASS] /api/tokens/{token_num} query status: {token_res["status"]}, Vendor: {token_res["vendor_name"]}')

# 6. Test Schemes & Mandi Rates
r = client.get('/api/schemes')
assert r.status_code == 200
print(f'[PASS] /api/schemes returned {len(r.get_json())} empowerment schemes')

r = client.get('/api/mandi-rates')
assert r.status_code == 200
print(f'[PASS] /api/mandi-rates returned {len(r.get_json())} wholesale benchmark rates')

# 7. Test Vendor Status & Advance Token
r = client.put(f'/api/vendors/{v1_id}/status', data=json.dumps({'next_token': True}), content_type='application/json')
assert r.status_code == 200
curr_tok = r.get_json()['vendor']['current_token_serving']
print(f'[PASS] /api/vendors/{v1_id}/status advanced token to #{curr_tok}')

print('ALL ENDPOINT TESTS PASSED PERFECTLY!')

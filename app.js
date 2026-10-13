/**
 * StreetBites & Dine - Master JavaScript Application
 * Zero-Commission Street Food & Restaurant Ecosystem
 */

let allVendors = [];
let currentCategory = 'all';
let currentVendorType = 'all';
let currentCity = 'Delhi NCR';
let isVegOnly = false;
let isOpenOnly = false;
let searchQuery = '';
let cart = [];
let appliedCoupon = null;
let currentVendorInModal = null;

// Initialize on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
  fetchVendors();
  fetchSchemes();
  fetchMandiRates();
  loadCartFromStorage();
});

// ============================================================================
// 1. Fetch & Render Vendors
// ============================================================================

async function fetchVendors() {
  try {
    const res = await fetch('/api/vendors');
    if (!res.ok) throw new Error('API request failed');
    allVendors = await res.json();
  } catch (err) {
    console.warn('API unavailable, loading offline mock dataset:', err);
    allVendors = getFallbackVendors();
  }
  populateVendorSelects();
  applyFilters();
}

function getFallbackVendors() {
  return [
    {
      id: 1,
      name: 'Gupta Ji Chaat & Pani Puri Bhandar',
      vendor_type: 'street_vendor',
      tagline: 'Crunchy Suji & Atta Golgappe with 5 Types of Flavored Spicy Pudina Water',
      category: 'Chaat & Street Food',
      landmark: 'Corner of Block B, Near Metro Pillar 142, Karol Bagh',
      city: 'Delhi NCR',
      phone: '+91 98112 34567',
      rating: 4.9,
      reviews_count: 340,
      image_url: 'https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=800&q=80',
      is_open: true,
      rush_level: 'medium',
      current_token_serving: 18,
      has_hygiene_badge: true,
      upi_id: 'guptachaat@oksbi',
      zero_commission_enabled: true,
      min_price: 30.0,
      menu: [
        { id: 101, name: 'Signature Suji Golgappe (6 Pcs)', description: 'Crispy suji puris with 5 flavored waters.', price: 40, is_veg: true, is_bestseller: true },
        { id: 102, name: 'Dahi Papdi Chaat Royale', description: 'Crispy papdi with sweet curd and chutneys.', price: 60, is_veg: true, is_bestseller: true },
        { id: 103, name: 'Kurkuri Aloo Tikki Pav', description: 'Crisp fried potato patty in warm pav.', price: 50, is_veg: true, is_bestseller: false }
      ]
    },
    {
      id: 2,
      name: 'Sharma Sweets & Chole Bhature Express',
      vendor_type: 'street_vendor',
      tagline: 'Fluffy Golden Bhature with Pindi Chole, Amla Achar & Sweet Lassi',
      category: 'North Indian Snacks',
      landmark: 'Shop 4, Main Market, Chandni Chowk',
      city: 'Delhi NCR',
      phone: '+91 98114 55667',
      rating: 4.8,
      reviews_count: 510,
      image_url: 'https://images.unsplash.com/photo-1626777552726-4a6b54c97e46?auto=format&fit=crop&w=800&q=80',
      is_open: true,
      rush_level: 'high',
      current_token_serving: 34,
      has_hygiene_badge: true,
      upi_id: 'sharmachole@paytm',
      zero_commission_enabled: true,
      min_price: 60.0,
      menu: [
        { id: 201, name: 'Special Pindi Chole Bhature (2 pcs)', description: 'Giant fluffy bhaturas with rich spiced chana.', price: 120, is_veg: true, is_bestseller: true },
        { id: 202, name: 'Thandi Malai Sweet Lassi in Kulhad', description: 'Thick creamy Punjabi sweet lassi.', price: 60, is_veg: true, is_bestseller: false }
      ]
    },
    {
      id: 3,
      name: 'Al-Noor Kathi Rolls & Shawarma Hub',
      vendor_type: 'street_vendor',
      tagline: 'Charcoal Grilled Chicken Kathi Rolls, Paneer Tikka Rolls & Rumali Wraps',
      category: 'Rolls & Wraps',
      landmark: 'Opposite City Center Mall, Sector 18',
      city: 'Noida',
      phone: '+91 99887 11223',
      rating: 4.9,
      reviews_count: 290,
      image_url: 'https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=800&q=80',
      is_open: true,
      rush_level: 'low',
      current_token_serving: 12,
      has_hygiene_badge: true,
      upi_id: 'alnoorkathi@icici',
      zero_commission_enabled: true,
      min_price: 50.0,
      menu: [
        { id: 301, name: 'Double Egg Double Chicken Kathi Roll', description: 'Flaky paratha loaded with grilled chicken.', price: 140, is_veg: false, is_bestseller: true },
        { id: 302, name: 'Paneer Tikka Mayo Roll', description: 'Charred paneer cubes in tandoori spices.', price: 110, is_veg: true, is_bestseller: false }
      ]
    },
    {
      id: 4,
      name: "Anna's 99 Variety Dosa Cart",
      vendor_type: 'food_truck',
      tagline: 'Crispy Butter Mysore Masala, Cheese Burst & Ghee Roast Dosas on Wheels',
      category: 'South Indian',
      landmark: 'Tech Park Gate 3, Cyber Hub Road',
      city: 'Gurugram',
      phone: '+91 97766 54321',
      rating: 4.9,
      reviews_count: 420,
      image_url: 'https://images.unsplash.com/photo-1668236543090-82eba5ee5976?auto=format&fit=crop&w=800&q=80',
      is_open: true,
      rush_level: 'medium',
      current_token_serving: 26,
      has_hygiene_badge: true,
      upi_id: 'annadosa@axl',
      zero_commission_enabled: true,
      min_price: 70.0,
      menu: [
        { id: 401, name: 'Butter Mysore Masala Dosa', description: 'Crisp crepe with red chili garlic chutney.', price: 90, is_veg: true, is_bestseller: true },
        { id: 402, name: 'Cheese Burst Sweet Corn Dosa', description: 'Loaded with mozzarella and herbs.', price: 130, is_veg: true, is_bestseller: false }
      ]
    },
    {
      id: 5,
      name: 'Tibetan Momo Corner & Thukpa Bar',
      vendor_type: 'street_vendor',
      tagline: 'Steamed, Pan-Fried Kurkure Momos with Fiery Red Dalle Chili Sauce',
      category: 'Momos & Street Fast Food',
      landmark: 'Kalyan Nagar, Outer Ring Road, Near Bus Stand',
      city: 'Bangalore',
      phone: '+91 96543 21098',
      rating: 4.7,
      reviews_count: 180,
      image_url: 'https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?auto=format&fit=crop&w=800&q=80',
      is_open: true,
      rush_level: 'low',
      current_token_serving: 8,
      has_hygiene_badge: true,
      upi_id: 'tibetanmomos@ybl',
      zero_commission_enabled: true,
      min_price: 60.0,
      menu: [
        { id: 501, name: 'Steamed Chicken Darjeeling Momos (8 pcs)', description: 'Thin dumplings with spiced chicken.', price: 100, is_veg: false, is_bestseller: true },
        { id: 502, name: 'Crispy Kurkure Veg Paneer Momos', description: 'Crunchy battered momos with hot garlic dip.', price: 90, is_veg: true, is_bestseller: true }
      ]
    },
    {
      id: 6,
      name: 'The Urban Tandoor & Royal Biryani',
      vendor_type: 'restaurant',
      tagline: 'Fine Indian Dining, Dum Biryani Handis, Tandoori Platters & Luxury Ambience',
      category: 'Biryani & Mughlai',
      landmark: 'Building 24, Outer Circle, Connaught Place',
      city: 'Delhi NCR',
      phone: '+91 99112 23344',
      rating: 4.9,
      reviews_count: 780,
      image_url: 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?auto=format&fit=crop&w=800&q=80',
      is_open: true,
      rush_level: 'medium',
      current_token_serving: 45,
      has_hygiene_badge: true,
      upi_id: 'urbantandoor@hdfcbank',
      zero_commission_enabled: false,
      min_price: 220.0,
      menu: [
        { id: 601, name: 'Dum Pukht Lucknowi Chicken Biryani Handi', description: 'Saffron basmati rice with marinated chicken.', price: 380, is_veg: false, is_bestseller: true },
        { id: 602, name: 'Dal Makhani Bukhara Style', description: '24-hour slow cooked black lentils with white butter.', price: 290, is_veg: true, is_bestseller: true }
      ]
    },
    {
      id: 7,
      name: 'Crust & Flame Artisanal Pizzeria',
      vendor_type: 'cafe',
      tagline: 'Wood-fired Neapolitan Pizzas, Truffle Pastas & Handcrafted Cold Brews',
      category: 'Italian & Cafe',
      landmark: '12th Main Road, Indiranagar',
      city: 'Bangalore',
      phone: '+91 98450 12345',
      rating: 4.8,
      reviews_count: 460,
      image_url: 'https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=800&q=80',
      is_open: true,
      rush_level: 'low',
      current_token_serving: 14,
      has_hygiene_badge: true,
      upi_id: 'crustandflame@icici',
      zero_commission_enabled: false,
      min_price: 180.0,
      menu: [
        { id: 701, name: 'Margherita Burrata Truffle Pizza', description: 'Fresh burrata, basil and truffle oil.', price: 450, is_veg: true, is_bestseller: true },
        { id: 702, name: 'Creamy Wild Mushroom Penne', description: 'Parmesan garlic cream sauce.', price: 380, is_veg: true, is_bestseller: false }
      ]
    }
  ];
}

function applyFilters() {
  let filtered = [...allVendors];

  // City filter
  if (currentCity !== 'all') {
    filtered = filtered.filter(v => v.city.toLowerCase() === currentCity.toLowerCase());
  }

  // Vendor Type filter
  if (currentVendorType !== 'all') {
    filtered = filtered.filter(v => v.vendor_type === currentVendorType);
  }

  // Category filter
  if (currentCategory !== 'all') {
    filtered = filtered.filter(v => v.category.toLowerCase().includes(currentCategory.toLowerCase()));
  }

  // Open only filter
  if (isOpenOnly) {
    filtered = filtered.filter(v => v.is_open);
  }

  // Search query filter
  if (searchQuery.trim()) {
    const q = searchQuery.toLowerCase().trim();
    filtered = filtered.filter(v => 
      v.name.toLowerCase().includes(q) ||
      (v.tagline && v.tagline.toLowerCase().includes(q)) ||
      v.landmark.toLowerCase().includes(q) ||
      v.category.toLowerCase().includes(q)
    );
  }

  renderVendors(filtered);
}

function renderVendors(vendors) {
  const container = document.getElementById('vendorsContainer');
  if (!vendors || vendors.length === 0) {
    container.innerHTML = `
      <div class="col-12 text-center py-5">
        <div class="fs-1 text-muted">🍲</div>
        <h5 class="fw-bold mt-2">No Food Spots Found</h5>
        <p class="text-muted small">Try adjusting your filters or search keywords.</p>
        <button class="btn btn-outline-warning btn-sm rounded-pill fw-bold" onclick="resetFilters()">Reset All Filters</button>
      </div>
    `;
    return;
  }

  container.innerHTML = vendors.map(v => {
    // Type badge format
    let typeBadge = '';
    if (v.vendor_type === 'street_vendor') {
      typeBadge = `<span class="vendor-type-pill"><i class="bi bi-cart3 me-1"></i>Street Thela</span>`;
    } else if (v.vendor_type === 'food_truck') {
      typeBadge = `<span class="vendor-type-pill"><i class="bi bi-truck me-1"></i>Food Truck</span>`;
    } else if (v.vendor_type === 'cafe') {
      typeBadge = `<span class="vendor-type-pill"><i class="bi bi-cup-hot me-1"></i>Cafe / Bistro</span>`;
    } else {
      typeBadge = `<span class="vendor-type-pill"><i class="bi bi-shop me-1"></i>Restaurant</span>`;
    }

    // Status badge
    const statusBadge = v.is_open 
      ? `<span class="vendor-status-pill bg-success text-white"><i class="bi bi-circle-fill me-1 smaller"></i>Open Now</span>`
      : `<span class="vendor-status-pill bg-danger text-white"><i class="bi bi-x-circle me-1 smaller"></i>Sold Out</span>`;

    // Rush level format
    let rushHtml = '';
    if (v.rush_level === 'low') {
      rushHtml = `<span class="rush-indicator rush-low"><i class="bi bi-lightning-charge"></i> Low Rush (&lt;5m wait)</span>`;
    } else if (v.rush_level === 'medium') {
      rushHtml = `<span class="rush-indicator rush-medium"><i class="bi bi-hourglass-split"></i> Moderate (10-15m)</span>`;
    } else {
      rushHtml = `<span class="rush-indicator rush-high"><i class="bi bi-fire"></i> High Rush (20+m)</span>`;
    }

    return `
      <div class="col-md-6 col-lg-4">
        <div class="vendor-card shadow-sm">
          <div class="vendor-card-img-wrapper">
            <img src="${v.image_url}" alt="${v.name}" class="vendor-card-img" loading="lazy">
            ${typeBadge}
            ${statusBadge}
          </div>
          <div class="p-3 d-flex flex-column flex-grow-1">
            <div class="d-flex justify-content-between align-items-start mb-1">
              <h5 class="fw-bold mb-0 text-truncate" title="${v.name}">${v.name}</h5>
              <span class="badge bg-warning text-dark fw-bold ms-2">★ ${v.rating.toFixed(1)}</span>
            </div>

            <p class="text-muted smaller mb-2 text-truncate-2">${v.tagline || v.category}</p>

            <div class="small text-muted mb-2 d-flex align-items-center">
              <i class="bi bi-geo-alt-fill text-danger me-1 flex-shrink-0"></i>
              <span class="text-truncate" title="${v.landmark}">${v.landmark}</span>
            </div>

            <!-- Badges Row -->
            <div class="d-flex flex-wrap gap-1 align-items-center mb-3">
              ${v.zero_commission_enabled ? `<span class="zero-commission-tag"><i class="bi bi-shield-check me-1"></i>0% Cut Thela</span>` : ''}
              ${v.has_hygiene_badge ? `<span class="badge bg-success-subtle text-success smaller"><i class="bi bi-patch-check-fill me-1"></i>FSSAI Certified</span>` : ''}
              ${rushHtml}
            </div>

            <!-- Token Counter & Price -->
            <div class="d-flex justify-content-between align-items-center py-2 border-top border-bottom my-2">
              <div class="token-serving-pill">
                <i class="bi bi-ticket-perforated text-warning me-1"></i>Now Serving: <strong>#TK-${v.current_token_serving}</strong>
              </div>
              <div class="small fw-bold text-muted">
                From <span class="text-dark fs-6">₹${v.min_price}</span>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="d-flex gap-2 mt-auto pt-2">
              <button class="btn btn-warning btn-sm flex-fill fw-bold rounded-pill" onclick="openVendorModal(${v.id})">
                <i class="bi bi-book-half me-1"></i> View Menu & Order
              </button>
              ${v.vendor_type === 'restaurant' ? `
                <button class="btn btn-outline-dark btn-sm rounded-pill fw-bold" onclick="openReservationModal(${v.id}, '${v.name.replace(/'/g, "\\'")}')" title="Reserve Table">
                  <i class="bi bi-calendar2-check"></i>
                </button>
              ` : ''}
            </div>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

// ============================================================================
// 2. Filter Handlers
// ============================================================================

function filterByCity(city) {
  currentCity = city;
  applyFilters();
}

function filterVendorType(type) {
  currentVendorType = type;
  document.querySelectorAll('.vendor-type-pills .nav-link').forEach(btn => btn.classList.remove('active'));
  event.target.classList.add('active');
  applyFilters();
}

function filterCategory(cat, element) {
  currentCategory = cat;
  document.querySelectorAll('.filter-bar button').forEach(btn => btn.classList.remove('active-filter'));
  if (element) element.classList.add('active-filter');
  applyFilters();
}

function toggleVegOnly(checked) {
  isVegOnly = checked;
  applyFilters();
}

function toggleOpenOnly(checked) {
  isOpenOnly = checked;
  applyFilters();
}

function handleSearch(val) {
  searchQuery = val;
  applyFilters();
}

function triggerSearch() {
  const val = document.getElementById('searchInput').value;
  searchQuery = val;
  applyFilters();
  const target = document.getElementById('explore');
  if (target) target.scrollIntoView({ behavior: 'smooth' });
}

function resetFilters() {
  currentCategory = 'all';
  currentVendorType = 'all';
  currentCity = 'all';
  searchQuery = '';
  document.getElementById('searchInput').value = '';
  document.getElementById('citySelect').value = 'all';
  document.querySelectorAll('.filter-bar button').forEach(btn => btn.classList.remove('active-filter'));
  const firstBtn = document.querySelector('.filter-bar button');
  if (firstBtn) firstBtn.classList.add('active-filter');
  applyFilters();
}

// ============================================================================
// 3. Vendor Menu Modal & Ordering
// ============================================================================

async function openVendorModal(vendorId) {
  try {
    const res = await fetch(`/api/vendors/${vendorId}`);
    const v = await res.json();
    currentVendorInModal = v;

    const header = document.getElementById('vendorModalHeader');
    header.innerHTML = `
      <div class="d-flex align-items-center gap-3">
        <img src="${v.image_url}" class="rounded-3" style="width: 70px; height: 70px; object-fit: cover;" alt="${v.name}">
        <div>
          <h5 class="fw-bold mb-1">${v.name}</h5>
          <div class="small text-muted mb-1"><i class="bi bi-geo-alt-fill text-danger me-1"></i>${v.landmark}</div>
          <div class="d-flex gap-2 align-items-center">
            <span class="badge bg-warning text-dark fw-bold">★ ${v.rating}</span>
            <span class="badge bg-dark">Now Serving #TK-${v.current_token_serving}</span>
            <span class="small text-muted">UPI: <code>${v.upi_id}</code></span>
          </div>
        </div>
      </div>
    `;

    const body = document.getElementById('vendorModalBody');
    if (!v.menu || v.menu.length === 0) {
      body.innerHTML = `<p class="text-center text-muted py-4">No menu items found for this stall.</p>`;
    } else {
      body.innerHTML = v.menu.map(item => `
        <div class="d-flex justify-content-between align-items-center menu-item-row">
          <div class="pe-3 flex-grow-1">
            <div class="d-flex align-items-center gap-2 mb-1">
              ${item.is_veg ? '<span class="veg-icon" title="Vegetarian"></span>' : '<span class="non-veg-icon" title="Non-Vegetarian"></span>'}
              <strong class="text-dark">${item.name}</strong>
              ${item.is_bestseller ? '<span class="badge bg-danger-subtle text-danger smaller">Bestseller</span>' : ''}
            </div>
            <p class="text-muted smaller mb-1">${item.description || ''}</p>
            <div class="fw-bold fs-6 text-dark">₹${item.price}</div>
          </div>
          <div class="flex-shrink-0 text-center">
            <button class="btn btn-outline-warning btn-sm fw-bold px-3 rounded-pill" onclick="addToCart(${item.id}, '${item.name.replace(/'/g, "\\'")}', ${item.price}, ${v.id}, ${item.is_veg})">
              + Add
            </button>
          </div>
        </div>
      `).join('');
    }

    updateCartBadge();
    const modal = new bootstrap.Modal(document.getElementById('vendorMenuModal'));
    modal.show();
  } catch (err) {
    console.error('Failed to open vendor modal:', err);
  }
}

// ============================================================================
// 4. Cart & Checkout Operations
// ============================================================================

function addToCart(itemId, name, price, vendorId, isVeg) {
  // If cart already has items from another vendor, confirm reset
  if (cart.length > 0 && cart[0].vendorId !== vendorId) {
    if (!confirm('You have items from another stall in your cart. Start a new cart for this vendor?')) {
      return;
    }
    cart = [];
  }

  const existing = cart.find(i => i.id === itemId);
  if (existing) {
    existing.quantity += 1;
  } else {
    cart.push({ id: itemId, name, price: parseFloat(price), vendorId, isVeg, quantity: 1 });
  }

  saveCart();
  renderCart();
  showToast(`Added ${name} to cart!`);
}

function updateCartQuantity(index, delta) {
  if (cart[index]) {
    cart[index].quantity += delta;
    if (cart[index].quantity <= 0) {
      cart.splice(index, 1);
    }
  }
  saveCart();
  renderCart();
}

function saveCart() {
  localStorage.setItem('sb_cart', JSON.stringify(cart));
  updateCartBadge();
}

function loadCartFromStorage() {
  const saved = localStorage.getItem('sb_cart');
  if (saved) {
    try {
      cart = JSON.parse(saved);
    } catch(e) {
      cart = [];
    }
  }
  updateCartBadge();
}

function updateCartBadge() {
  const count = cart.reduce((acc, it) => acc + it.quantity, 0);
  const badge = document.getElementById('cartCountBadge');
  if (badge) badge.innerText = count;
  document.querySelectorAll('.modal-cart-count').forEach(el => el.innerText = count);
}

function renderCart() {
  const container = document.getElementById('cartItemsList');
  updateCartBadge();

  if (cart.length === 0) {
    container.innerHTML = `
      <div class="text-center py-4 text-muted">
        <i class="bi bi-cart-x fs-2"></i>
        <p class="mt-2 mb-0">Your cart is empty.</p>
        <small>Select delicious snacks or dishes to order!</small>
      </div>
    `;
    document.getElementById('cartSubtotal').innerText = '₹0';
    document.getElementById('cartDiscount').innerText = '-₹0';
    document.getElementById('cartTotal').innerText = '₹0';
    return;
  }

  container.innerHTML = cart.map((item, idx) => `
    <div class="d-flex justify-content-between align-items-center py-2 border-bottom">
      <div>
        <div class="fw-bold small">${item.name}</div>
        <div class="text-muted smaller">₹${item.price} each</div>
      </div>
      <div class="d-flex align-items-center gap-2">
        <button class="btn btn-sm btn-outline-secondary px-2 py-0" onclick="updateCartQuantity(${idx}, -1)">-</button>
        <span class="fw-bold small">${item.quantity}</span>
        <button class="btn btn-sm btn-outline-secondary px-2 py-0" onclick="updateCartQuantity(${idx}, 1)">+</button>
        <span class="fw-bold small ms-2">₹${item.price * item.quantity}</span>
      </div>
    </div>
  `).join('');

  const subtotal = cart.reduce((acc, it) => acc + (it.price * it.quantity), 0);
  let discount = 0;
  if (appliedCoupon) {
    if (appliedCoupon.discount_percent > 0) {
      discount = (subtotal * appliedCoupon.discount_percent) / 100;
    } else if (appliedCoupon.flat_discount > 0) {
      discount = appliedCoupon.flat_discount;
    }
  }

  const total = Math.max(0, subtotal - discount);
  document.getElementById('cartSubtotal').innerText = `₹${subtotal.toFixed(2)}`;
  document.getElementById('cartDiscount').innerText = `-₹${discount.toFixed(2)}`;
  document.getElementById('cartTotal').innerText = `₹${total.toFixed(2)}`;
}

async function applyCoupon() {
  const input = document.getElementById('couponInput');
  const code = input.value.trim().toUpperCase();
  const msg = document.getElementById('couponMessage');

  if (!code) return;

  try {
    const res = await fetch('/api/coupons/validate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code })
    });
    const data = await res.json();
    if (data.valid) {
      appliedCoupon = data.coupon;
      msg.className = 'small mb-3 text-success';
      msg.innerHTML = `<i class="bi bi-check-circle me-1"></i> Coupon <strong>${code}</strong> applied successfully!`;
      renderCart();
    } else {
      appliedCoupon = null;
      msg.className = 'small mb-3 text-danger';
      msg.innerHTML = `<i class="bi bi-x-circle me-1"></i> Invalid coupon code.`;
      renderCart();
    }
  } catch (err) {
    console.error('Coupon error:', err);
  }
}

// Place Order & Generate Live Digital Token
async function placeOrderAndGenerateToken() {
  if (cart.length === 0) {
    alert('Please add items to cart before placing an order.');
    return;
  }

  const name = document.getElementById('customerName').value.trim() || 'Food Lover';
  const phone = document.getElementById('customerPhone').value.trim() || '+91 98765 00000';
  const orderType = document.getElementById('orderType').value;
  const payMethod = document.querySelector('input[name="paymentMethod"]:checked').value;
  const couponCode = appliedCoupon ? appliedCoupon.code : null;

  const payload = {
    vendor_id: cart[0].vendorId,
    name,
    phone,
    order_type: orderType,
    payment_method: payMethod,
    coupon_code: couponCode,
    discount: appliedCoupon ? (appliedCoupon.discount_percent ? 15 : 30) : 0,
    items: cart.map(it => ({ name: it.name, price: it.price, quantity: it.quantity }))
  };

  try {
    const res = await fetch('/api/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await res.json();

    if (res.ok) {
      // Clear cart
      cart = [];
      appliedCoupon = null;
      saveCart();
      renderCart();

      // Close cart modal
      const cartModalEl = document.getElementById('cartModal');
      const cartModal = bootstrap.Modal.getInstance(cartModalEl);
      if (cartModal) cartModal.hide();

      // Show token tracking modal with new token!
      document.getElementById('tokenQueryInput').value = result.token_number;
      queryTokenStatus(result.token_number);

      const trackModal = new bootstrap.Modal(document.getElementById('tokenTrackModal'));
      trackModal.show();

      showToast(`🎉 Order Placed! Your Token: ${result.token_number}`);
    } else {
      alert(result.error || 'Failed to place order.');
    }
  } catch (err) {
    console.error('Order placement error:', err);
    alert('Network error while placing order.');
  }
}

// ============================================================================
// 5. Live Token Tracking
// ============================================================================

async function queryTokenStatus(tokenParam) {
  const token = tokenParam || document.getElementById('tokenQueryInput').value.trim();
  if (!token) return;

  try {
    const res = await fetch(`/api/tokens/${token}`);
    const data = await res.json();

    if (res.ok) {
      document.getElementById('tokenDisplayNumber').innerText = data.token_number;
      document.getElementById('tokenStallName').innerText = data.vendor_name;
      document.getElementById('tokenStatusBadge').innerText = data.status;
      document.getElementById('stallServingToken').innerText = `#TK-${data.now_serving}`;

      // Update tracker step active classes
      const s1 = document.getElementById('step1');
      const s2 = document.getElementById('step2');
      const s3 = document.getElementById('step3');
      const s4 = document.getElementById('step4');

      [s1, s2, s3, s4].forEach(s => {
        s.className = 'tracker-step';
      });

      if (data.status === 'Order Placed') {
        s1.className = 'tracker-step active';
      } else if (data.status === 'Preparing') {
        s1.className = 'tracker-step completed';
        s2.className = 'tracker-step active';
      } else if (data.status === 'Ready for Pickup') {
        s1.className = 'tracker-step completed';
        s2.className = 'tracker-step completed';
        s3.className = 'tracker-step active';
      } else if (data.status === 'Completed') {
        s1.className = 'tracker-step completed';
        s2.className = 'tracker-step completed';
        s3.className = 'tracker-step completed';
        s4.className = 'tracker-step completed';
      }
    } else {
      document.getElementById('tokenDisplayNumber').innerText = 'Not Found';
      document.getElementById('tokenStallName').innerText = 'Please check token number';
      document.getElementById('tokenStatusBadge').innerText = 'Invalid';
    }
  } catch (err) {
    console.error('Token fetch error:', err);
  }
}

// ============================================================================
// 6. Vendor Portal & Self-Service Management
// ============================================================================

function populateVendorSelects() {
  const sel = document.getElementById('manageVendorSelect');
  if (!sel) return;

  sel.innerHTML = allVendors.map(v => `
    <option value="${v.id}">${v.name} (${v.vendor_type === 'street_vendor' ? 'Street Stall' : 'Restaurant'})</option>
  `).join('');

  if (allVendors.length > 0) {
    loadVendorDashboard(allVendors[0].id);
  }
}

function loadVendorDashboard(vendorId) {
  const v = allVendors.find(x => x.id === parseInt(vendorId));
  if (!v) return;

  document.getElementById('dashServingToken').innerText = `#TK-${v.current_token_serving}`;
  document.getElementById('qrStallTitle').innerText = v.name;
}

async function updateVendorLiveStatus(isOpen) {
  const sel = document.getElementById('manageVendorSelect');
  const vendorId = sel.value;

  try {
    const res = await fetch(`/api/vendors/${vendorId}/status`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ is_open: isOpen })
    });
    if (res.ok) {
      showToast(isOpen ? 'Stall marked OPEN 🟢' : 'Stall marked CLOSED 🔴');
      fetchVendors();
    }
  } catch (err) {
    console.error('Status update error:', err);
  }
}

async function advanceNextToken() {
  const sel = document.getElementById('manageVendorSelect');
  const vendorId = sel.value;

  try {
    const res = await fetch(`/api/vendors/${vendorId}/status`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ next_token: true })
    });
    const data = await res.json();
    if (res.ok) {
      document.getElementById('dashServingToken').innerText = `#TK-${data.vendor.current_token_serving}`;
      showToast(`Now Calling Token #TK-${data.vendor.current_token_serving}! 📢`);
      fetchVendors();
    }
  } catch (err) {
    console.error('Next token error:', err);
  }
}

async function updateRushLevel(level) {
  const sel = document.getElementById('manageVendorSelect');
  const vendorId = sel.value;

  try {
    const res = await fetch(`/api/vendors/${vendorId}/status`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ rush_level: level })
    });
    if (res.ok) {
      showToast(`Rush level set to ${level.toUpperCase()} ⚡`);
      fetchVendors();
    }
  } catch (err) {
    console.error('Rush level error:', err);
  }
}

async function addNewMenuItemToStall() {
  const sel = document.getElementById('manageVendorSelect');
  const vendorId = sel.value;
  const name = document.getElementById('newDishName').value.trim();
  const price = document.getElementById('newDishPrice').value.trim();

  if (!name || !price) {
    alert('Please enter dish name and price.');
    return;
  }

  try {
    const res = await fetch('/api/menu', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        vendor_id: vendorId,
        name,
        price: parseFloat(price),
        category: 'Specialty',
        is_veg: true
      })
    });
    if (res.ok) {
      document.getElementById('newDishName').value = '';
      document.getElementById('newDishPrice').value = '';
      showToast(`Added ${name} to your stall menu! 🍳`);
      fetchVendors();
    }
  } catch (err) {
    console.error('Add menu item error:', err);
  }
}

async function handleVendorRegistration(e) {
  e.preventDefault();
  const name = document.getElementById('regName').value.trim();
  const vendor_type = document.getElementById('regType').value;
  const landmark = document.getElementById('regLandmark').value.trim();
  const category = document.getElementById('regCategory').value.trim();
  const city = document.getElementById('regCity').value;
  const phone = document.getElementById('regPhone').value.trim();
  const upi_id = document.getElementById('regUpi').value.trim();
  const initial_dish = document.getElementById('regInitialDish').value.trim();
  const initial_price = document.getElementById('regInitialPrice').value.trim();

  const payload = {
    name,
    vendor_type,
    landmark,
    category,
    city,
    phone,
    upi_id,
    initial_dish,
    initial_price: initial_price ? parseFloat(initial_price) : 50.0
  };

  try {
    const res = await fetch('/api/vendors', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await res.json();
    if (res.ok) {
      alert(`🎉 Stall "${name}" registered successfully with 0% platform fee!`);
      document.getElementById('vendorRegForm').reset();
      fetchVendors();

      // Switch to manage stall tab
      const tabBtn = document.querySelector('button[data-bs-target="#tabManageStall"]');
      if (tabBtn) tabBtn.click();
    } else {
      alert(result.error || 'Failed to register vendor.');
    }
  } catch (err) {
    console.error('Registration error:', err);
  }
}

// ============================================================================
// 7. Restaurant Table Reservation
// ============================================================================

function openReservationModal(vendorId, vendorName) {
  document.getElementById('resVendorId').value = vendorId;
  document.getElementById('resVendorName').value = vendorName;
  const today = new Date().toISOString().split('T')[0];
  document.getElementById('resDate').value = today;

  const modal = new bootstrap.Modal(document.getElementById('reservationModal'));
  modal.show();
}

async function submitReservation() {
  const vendor_id = document.getElementById('resVendorId').value;
  const name = document.getElementById('resName').value.trim();
  const phone = document.getElementById('resPhone').value.trim();
  const date = document.getElementById('resDate').value;
  const time = document.getElementById('resTime').value;
  const guests = document.getElementById('resGuests').value;
  const seating = document.getElementById('resSeating').value;

  try {
    const res = await fetch('/api/reservations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        vendor_id,
        name,
        phone,
        email: 'customer@example.com',
        date,
        time,
        guests,
        seating_area: seating
      })
    });
    const data = await res.json();
    if (res.ok) {
      const modalEl = document.getElementById('reservationModal');
      const modal = bootstrap.Modal.getInstance(modalEl);
      if (modal) modal.hide();

      alert(`🎉 Table Reserved Successfully!\nBooking Ref: ${data.reservation.booking_ref}\nDate: ${date} at ${time}`);
    }
  } catch (err) {
    console.error('Reservation error:', err);
  }
}

// ============================================================================
// 8. Schemes & Mandi Rates
// ============================================================================

async function fetchSchemes() {
  try {
    const res = await fetch('/api/schemes');
    const schemes = await res.json();
    const container = document.getElementById('schemesContainer');
    if (!container) return;

    container.innerHTML = schemes.map(s => `
      <div class="col-md-4">
        <div class="card h-100 border-0 rounded-4 shadow-sm p-4 bg-white">
          <span class="badge bg-warning-subtle text-warning-emphasis px-3 py-1 rounded-pill fw-bold smaller w-auto align-self-start mb-2">${s.badge}</span>
          <h5 class="fw-bold mb-2">${s.title}</h5>
          <p class="text-muted small mb-3">${s.summary}</p>
          ${s.loan_amount ? `
            <div class="p-2 bg-light rounded-3 small mb-2">
              <strong>Loan Amount:</strong> ${s.loan_amount}<br>
              <strong>Subsidy:</strong> ${s.interest_subsidy}
            </div>
          ` : ''}
          ${s.checklist ? `
            <ul class="text-muted smaller ps-3 mb-2">
              ${s.checklist.map(c => `<li>${c}</li>`).join('')}
            </ul>
          ` : ''}
          ${s.portal_url ? `
            <a href="${s.portal_url}" target="_blank" class="btn btn-outline-dark btn-sm rounded-pill fw-bold mt-auto">
              Visit Official Portal <i class="bi bi-box-arrow-up-right ms-1"></i>
            </a>
          ` : '<span class="badge bg-success-subtle text-success small mt-auto">Enabled on Platform</span>'}
        </div>
      </div>
    `).join('');
  } catch (err) {
    console.error('Schemes load error:', err);
  }
}

async function fetchMandiRates() {
  try {
    const res = await fetch('/api/mandi-rates');
    const rates = await res.json();
    const tbody = document.getElementById('mandiRatesTable');
    if (!tbody) return;

    tbody.innerHTML = rates.map(r => {
      let trendIcon = '<span class="text-success"><i class="bi bi-arrow-down-right"></i> Decreased</span>';
      if (r.trend === 'up') trendIcon = '<span class="text-danger"><i class="bi bi-arrow-up-right"></i> Higher</span>';
      else if (r.trend === 'stable') trendIcon = '<span class="text-muted"><i class="bi bi-dash"></i> Steady</span>';

      return `
        <tr>
          <td class="fw-bold">${r.item}</td>
          <td><span class="badge bg-light text-dark fs-6 border">${r.mandi_rate}</span></td>
          <td>${trendIcon}</td>
          <td class="text-muted small">${r.source}</td>
        </tr>
      `;
    }).join('');
  } catch (err) {
    console.error('Mandi load error:', err);
  }
}

// ============================================================================
// 9. UI Helpers & Theme Toggle
// ============================================================================

function toggleTheme() {
  const html = document.documentElement;
  const current = html.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);

  const icon = document.getElementById('themeIcon');
  if (icon) {
    icon.className = next === 'dark' ? 'bi bi-sun-fill text-warning' : 'bi bi-moon-stars-fill';
  }
}

function showToast(msg) {
  const container = document.getElementById('toastContainer');
  const id = 'toast_' + Date.now();
  const toastHtml = `
    <div id="${id}" class="toast align-items-center text-bg-dark border-0 shadow-lg" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="d-flex">
        <div class="toast-body small fw-semibold">
          <i class="bi bi-info-circle text-warning me-2"></i>${msg}
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
    </div>
  `;
  container.insertAdjacentHTML('beforeend', toastHtml);
  const toastEl = document.getElementById(id);
  const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
  toast.show();
  toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
}

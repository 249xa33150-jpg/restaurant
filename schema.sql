-- ============================================================================
-- Flavor Haven - MySQL Database Schema & Initial Data
-- ============================================================================

CREATE DATABASE IF NOT EXISTS flavor_haven_db;
USE flavor_haven_db;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    role VARCHAR(20) DEFAULT 'user', -- 'user' or 'admin'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories Table
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    slug VARCHAR(50) NOT NULL UNIQUE
);

-- Menu Items Table
CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    rating DECIMAL(3, 1) DEFAULT 4.8,
    image_url VARCHAR(255),
    is_veg BOOLEAN DEFAULT TRUE,
    is_chef_special BOOLEAN DEFAULT FALSE,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders Table
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_number VARCHAR(50) NOT NULL UNIQUE,
    user_id INT,
    customer_name VARCHAR(100) NOT NULL,
    customer_phone VARCHAR(20) NOT NULL,
    delivery_address TEXT NOT NULL,
    order_type VARCHAR(20) DEFAULT 'delivery',
    payment_method VARCHAR(30) NOT NULL,
    payment_status VARCHAR(20) DEFAULT 'Paid',
    status VARCHAR(30) DEFAULT 'Preparing',
    subtotal DECIMAL(10, 2) NOT NULL,
    discount DECIMAL(10, 2) DEFAULT 0.00,
    tax DECIMAL(10, 2) DEFAULT 0.00,
    total_amount DECIMAL(10, 2) NOT NULL,
    coupon_code VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Order Items Table
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    menu_item_id INT,
    item_name VARCHAR(150) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

-- Table Reservations Table
CREATE TABLE IF NOT EXISTS reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_ref VARCHAR(50) NOT NULL UNIQUE,
    user_id INT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    res_date DATE NOT NULL,
    res_time VARCHAR(20) NOT NULL,
    guests INT NOT NULL,
    seating_area VARCHAR(50) DEFAULT 'Main Dining',
    special_request TEXT,
    status VARCHAR(20) DEFAULT 'Confirmed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Reviews Table
CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    customer_role VARCHAR(100),
    avatar_url VARCHAR(255),
    rating INT DEFAULT 5,
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Coupons Table
CREATE TABLE IF NOT EXISTS coupons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(30) NOT NULL UNIQUE,
    discount_percentage DECIMAL(5, 2) DEFAULT 0,
    flat_discount DECIMAL(10, 2) DEFAULT 0,
    min_order DECIMAL(10, 2) DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

-- Initial Coupons Data
INSERT INTO coupons (code, discount_percentage, min_order) VALUES ('HAVEN20', 20.00, 500.00) ON DUPLICATE KEY UPDATE code=code;
INSERT INTO coupons (code, flat_discount, min_order) VALUES ('FIRST50', 0, 300.00) ON DUPLICATE KEY UPDATE code=code;

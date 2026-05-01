-- Create Categories Table
CREATE TABLE IF NOT EXISTS categories (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    image_url TEXT NOT NULL,
    "order" INTEGER DEFAULT 0
);

-- Create Dishes Table
CREATE TABLE IF NOT EXISTS dishes (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    price NUMERIC NOT NULL,
    category TEXT NOT NULL,
    image_url TEXT NOT NULL,
    is_popular BOOLEAN DEFAULT FALSE
);

-- Create Cart Table
CREATE TABLE IF NOT EXISTS cart (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    dish_id TEXT REFERENCES dishes(id) ON DELETE CASCADE,
    dish_name TEXT NOT NULL,
    dish_price NUMERIC NOT NULL,
    dish_image TEXT NOT NULL,
    quantity INTEGER DEFAULT 1,
    UNIQUE(session_id, dish_id)
);

-- Create Orders Table
CREATE TABLE IF NOT EXISTS orders (
    id TEXT PRIMARY KEY,
    order_number TEXT NOT NULL,
    session_id TEXT NOT NULL,
    table_number INTEGER NOT NULL,
    items JSONB NOT NULL,
    total NUMERIC NOT NULL,
    status TEXT DEFAULT 'pending',
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Create Notifications Table
CREATE TABLE IF NOT EXISTS notifications (
    id TEXT PRIMARY KEY,
    order_id TEXT REFERENCES orders(id) ON DELETE CASCADE,
    order_number TEXT NOT NULL,
    table_number INTEGER NOT NULL,
    message TEXT NOT NULL,
    read BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

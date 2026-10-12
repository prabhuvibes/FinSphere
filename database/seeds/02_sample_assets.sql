-- FinSphere Seed Data: Sample Assets
-- This file contains initial asset data for the V1 MVP
-- Note: Prices are sample/demo data for development purposes

-- =====================================================
-- SAMPLE INDIAN STOCKS
-- =====================================================

INSERT INTO assets (id, symbol, name, asset_type_id, description, sector, market, data_source, is_demo_data) VALUES
-- Large Cap Stocks
('750e8400-e29b-41d4-a716-446655440001',
 'RELIANCE',
 'Reliance Industries Limited',
 (SELECT id FROM asset_types WHERE name = 'stock'),
 'Diversified conglomerate with interests in energy, retail, telecommunications, and digital services',
 'Energy & Diversified',
 'NSE',
 'Demo Data',
 true),

('750e8400-e29b-41d4-a716-446655440002',
 'TCS',
 'Tata Consultancy Services',
 (SELECT id FROM asset_types WHERE name = 'stock'),
 'Leading global IT services and consulting company',
 'Information Technology',
 'NSE',
 'Demo Data',
 true),

('750e8400-e29b-41d4-a716-446655440003',
 'HDFCBANK',
 'HDFC Bank Limited',
 (SELECT id FROM asset_types WHERE name = 'stock'),
 'Leading private sector bank offering banking and financial services',
 'Banking',
 'NSE',
 'Demo Data',
 true),

('750e8400-e29b-41d4-a716-446655440004',
 'INFY',
 'Infosys Limited',
 (SELECT id FROM asset_types WHERE name = 'stock'),
 'Global leader in next-generation digital services and consulting',
 'Information Technology',
 'NSE',
 'Demo Data',
 true),

('750e8400-e29b-41d4-a716-446655440005',
 'ICICIBANK',
 'ICICI Bank Limited',
 (SELECT id FROM asset_types WHERE name = 'stock'),
 'Leading private sector bank providing comprehensive financial solutions',
 'Banking',
 'NSE',
 'Demo Data',
 true),

-- Mid Cap Stocks
('750e8400-e29b-41d4-a716-446655440006',
 'BHARTIARTL',
 'Bharti Airtel Limited',
 (SELECT id FROM asset_types WHERE name = 'stock'),
 'Leading telecommunications company providing mobile, broadband and digital services',
 'Telecommunications',
 'NSE',
 'Demo Data',
 true),

('750e8400-e29b-41d4-a716-446655440007',
 'WIPRO',
 'Wipro Limited',
 (SELECT id FROM asset_types WHERE name = 'stock'),
 'Global IT consulting and services company',
 'Information Technology',
 'NSE',
 'Demo Data',
 true),

('750e8400-e29b-41d4-a716-446655440008',
 'KOTAKBANK',
 'Kotak Mahindra Bank',
 (SELECT id FROM asset_types WHERE name = 'stock'),
 'Private sector bank offering banking and financial services',
 'Banking',
 'NSE',
 'Demo Data',
 true),

-- ETF
('750e8400-e29b-41d4-a716-446655440009',
 'NIFTYBEES',
 'Nippon India ETF Nifty BeES',
 (SELECT id FROM asset_types WHERE name = 'etf'),
 'Exchange Traded Fund tracking the Nifty 50 index',
 'Index Fund',
 'NSE',
 'Demo Data',
 true);

-- =====================================================
-- SAMPLE ASSET PRICES (Last 30 days)
-- =====================================================

-- RELIANCE - Current ~₹2,450
INSERT INTO asset_prices (asset_id, price, volume, market_cap, timestamp, data_source, is_demo_data)
SELECT
    '750e8400-e29b-41d4-a716-446655440001',
    2450 + (random() * 100 - 50), -- Random variation ±50
    (random() * 10000000 + 5000000)::BIGINT,
    16500000, -- ₹16.5 lakh crores
    CURRENT_TIMESTAMP - (i || ' days')::INTERVAL,
    'Demo Data',
    true
FROM generate_series(0, 30) AS i;

-- TCS - Current ~₹3,800
INSERT INTO asset_prices (asset_id, price, volume, market_cap, timestamp, data_source, is_demo_data)
SELECT
    '750e8400-e29b-41d4-a716-446655440002',
    3800 + (random() * 150 - 75),
    (random() * 3000000 + 1000000)::BIGINT,
    13800000,
    CURRENT_TIMESTAMP - (i || ' days')::INTERVAL,
    'Demo Data',
    true
FROM generate_series(0, 30) AS i;

-- HDFCBANK - Current ~₹1,650
INSERT INTO asset_prices (asset_id, price, volume, market_cap, timestamp, data_source, is_demo_data)
SELECT
    '750e8400-e29b-41d4-a716-446655440003',
    1650 + (random() * 80 - 40),
    (random() * 8000000 + 3000000)::BIGINT,
    12500000,
    CURRENT_TIMESTAMP - (i || ' days')::INTERVAL,
    'Demo Data',
    true
FROM generate_series(0, 30) AS i;

-- INFY - Current ~₹1,450
INSERT INTO asset_prices (asset_id, price, volume, market_cap, timestamp, data_source, is_demo_data)
SELECT
    '750e8400-e29b-41d4-a716-446655440004',
    1450 + (random() * 70 - 35),
    (random() * 5000000 + 2000000)::BIGINT,
    6000000,
    CURRENT_TIMESTAMP - (i || ' days')::INTERVAL,
    'Demo Data',
    true
FROM generate_series(0, 30) AS i;

-- ICICIBANK - Current ~₹1,150
INSERT INTO asset_prices (asset_id, price, volume, market_cap, timestamp, data_source, is_demo_data)
SELECT
    '750e8400-e29b-41d4-a716-446655440005',
    1150 + (random() * 60 - 30),
    (random() * 7000000 + 2500000)::BIGINT,
    8000000,
    CURRENT_TIMESTAMP - (i || ' days')::INTERVAL,
    'Demo Data',
    true
FROM generate_series(0, 30) AS i;

-- BHARTIARTL - Current ~₹1,550
INSERT INTO asset_prices (asset_id, price, volume, market_cap, timestamp, data_source, is_demo_data)
SELECT
    '750e8400-e29b-41d4-a716-446655440006',
    1550 + (random() * 75 - 37.5),
    (random() * 6000000 + 2000000)::BIGINT,
    9000000,
    CURRENT_TIMESTAMP - (i || ' days')::INTERVAL,
    'Demo Data',
    true
FROM generate_series(0, 30) AS i;

-- WIPRO - Current ~₹560
INSERT INTO asset_prices (asset_id, price, volume, market_cap, timestamp, data_source, is_demo_data)
SELECT
    '750e8400-e29b-41d4-a716-446655440007',
    560 + (random() * 30 - 15),
    (random() * 4000000 + 1500000)::BIGINT,
    2800000,
    CURRENT_TIMESTAMP - (i || ' days')::INTERVAL,
    'Demo Data',
    true
FROM generate_series(0, 30) AS i;

-- KOTAKBANK - Current ~₹1,750
INSERT INTO asset_prices (asset_id, price, volume, market_cap, timestamp, data_source, is_demo_data)
SELECT
    '750e8400-e29b-41d4-a716-446655440008',
    1750 + (random() * 85 - 42.5),
    (random() * 3500000 + 1000000)::BIGINT,
    3500000,
    CURRENT_TIMESTAMP - (i || ' days')::INTERVAL,
    'Demo Data',
    true
FROM generate_series(0, 30) AS i;

-- NIFTYBEES - Current ~₹245
INSERT INTO asset_prices (asset_id, price, volume, market_cap, timestamp, data_source, is_demo_data)
SELECT
    '750e8400-e29b-41d4-a716-446655440009',
    245 + (random() * 12 - 6),
    (random() * 2000000 + 500000)::BIGINT,
    NULL, -- ETF doesn't have market cap
    CURRENT_TIMESTAMP - (i || ' days')::INTERVAL,
    'Demo Data',
    true
FROM generate_series(0, 30) AS i;

-- =====================================================
-- SAMPLE ASSET METRICS
-- =====================================================

-- Add P/E ratios, 52-week high/low, etc.
INSERT INTO asset_metrics (asset_id, metric_name, metric_value, timestamp, data_source) VALUES
('750e8400-e29b-41d4-a716-446655440001', 'pe_ratio', 28.5, CURRENT_TIMESTAMP, 'Demo Data'),
('750e8400-e29b-41d4-a716-446655440001', '52_week_high', 2650.00, CURRENT_TIMESTAMP, 'Demo Data'),
('750e8400-e29b-41d4-a716-446655440001', '52_week_low', 2150.00, CURRENT_TIMESTAMP, 'Demo Data'),

('750e8400-e29b-41d4-a716-446655440002', 'pe_ratio', 32.4, CURRENT_TIMESTAMP, 'Demo Data'),
('750e8400-e29b-41d4-a716-446655440002', '52_week_high', 4100.00, CURRENT_TIMESTAMP, 'Demo Data'),
('750e8400-e29b-41d4-a716-446655440002', '52_week_low', 3200.00, CURRENT_TIMESTAMP, 'Demo Data'),

('750e8400-e29b-41d4-a716-446655440003', 'pe_ratio', 19.8, CURRENT_TIMESTAMP, 'Demo Data'),
('750e8400-e29b-41d4-a716-446655440003', '52_week_high', 1750.00, CURRENT_TIMESTAMP, 'Demo Data'),
('750e8400-e29b-41d4-a716-446655440003', '52_week_low', 1400.00, CURRENT_TIMESTAMP, 'Demo Data');

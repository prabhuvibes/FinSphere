-- FinSphere Database Schema
-- PostgreSQL 14+
-- Created: 2026-10-12
-- Purpose: Financial learning and paper trading platform

-- Enable UUID extension for better security
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- USERS & AUTHENTICATION
-- =====================================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true,
    -- Optional profile fields
    knowledge_level VARCHAR(50) CHECK (knowledge_level IN ('beginner', 'intermediate', 'advanced')),
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- =====================================================
-- LEARNING CONTENT
-- =====================================================

CREATE TABLE courses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100) NOT NULL,
    difficulty_level VARCHAR(50) CHECK (difficulty_level IN ('beginner', 'intermediate', 'advanced')),
    display_order INTEGER NOT NULL,
    is_published BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE lessons (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    course_id UUID NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    display_order INTEGER NOT NULL,
    estimated_duration_minutes INTEGER,
    is_published BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_lessons_course_id ON lessons(course_id);
CREATE INDEX idx_lessons_display_order ON lessons(course_id, display_order);

CREATE TABLE user_lesson_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    lesson_id UUID NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, lesson_id)
);

CREATE INDEX idx_user_lesson_progress_user_id ON user_lesson_progress(user_id);
CREATE INDEX idx_user_lesson_progress_lesson_id ON user_lesson_progress(lesson_id);

-- =====================================================
-- ASSETS & MARKET DATA
-- =====================================================

CREATE TABLE asset_types (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Pre-populate asset types
INSERT INTO asset_types (name, description) VALUES
    ('stock', 'Individual company stocks'),
    ('etf', 'Exchange-traded funds'),
    ('mutual_fund', 'Mutual funds'),
    ('bond', 'Government and corporate bonds'),
    ('crypto', 'Cryptocurrencies');

CREATE TABLE assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    symbol VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    asset_type_id UUID NOT NULL REFERENCES asset_types(id),
    description TEXT,
    sector VARCHAR(100),
    market VARCHAR(50),
    is_active BOOLEAN DEFAULT true,
    -- Data source tracking
    data_source VARCHAR(100),
    is_demo_data BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_assets_symbol ON assets(symbol);
CREATE INDEX idx_assets_asset_type ON assets(asset_type_id);
CREATE INDEX idx_assets_is_active ON assets(is_active);

CREATE TABLE asset_prices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
    price DECIMAL(20, 4) NOT NULL,
    volume BIGINT,
    market_cap DECIMAL(20, 2),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    data_source VARCHAR(100),
    is_demo_data BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT price_positive CHECK (price > 0)
);

CREATE INDEX idx_asset_prices_asset_id ON asset_prices(asset_id);
CREATE INDEX idx_asset_prices_timestamp ON asset_prices(timestamp DESC);
CREATE INDEX idx_asset_prices_asset_timestamp ON asset_prices(asset_id, timestamp DESC);

CREATE TABLE asset_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id UUID NOT NULL REFERENCES assets(id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(20, 4),
    metric_text TEXT,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    data_source VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_asset_metrics_asset_id ON asset_metrics(asset_id);
CREATE INDEX idx_asset_metrics_name ON asset_metrics(metric_name);

-- =====================================================
-- PORTFOLIOS & HOLDINGS
-- =====================================================

CREATE TABLE portfolios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    initial_balance DECIMAL(20, 2) NOT NULL,
    current_cash DECIMAL(20, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    CONSTRAINT initial_balance_positive CHECK (initial_balance > 0),
    CONSTRAINT current_cash_non_negative CHECK (current_cash >= 0)
);

CREATE INDEX idx_portfolios_user_id ON portfolios(user_id);
CREATE INDEX idx_portfolios_is_active ON portfolios(is_active);

CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id) ON DELETE CASCADE,
    asset_id UUID NOT NULL REFERENCES assets(id),
    transaction_type VARCHAR(10) NOT NULL CHECK (transaction_type IN ('buy', 'sell')),
    quantity DECIMAL(20, 8) NOT NULL,
    price_per_unit DECIMAL(20, 4) NOT NULL,
    total_amount DECIMAL(20, 2) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    CONSTRAINT quantity_positive CHECK (quantity > 0),
    CONSTRAINT price_positive CHECK (price_per_unit > 0),
    CONSTRAINT total_amount_positive CHECK (total_amount > 0)
);

CREATE INDEX idx_transactions_portfolio_id ON transactions(portfolio_id);
CREATE INDEX idx_transactions_asset_id ON transactions(asset_id);
CREATE INDEX idx_transactions_timestamp ON transactions(timestamp DESC);
CREATE INDEX idx_transactions_portfolio_timestamp ON transactions(portfolio_id, timestamp DESC);

CREATE TABLE holdings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    portfolio_id UUID NOT NULL REFERENCES portfolios(id) ON DELETE CASCADE,
    asset_id UUID NOT NULL REFERENCES assets(id),
    quantity DECIMAL(20, 8) NOT NULL,
    average_buy_price DECIMAL(20, 4) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(portfolio_id, asset_id),
    CONSTRAINT quantity_positive CHECK (quantity > 0),
    CONSTRAINT average_buy_price_positive CHECK (average_buy_price > 0)
);

CREATE INDEX idx_holdings_portfolio_id ON holdings(portfolio_id);
CREATE INDEX idx_holdings_asset_id ON holdings(asset_id);

-- =====================================================
-- INVESTMENT JOURNAL
-- =====================================================

CREATE TABLE journal_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    portfolio_id UUID REFERENCES portfolios(id) ON DELETE SET NULL,
    asset_id UUID REFERENCES assets(id) ON DELETE SET NULL,
    transaction_id UUID REFERENCES transactions(id) ON DELETE SET NULL,
    -- Initial thesis
    title VARCHAR(255) NOT NULL,
    investment_thesis TEXT NOT NULL,
    assumptions TEXT,
    expected_outcome TEXT,
    risk_assessment TEXT,
    entry_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    -- Review
    review_notes TEXT,
    actual_outcome TEXT,
    lessons_learned TEXT,
    review_date TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_journal_entries_user_id ON journal_entries(user_id);
CREATE INDEX idx_journal_entries_portfolio_id ON journal_entries(portfolio_id);
CREATE INDEX idx_journal_entries_entry_date ON journal_entries(entry_date DESC);

-- =====================================================
-- INVESTMENT ANALYZER SCENARIOS
-- =====================================================

CREATE TABLE analyzer_scenarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    -- Input parameters
    investment_amount DECIMAL(20, 2) NOT NULL,
    goal TEXT,
    time_horizon_months INTEGER,
    risk_preference VARCHAR(50) CHECK (risk_preference IN ('conservative', 'moderate', 'aggressive')),
    -- Scenario results (stored as JSON for flexibility)
    scenarios JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT investment_amount_positive CHECK (investment_amount > 0),
    CONSTRAINT time_horizon_positive CHECK (time_horizon_months > 0)
);

CREATE INDEX idx_analyzer_scenarios_user_id ON analyzer_scenarios(user_id);
CREATE INDEX idx_analyzer_scenarios_created_at ON analyzer_scenarios(created_at DESC);

-- =====================================================
-- AUDIT & SECURITY
-- =====================================================

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100),
    entity_id UUID,
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    details JSONB
);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp DESC);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);

-- =====================================================
-- FUNCTIONS & TRIGGERS
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at trigger to relevant tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_courses_updated_at BEFORE UPDATE ON courses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_lessons_updated_at BEFORE UPDATE ON lessons
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_assets_updated_at BEFORE UPDATE ON assets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_portfolios_updated_at BEFORE UPDATE ON portfolios
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_holdings_updated_at BEFORE UPDATE ON holdings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_journal_entries_updated_at BEFORE UPDATE ON journal_entries
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- VIEWS FOR COMMON QUERIES
-- =====================================================

-- Portfolio summary view
CREATE VIEW portfolio_summary AS
SELECT
    p.id as portfolio_id,
    p.user_id,
    p.name as portfolio_name,
    p.current_cash,
    COUNT(DISTINCT h.asset_id) as total_assets,
    SUM(h.quantity * ap.price) as holdings_value,
    p.current_cash + COALESCE(SUM(h.quantity * ap.price), 0) as total_value,
    p.initial_balance,
    (p.current_cash + COALESCE(SUM(h.quantity * ap.price), 0) - p.initial_balance) as total_gain_loss,
    ((p.current_cash + COALESCE(SUM(h.quantity * ap.price), 0) - p.initial_balance) / p.initial_balance * 100) as gain_loss_percentage
FROM portfolios p
LEFT JOIN holdings h ON p.id = h.portfolio_id
LEFT JOIN LATERAL (
    SELECT price
    FROM asset_prices
    WHERE asset_id = h.asset_id
    ORDER BY timestamp DESC
    LIMIT 1
) ap ON true
WHERE p.is_active = true
GROUP BY p.id, p.user_id, p.name, p.current_cash, p.initial_balance;

-- User learning progress view
CREATE VIEW user_learning_progress AS
SELECT
    u.id as user_id,
    c.id as course_id,
    c.title as course_title,
    COUNT(DISTINCT l.id) as total_lessons,
    COUNT(DISTINCT ulp.lesson_id) as completed_lessons,
    ROUND(COUNT(DISTINCT ulp.lesson_id)::NUMERIC / NULLIF(COUNT(DISTINCT l.id), 0) * 100, 2) as completion_percentage
FROM users u
CROSS JOIN courses c
LEFT JOIN lessons l ON c.id = l.course_id AND l.is_published = true
LEFT JOIN user_lesson_progress ulp ON u.id = ulp.user_id AND l.id = ulp.lesson_id
WHERE c.is_published = true
GROUP BY u.id, c.id, c.title;

-- Asset latest prices view
CREATE VIEW asset_latest_prices AS
SELECT DISTINCT ON (a.id)
    a.id as asset_id,
    a.symbol,
    a.name,
    at.name as asset_type,
    ap.price,
    ap.volume,
    ap.market_cap,
    ap.timestamp,
    ap.data_source,
    ap.is_demo_data
FROM assets a
JOIN asset_types at ON a.asset_type_id = at.id
LEFT JOIN asset_prices ap ON a.id = ap.asset_id
WHERE a.is_active = true
ORDER BY a.id, ap.timestamp DESC;

-- =====================================================
-- COMMENTS FOR DOCUMENTATION
-- =====================================================

COMMENT ON TABLE users IS 'User accounts and authentication information';
COMMENT ON TABLE courses IS 'Educational courses on financial topics';
COMMENT ON TABLE lessons IS 'Individual lessons within courses';
COMMENT ON TABLE user_lesson_progress IS 'Tracks which lessons users have completed';
COMMENT ON TABLE assets IS 'Financial instruments available for exploration and trading';
COMMENT ON TABLE asset_prices IS 'Historical and current price data for assets';
COMMENT ON TABLE portfolios IS 'Virtual portfolios for paper trading';
COMMENT ON TABLE transactions IS 'Buy and sell transactions in portfolios';
COMMENT ON TABLE holdings IS 'Current asset holdings in each portfolio';
COMMENT ON TABLE journal_entries IS 'Investment thesis and reflection journal';
COMMENT ON TABLE analyzer_scenarios IS 'Saved investment scenario comparisons';
COMMENT ON TABLE audit_logs IS 'Security and activity audit trail';

-- =====================================================
-- INITIAL DATA SETUP
-- =====================================================

-- Note: Seed data for courses, lessons, and sample assets
-- will be provided in separate seed files in database/seeds/

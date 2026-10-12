# FinSphere Database Setup Guide

## Quick Start

### Prerequisites
- PostgreSQL 14 or higher installed
- `psql` command-line tool
- Database user with CREATE DATABASE privileges

### 1. Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE finsphere;

# Connect to the database
\c finsphere
```

### 2. Run Schema

```bash
# From the database directory
psql -U postgres -d finsphere -f schema.sql
```

### 3. Load Seed Data

```bash
# Load learning content
psql -U postgres -d finsphere -f seeds/01_learning_content.sql

# Load sample assets
psql -U postgres -d finsphere -f seeds/02_sample_assets.sql
```

### 4. Verify Setup

```sql
-- Check tables were created
\dt

-- Check sample data
SELECT COUNT(*) FROM courses;
SELECT COUNT(*) FROM lessons;
SELECT COUNT(*) FROM assets;
SELECT COUNT(*) FROM asset_prices;

-- Test views
SELECT * FROM asset_latest_prices LIMIT 5;
```

---

## Development Workflow

### Local Development Setup

```bash
# Create development database
createdb finsphere_dev

# Run schema
psql -d finsphere_dev -f schema.sql

# Load seed data
psql -d finsphere_dev -f seeds/01_learning_content.sql
psql -d finsphere_dev -f seeds/02_sample_assets.sql
```

### Testing Database

```bash
# Create test database
createdb finsphere_test

# Run schema (automated in test scripts)
psql -d finsphere_test -f schema.sql
```

---

## Connection Configuration

### Environment Variables

Create `.env` file in backend directory:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/finsphere
DB_HOST=localhost
DB_PORT=5432
DB_NAME=finsphere
DB_USER=your_username
DB_PASSWORD=your_password

# For testing
TEST_DATABASE_URL=postgresql://username:password@localhost:5432/finsphere_test
```

**⚠️ IMPORTANT: Never commit `.env` files to git!**

### Python Connection (FastAPI)

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

---

## Database Maintenance

### Backup

```bash
# Full backup
pg_dump finsphere > backup_$(date +%Y%m%d).sql

# Schema only
pg_dump --schema-only finsphere > schema_backup.sql

# Data only
pg_dump --data-only finsphere > data_backup.sql
```

### Restore

```bash
# Restore from backup
psql -d finsphere < backup_20261012.sql
```

### Reset Database

```bash
# Drop and recreate
dropdb finsphere
createdb finsphere
psql -d finsphere -f schema.sql
psql -d finsphere -f seeds/01_learning_content.sql
psql -d finsphere -f seeds/02_sample_assets.sql
```

---

## Common Queries

### User Management

```sql
-- Create test user
INSERT INTO users (email, password_hash, full_name, knowledge_level)
VALUES ('test@example.com', '$2b$12$...', 'Test User', 'beginner');

-- Get user with portfolios
SELECT u.*, p.name as portfolio_name, p.current_cash
FROM users u
LEFT JOIN portfolios p ON u.id = p.user_id
WHERE u.email = 'test@example.com';
```

### Portfolio Operations

```sql
-- Create portfolio for user
INSERT INTO portfolios (user_id, name, initial_balance, current_cash)
VALUES ('user-uuid-here', 'My First Portfolio', 1000000, 1000000);

-- Get portfolio summary
SELECT * FROM portfolio_summary WHERE user_id = 'user-uuid-here';

-- Get holdings with current prices
SELECT
    h.quantity,
    h.average_buy_price,
    a.symbol,
    a.name,
    ap.price as current_price,
    (ap.price - h.average_buy_price) as gain_loss_per_unit,
    ((ap.price - h.average_buy_price) / h.average_buy_price * 100) as gain_loss_percentage
FROM holdings h
JOIN assets a ON h.asset_id = a.id
JOIN asset_latest_prices ap ON a.id = ap.asset_id
WHERE h.portfolio_id = 'portfolio-uuid-here';
```

### Learning Progress

```sql
-- Get user's course progress
SELECT * FROM user_learning_progress WHERE user_id = 'user-uuid-here';

-- Mark lesson as completed
INSERT INTO user_lesson_progress (user_id, lesson_id)
VALUES ('user-uuid-here', 'lesson-uuid-here')
ON CONFLICT (user_id, lesson_id) DO NOTHING;
```

### Asset Data

```sql
-- Get latest prices for all active stocks
SELECT * FROM asset_latest_prices
WHERE asset_type = 'stock' AND is_active = true
ORDER BY symbol;

-- Get price history for specific asset
SELECT price, timestamp
FROM asset_prices
WHERE asset_id = 'asset-uuid-here'
ORDER BY timestamp DESC
LIMIT 30;
```

---

## Performance Optimization

### Analyze Query Performance

```sql
-- Explain query
EXPLAIN ANALYZE
SELECT * FROM portfolio_summary WHERE user_id = 'some-uuid';

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

### Maintenance Tasks

```sql
-- Update statistics
ANALYZE;

-- Vacuum tables
VACUUM ANALYZE;

-- Reindex if needed
REINDEX DATABASE finsphere;
```

---

## Troubleshooting

### Connection Issues

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check connection
psql -U postgres -h localhost -p 5432
```

### Permission Issues

```sql
-- Grant privileges to user
GRANT ALL PRIVILEGES ON DATABASE finsphere TO your_username;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_username;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_username;
```

### Schema Issues

```sql
-- Check if table exists
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public';

-- Check table structure
\d users

-- Check constraints
SELECT constraint_name, constraint_type
FROM information_schema.table_constraints
WHERE table_name = 'users';
```

---

## Security Best Practices

### 1. Password Hashing
Never store plain text passwords. Use bcrypt in your backend:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed = pwd_context.hash("user_password")
```

### 2. SQL Injection Prevention
Always use parameterized queries:

```python
# Good ✅
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))

# Bad ❌ - SQL injection vulnerable
cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

### 3. Connection Security
Use SSL for production:

```python
DATABASE_URL = "postgresql://user:pass@host/db?sslmode=require"
```

### 4. Secrets Management
- Use environment variables for credentials
- Never commit `.env` files
- Use secret management services in production (AWS Secrets Manager, etc.)

---

## Migration Strategy (Future)

For V1, we use single schema file. For future versions:

```
database/
├── migrations/
│   ├── 001_initial_schema.sql
│   ├── 002_add_crypto_support.sql
│   └── 003_add_social_features.sql
└── schema_migrations table to track versions
```

---

## Team Collaboration

### Before Starting Work
```bash
git pull origin main
psql -d finsphere_dev < database/schema.sql
```

### After Schema Changes
1. Update `schema.sql`
2. Document changes in commit message
3. Update this README if needed
4. Notify team to rebuild their local databases

---

## Production Deployment (Future)

### Checklist
- [ ] Use managed PostgreSQL service (AWS RDS, etc.)
- [ ] Enable automated backups
- [ ] Set up monitoring and alerts
- [ ] Use connection pooling (PgBouncer)
- [ ] Configure SSL/TLS
- [ ] Set up read replicas if needed
- [ ] Regular backup testing
- [ ] Database performance monitoring

---

## Quick Reference

### Useful psql Commands

```bash
\l              # List databases
\c dbname       # Connect to database
\dt             # List tables
\d tablename    # Describe table
\dv             # List views
\di             # List indexes
\df             # List functions
\du             # List users
\q              # Quit
```

### Database Info

```sql
-- Database size
SELECT pg_size_pretty(pg_database_size('finsphere'));

-- Table sizes
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Row counts
SELECT schemaname, tablename, n_live_tup as rows
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;
```

---

## Support

For database-related issues:
1. Check this README
2. Review `ER_DIAGRAM.md` for schema details
3. Consult team members
4. Check PostgreSQL documentation: https://www.postgresql.org/docs/

---

**Last Updated:** 2026-10-12  
**Schema Version:** 1.0 (V1 MVP)  
**PostgreSQL Version:** 14+

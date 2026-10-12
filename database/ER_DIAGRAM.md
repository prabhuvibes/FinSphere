# FinSphere Database Entity-Relationship Diagram

## Database Overview

FinSphere uses PostgreSQL 14+ with a normalized relational schema designed for:
- **Security**: UUID primary keys, password hashing, audit logging
- **Scalability**: Indexed queries, optimized views, efficient relationships
- **Data Integrity**: Foreign keys, constraints, triggers
- **Flexibility**: JSONB for analyzer scenarios, extensible design

---

## Core Entities & Relationships

### 1. Users & Authentication
```
users
├── id (UUID, PK)
├── email (unique, indexed)
├── password_hash
├── full_name
├── knowledge_level
├── is_active
└── timestamps
```

**Relationships:**
- One user → Many portfolios
- One user → Many journal entries
- One user → Many lesson progress records
- One user → Many analyzer scenarios

---

### 2. Learning System

```
courses                      lessons                    user_lesson_progress
├── id (PK)                 ├── id (PK)                ├── id (PK)
├── title                   ├── course_id (FK)         ├── user_id (FK)
├── category                ├── title                  ├── lesson_id (FK)
├── difficulty_level        ├── content                └── completed_at
├── display_order           ├── display_order
└── is_published            └── estimated_duration
```

**Relationships:**
- One course → Many lessons (CASCADE DELETE)
- One lesson → Many user_lesson_progress records
- One user → Many user_lesson_progress records

---

### 3. Assets & Market Data

```
asset_types                 assets                      asset_prices
├── id (PK)                ├── id (PK)                 ├── id (PK)
├── name (unique)          ├── symbol (unique)         ├── asset_id (FK)
└── description            ├── name                    ├── price
                           ├── asset_type_id (FK)      ├── volume
                           ├── sector                  ├── market_cap
                           ├── market                  ├── timestamp (indexed)
                           ├── data_source             ├── data_source
                           └── is_demo_data            └── is_demo_data

                           asset_metrics
                           ├── id (PK)
                           ├── asset_id (FK)
                           ├── metric_name
                           ├── metric_value
                           ├── timestamp
                           └── data_source
```

**Relationships:**
- One asset_type → Many assets
- One asset → Many asset_prices (CASCADE DELETE)
- One asset → Many asset_metrics (CASCADE DELETE)
- One asset → Many holdings
- One asset → Many transactions

---

### 4. Portfolios & Trading

```
portfolios                  transactions                holdings
├── id (PK)                ├── id (PK)                 ├── id (PK)
├── user_id (FK)           ├── portfolio_id (FK)       ├── portfolio_id (FK)
├── name                   ├── asset_id (FK)           ├── asset_id (FK)
├── initial_balance        ├── transaction_type        ├── quantity
├── current_cash           ├── quantity                ├── average_buy_price
├── is_active              ├── price_per_unit          └── updated_at
└── timestamps             ├── total_amount
                           ├── timestamp
                           └── notes
```

**Relationships:**
- One user → Many portfolios (CASCADE DELETE)
- One portfolio → Many transactions (CASCADE DELETE)
- One portfolio → Many holdings (CASCADE DELETE)
- One portfolio, one asset → One holding (UNIQUE constraint)

---

### 5. Investment Journal

```
journal_entries
├── id (PK)
├── user_id (FK)
├── portfolio_id (FK, optional)
├── asset_id (FK, optional)
├── transaction_id (FK, optional)
├── title
├── investment_thesis
├── assumptions
├── expected_outcome
├── risk_assessment
├── entry_date
├── review_notes
├── actual_outcome
├── lessons_learned
└── review_date
```

**Relationships:**
- One user → Many journal_entries (CASCADE DELETE)
- One portfolio → Many journal_entries (SET NULL on delete)
- One asset → Many journal_entries (SET NULL on delete)
- One transaction → Many journal_entries (SET NULL on delete)

---

### 6. Investment Analyzer

```
analyzer_scenarios
├── id (PK)
├── user_id (FK)
├── investment_amount
├── goal
├── time_horizon_months
├── risk_preference
├── scenarios (JSONB)
└── created_at
```

**Relationships:**
- One user → Many analyzer_scenarios (CASCADE DELETE)

---

### 7. Audit & Security

```
audit_logs
├── id (PK)
├── user_id (FK, optional)
├── action
├── entity_type
├── entity_id
├── ip_address
├── user_agent
├── timestamp
└── details (JSONB)
```

**Relationships:**
- One user → Many audit_logs (SET NULL on delete)

---

## Visual ER Diagram

```
┌─────────────┐
│    users    │
└──────┬──────┘
       │
       ├─────────────────────────────────────┐
       │                                     │
       ▼                                     ▼
┌─────────────────┐                  ┌──────────────────┐
│   portfolios    │                  │ journal_entries  │
└────────┬────────┘                  └──────────────────┘
         │                                   
         ├──────────┬──────────┐            
         ▼          ▼          ▼            
   ┌──────────┐ ┌──────────┐ ┌──────────┐
   │holdings  │ │transactions│journal   │
   └────┬─────┘ └─────┬──────┘entries   │
        │             │                  │
        └─────────────┼──────────────────┘
                      │
                      ▼
              ┌───────────────┐
              │    assets     │
              └───────┬───────┘
                      │
         ┌────────────┼────────────┐
         ▼            ▼            ▼
  ┌────────────┐ ┌────────────┐ ┌──────────────┐
  │asset_prices│ │asset_metrics│ │asset_types   │
  └────────────┘ └────────────┘ └──────────────┘

┌─────────────┐
│    users    │
└──────┬──────┘
       │
       ├──────────────────────┐
       ▼                      ▼
┌────────────────┐    ┌─────────────────────┐
│    courses     │    │user_lesson_progress │
└────────┬───────┘    └─────────────────────┘
         │                      ▲
         ▼                      │
    ┌─────────┐                │
    │ lessons │────────────────┘
    └─────────┘

┌─────────────┐
│    users    │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│analyzer_scenarios   │
└─────────────────────┘

┌─────────────┐
│    users    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ audit_logs  │
└─────────────┘
```

---

## Key Design Decisions

### 1. **UUID Primary Keys**
- Better security (not sequential/guessable)
- Distributed system ready
- No collision risk in merges

### 2. **Soft Deletes**
- `is_active` flags on users, portfolios, assets
- Preserves historical data
- Allows "undelete" functionality

### 3. **Timestamp Tracking**
- `created_at` and `updated_at` on all major tables
- Automatic triggers for `updated_at`
- Timezone-aware (UTC storage)

### 4. **Data Integrity**
- Foreign key constraints with appropriate CASCADE/SET NULL
- CHECK constraints for business rules (positive values, valid enums)
- UNIQUE constraints prevent duplicates

### 5. **Performance Optimization**
- Strategic indexes on foreign keys
- Composite indexes for common query patterns
- Materialized views for complex aggregations

### 6. **Flexible Data Storage**
- JSONB for analyzer scenarios (allows iteration without schema changes)
- JSONB for audit log details (captures any metadata)

### 7. **Security Features**
- Password hashing (handled by backend, not stored plain)
- Audit logging for compliance
- Email validation via CHECK constraint
- Data isolation by user_id

---

## Important Constraints

### Portfolio Integrity
- `current_cash >= 0` (can't go negative)
- `initial_balance > 0` (must start with funds)

### Transaction Validation
- `quantity > 0` (no zero-quantity trades)
- `price_per_unit > 0` (price must be positive)
- `total_amount = quantity * price_per_unit` (calculated by backend)

### Holdings
- UNIQUE(portfolio_id, asset_id) - one holding per asset per portfolio
- `quantity > 0` - automatically deleted when quantity reaches 0

---

## Views for Common Queries

### 1. `portfolio_summary`
Aggregates portfolio value with current asset prices:
- Current cash
- Holdings value (live prices)
- Total value
- Gain/loss (amount and percentage)

### 2. `user_learning_progress`
Shows completion status for each course:
- Total lessons
- Completed lessons
- Completion percentage

### 3. `asset_latest_prices`
Most recent price for each asset:
- Eliminates need to query with ORDER BY + LIMIT
- Indexed for fast lookups

---

## Migration Strategy

For V1 MVP:
1. Create schema with `schema.sql`
2. Verify all tables created successfully
3. Seed initial data (asset_types, sample courses)
4. Test constraints with invalid data
5. Verify triggers work (updated_at)

For Future Versions:
- Use migration files (`001_initial.sql`, `002_add_feature.sql`)
- Track migrations in `schema_migrations` table
- Never modify existing migrations
- Always create new migration files

---

## Sample Queries

### Get user's portfolios with current value
```sql
SELECT * FROM portfolio_summary WHERE user_id = ?;
```

### Get user's learning progress
```sql
SELECT * FROM user_learning_progress WHERE user_id = ?;
```

### Get latest asset prices
```sql
SELECT * FROM asset_latest_prices WHERE asset_type = 'stock' AND is_active = true;
```

### Get portfolio transaction history
```sql
SELECT t.*, a.symbol, a.name
FROM transactions t
JOIN assets a ON t.asset_id = a.id
WHERE t.portfolio_id = ?
ORDER BY t.timestamp DESC;
```

### Calculate portfolio performance
```sql
SELECT
    portfolio_id,
    portfolio_name,
    total_value,
    initial_balance,
    gain_loss_percentage
FROM portfolio_summary
WHERE user_id = ?;
```

---

## Next Steps

1. ✅ Schema design complete
2. 📝 Create seed data files
3. 🧪 Test schema with sample data
4. 🔧 Set up database migrations framework
5. 📡 Design API contracts based on schema

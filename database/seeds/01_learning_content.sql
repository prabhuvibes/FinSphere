-- FinSphere Seed Data: Sample Learning Content
-- This file contains initial courses and lessons for the V1 MVP

-- =====================================================
-- COURSES
-- =====================================================

INSERT INTO courses (id, title, description, category, difficulty_level, display_order, is_published) VALUES
('550e8400-e29b-41d4-a716-446655440001',
 'Financial Basics',
 'Understanding fundamental concepts of personal finance and investing',
 'Fundamentals',
 'beginner',
 1,
 true),

('550e8400-e29b-41d4-a716-446655440002',
 'Understanding Risk and Return',
 'Learn about the relationship between investment risk and potential returns',
 'Fundamentals',
 'beginner',
 2,
 true),

('550e8400-e29b-41d4-a716-446655440003',
 'Introduction to Stocks',
 'What are stocks, how they work, and basic stock market concepts',
 'Stocks',
 'beginner',
 3,
 true),

('550e8400-e29b-41d4-a716-446655440004',
 'Portfolio Diversification',
 'Why and how to diversify your investment portfolio',
 'Strategy',
 'intermediate',
 4,
 true);

-- =====================================================
-- LESSONS
-- =====================================================

-- Course 1: Financial Basics
INSERT INTO lessons (id, course_id, title, content, display_order, estimated_duration_minutes, is_published) VALUES
('650e8400-e29b-41d4-a716-446655440001',
 '550e8400-e29b-41d4-a716-446655440001',
 'What is Investing?',
 'Investing is the act of allocating money or resources with the expectation of generating income or profit over time. Unlike saving, which focuses on preserving money, investing involves taking calculated risks to grow your wealth.

**Key Concepts:**
- **Assets**: Things you can invest in (stocks, bonds, real estate, etc.)
- **Returns**: The profit or loss from your investment
- **Time Horizon**: How long you plan to keep your money invested
- **Compound Growth**: Earning returns on your returns

**Why Invest?**
1. Beat inflation - Keep your purchasing power
2. Build wealth - Grow your money over time
3. Achieve goals - Fund retirement, education, or major purchases

Remember: All investments carry some level of risk. The key is understanding and managing that risk.',
 1,
 8,
 true),

('650e8400-e29b-41d4-a716-446655440002',
 '550e8400-e29b-41d4-a716-446655440001',
 'Understanding Financial Goals',
 'Before investing, you need clear financial goals. Goals give your investments purpose and help you choose the right strategy.

**Types of Financial Goals:**

**Short-term (1-3 years):**
- Emergency fund
- Down payment for a car
- Vacation savings

**Medium-term (3-10 years):**
- House down payment
- Wedding expenses
- Starting a business

**Long-term (10+ years):**
- Retirement
- Children''s education
- Financial independence

**SMART Goals Framework:**
- **Specific**: "Save ₹50 lakhs" not "Save money"
- **Measurable**: Track your progress
- **Achievable**: Realistic given your income
- **Relevant**: Aligned with your values
- **Time-bound**: Clear deadline

Your investment strategy should match your goals timeline and risk tolerance.',
 2,
 10,
 true),

('650e8400-e29b-41d4-a716-446655440003',
 '550e8400-e29b-41d4-a716-446655440001',
 'Time Value of Money',
 'Money available today is worth more than the same amount in the future. This concept is fundamental to all investing decisions.

**Why does money have time value?**

1. **Earning Potential**: Money today can be invested to earn returns
2. **Inflation**: Money loses purchasing power over time
3. **Opportunity Cost**: Delayed money means missed opportunities

**Example:**
If you invest ₹10,000 today at 10% annual return:
- Year 1: ₹11,000
- Year 5: ₹16,105
- Year 10: ₹25,937
- Year 20: ₹67,275

This is the power of compound interest - earning returns on your returns.

**Key Takeaway:**
Start investing early. Even small amounts invested young can grow significantly over time. A 25-year-old investing ₹5,000/month will likely have more at retirement than a 35-year-old investing ₹10,000/month, thanks to the extra 10 years of compound growth.',
 3,
 12,
 true);

-- Course 2: Understanding Risk and Return
INSERT INTO lessons (id, course_id, title, content, display_order, estimated_duration_minutes, is_published) VALUES
('650e8400-e29b-41d4-a716-446655440004',
 '550e8400-e29b-41d4-a716-446655440002',
 'The Risk-Return Relationship',
 'In investing, risk and potential return are directly related. Understanding this relationship is crucial for making informed decisions.

**Core Principle:**
Higher potential returns come with higher risk. Lower risk investments offer lower potential returns.

**Risk-Return Spectrum:**

**Low Risk, Low Return:**
- Savings accounts (3-4% return)
- Government bonds (5-7% return)
- Risk: Very low
- Best for: Emergency funds, short-term goals

**Medium Risk, Medium Return:**
- Corporate bonds (7-9% return)
- Balanced mutual funds (8-12% return)
- Risk: Moderate
- Best for: Medium-term goals

**Higher Risk, Higher Potential Return:**
- Stocks (12-15% historical average)
- Equity mutual funds (12-18% potential)
- Risk: High (can lose value)
- Best for: Long-term goals

**Important Note:**
Higher risk doesn''t guarantee higher returns - it means higher potential returns AND higher potential losses. Your job is to find the right balance for your situation.',
 1,
 15,
 true),

('650e8400-e29b-41d4-a716-446655440005',
 '550e8400-e29b-41d4-a716-446655440002',
 'Types of Investment Risk',
 'Risk comes in many forms. Understanding different types helps you make better decisions.

**1. Market Risk**
The risk that the overall market declines, affecting your investments.
- Example: Stock market crash affects all stocks
- Mitigation: Diversification, long time horizon

**2. Inflation Risk**
The risk that your returns don''t keep pace with rising prices.
- Example: 4% savings account with 6% inflation = losing purchasing power
- Mitigation: Invest in assets that historically beat inflation (stocks, real estate)

**3. Liquidity Risk**
The risk you can''t sell an investment quickly without significant loss.
- Example: Real estate takes time to sell
- Mitigation: Keep emergency funds in liquid assets

**4. Company-Specific Risk**
Risk that a particular company performs poorly.
- Example: Bad management, product failure, scandal
- Mitigation: Diversify across multiple companies

**5. Interest Rate Risk**
Changes in interest rates affecting investment values.
- Example: Rising rates can decrease bond prices
- Mitigation: Diversify bond maturities

**Your Risk Profile:**
Your ideal risk level depends on:
- Time horizon (longer = can take more risk)
- Financial goals
- Income stability
- Personal comfort with volatility',
 2,
 18,
 true);

-- Course 3: Introduction to Stocks
INSERT INTO lessons (id, course_id, title, content, display_order, estimated_duration_minutes, is_published) VALUES
('650e8400-e29b-41d4-a716-446655440006',
 '550e8400-e29b-41d4-a716-446655440003',
 'What Are Stocks?',
 'A stock represents ownership in a company. When you buy stock, you become a shareholder - a part owner of that business.

**How Stocks Work:**

When a company needs money to grow, it can sell pieces of ownership (shares) to the public. This is called "going public" or an IPO (Initial Public Offering).

**As a Shareholder, You Get:**
1. **Potential Price Appreciation**: If the company does well, stock price may rise
2. **Dividends**: Some companies share profits with shareholders
3. **Voting Rights**: Say in major company decisions (usually 1 vote per share)

**Stock Prices:**
Prices change based on:
- Company performance (revenue, profits)
- Future expectations (growth potential)
- Market sentiment (investor confidence)
- Economic conditions
- Industry trends

**Example:**
If you bought 10 shares of Company ABC at ₹500 each (₹5,000 total), and the price rises to ₹700, your investment is now worth ₹7,000 - a ₹2,000 gain (40% return). But prices can also fall.

**Remember:**
Stocks are not lottery tickets. You''re buying real ownership in real businesses. Success comes from understanding the businesses you invest in.',
 1,
 12,
 true),

('650e8400-e29b-41d4-a716-446655440007',
 '550e8400-e29b-41d4-a716-446655440003',
 'How the Stock Market Works',
 'The stock market is where buyers and sellers come together to trade shares of publicly listed companies.

**Key Players:**

**1. Stock Exchanges**
- Physical or electronic marketplaces
- India: BSE (Bombay Stock Exchange), NSE (National Stock Exchange)
- Ensure fair trading, regulate listed companies

**2. Brokers**
- Intermediaries between you and the exchange
- You can''t buy stocks directly; you need a broker account
- Modern brokers offer online/mobile apps

**3. Companies**
- List their shares for public trading
- Must meet exchange requirements and regulations
- Regularly disclose financial information

**4. Investors (You!)**
- Buy and sell shares through brokers
- Make decisions based on research and goals

**How Trading Works:**

1. You place an order through your broker
2. Order goes to the exchange
3. Exchange matches buyers with sellers
4. Trade executes at agreed price
5. Shares transfer to your demat account

**Market Hours:**
Indian markets open 9:15 AM - 3:30 PM on weekdays (excluding holidays)

**Order Types:**
- **Market Order**: Buy/sell at current market price (executes immediately)
- **Limit Order**: Buy/sell only at your specified price or better

**Important:**
Markets can be volatile (prices change rapidly). This is normal. Long-term investors focus on company fundamentals, not daily price movements.',
 2,
 20,
 true);

-- Course 4: Portfolio Diversification
INSERT INTO lessons (id, course_id, title, content, display_order, estimated_duration_minutes, is_published) VALUES
('650e8400-e29b-41d4-a716-446655440008',
 '550e8400-e29b-41d4-a716-446655440004',
 'Why Diversification Matters',
 'Diversification is the practice of spreading investments across different assets to reduce risk. It''s the closest thing to a "free lunch" in investing.

**The Problem Diversification Solves:**

If you invest everything in one company and it fails, you lose everything. But if you invest in 20 companies and one fails, you only lose 5% of your portfolio.

**Don''t Put All Your Eggs in One Basket:**

Imagine three investors, each with ₹1 lakh:
- **Investor A**: All ₹1L in Tech Company X
- **Investor B**: ₹50K in Tech X, ₹50K in Bank Y
- **Investor C**: Spread across 10 different companies

Tech Company X faces scandal, stock drops 50%.

Results:
- Investor A: Lost ₹50,000 (50% loss)
- Investor B: Lost ₹25,000 (25% loss)
- Investor C: Lost ₹5,000 (5% loss)

**Types of Diversification:**

**1. Across Companies**
Don''t invest in just one or two stocks

**2. Across Sectors**
Technology, Banking, Healthcare, Consumer Goods, etc.
Different sectors perform well at different times

**3. Across Asset Classes**
Stocks, bonds, gold, real estate
When stocks fall, bonds might hold steady

**4. Across Geographies** (Advanced)
Indian companies, US companies, emerging markets

**Common Mistake:**
Owning 10 different tech stocks isn''t true diversification - they''ll likely move together. Real diversification means spreading across different types of investments.

**How Much Diversification?**
- Too little: Excessive risk
- Too much: Hard to track, diminishing benefits
- Sweet spot: 15-30 stocks across 5-8 sectors (or use mutual funds/ETFs)',
 1,
 15,
 true),

('650e8400-e29b-41d4-a716-446655440009',
 '550e8400-e29b-41d4-a716-446655440004',
 'Building a Balanced Portfolio',
 'A balanced portfolio matches your goals, timeline, and risk tolerance while providing adequate diversification.

**Asset Allocation by Age (Rule of Thumb):**

**In Your 20s-30s:**
- Stocks: 70-80%
- Bonds: 15-20%
- Cash: 5-10%
- Rationale: Long time horizon, can weather volatility

**In Your 40s-50s:**
- Stocks: 50-60%
- Bonds: 30-40%
- Cash: 10%
- Rationale: Moderate time horizon, balancing growth and stability

**Near/In Retirement:**
- Stocks: 30-40%
- Bonds: 50-60%
- Cash: 10-20%
- Rationale: Preservation focus, need stability

**Sample Portfolio for a 28-year-old with ₹5 lakh:**

**Equity (70% = ₹3.5L):**
- Large-cap stocks/ETF: ₹1.5L (40%)
- Mid-cap stocks/fund: ₹1L (30%)
- Small-cap stocks/fund: ₹0.5L (15%)
- International stocks: ₹0.5L (15%)

**Debt (20% = ₹1L):**
- Corporate bonds/debt funds: ₹0.7L
- Fixed deposits: ₹0.3L

**Others (10% = ₹0.5L):**
- Gold ETF: ₹0.3L
- Cash/liquid funds: ₹0.2L

**Rebalancing:**
Review your portfolio every 6-12 months. If stocks perform well and become 85% of your portfolio (vs. target 70%), sell some stocks and buy bonds to restore balance.

**Remember:**
These are guidelines, not rules. Your personal situation matters most. A conservative person might hold more bonds, an aggressive investor more stocks.',
 2,
 20,
 true);

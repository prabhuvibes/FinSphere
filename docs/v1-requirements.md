# FinSphere V1 Requirements

**Status:** Proposed MVP baseline  
**Project context:** Final-year college project, five-person team, approximately four weeks for the initial implementation

## 1. Purpose

FinSphere is a web application that helps beginner users learn core financial concepts, explore a small set of market assets, compare investment scenarios, practice with virtual money, and review their decisions. The V1 is an educational decision-support prototype. It does not execute real investments or promise returns.

The product principle is: **Teach users how to think about financial decisions; do not tell them what to buy or sell.**

## 2. V1 outcome

A user should be able to complete this end-to-end journey:

1. Create an account and sign in.
2. Read a short financial learning path.
3. Explore a curated asset and understand a small number of displayed metrics.
4. Enter a goal, amount, time horizon, and risk preference to compare illustrative scenarios.
5. Practice a simulated trade using virtual funds.
6. Review the resulting portfolio and record the reasoning in a journal.

The project is successful when this journey works reliably with the available market data and can be demonstrated from the browser against a real API server and database.

## 3. Target users and roles

### Learner

The primary V1 user. The learner can access educational content, explore assets, compare hypothetical scenarios, simulate transactions, and review personal portfolio and journal data.

### Content administrator

V1 does not require a full administration console. The team may maintain lessons and the initial asset catalogue through database seed data or a simple protected interface if time permits.

## 4. Scope

### Must have for the college MVP

- Responsive web client, backend API, and PostgreSQL database.
- Account registration and sign-in with protected user-specific data.
- A small set of curated lessons covering financial basics, risk, diversification, and investing.
- A bounded asset catalogue with detail pages and clearly labelled data timestamps.
- Explanations for the limited metrics shown on asset pages.
- A rule-based Investment Analyzer that returns multiple illustrative scenarios from user inputs.
- Paper trading with virtual cash, transaction history, holdings, and basic portfolio value.
- A journal entry to capture a simulated decision thesis and a later reflection.
- Sample or seeded data as a documented fallback if a usable market-data API is unavailable.

### Should have if core flows are stable

- Lesson completion tracking.
- A simple historical price chart for assets with available data.
- Basic risk summaries such as historical range or volatility, only where the calculation and data can be explained.
- A small admin utility for maintaining learning content or asset seed data.

### Stretch only

- An AI Mentor that explains supplied concepts or displayed metrics in plain language. It must not issue unqualified buy/sell commands. The V1 must remain complete without AI.
- Additional technical indicators such as RSI or moving averages, provided the team can validate their calculations and explain their limits.

### Explicitly out of scope for V1

- Real-money orders, brokerage integration, payments, custody, or autonomous trading.
- Guaranteed-return language or personalized buy/sell recommendations.
- Broad real-time coverage of every asset class or market.
- A professional portfolio optimizer, advanced backtesting engine, or complex stress-testing suite.
- Full news ingestion, AI sentiment scoring, crypto on-chain analytics, and extensive gamification.
- Microservices or a separate production administration platform.

## 5. Functional requirements

### Accounts and privacy

**FR-01 — Registration:** A visitor can create an account using the required profile fields. The system rejects duplicate accounts and invalid input with understandable feedback.

**FR-02 — Sign-in and sign-out:** A registered user can sign in and sign out. Protected pages require a valid session or token.

**FR-03 — Data isolation:** A user can only read or change their own profile, portfolios, trades, and journal entries.

### Learning

**FR-04 — Browse lessons:** A signed-in user can browse the published V1 lessons grouped by topic and open lesson content.

**FR-05 — Learning progress (should have):** When implemented, lesson completion is saved per user and shown when the user returns.

### Asset exploration and explanation

**FR-06 — Browse assets:** A user can browse the bounded V1 asset list and open an asset detail page.

**FR-07 — View asset information:** The detail page shows the asset name, symbol, asset type, available price/history, and a limited set of supported metrics.

**FR-08 — Identify data freshness:** Each price or historical-data view shows its source or demo-data label and observation/update time. Missing data is shown as unavailable, not silently replaced with a fabricated current value.

**FR-09 — Explain metrics:** Each displayed metric has a short plain-language explanation and avoids presenting the metric as a standalone recommendation.

### Investment Analyzer

**FR-10 — Collect scenario inputs:** The analyzer accepts an investment amount, goal, time horizon, and risk preference. Inputs are validated and can be changed before results are generated.

**FR-11 — Compare scenarios:** The analyzer returns at least three illustrative allocation scenarios, such as capital-preservation-oriented, balanced, and growth-oriented. Results identify allocation assumptions and describe relative risk, liquidity, and growth trade-offs.

**FR-12 — Avoid false certainty:** Results are labelled hypothetical and educational. They do not claim to predict returns, identify a single best investment, or guarantee an outcome. If numerical projections are included, the assumptions and limitations are visible alongside them.

### Paper trading and portfolio

**FR-13 — Create a virtual portfolio:** A user can create a portfolio with a stated virtual starting balance.

**FR-14 — Simulate a transaction:** A user can record a simulated buy or sell for a supported asset and quantity. The server validates available virtual cash or holdings and stores the transaction price and timestamp used.

**FR-15 — View holdings:** A user can see current virtual cash, positions, and transaction history for their own portfolio.

**FR-16 — View basic performance:** The portfolio shows a clearly defined basic value or gain/loss calculation based on the available market snapshot. Stale or missing prices are labelled.

### Investment journal

**FR-17 — Record a thesis:** A user can save a journal entry with an asset, reason for considering it, assumptions, expected outcome, and associated simulated trade when applicable.

**FR-18 — Review a decision:** A user can later add review notes about the outcome and what they learned.

### Optional AI Mentor

**FR-19 — Explain, do not direct (stretch):** If included, the AI Mentor receives only the user's question and the relevant displayed educational context. It explains concepts and uncertainty, does not invent unavailable data, and does not return unqualified buy/sell instructions.

## 6. Non-functional requirements

- **Usability:** Core flows use clear labels, consistent navigation, readable charts, and responsive layouts.
- **Security:** Passwords are stored as secure hashes; secrets are kept outside source control; inputs are validated; API routes enforce authentication and ownership checks.
- **Data integrity:** Simulated trades, cash balances, and holdings remain consistent after each accepted transaction.
- **Transparency:** The interface identifies simulated transactions, sample data, data timestamps, and analyzer assumptions.
- **Maintainability:** Frontend, API, business rules, database access, and external data adapters have clear boundaries.
- **Reliability:** Failures from a data provider do not prevent lessons and simulated flows from working; the app displays a clear unavailable/stale-data state.
- **Accessibility baseline:** Forms have labels, keyboard navigation works for core controls, and meaning is not conveyed by color alone.

## 7. MVP acceptance checklist

The V1 is ready for the college demonstration when:

- A user can register, sign in, sign out, and access only their own records.
- The user can open and complete the core learning content.
- The user can browse a seeded or live asset and see a data timestamp and metric explanations.
- The analyzer produces three distinguishable hypothetical scenarios with visible assumptions and trade-offs.
- A user can create a virtual portfolio, simulate a valid transaction, and see the resulting cash and holdings.
- Invalid or unaffordable simulated trades are rejected without changing the portfolio.
- A user can create and later review a journal entry.
- The application clearly distinguishes simulation from real investing and communicates data limitations.
- The main journey works against the team's client, API server, and database in the demo environment.

## 8. Four-week delivery priorities

1. **Week 1 — Define and scaffold:** confirm this scope, wireframe the core journey, agree API boundaries, create the database model, and seed sample content/data.
2. **Week 2 — Foundation:** implement accounts, navigation, lessons, asset browse/detail, and persistence.
3. **Week 3 — Decision and simulation:** implement scenario comparison, paper trading, holdings, and journal flows.
4. **Week 4 — Integrate and demonstrate:** stabilize the end-to-end path, improve usability, verify data labels and calculations, and prepare the presentation.

If schedule slips, preserve the complete journey with seeded data and rule-based scenarios. Defer AI, live-data coverage, advanced indicators, and analytics before weakening account isolation or transaction correctness.

## 9. Decisions to confirm before database design

These are the few product decisions that affect the schema and API design:

1. **Initial asset universe:** which small set of instruments and asset types will the demo support?
2. **Price source:** which permitted market-data provider will be used, or will V1 use seeded snapshots only?
3. **Starting virtual balance:** what amount should each new paper portfolio receive?
4. **Registration fields:** which fields are truly needed beyond name, email, and password?
5. **Analyzer output:** should V1 show allocation percentages only, or also include illustrative numeric projections with explicit assumptions?

Unless the team decides otherwise, use seeded asset snapshots, a configurable virtual starting balance, minimal account fields, and allocation-based scenarios without return forecasts.


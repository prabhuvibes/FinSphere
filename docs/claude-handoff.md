# FinSphere Project Handoff for Claude

> **Instructions for Claude:** Take over as the project's technical and product co-planner and lead the next stages of work with the student. Continue the work in the existing GitHub repository named below. Do not create a replacement repository. Read the repository files before changing scope or implementation. Keep the college V1 small enough for the stated timeline, explain trade-offs plainly, and update GitHub with each agreed, reviewable project change.

## 1. Project identity

- **Name:** FinSphere
- **Tagline:** Learn. Explore. Analyze. Simulate. Invest.
- **Type:** Final-year college web application and a possible foundation for a future product
- **Current objective:** Deliver a credible, working V1 for the college project; preserve a sensible path for later semesters without trying to build the full long-term vision now.
- **Product principle:** “Don't tell the user what to think. Teach them how to think.”

FinSphere is not intended to be just a stock-prediction website, trading bot, or CRUD exercise. It is envisioned as a financial-market learning and decision environment that helps a beginner build understanding and practice decisions safely.

## 2. Exact GitHub repository and continuation instructions

- **Repository:** [https://github.com/prabhuvibes/FinSphere](https://github.com/prabhuvibes/FinSphere)
- **Owner/name:** `prabhuvibes/FinSphere`
- **Visibility:** Private
- **Default branch:** `main`
- **Continue in this exact repository.** Do not create a fork or a differently named repository unless the student explicitly asks.
- Review `README.md`, `.gitignore`, `docs/v1-requirements.md`, and this handoff before proceeding.
- Commit and push agreed changes to this repository so the GitHub copy stays current. Verify the changes appear on `main` after publishing.
- A prior local folder was created at `C:\Users\ASUS\Documents\Codex\2026-10-08\he\FinSphere`. That local copy has a separate initial Git history from the GitHub repository; prefer cloning the GitHub repository fresh rather than assuming this local directory is synchronized. The terminal GitHub credential was invalid at the last check; use an authenticated GitHub integration or ask the student to reconnect GitHub before pushing. Never ask them to paste a password, token, or one-time code into chat.

At the time this handoff was written, GitHub contained:

- `README.md` — project overview and technical direction
- `.gitignore` — common Node.js and Python exclusions
- `docs/v1-requirements.md` — proposed V1 MVP requirements
- `docs/claude-handoff.md` — this handoff

## 3. Full product vision

The long-term product journey is:

**Learn → Explore → Analyze → Simulate → Invest → Track → Review → Improve**

The envisioned product may eventually include:

1. **Learn:** Beginner-to-advanced material on financial basics, stocks, ETFs, mutual funds, bonds, gold, crypto, risk/return, diversification, compounding, fundamental and technical analysis, portfolios, and advanced concepts.
2. **Explore:** Assets, companies, sectors, markets, historical performance, trends, news and events.
3. **Analyze:** Fundamental, technical, valuation, volatility, risk, sector and news context, explained in understandable language.
4. **Investment Analyzer:** Collect a user's goal, amount, horizon, risk tolerance, acceptable downside, liquidity needs, knowledge level, preferences and constraints. Compare multiple hypothetical scenarios and show assumptions and trade-offs; do not pronounce one scenario “best.” Advanced future analysis may include volatility, correlation, beta, Sharpe ratio, drawdown, sector exposure, optimization and stress testing.
5. **Simulate:** Virtual-money investing, portfolios, historical scenarios, crash simulations, strategy tests and backtesting.
6. **Portfolio:** Allocation, holdings, performance, risk, diversification, sector concentration and watchlists.
7. **AI Mentor:** Explain concepts, metrics, analysis, terminology and trade-offs; help the user learn from decisions, not act as a magical buy/sell predictor.
8. **Market Intelligence:** News, company events, sector developments, market context and sentiment.
9. **Investment Journal:** Record a thesis, assumptions, expected outcome and risk; later compare with the outcome and reflect on lessons.
10. **Goals and progress:** Connect learning/investing to goals and track learning milestones, simulations and progress.
11. **Crypto:** Dedicated exploration and analysis, with metrics only where reliable data is available.
12. **Real investing:** Possible long-term brokerage integration with regulated infrastructure; future product work only.

This list describes the broad vision, not V1 delivery scope.

## 4. College-project context

- The student is in the final year / 7th semester; the project should be extendable in the 8th semester.
- The team has **five people**.
- The initial build has roughly **four weeks**.
- The college requires an actual **client + server + database** web application.
- The result should be technically credible and demonstrable, but realistically achievable.
- The student wants a practical co-planner who challenges scope and assumptions rather than agreeing automatically.
- The project may eventually become a serious product, but startup-scale requirements must not overwhelm the college MVP.

## 5. Proposed V1 product definition

V1 should demonstrate one complete, understandable loop for a beginner:

1. Register and sign in.
2. Learn a few core concepts.
3. Explore a small curated set of assets and understand the metrics shown.
4. Compare three illustrative investment scenarios from simple user inputs.
5. Paper trade with virtual money.
6. See resulting holdings and basic portfolio value.
7. Record the reason for a simulated decision and later review it.

### Proposed must-have scope

- Responsive web client, backend API and PostgreSQL database.
- Registration, sign-in/sign-out and user-data isolation.
- A small, curated lesson set for financial basics, investing, risk and diversification.
- A limited asset catalogue and detail pages with clearly labelled timestamps/source or demo-data labels.
- Plain-language explanations for the few asset metrics shown.
- Rule-based Investment Analyzer returning at least three hypothetical allocation scenarios (capital-preservation-oriented, balanced, growth-oriented) with assumptions and trade-offs.
- Paper trading with virtual cash, transaction history, holdings and basic portfolio value/performance.
- Investment journal entries for thesis, assumptions, expected outcome and later reflection.
- Seeded sample data as a dependable fallback if a market-data provider is unavailable or unsuitable.

### Conditional / stretch scope

- Lesson-progress tracking, simple charts, risk summaries and a basic content-maintenance utility after the end-to-end path is reliable.
- AI Mentor only if the core flows are stable and a safe, useful integration can be completed. The application must work without AI.
- Technical indicators only in a small, verified set and with plain explanations.

### Exclude from the first month

- Real-money trading, brokerage, payment or custody features.
- Buy/sell recommendations, trading automation, guaranteed returns or claims that projections are predictions.
- All-market real-time coverage, large-scale news/sentiment pipelines, advanced portfolio optimization, deep backtesting, extensive crypto on-chain metrics, elaborate gamification or microservices.

## 6. Product, data and safety constraints

- Explain how to reason about choices; do not tell the user what to buy or sell.
- The Analyzer generates **scenarios**, not a recommendation or certain future outcome.
- Clearly state assumptions, uncertainty and data timestamps. Label simulated transactions and seeded/demo data.
- Do not fabricate a current price when data is missing. Show an unavailable/stale-data state.
- No real investments occur in V1; no payment, brokerage or custody capability is present.
- Protect account data: hash passwords, validate requests, keep credentials/secrets out of Git, and enforce ownership on user-specific API operations.
- Keep the system useful if market data or AI is unavailable.
- Minimize personal information collected. Basic registration should need only what the V1 genuinely uses.
- Any future public or real-money release needs a separate review of applicable data licensing, security, privacy and financial obligations.

## 7. Proposed technical direction

- **Frontend:** React or Next.js
- **Backend:** Python with FastAPI, REST API
- **Database:** PostgreSQL
- **Authentication:** Secure session or JWT design; select one consistent implementation for the MVP
- **Integrations:** Market-data API and optional AI/LLM API behind server-side adapters
- **Visualization:** Charts only for data the team can source and label reliably
- **Deployment:** Local development first; Docker/deployment if time permits

Prefer a modular monolith for V1. Keep frontend, API routes, business rules, persistence and external-service adapters separated enough to extend, without adding microservice operations overhead.

## 8. Requirements already drafted

`docs/v1-requirements.md` contains the current proposed MVP requirements, including functional requirements FR-01 through FR-19, non-functional requirements, acceptance checklist, four-week priorities and unresolved product decisions.

Treat it as a **proposed baseline**, not as a fully approved specification. Before database design, resolve the decisions below with the student or proceed with the stated recommended defaults and clearly record them.

## 9. Open decisions and recommended defaults

1. **Asset universe:** Choose a narrow list. Recommended starting point: a small set of Indian equities plus one broad-market ETF, subject to data availability. Avoid supporting every asset category in V1.
2. **Market data:** Recommended: seeded historical/sample snapshots for a dependable demonstration, visibly labelled. Add an external provider only after verifying access, terms, rate limits and availability. Never commit API keys.
3. **Paper-trading starting balance:** Make it configurable. A proposed demo default is ₹10,00,000, matching the earlier simulator example; confirm with the student.
4. **Registration fields:** Keep to name, email and password unless a feature genuinely requires an additional field. Knowledge level can be optional profile data.
5. **Analyzer:** Recommended: allocation percentages and qualitative risk/liquidity/growth trade-offs only; no numeric future-return forecast in V1. Required inputs can be amount, goal, time horizon and risk preference. Maximum drawdown, liquidity, knowledge and asset preferences may be deferred or optional.
6. **Lesson content:** Start with a few complete lessons rather than many empty courses. Have the student/team review educational claims and cite content sources in project documentation.

## 10. Agreed planning sequence

Continue the product-planning work in this order:

1. Finalize V1 requirements and acceptance criteria.
2. Define database entities and constraints.
3. Produce the ER diagram.
4. Define backend/system architecture.
5. Specify API contracts.
6. Plan frontend pages and core UX.
7. Divide delivery across five teammates and refine the four-week roadmap.
8. Implement the end-to-end MVP, keeping the repository updated.

The immediate next deliverable after confirming V1 requirements is the **database model**. It should support accounts, learning content/progress, assets and timestamped snapshots, portfolios, simulated trades, journal entries, and only include goals if they are retained in the V1 flow. Avoid creating tables for every long-term vision feature.

## 11. Suggested four-week delivery frame

- **Week 1:** Freeze scope, sketch core screens, agree contracts, create schema and seed content/data.
- **Week 2:** Accounts, navigation, lessons, asset browse/detail and persistence.
- **Week 3:** Scenario comparison, virtual trades, holdings and journal.
- **Week 4:** Integrate, refine usability, verify calculations/data labels, prepare demo and explain limitations.

If schedule slips, preserve the complete user journey with seeded data and rule-based scenarios. Defer AI, wide live-data coverage, advanced indicators and analytics before compromising data isolation or transaction correctness.

## 12. How to collaborate with the student

- Continue as the primary technical/product co-planner for this project.
- Explain the reason behind scope decisions and respectfully challenge additions that do not fit the one-month college MVP.
- Work one planning step at a time; do not jump into a large codebase before requirements and data boundaries are clear.
- Ask only for choices that materially affect the design. Offer a sensible recommendation and explain the trade-off.
- Keep the student informed about what changed, why, and how to verify it.
- When implementing, make small, reviewable changes, preserve a runnable end-to-end application, and update the exact `prabhuvibes/FinSphere` repository.
- Do not claim a feature is implemented unless it exists and has been checked.


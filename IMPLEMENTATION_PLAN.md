# Dev Dashboard — Implementation Plan

## General Philosophy

Implement incrementally.

Do NOT build the entire application at once.

Workflow:

implement  
→ test  
→ stabilize  
→ continue

---

## Phase 1 — Bootstrap

- Initialize Django project
- Create apps
- Configure settings/env/db/static/templates
- Setup base layout
- Configure SQLite/Postgres switching

---

## Phase 2 — Accounts

- Profile model
- Auto-create signal
- Signup/login/logout
- Profile page

Validation:
- auth fully works

---

## Phase 3 — Goals

- Goal model
- Slug logic
- Admin
- Services
- Selectors
- CRUD pages

Validation:
- full goal lifecycle works

---

## Phase 4 — Habits

- Habit model
- HabitEntry model
- Unique daily constraint
- Services/selectors
- CRUD/logging pages

Validation:
- habits log correctly

---

## Phase 5 — Reviews

- DailyReview model
- Unique daily review constraint
- Services/selectors
- Review pages/history

Validation:
- reviews function correctly

---

## Phase 6 — Project Snapshots

- ProjectSnapshot model
- Slug logic
- Services/selectors
- CRUD pages

Validation:
- project monitoring works

---

## Phase 7 — Dashboard

- Dashboard selectors
- Aggregate homepage
- Widget partials

Validation:
- homepage useful and aggregated

---

## Phase 8 — HTMX Enhancement

Add HTMX for:

- habit logging
- review updates
- inline updates
- widget refresh

Validation:
- dynamic UX works well

---

## Phase 9 — Testing

Add tests for:

- goal lifecycle
- habits
- reviews
- projects
- dashboard aggregation

---

## Phase 10 — Polish

- README
- screenshots
- documentation
- cleanup

---

## Future Phase

Optional:

- weekly summary
- streak analytics
- charts
- integrations
- ecosystem linking

NOT MVP.

---

## Commit Discipline

Recommended commits:

- feat: bootstrap project
- feat: implement accounts
- feat: implement goals
- feat: implement habits
- feat: implement reviews
- feat: implement projects overview
- feat: implement dashboard
- feat: enhance HTMX UX
- test: add workflow tests
- docs: finalize README
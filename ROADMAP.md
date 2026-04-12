# Dev Dashboard Roadmap

This file tracks released milestones and the next planned capability layers.

## Released

### v0.1.0

Single-user MVP completed:

- authentication and profile
- goals
- habits and habit entries
- daily reviews
- project snapshots
- dashboard homepage
- selective HTMX improvements
- workflow-oriented tests
- documentation and screenshots

### v0.1.1

Dashboard UX Improvements completed:

- dashboard became a stronger daily entry point
- homepage now highlights what needs attention today
- quick actions were improved from the homepage
- mobile-first dashboard flow was polished

### v0.1.2

Habit Progress Layer completed:

- current streak
- last completed date
- weekly completion count
- compact habit progress visibility in key habit-related views

### v0.2.0

Weekly Summary System completed:

- cross-domain weekly summary page
- weekly aggregation for habits, reviews, goals, and projects
- reusable week range helper for current or arbitrary weeks
- read-only reflection layer built on existing data
- mobile-friendly weekly summary view

### v0.2.1

Weekly Summary UX Refinement completed:

- visible previous/current/next week navigation
- clear current-week awareness when viewing other weeks
- explicit "Back to current week" action
- clearer weekly header and at-a-glance summary
- better empty states across weekly blocks
- stronger quick links to related pages
- improved mobile readability for the weekly page

### v0.3.0

Weekly Reflection Write Layer completed:

- added `WeeklyReflection` as a structured weekly write model
- enforced one reflection per week with Monday-normalized `week_start_date`
- added review-domain services and selectors for weekly reflection flows
- integrated reflection display and create/edit entry points into weekly summary
- kept weekly summary as the cross-domain read layer and reflection as a review-domain write layer
- completed the execution -> aggregation -> reflection loop

## Planned

### Guiding Structure

- `v0.3.x` -> refine weekly reflection
- `v0.4.x` -> add system visibility signals
- `v0.5.x` -> introduce domain relationships
- `v0.6.x` -> engineering hardening and portfolio strength

---

## v0.3.x — Reflection Refinement

Goal:
Strengthen weekly reflection without creating a new product layer.

### v0.3.1 — Reflection UX Improvements

- cleaner reflection block on weekly page
- better create/edit flow
- clearer empty state when reflection is missing
- mobile polish for weekly reflection form

### v0.3.2 — Reflection Continuity

- show a compact snippet from last week's reflection
- show previous `next_week_focus` when writing a new reflection
- add a small continuity hint between weeks

Note:
This should act as a continuity aid, not a memory system.

---

## v0.4.x — Visibility & Signals Layer

Goal:
Improve system awareness without turning the product into an analytics dashboard.

### v0.4.0 — System Signals

#### Goals

- goals touched this week
- goals not updated recently

Definition:
- touched = created or updated this week

#### Projects

- stale projects based on `last_updated`
- clearer `last_updated` visibility

#### Habits

- missed yesterday
- low activity this week

#### Weekly

- simple completeness signal:
  - habits touched
  - reviews count
  - reflection present

Constraints:

- no charts
- no scoring engine
- no complex metrics
- no trend dashboards

Note:
If comparison vs last week is added, it must remain a very light textual hint.

---

## v0.5.x — Cross-domain Relationships

Goal:
Make the system more connected without breaking simplicity.

### v0.5.0 — Goal ↔ Project Linking

- a goal may optionally link to a project
- project detail shows related goals
- goal detail may show linked project

### v0.5.1 — Navigation Improvements

- stronger navigation from weekly summary to related goals/projects
- stronger navigation from goals to projects
- stronger navigation from dashboard to linked entities

### v0.5.x — Optional Relationship Expansion

Maybe later:

- Habit ↔ Goal linking, only if it remains structurally simple

Constraints:

- no automatic rollups
- no dependency graph
- no derived scoring logic

---

## v0.6.x — Engineering & Portfolio Layer

Goal:
Strengthen the project as an engineering artifact.

### v0.6.0 — Observability

- basic structured logging
- optional Sentry integration
- better error visibility in production

### v0.6.1 — Performance Pass

- `select_related` / `prefetch_related` audit
- selector optimization
- remove obvious query duplication

### v0.6.2 — Documentation / API Surface

- improve README and architecture docs
- document routes and flows
- optional API/schema work only if API becomes a real product need

---

## Not Planned Yet

- AI summaries
- integrations
- reminders
- notifications
- calendar sync
- advanced analytics

## Update Policy

When planning future work:

- append new releases here
- keep versioning disciplined
- describe each release by goal, scope, and notes
- avoid mixing small polish releases with major capability jumps

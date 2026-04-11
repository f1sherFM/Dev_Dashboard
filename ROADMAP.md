# Dev Dashboard Roadmap

This file tracks planned product iterations after `v0.1.0`.

Rule:

- all upcoming release planning updates should be added here
- `v0.1.x` releases refine and strengthen the existing MVP loop
- `v0.2.x` and above add new capability layers

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

No next release is locked yet.

## Update Policy

When planning future work:

- append new releases here
- keep versioning disciplined
- describe each release by goal, scope, and notes
- avoid mixing small polish releases with major capability jumps

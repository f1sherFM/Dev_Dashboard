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

## Planned

### v0.3.0

Weekly Reflection Write Layer

Goal:

Introduce a structured weekly reflection workflow on top of the existing weekly summary.

This is the first step that adds a new write-layer to the weekly loop.

Product Direction:

Dev Dashboard already supports:

- daily execution (habits, daily review)
- weekly aggregation (weekly summary)

v0.3.0 adds:

- intentional weekly reflection
- structured thinking about progress, problems, and next steps

This should feel like a natural extension of the existing weekly summary,
not a separate journaling system.

Core Feature:

Add a weekly reflection input tied to a specific week.

Each week can have at most one reflection.

Domain Model:

Introduce a new model:

`WeeklyReflection`

Fields (MVP scope):

- week_start_date (DateField, unique)
- wins (TextField)
- problems (TextField)
- lessons (TextField)
- next_week_focus (TextField)
- created_at
- updated_at

Rules:

- one reflection per week (unique on week_start_date)
- week is defined by Monday–Sunday boundaries
- reflection is optional (user may skip a week)

Week Normalization Rule:

Any incoming date used for weekly reflection must always be normalized
to that week’s Monday.

This means:

- the service accepts a week-related date
- the service converts it to the Monday of that week
- the stored `week_start_date` is always the normalized Monday

This prevents duplicate weekly reflections for the same calendar week.

Ownership of Responsibility:

Keep boundaries strict:

- `WeeklyReflection` belongs to the `reviews` app
- create/update/get-by-week logic lives in:
  - `reviews/services.py`
  - `reviews/selectors.py`

- cross-domain weekly aggregation remains in:
  - `dashboard/selectors.py`

- the dashboard weekly page reads already prepared data
  and should not own weekly reflection business rules

This keeps weekly reflection as a review-domain write flow,
while preserving weekly summary as a dashboard-domain read flow.

Integration with Weekly Summary:

Weekly reflection must stay inside the weekly summary flow.

Rules:

- do NOT build a standalone weekly reflection subsystem
- weekly summary page shows the reflection block
- if reflection does not exist:
  - show "Write weekly reflection"
- if reflection exists:
  - show "Edit weekly reflection"

A separate create/edit route may exist technically,
but the UX anchor must remain inside the weekly summary page.

Reflection should appear as the final section of the weekly page.

UI Scope:

Add:

- reflection section at the bottom of weekly summary page
- simple form
- clear CTA:
  - "Write weekly reflection"
  - "Edit weekly reflection"

Keep UI:

- minimal
- distraction-free
- mobile-friendly

Do NOT add:

- rich text editor
- markdown editor
- attachments
- complex formatting tools

Architecture Rules:

- all write logic goes through `reviews/services.py`
- all reflection read logic goes through `reviews/selectors.py`
- cross-domain weekly summary logic stays in `dashboard/selectors.py`
- views remain thin
- templates contain no business logic
- do not duplicate weekly aggregation logic

Out of Scope:

Do NOT include:

- analytics on reflections
- AI summaries
- sentiment analysis
- tagging system
- attachments/files
- export/sharing
- reminders/notifications

Testing:

Add tests for:

- one reflection per week constraint
- normalization of incoming dates to Monday
- create/update flow via service
- correct association with week_start_date
- rendering on weekly summary page
- edit vs create behavior

Why this is v0.3.0:

This release introduces:

- a new domain model
- a new write workflow
- a new user behavior pattern (weekly reflection)

This is a clear expansion of product capability, not just refinement.

Expected Outcome:

After v0.3.0, Dev Dashboard supports:

- daily execution loop
- weekly summary (read)
- weekly reflection (write)

This completes a full:

execution → aggregation → reflection loop

## Update Policy

When planning future work:

- append new releases here
- keep versioning disciplined
- describe each release by goal, scope, and notes
- avoid mixing small polish releases with major capability jumps

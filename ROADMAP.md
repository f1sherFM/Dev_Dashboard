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

## Planned

### v0.1.1 — Dashboard UX Improvements

Goal:

Make the dashboard the best daily entry point.

Scope:

- improve homepage daily flow
- highlight what needs attention today
- reduce friction for core actions from the dashboard
- improve mobile-first usability for repeated daily use

Notes:

- keep dashboard as a read/interaction layer, not a new domain
- do not add analytics, charts, or notifications here

### v0.1.2 — Habit Progress Layer

Goal:

Add lightweight progress visibility to habits without turning the app into an analytics system.

Scope:

- current streak
- last completed date
- recent completion summary
- practical progress indicators on habit pages and related views

Notes:

- keep the model simple
- no heavy charts
- no advanced analytics engine

### v0.2.0 — Weekly Summary System

Goal:

Add a weekly reflection and summary layer on top of the existing daily system.

Scope:

- weekly summary page
- weekly aggregation for habits
- weekly review coverage
- goal/project weekly visibility
- structured weekly reflection workflow

Notes:

- build on existing services/selectors architecture
- keep it useful and calm
- do not overexpand into reporting for reporting's sake

## Update Policy

When planning future work:

- append new releases here
- keep versioning disciplined
- describe each release by goal, scope, and notes
- avoid mixing small polish releases with major capability jumps

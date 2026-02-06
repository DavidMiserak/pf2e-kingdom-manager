# PF2E Kingdom Manager Documentation

Welcome to the PF2E Kingdom Manager documentation. This guide will help you set up, use, and understand the kingdom turn tracking system for Pathfinder 2E Kingmaker.

## Quick Links

**For Players & GMs**:

- **[Getting Started](GETTING_STARTED.md)** — 5-minute setup and first turn
- **[User Guide](USER_GUIDE.md)** — Complete guide to using the app
- **[Kingdom Turns](KINGDOM_TURNS.md)** — Detailed turn mechanics and phases
- **[Rules Reference](RULES_REFERENCE.md)** — PF2E Kingmaker rules summary

**For Developers**:

- **[Project README](../README.md)** — Development setup and architecture
- **[Product Requirements](PRD.md)** — Full system design and scope

---

## What Is This?

The **PF2E Kingdom Manager** is a web application that helps GMs and players track Pathfinder 2E kingdom turns offline. Instead of enforcing a rigid phase structure, it allows free-form activity logging and manual state management—giving your table flexibility to adapt to your playstyle.

### Core Features

✅ **Kingdom State Tracking**: Manage ability scores, resources, unrest, ruin, and commodities
✅ **Turn Snapshots**: Create turns as checkpoints; log unlimited activities per turn
✅ **Activity Logging**: Free-form records of what your kingdom did each month
✅ **Multi-User**: GM has full control; players can log activities and view kingdom state
✅ **No Dice Automation**: Roll dice at your table; the tool tracks results
✅ **Flexible Phases**: Log activities in any order; no enforced turn structure

---

## Where to Start

### If You're New to This App

1. **[Getting Started](GETTING_STARTED.md)** (5 minutes)
    - Create your kingdom
    - Invite players
    - Log your first turn

2. **[User Guide](USER_GUIDE.md)** (deep dive)
    - Learn all features
    - Understand permissions
    - Master workflows

### If You Know the App but Need Kingmaker Rules

- **[Rules Reference](RULES_REFERENCE.md)** — Quick lookup for mechanics
- **[Kingdom Turns](KINGDOM_TURNS.md)** — Complete step-by-step turn guide

### If You're Running a Campaign

Keep these handy during sessions:

- **[Kingdom Turns](KINGDOM_TURNS.md)** — Checklist to run each turn
- **[Rules Reference](RULES_REFERENCE.md)** — DCs, modifiers, and penalties

---

## Documentation Overview

### [GETTING_STARTED.md](GETTING_STARTED.md)

**For**: First-time users
**Length**: ~10 minutes
**Covers**:

- Account setup and login
- Creating your first kingdom
- Logging your first turn
- Common workflows

**Start here if**: You just deployed the app and want to get running quickly.

---

### [USER_GUIDE.md](USER_GUIDE.md)

**For**: GMs and players using the app regularly
**Length**: ~30 minutes
**Covers**:

- Core concepts (Kingdoms, Turns, Activities)
- Full feature walkthrough (Dashboard, Leadership, Skills, Members)
- Permission model
- Tips and tricks
- Troubleshooting

**Start here if**: You've created a kingdom and want to master all features.

---

### [KINGDOM_TURNS.md](KINGDOM_TURNS.md)

**For**: GMs running turns at the table
**Length**: ~20 minutes (reference)
**Covers**:

- Five turn phases in detail
- Step-by-step mechanics
- Unrest and Ruin escalation
- Turn checklist
- Common scenarios

**Start here if**: You're about to run a kingdom turn and need the mechanics.

---

### [RULES_REFERENCE.md](RULES_REFERENCE.md)

**For**: Quick lookup of PF2E Kingmaker rules
**Length**: ~10 minutes (reference)
**Covers**:

- Kingdom creation
- Ability scores
- Skills and modifiers
- Resource management
- Settlements and leveling
- Leadership roles

**Start here if**: You need to look up a mechanic quickly (no turn context needed).

---

### [PRD.md](PRD.md)

**For**: Understanding what this app is designed to do
**Length**: ~30 minutes (reference)
**Covers**:

- Product vision and scope
- Phases and roadmap
- Architecture overview
- Feature specifications by phase

**Start here if**: You're a developer or want to understand the design.

---

## Common Questions

**Q: Does the app enforce turn phases?**
A: No. You can log activities in any order and manually adjust state. This gives you flexibility to adapt to your table's playstyle.

**Q: Do I need to roll dice in the app?**
A: No. You roll dice at your table as normal. The tool just tracks results and calculates modifiers for reference.

**Q: Can players edit kingdom state?**
A: No. Only the GM can modify kingdom state (ability scores, RP, commodities, etc.). Players can only log activities they performed.

**Q: What if I made a mistake?**
A: You can edit activities and turn state. If a turn is locked, ask the GM to unlock it.

**Q: Where's the feature for territories/hexes/settlements?**
A: Those are in Phase 3 of development. For now, manage hexes and settlements with a separate map or spreadsheet.

---

## Roadmap

- **Phase 1** ✅ Kingdom core state, leadership, skills
- **Phase 2** ✅ Turns and activity logging
- **Phase 3** 🔄 Territory management (hexes, settlements, structures, work sites)
- **Phase 4** 🔄 Quality of life (skill check calculator, turn summaries, activity history)

---

## Getting Help

**Within the app**: Hover over field labels or icons for tooltips.

**In documentation**: Check the relevant guide above.

**With rules**: See [RULES_REFERENCE.md](RULES_REFERENCE.md) or the [official PF2E Kingmaker rules](https://2e.aonprd.com/Rules.aspx?ID=1739).

**For bugs or feature requests**: Contact the GM or create an issue on the project repository.

---

## Tips for Success

1. **Run turns regularly** — Monthly check-ins keep players invested in the kingdom
2. **Take notes** — Use the activity description field extensively
3. **Track modifiers** — Note bonuses and penalties in activity descriptions for context
4. **Plan ahead** — Talk with players between sessions about next turn's activities
5. **Keep it free-form** — Don't stress about strict phase order; adapt to your table's pace

---

## Useful Links

- **[Pathfinder 2E Kingmaker Rules](https://2e.aonprd.com/Rules.aspx?ID=1739)** — Official rules overview
- **[Pathfinder 2E Kingmaker Turns](https://2e.aonprd.com/Rules.aspx?ID=1794)** — Official turn mechanics
- **[Project Repository](../README.md)** — Source code and development info

---

Good luck with your kingdom! 👑

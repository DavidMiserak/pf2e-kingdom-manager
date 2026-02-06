# PF2E Kingdom Manager - User Guide

The PF2E Kingdom Manager is a web application that helps GMs and players track Pathfinder 2E kingdom turns offline. Instead of enforcing a rigid phase structure, it allows free-form activity logging and manual state management—giving you flexibility to adapt to your table's playstyle.

## Core Concepts

### Kingdoms

Your kingdom is the central entity tracking:

- 4 Ability Scores (Culture, Economy, Loyalty, Stability)
- Kingdom Level (1-20)
- Experience Points (XP)
- Resource Points (RP)
- Unrest and Ruin counters
- 5 Commodity stockpiles
- Members and their permissions

### Kingdom Turns

Each turn represents one month in-game. Turns are snapshots of kingdom state and contain:

- Turn number (auto-incremented)
- Unrest, Ruin, and commodity values at turn start
- Associated activities and outcome logging

### Activities

Activities are free-form log entries describing what the kingdom did during a turn:

- Who performed it (which leader or group)
- What was attempted (leadership check, construction, etc.)
- Degree of success (critical success, success, failure, critical failure)
- Any resource or commodity changes
- Notes on outcomes

## Getting Started

### 1. Create a Kingdom

1. Click **Create Kingdom** on the home page
2. Fill in the kingdom details:
    - **Name**: Your kingdom's name
    - **Charter**: Select your charter type (Conquest, Expansion, Exploration, Grant, or Open)
    - **Heartland**: Select your heartland terrain type
    - **Government**: Choose your government type
    - **Starting Capital Settlement**: Name your first settlement
3. Assign leadership roles (8 positions: Ruler, Counselor, General, Emissary, Magister, Treasurer, Viceroy, Warden)
4. Set initial ability scores (typically 10, modified by charter and heartland boosts/flaws)
5. Click **Create**

### 2. Invite Members

1. Go to your kingdom's **Members** page
2. Copy the kingdom share link and distribute to your players
3. Players can view all kingdom state
4. Only the GM can modify kingdom state directly; players log activities

### 3. Log Your First Turn

1. Navigate to your kingdom **Dashboard**
2. Click **Create Turn** to start a new turn
3. Set the turn's starting state:
    - Unrest level
    - Ruin counters (Corruption, Crime, Decay, Strife)
    - Commodity stockpiles (Food, Lumber, Ore, Stone, Luxuries)
    - Resource Points rolled
4. Click **Create Turn**

### 4. Log Activities

While a turn is active:

1. Click **Log Activity** on the turn detail page
2. Record the activity:
    - **Activity Type**: What was attempted (e.g., "Claim Hex", "Build Structure", "Diplomacy Check")
    - **Description**: Free-form notes on what happened
    - **Degree of Success**: Critical Success, Success, Failure, or Critical Failure
    - **RP/Commodities Spent**: If the activity consumed resources
3. Click **Create Activity**

**Note**: There's no phase enforcement. Log activities in any order and at any time during the turn.

### 5. Complete a Turn

Once all activities are logged:

1. On the turn detail page, click **Complete Turn**
2. Record ending state:
    - Final Unrest and Ruin values
    - Final commodity stockpiles
    - Any kingdom XP earned
3. The system calculates: `Total RP spent + Unspent RP (converted to XP at 1:1 ratio)`
4. Click **Mark Complete**

The turn is now locked; you can view history but not edit activities. Start a new turn when ready.

## Interpreting the Dashboard

Your kingdom **Dashboard** shows at a glance:

- **Core Stats**: Current ability scores, level, XP progress
- **Leadership Roles**: Who holds each position; any vacant roles
- **Resources**: Current RP, commodities in stockpile
- **Status**: Current Unrest and Ruin counters
- **Recent Activity**: Latest 10 activities logged

## Skill Checks

The system does **not** automate dice rolls. Instead:

1. At your table, roll `d20 + kingdom skill modifier`
2. Determine the degree of success (critical success, success, failure, critical failure) against Control DC
3. Log the activity with the outcome
4. Note any modifiers applied (leadership role bonuses, Unrest penalties, etc.) in activity notes

**Kingdom Skill Modifier Formula**:

```matlab
Modifier = Key Ability Score Modifier + Proficiency Bonus + Bonuses - Penalties
```

Example: A Diplomacy check using Culture might be:

```matlab
+2 (Culture modifier) + 1 (Trained) + 0 (other) - 1 (Unrest) = +2 total
```

## Managing Resources

### Resource Points (RP)

1. Roll `kingdom level + 4d6` each turn during Upkeep
2. Log activities that spend RP (construction, diplomacy, etc.)
3. At turn end, sum spent RP
4. Unspent RP converts to XP at 1:1 ratio (cap 120/turn)

### Commodities

Track stockpiles of Food, Lumber, Ore, Stone, and Luxuries:

1. Update stockpile values when gathering or spending
2. Pay Consumption with Food (see Rules Reference)
3. Use commodities for construction and trade activities

## Tracking Penalties

### Unrest

- Record current Unrest on each turn
- Apply penalties in skill checks (`–1` at 1+, `–2` at 5+, `–3` at 10+, `–4` at 15+)
- Note the source (failed check, event, etc.) in activity logs

### Ruin

- Track Corruption, Crime, Decay, and Strife separately
- When any counter exceeds 10, the threshold resets and penalty accumulates
- Apply penalties to checks using the opposed ability score
- Note accumulated penalties in activity descriptions

## Leveling Up

When your kingdom earns 1,000 XP:

1. Click **Level Up** on the Dashboard
2. Update the kingdom's level (+1)
3. Add new feats (every 2 levels)
4. Increase skill proficiencies as needed (every 2 levels)
5. Grant ability boosts (every 5 levels)
6. Note improved Control DC in rules reference

## Viewing History

1. On the **Dashboard**, view recent activities
2. Click a turn to see all activities logged that turn
3. Activities show who created them, when, degree of success, and resources spent
4. Edit or delete activities if the GM allows corrections

## Permissions

| Action                | GM  | Player |
| --------------------- | --- | ------ |
| View kingdom state    | ✓   | ✓      |
| Modify kingdom state  | ✓   | ✗      |
| Create activities     | ✓   | ✓      |
| Edit own activities   | ✓   | ✓      |
| Delete own activities | ✓   | ✓      |
| Create/complete turns | ✓   | ✗      |
| View all members      | ✓   | ✓      |

## Tips & Tricks

### Free-Form Logging

You don't have to follow strict Upkeep → Commerce → Activity → Event order. Log activities as they happen and adjust turn state manually at any time.

### No Dice Automation

Roll dice at your table as normal and manually record outcomes. The system calculates modifiers for reference but doesn't automate rolls.

### Activity Notes

Use the **Description** field extensively. Include:

- DC and modifier details
- Why the check was attempted
- Narrative flavor
- Any special effects or outcomes

### Turn Snapshots

Turns act as checkpoints. If a turn is "Complete," you can review the full state at that point in time. Start a new turn to continue playing.

### Leadership Tracking

Keep leadership assignments current on the **Leadership** page. Vacant roles impose penalties on kingdom checks—remember to adjust modifiers when roles change mid-turn.

## Troubleshooting

**Can't create a kingdom?**

- Ensure you're logged in (check top-right)
- Your email must be verified
- Contact the GM if you don't see the form

**Activities showing wrong degree of success?**

- Degrees of success are recorded manually; check the activity log
- You can edit activities to correct errors

**Confused about modifiers?**

- See the Rules Reference for full skill definitions
- Note Unrest and Ruin penalties when logging checks
- Use activity descriptions to explain the math

## Next Steps

- Read the **Rules Reference** for complete PF2E Kingmaker rules
- Explore the **Leadership**, **Skills**, and **Members** pages for additional kingdom management
- See the **Territory** section (when available) for hex and settlement management

# Kingdom Turns - Detailed Guide

This document provides step-by-step instructions for conducting a kingdom turn in Pathfinder 2E Kingmaker.

## Overview

Each kingdom turn represents one month of in-game time and consists of **five sequential phases**. While the PF2E Kingdom Manager does not enforce phase order, understanding these phases helps organize your activities and ensure nothing is forgotten.

## Phase 1: Upkeep Phase

The Upkeep Phase handles administrative tasks and resource collection.

### Step 1: Assign Leadership Roles

- The Ruler or Councilor designates (or redesignates) the eight leadership roles
- Each role must be filled by a PC or NPC
- Vacant roles impose penalties on kingdom checks tied to that position
- Roles: Ruler, Counselor, General, Emissary, Magister, Treasurer, Viceroy, Warden

**In the tool**: Update leadership on the **Leadership** page; roles persist across turns unless changed.

### Step 2: Adjust Unrest

Unrest increases at the start of this phase based on conditions:

- **+1** for each overcrowded settlement
- **+1** if the kingdom is at war

**Overcrowded Settlement**: A settlement exceeds its population capacity (determined by settlement size and structures).

**In the tool**: Manually increase Unrest when creating a new turn or updating turn state.

### Step 3: Roll Resource Dice

Roll Resource Dice using this formula:

```matlab
Resource Dice = Kingdom Level + 4 + Bonus Dice - Penalty Dice
```

**Example**: A 5th-level kingdom rolls `5 + 4 = 9d6` for resources (assuming no bonuses or penalties).

**Bonuses** come from:

- Specific kingdom feats
- Favorable trade agreements
- Successful Commerce phase activities

**Penalties** come from:

- Anarchy (–4 dice)
- Low Stability or Economy (at GM's discretion)
- Other events or conditions

**Result**: Total the dice. This is your kingdom's **Resource Points (RP)** for the turn.

**In the tool**: Record the rolled total as "Resource Points rolled" when creating a turn.

### Step 4: Pay Consumption

Your kingdom must pay **Consumption** using Food commodities.

#### Calculate Consumption

```matlab
Kingdom Consumption = Settlement Consumption + Army Consumption - Farmland Hexes + Modifiers
```

**Settlement Consumption**: Each settlement consumes based on its population.

- **Village**: 1 Consumption
- **Town**: 4 Consumption
- **City**: 9 Consumption
- **Metropolis**: 10+ Consumption

**Army Consumption**: During wartime, armies consume Food commodities (see your specific army rules).

**Farmland Hexes**: Subtract 1 Consumption per farmland hex claimed by your settlements' influence radius. This represents grain production.

**Modifiers**: Some structures reduce consumption (e.g., Aqueducts, Granaries).

#### Pay or Suffer

You must have enough Food commodities to cover Consumption.

##### Option A: Pay in Full

- Spend Food commodities equal to Consumption
- No penalties

##### Option B: Tap Treasury

- Pay 5 RP per 1 Consumption unpaid
- No Unrest increase

##### Option C: Generate Unrest

- Don't pay, or can't afford RP payout
- Gain `1d4 Unrest` for each Consumption unpaid

**In the tool**: Record consumption in activity notes; update Food commodities and/or RP accordingly.

---

## Phase 2: Commerce Phase

The Commerce Phase generates income and manages trade.

### Step 1: Collect Taxes

The Treasurer or Ruler conducts an **Economy check** to collect taxes.

**Check**: Economy-based check (Modifier = Economy ability modifier + Proficiency + bonuses - penalties)

**DC**: Control DC (base 14, scales with kingdom level and situation)

**Success**: Gain `2d6 + Treasurer's level` RP (or double on critical success).

**Failure**: Reduce Unrest by 1 (failure nets a small advantage to prevent economic collapse).

**Alternative**: Instead of a check, attempt a **flat DC 11 check** to reduce Unrest by 1 (no RP).

**In the tool**: Log a "Collect Taxes" activity with the degree of success and RP gained.

### Step 2: Approve Expenses

The Treasurer approves spending on:

- **Improve Lifestyle**: Spend RP to improve settlement conditions and reduce Unrest
- **Tap Treasury**: Spend RP to cover unpaid Consumption (already covered in Upkeep)

**In the tool**: Log activities related to lifestyle improvements or treasury management.

### Step 3: Trade Commodities

Convert commodities to Resource Points as needed:

- **Trade Commodity**: Spend specific commodities (Lumber, Ore, Stone, Luxuries) to gain RP
- Each commodity has a standard trade rate (varies by commodity type and season)

**In the tool**: Record commodity trades in activity notes; update RP and commodity stockpiles.

### Step 4: Manage Trade Agreements

- Establish new trade agreements with neighboring settlements or regions
- Fulfill existing trade agreement requirements
- Trade agreements may grant RP, commodities, or other benefits

**In the tool**: Log trade agreement activities; note any ongoing benefits or penalties.

---

## Phase 3: Activity Phase

The Activity Phase is where the kingdom actively pursues growth and development. Three types of activities are available:

### Leadership Activities

The Ruler and PCs with leadership roles can attempt activities tied to their position:

- **Arts** (Counselor + Culture): Establish a new art tradition, construct a theater, etc.
- **Folklore** (Counselor + Culture): Record history, preserve heritage
- **Magic** (Magister + Culture): Research magical techniques, protect against magical threats
- **Industry** (Treasurer + Economy): Build a workshop, establish a trade route
- **Trade** (Emissary + Economy): Negotiate trade agreements, establish commerce
- **Scholarship** (Magister + Economy): Research technologies, advance knowledge
- **Agriculture** (Viceroy + Loyalty): Improve farmland, increase food production
- **Politics** (Counselor + Loyalty): Improve relations with local factions
- **Wilderness** (Warden + Loyalty): Tame wild lands, establish hunting grounds
- **Defense** (General + Stability): Strengthen fortifications, train militia
- **Engineering** (Treasurer + Stability): Construct infrastructure, build bridges
- **Intrigue** (Magister + Stability): Conduct espionage, gather intelligence
- **Warfare** (General + Stability): Engage in military campaigns, battle enemies

**Limits**:

- Up to **2-3 Leadership Activities per PC** (depending on capital structures)
- Requires the appropriate leader to be assigned and present

**Check DC**: Control DC (base 14, scales with kingdom level)

**Results**:

- **Critical Success**: Full activity effect + bonus (advance two steps, double resources, etc.)
- **Success**: Full activity effect
- **Failure**: Activity fails; may incur penalties or Unrest
- **Critical Failure**: Activity fails with additional consequences

**Resource Cost**: Most activities cost RP and/or commodities.

**In the tool**: Log each leadership activity with the leader's name, activity type, degree of success, and resources spent.

### Region Activities

The kingdom can collectively perform up to **3 Region Activities**:

- **Claim Hex**: Expand territory into adjacent unclaimed hexes (costs 2 RP)
- **Clear Hex**: Remove terrain obstacles or hazards from a hex (costs 3 RP, requires success)
- **Establish Work Site**: Create a farm, mine, or lumber camp on a hex (costs 2 RP + commodities)
- **Establish Settlement**: Settle a new village, town, or city (costs 50+ RP + commodities, requires success)

**Limits**:

- Total of 3 Region Activities per turn
- Some activities have prerequisites (e.g., must have adequate RP, adjacent hexes)

**Favored Land Benefit**: The kingdom can perform 2 activities simultaneously in heartland terrain at **–2 penalty** to both.

**In the tool**: Log region activities; note hex locations and results.

### Civic Activities

One activity per settlement:

- **Build Structure**: Construct a building in a settlement's urban grid (costs RP + commodities)
- **Demolish Building**: Remove a structure (frees up urban grid space)
- **Manage Settlement**: Improve or adjust settlement operations (various costs and effects)

**Limits**:

- Only 1 per settlement per turn
- Limited by available urban grid space

**In the tool**: Log civic activities; note which settlement and what structure.

---

## Phase 4: Event Phase

The Event Phase wraps up the turn with randomized events and advancement.

### Step 1: Check for Random Event

Attempt a **flat DC 16 check**:

- **Success**: A random event occurs
- **Failure**: No event this turn, but DC decreases by 5 for next turn

**Cumulative Effect**: If you avoid events for multiple turns, they become more likely.

**In the tool**: Manually determine and log whether an event occurs this turn.

### Step 2: Event Resolution

If an event occurred, resolve it:

- Roll on the event table (see detailed event rules in the full rulebook)
- Apply consequences (Unrest, commodity loss, RP cost, etc.)
- Narrate the outcome

**In the tool**: Log the event as an activity; note any consequences.

### Step 3: Award Kingdom XP

Kingdom XP is awarded from two sources:

**Random Events**: +30 XP if an event occurred this turn

**Unspent RP**: Convert remaining RP to XP at a **1:1 ratio**, with a cap of **120 XP per turn**

**Example**:

- Kingdom starts with 50 RP
- Spends 25 RP on activities
- 25 RP remaining → Convert to 25 XP (below the 120 cap)
- Event occurred → +30 XP
- Total XP this turn: 55 XP

**In the tool**: Record RP spent, remaining RP, event XP, and total XP awarded when completing a turn.

### Step 4: Increase Kingdom Level

When your kingdom's total XP exceeds **1,000 XP**, it levels up:

1. Subtract 1,000 from total XP (carry over the remainder)
2. Increase kingdom level by 1 (max level = party level)
3. Update Control DC
4. Award new benefits:
    - Feats: Every 2 levels, gain a kingdom feat
    - Skills: Every 2 levels, increase a skill's proficiency (up to Legendary)
    - Ability Boosts: Every 5 levels, gain an ability boost to any ability score

**In the tool**: Click **Level Up** on the Dashboard; update level, feats, skill proficiencies, and abilities.

---

## Unrest and Ruin Consequences

### Unrest Escalation

Unrest accumulates during a turn. At thresholds, the kingdom suffers penalties:

| Unrest | Effect                                                                            |
| ------ | --------------------------------------------------------------------------------- |
| 1–4    | –1 status penalty to kingdom checks                                               |
| 5–9    | –2 status penalty to kingdom checks                                               |
| 10–14  | –3 status penalty to kingdom checks, lose hex (DC 11 check to prevent)            |
| 15–19  | –4 status penalty to kingdom checks, accumulate Ruin                              |
| 20+    | **Anarchy**: Only "Quell Unrest" activities allowed; all checks worsen one degree |

### Ruin Generation

When Unrest reaches 10 or higher, generate `1d10 Ruin points` distributed among Corruption, Crime, Decay, and Strife.

If a Ruin category accumulates past its threshold (initially 10), the threshold resets and an **Accumulated Penalty** applies to all checks using the opposed ability score.

---

## Quick Reference: Turn Checklist

### **Upkeep Phase**

- [ ] Assign/confirm leadership roles
- [ ] Add +1 Unrest per overcrowded settlement or if at war
- [ ] Roll Resource Dice (KL + 4 ± modifiers)
- [ ] Calculate and pay Consumption (Food commodities or 5 RP per point, or take 1d4 Unrest)

### **Commerce Phase**

- [ ] Collect Taxes (Economy check or flat DC 11 check for Unrest reduction)
- [ ] Approve Expenses (lifestyle improvements, treasury taps)
- [ ] Trade Commodities for RP as needed
- [ ] Manage Trade Agreements

### **Activity Phase**

- [ ] Log Leadership Activities (up to 2–3 per PC leader)
- [ ] Log Region Activities (up to 3 total)
- [ ] Log Civic Activities (up to 1 per settlement)

### **Event Phase**

- [ ] Check for Random Event (DC 16 flat check, –5 cumulative if avoided)
- [ ] Resolve Event if it occurs
- [ ] Award Kingdom XP (30 for event + 1:1 RP conversion, max 120)
- [ ] Level Up if XP exceeds 1,000

### **End of Turn**

- [ ] Record final Unrest and Ruin values
- [ ] Record final commodity stockpiles
- [ ] Record XP and new kingdom level (if leveled)
- [ ] Mark turn complete

---

## Common Scenarios

### Anarchy

If Unrest reaches 20+, the kingdom enters anarchy. While in anarchy:

- **Only "Quell Unrest" activities** are available
- **All checks worsen by one degree** (critical success becomes success, etc.)
- The kingdom must take multiple turns to reduce Unrest and escape anarchy

**Quell Unrest Activity**: Economy or Loyalty check (DC Control DC + 5). Success reduces Unrest by 1d4; critical success by 2d4.

### Dealing with Ruin Accumulation

Ruin counters accumulate slowly but have severe long-term effects. To reduce Ruin:

- Use "Repair Ruin" activities (check against Control DC, costs RP)
- Build specific structures that reduce Ruin (e.g., courthouse for Crime)
- Maintain ability scores above Ruin thresholds

### Wartime Turns

During military campaigns, armies consume resources and modify turn mechanics:

- **+1 Unrest** in Upkeep Phase
- **Army Activities** available in Activity Phase
- **Military Events** may occur instead of standard events
- Settlements may be threatened or damaged

---

## Tips for Running Turns

1. **Use the Checklist**: Reference the checklist above to ensure no steps are skipped
2. **Track Everything**: Write down RP spent, Unrest changes, and resources consumed each turn
3. **Free-Form Logging**: The PF2E Kingdom Manager allows you to log activities in any order; you don't need to follow strict phase order if your table prefers a different flow
4. **Narrative First**: Remember that activities should drive the story; use the mechanics to support the narrative
5. **Plan Ahead**: Talk with your players between sessions about what activities they want to pursue next turn so prep work isn't necessary

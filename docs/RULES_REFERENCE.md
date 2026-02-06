# Pathfinder 2E Kingmaker Rules Reference

This document provides a quick reference for Pathfinder 2E Kingmaker rules. For complete rules, see [the official rules](https://2e.aonprd.com/Rules.aspx?ID=1739).

## Kingdom Creation (10 Steps)

When establishing a kingdom, you'll configure:

1. **Charter** (Conquest, Expansion, Exploration, Grant, or Open) - grants ability boosts/flaws
2. **Heartland Terrain** - provides an additional ability boost
3. **Government** (Despotism, Feudalism, Oligarchy, Republic, Thaumocracy, Yeomanry) - grants skill proficiencies and effects
4. **Leadership Roles** - assign PCs and NPCs to eight positions
5. **First Village** - establish your capital settlement

## Kingdom Ability Scores

Your kingdom has four core ability scores, each starting at 10 and modified by boosts (+2) or flaws (-2):

| Ability       | Represents                             |
| ------------- | -------------------------------------- |
| **Culture**   | Arts, sciences, learning, and heritage |
| **Economy**   | Trade, production, and commerce        |
| **Loyalty**   | Citizens' trust and unity              |
| **Stability** | Infrastructure, health, and defense    |

## Kingdom Turn Phases

Each kingdom turn (one month) progresses through four phases:

### 1. Upkeep Phase

- Adjust leadership role assignments
- Modify Unrest based on settlement crowding
- Roll Resource Dice: `kingdom level + 4d6` dice
- Pay Consumption using Food commodities

### 2. Commerce Phase

- Collect Taxes
- Approve expenses
- Trade Commodities
- Manage Trade Agreements

### 3. Activity Phase

The kingdom can perform three types of activities:

- **Leadership Activities** (up to 3 per PC leader): diplomacy, construction, espionage, etc.
- **Region Activities** (up to 3 collectively): claim hexes, clear terrain, establish work sites
- **Civic Activities** (one per settlement): build structures, demolish buildings

### 4. Event Phase

- Check for random events (DC 16)
- Award kingdom XP
- Check for kingdom leveling

## Kingdom Skills

Each leadership role is tied to skills for conducting checks. Skills consist of:

```matlab
Check Result = d20 + Skill Modifier
Skill Modifier = Key Ability Score Modifier + Proficiency Bonus + Other Bonuses - Penalties
```

### Eight Kingdom Skills

| Skill       | Ability   | Leadership Role |
| ----------- | --------- | --------------- |
| Arts        | Culture   | Counselor       |
| Folklore    | Culture   | Counselor       |
| Magic       | Culture   | Magister        |
| Industry    | Economy   | Treasurer       |
| Trade       | Economy   | Emissary        |
| Scholarship | Economy   | Magister        |
| Agriculture | Loyalty   | Viceroy         |
| Politics    | Loyalty   | Counselor       |
| Wilderness  | Loyalty   | Warden          |
| Defense     | Stability | General         |
| Engineering | Stability | Treasurer       |
| Intrigue    | Stability | Magister        |
| Warfare     | Stability | General         |

## Resource Management

### Resource Points (RP)

- Rolled each turn using Resource Dice
- Spent on kingdom activities
- Unspent RP converts to kingdom XP (1:1 ratio, max 120 per turn)

### Commodities

Five types of commodities gathered, stored, and spent:

- Food
- Lumber
- Ore
- Stone
- Luxuries

### Consumption

Settlements and armies require provisions. Each point of Consumption must be paid with Food commodities. If unpaid:

- Pay 5 RP per point of Consumption, OR
- Generate 1d4 Unrest

## Persistent Penalties

### Unrest (0-20+)

Citizens' dissatisfaction. Exceeding thresholds imposes penalties:

| Unrest | Penalty                     |
| ------ | --------------------------- |
| 1+     | –1 status penalty to checks |
| 5+     | –2 penalty                  |
| 10+    | –3 penalty                  |
| 15+    | –4 penalty                  |
| 20+    | Kingdom falls into anarchy  |

### Ruin (Corruption, Crime, Decay, Strife)

Four categories of Ruin opposed to kingdom ability scores:

- **Corruption** opposes Culture
- **Crime** opposes Loyalty
- **Decay** opposes Stability
- **Strife** opposes Economy

When Ruin in a category exceeds 10 (the initial threshold), the threshold resets and a penalty accumulates. Accumulated penalties apply to all checks using that ability.

## Settlements

Settlements occupy **Urban Grids** (3×3 blocks of 2×2 lots each). Settlement size determines capabilities:

| Settlement Type | Blocks | Kingdom Level |
| --------------- | ------ | ------------- |
| Village         | 1      | 1st           |
| Town            | 4      | 3rd           |
| City            | 9      | 9th           |
| Metropolis      | 10+    | 15th          |

### Settlement Influence

Settlements provide benefits to nearby hexes based on type and size.

## Kingdom Leveling

Your kingdom level starts at 1st and caps at your party level.

Leveling requires **1,000 XP** and grants:

- Additional feats every 2 levels
- Skill increases every 2 levels
- Ability boosts every 5 levels
- Enhanced **Control DC** (base 14, scales with level)
- Expanded settlement options
- Expanded hex-claiming capability

### Control DC

Represents the difficulty of kingdom tasks. Increases with kingdom level, reflecting growing complexity as your kingdom expands.

## Fame/Infamy

Tracks kingdom reputation (max 3 points initially).

### Earning Points

- Critical successes on kingdom checks
- Building appropriate structures
- Creating masterpieces
- Noteworthy PC actions

### Spending Points

- Reroll kingdom checks
- Prevent Anarchy or Ruin penalties

## Territory Management

### Hexes

Kingdom territory expands one hex at a time through activities like "Claim Hex" and "Clear Hex."

### Favored Land

Your kingdom can perform two Region activities simultaneously in heartland terrain (with –2 penalty to both).

### Work Sites

Work sites are established on hexes to gather commodities or provide other benefits.

## Leadership Roles

Eight leadership positions, each with specific vacancy penalties:

| Role          | Ability   | Typical Skills               |
| ------------- | --------- | ---------------------------- |
| **Ruler**     | Loyalty   | Chosen by party              |
| **Counselor** | Loyalty   | Politics, Arts, Folklore     |
| **General**   | Stability | Defense, Warfare             |
| **Emissary**  | Culture   | Trade, Diplomacy             |
| **Magister**  | Culture   | Magic, Intrigue, Scholarship |
| **Treasurer** | Economy   | Industry, Engineering        |
| **Viceroy**   | Loyalty   | Agriculture, Politics        |
| **Warden**    | Loyalty   | Wilderness, Defense          |

Vacant roles impose automatic penalties on kingdom checks that rely on them.

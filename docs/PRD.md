# Pathfinder 2E Kingmaker Kingdom Manager - Product Requirements Document

A free-form kingdom turn tracker designed for tabletop play enables
**players to log activities** and **GMs to configure kingdom state**
without enforcing strict phase order. The system models Paizo's
kingdom rules as a persistent game state rather than an automated turn
engine.

## Core system architecture

The Kingmaker kingdom management system treats the kingdom as a
"character" with its own ability scores, skills, proficiencies, and
level progression. Each kingdom turn represents one month of in-game
time, during which players perform various activities that modify
kingdom statistics.

**Four ability scores** drive all kingdom mechanics: **Culture**
(arts, sciences, learning), **Economy** (trade, industry, production),
**Loyalty** (spirit, trust, unity), and **Stability** (infrastructure,
health, defense). Each ability score has an associated modifier
calculated from the score value, following standard Pathfinder 2E
conventions.

The kingdom earns XP from completing activities, converting unspent
Resource Points, and achieving milestones. At **1,000 XP**, the
kingdom levels up (maximum level equals party level). Higher kingdom
levels increase proficiency bonuses, unlock new activities, and
provide access to advanced structures.

---

## Kingdom statistics requiring persistent storage

### Primary resources (per-turn values)

| Statistic                | Type    | Description                                                                                                                         |
| ------------------------ | ------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Resource Points (RP)** | Integer | Rolled fresh each turn: `(kingdom_level + 4 + bonus_dice - penalty_dice) × Resource Die`. Unspent RP converts to XP (max 120/turn). |
| **Resource Dice**        | Integer | Number of dice to roll; calculated from level + modifiers                                                                           |
| **Resource Die Type**    | Enum    | d4/d6/d8/d10/d12 based on kingdom Size                                                                                              |
| **Bonus/Penalty Dice**   | Integer | Modifiers carrying over from previous turn                                                                                          |

### Persistent kingdom statistics

| Statistic       | Type     | Range                 | Notes                                                           |
| --------------- | -------- | --------------------- | --------------------------------------------------------------- |
| **Level**       | Integer  | 1-20                  | Max = party level                                               |
| **XP**          | Integer  | 0-999+                | Resets after leveling                                           |
| **Size**        | Computed | Hex count             | Determines Resource Die, Control DC modifier, commodity storage |
| **Control DC**  | Computed | 14+                   | Base DC (level-based) + Size modifier (+0 to +4)                |
| **Unrest**      | Integer  | 0-20+                 | At 20+, kingdom enters anarchy                                  |
| **Fame/Infamy** | Integer  | 0-3 (0-4 at level 20) | Resets each turn; type chosen at creation                       |

### Ability scores and modifiers

```text
Kingdom
├── culture_score: int
├── culture_modifier: int (derived)
├── economy_score: int
├── economy_modifier: int (derived)
├── loyalty_score: int
├── loyalty_modifier: int (derived)
├── stability_score: int
├── stability_modifier: int (derived)
```

### Ruin tracking (four separate counters)

Each Ruin type opposes one ability score and accumulates independently:

| Ruin           | Opposes   | Repair Skill | Effect                           |
| -------------- | --------- | ------------ | -------------------------------- |
| **Corruption** | Culture   | Arts         | Item penalty to Culture checks   |
| **Crime**      | Economy   | Trade        | Item penalty to Economy checks   |
| **Strife**     | Loyalty   | Intrigue     | Item penalty to Loyalty checks   |
| **Decay**      | Stability | Engineering  | Item penalty to Stability checks |

For each Ruin, track:

- **points**: Current accumulated points (0+)
- **threshold**: Default 10; increases by 2 when Ruin Resistance is applied
- **penalty**: Item penalty applied when points exceed threshold

When points exceed threshold: subtract threshold from points, increment penalty by 1.

### Commodity stockpiles

Five commodity types with storage limits based on kingdom Size:

| Size (Hexes)     | Storage Limit | Resource Die |
| ---------------- | ------------- | ------------ |
| 1-9 (Territory)  | 4 each        | d4           |
| 10-24 (Province) | 8 each        | d6           |
| 25-49 (State)    | 12 each       | d8           |
| 50-99 (Country)  | 16 each       | d10          |
| 100+ (Dominion)  | 20 each       | d12          |

Storage structures (Granary, Lumberyard, Foundry) add +1 to specific commodity caps.

```bash
Kingdom
├── food: int
├── lumber: int
├── ore: int
├── stone: int
├── luxuries: int
```

---

## Leadership role data model

Eight leadership roles must be tracked, each assignable to one
character (PC or NPC). The system needs to record role assignment,
investment status, and vacancy state.

### Leadership role reference data

| Role          | Key Ability | Vacancy Penalty                           |
| ------------- | ----------- | ----------------------------------------- |
| **Ruler**     | Loyalty     | -1 all checks; +1d4 Unrest; Control DC +2 |
| **Counselor** | Culture     | -1 Culture-based checks                   |
| **General**   | Stability   | -4 Warfare activities                     |
| **Emissary**  | Loyalty     | -1 Loyalty-based checks                   |
| **Magister**  | Culture     | -4 Warfare activities                     |
| **Treasurer** | Economy     | -1 Economy-based checks                   |
| **Viceroy**   | Economy     | -1 Stability-based checks                 |
| **Warden**    | Stability   | -4 Region activities                      |

### Investment system

- **4 roles** can be invested at any time
- Invested roles provide **status bonus** to all skill checks using that role's key ability:
    - Levels 1-7: +1 status bonus
    - Levels 8-15: +2 status bonus
    - Levels 16+: +3 status bonus

### Role assignment model

```python
class LeadershipAssignment(models.Model):
    kingdom = models.ForeignKey('Kingdom')
    role = models.CharField(choices=ROLE_CHOICES)  # ruler, counselor, general, etc.
    character_name = models.CharField(max_length=100)
    is_pc = models.BooleanField(default=True)
    is_invested = models.BooleanField(default=False)
    is_vacant = models.BooleanField(default=False)
    downtime_fulfilled = models.BooleanField(default=True)  # Did they spend required week?
    user = models.ForeignKey('User', null=True)  # Link to player account for PCs
```

---

## Kingdom skills system

Sixteen kingdom skills, each tied to one of the four ability
scores. Proficiency levels unlock activities and provide check
bonuses.

### Skill reference data

| Skill           | Key Ability | Notable Activities                                         |
| --------------- | ----------- | ---------------------------------------------------------- |
| **Agriculture** | Loyalty     | Harvest Crops, Establish Farmland                          |
| **Arts**        | Culture     | Craft Luxuries, Create Masterpiece, Quell Unrest           |
| **Boating**     | Economy     | Go Fishing, Establish Trade Agreement                      |
| **Defense**     | Stability   | Fortify Hex, Garrison Army                                 |
| **Engineering** | Stability   | Build Structure, Establish Work Site, Establish Settlement |
| **Exploration** | Economy     | Claim Hex, Clear Hex, Abandon Hex                          |
| **Folklore**    | Culture     | Celebrate Holiday, Quell Unrest                            |
| **Industry**    | Economy     | Trade Commodities, Establish Trade Agreement               |
| **Intrigue**    | Loyalty     | Clandestine Business, Quell Unrest                         |
| **Magic**       | Culture     | Supernatural Solution, Prognostication                     |
| **Politics**    | Loyalty     | Improve Lifestyle, Quell Unrest, New Leadership            |
| **Scholarship** | Culture     | Creative Solution, Rest and Relax                          |
| **Statecraft**  | Loyalty     | Send Diplomatic Envoy, Request Foreign Aid                 |
| **Trade**       | Economy     | Collect Taxes, Capital Investment                          |
| **Warfare**     | Loyalty     | Deploy Army, Train Army                                    |
| **Wilderness**  | Stability   | Gather Livestock, Rest and Relax                           |

### Proficiency tracking

```python
class KingdomSkillProficiency(models.Model):
    kingdom = models.ForeignKey('Kingdom')
    skill = models.CharField(choices=SKILL_CHOICES)
    proficiency = models.CharField(choices=[
        ('untrained', 'Untrained'),  # +0
        ('trained', 'Trained'),       # level + 2
        ('expert', 'Expert'),         # level + 4
        ('master', 'Master'),         # level + 6
        ('legendary', 'Legendary'),   # level + 8
    ])
```

Proficiency unlocks: Trained at level 1 (initial), Expert at 3, Master at 7, Legendary at 15.

### Skill check formula

```matlab
1d20 + ability_modifier + proficiency_bonus + status_bonus + circumstance_bonus + item_bonus - penalties
```

Where:

- **ability_modifier**: From linked ability score
- **proficiency_bonus**: 0 (untrained) or level + 2/4/6/8
- **status_bonus**: From invested leadership roles (+1/+2/+3)
- **circumstance_bonus**: From activities like Collect Taxes, Improve Lifestyle
- **item_bonus**: From structures; also negative from Ruin penalties
- **penalties**: Vacancy penalties, Unrest penalties (-1 at 1+, -2 at 5+, -3 at 10+, -4 at 15+)

---

## Activity logging system

Since the app uses **free-form activity logging** without enforced
phase order, activities should be logged as discrete events rather
than constrained by turn phase.

### Activity reference data

Activities have traits indicating their category: **Upkeep**, **Commerce**, **Leadership**, **Region**, **Civic**, **Fortune**, **Downtime**.

Key constraints (for reference/display, not enforcement):

- **Leadership activities**: 2-3 per PC leader per turn (3 if capital has Castle/Palace/Town Hall)
- **Region activities**: 3 total per turn (collective)
- **Civic activities**: 1 per settlement per turn

### Activity log model

```python
class ActivityLog(models.Model):
    kingdom = models.ForeignKey('Kingdom')
    turn_number = models.IntegerField()
    activity_name = models.CharField(max_length=100)
    activity_trait = models.CharField(choices=TRAIT_CHOICES)  # leadership, region, civic, etc.
    skill_used = models.CharField(choices=SKILL_CHOICES, null=True)
    performed_by = models.ForeignKey('LeadershipAssignment', null=True)
    settlement = models.ForeignKey('Settlement', null=True)  # For Civic activities
    hex = models.ForeignKey('Hex', null=True)  # For Region activities

    # Roll tracking (optional - GM may enter results)
    roll_result = models.IntegerField(null=True)
    total_modifier = models.IntegerField(null=True)
    dc = models.IntegerField(null=True)
    degree_of_success = models.CharField(choices=[
        ('critical_success', 'Critical Success'),
        ('success', 'Success'),
        ('failure', 'Failure'),
        ('critical_failure', 'Critical Failure'),
    ], null=True)

    notes = models.TextField(blank=True)  # Free-form outcome description
    created_at = models.DateTimeField(auto_now_add=True)
```

### Degree of success determination

- **Critical Success**: Beat DC by 10+ OR natural 20 that would succeed
- **Success**: Meet or beat DC
- **Failure**: Below DC
- **Critical Failure**: Miss DC by 10+ OR natural 1 that would fail

---

## Settlement and hex tracking

### Hex model

```python
class Hex(models.Model):
    kingdom = models.ForeignKey('Kingdom')
    coordinates = models.CharField(max_length=10)  # e.g., "A1", "B3"

    terrain_type = models.CharField(choices=[
        ('plains', 'Plains'),
        ('forest', 'Forest'),
        ('hills', 'Hills'),
        ('mountains', 'Mountains'),
        ('swamp', 'Swamp'),
        ('lake', 'Lake'),
    ])

    status = models.CharField(choices=[
        ('unexplored', 'Unexplored'),
        ('reconnoitered', 'Reconnoitered'),
        ('claimed', 'Claimed'),
        ('lost', 'Lost'),
    ])

    # Terrain features (typically one per hex)
    has_road = models.BooleanField(default=False)
    has_bridge = models.BooleanField(default=False)
    is_farmland = models.BooleanField(default=False)
    is_landmark = models.BooleanField(default=False)
    is_refuge = models.BooleanField(default=False)
    has_resource = models.CharField(choices=[
        ('none', 'None'),
        ('lumber', 'Lumber Resource'),
        ('ore', 'Ore Resource'),
        ('stone', 'Stone Resource'),
    ], default='none')

    notes = models.TextField(blank=True)


class WorkSite(models.Model):
    hex = models.OneToOneField('Hex')
    site_type = models.CharField(choices=[
        ('lumber_camp', 'Lumber Camp'),
        ('mine', 'Mine'),
        ('quarry', 'Quarry'),
    ])
    # Production: 1 commodity/turn; 2 if hex has matching resource
```

### Settlement model

```python
class Settlement(models.Model):
    kingdom = models.ForeignKey('Kingdom')
    hex = models.OneToOneField('Hex')
    name = models.CharField(max_length=100)

    settlement_type = models.CharField(choices=[
        ('village', 'Village'),    # 1 block, ≤400 pop, 1 consumption
        ('town', 'Town'),          # 2-4 blocks, 2 consumption
        ('city', 'City'),          # 5-9 blocks, 4 consumption
        ('metropolis', 'Metropolis'),  # 10+ blocks, 6 consumption
    ])

    is_capital = models.BooleanField(default=False)

    # Computed from blocks/lots - but may be overridden by GM
    level = models.IntegerField(default=1)  # Blocks with structures
    consumption = models.IntegerField(default=1)

    # Border tracking
    water_borders = models.JSONField(default=list)  # e.g., ['north', 'east']

    notes = models.TextField(blank=True)
```

### Settlement influence radius

| Type       | Radius  | Effect         |
| ---------- | ------- | -------------- |
| Village    | 0 hexes | Own hex only   |
| Town       | 1 hex   | Adjacent hexes |
| City       | 2 hexes | Within 2 hexes |
| Metropolis | 3 hexes | Within 3 hexes |

Capital provides bonuses to ALL claimed hexes regardless of influence.

### Simplified structure tracking

Rather than modeling every lot, a simplified approach tracks structures per settlement:

```python
class SettlementStructure(models.Model):
    settlement = models.ForeignKey('Settlement')
    structure_name = models.CharField(max_length=100)
    lots_occupied = models.IntegerField(default=1)
    block_number = models.IntegerField(null=True)  # Optional detailed placement
    is_residential = models.BooleanField(default=False)
    is_infrastructure = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
```

Structure reference data (RP costs, commodity costs, effects) can be
stored as static JSON or a separate reference table that the GM
doesn't need to edit.

---

## Turn tracking model

```python
class KingdomTurn(models.Model):
    kingdom = models.ForeignKey('Kingdom')
    turn_number = models.IntegerField()
    in_game_month = models.CharField(max_length=50, blank=True)

    # Snapshot of starting state
    starting_rp = models.IntegerField(null=True)
    resource_dice_rolled = models.CharField(max_length=50, blank=True)  # e.g., "6d6"

    # Commerce phase choices
    collected_taxes = models.BooleanField(default=False)
    improved_lifestyle = models.BooleanField(default=False)
    tapped_treasury = models.BooleanField(default=False)

    # End-of-turn results
    ending_rp = models.IntegerField(null=True)
    rp_converted_to_xp = models.IntegerField(null=True)
    xp_gained = models.IntegerField(null=True)
    leveled_up = models.BooleanField(default=False)

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True)
```

---

## User and permission model

```python
class User(AbstractUser):
    # Standard Django auth fields
    pass


class KingdomMembership(models.Model):
    user = models.ForeignKey('User')
    kingdom = models.ForeignKey('Kingdom')
    role = models.CharField(choices=[
        ('gm', 'Game Master'),
        ('player', 'Player'),
    ])
    leadership_assignment = models.ForeignKey('LeadershipAssignment', null=True)


# Permissions:
# - GM: Full read/write on all kingdom data
# - Player: Read all kingdom data; write only to their assigned leadership role's activities
```

---

## Recommended entity relationship diagram

```bash
User
├── KingdomMembership (M2M through)
│   └── Kingdom
│       ├── LeadershipAssignment (8 roles max)
│       ├── KingdomSkillProficiency (16 skills)
│       ├── Hex (many)
│       │   └── WorkSite (0-1)
│       ├── Settlement (many)
│       │   └── SettlementStructure (many)
│       ├── KingdomTurn (many)
│       │   └── ActivityLog (many)
│       ├── TradeAgreement (many)
│       └── DiplomaticRelation (many)
```

---

## Out of scope (per requirements)

- **Kingdom events**: GM handles separately; no event tables or random event generation
- **Foundry VTT integration**: Standalone app only
- **Strict phase enforcement**: Activities logged freely; constraints shown as guidance only
- **Dice rolling**: Optional - users can enter roll results manually
- **Warfare/Army tracking**: Can be added as future enhancement

---

## Implementation priorities

**Phase 1 - Core kingdom state**:

- Kingdom model with all statistics
- User authentication and kingdom membership
- Leadership role assignment
- Skill proficiency tracking

**Phase 2 - Turn logging**:

- KingdomTurn model
- ActivityLog with free-form entry
- Turn state snapshots

**Phase 3 - Territory management**:

- Hex tracking
- Settlement and structure tracking
- Work site commodity generation

**Phase 4 - Quality of life**:

- Skill check calculator (display-only)
- Turn summary reports
- Activity history per leader

This data model captures the mechanical requirements of PF2E Kingmaker
kingdom management while supporting the free-form, GM-controlled
workflow you've specified. The emphasis on logging rather than
automation keeps complexity manageable while still providing useful
tracking for all the interconnected kingdom statistics.

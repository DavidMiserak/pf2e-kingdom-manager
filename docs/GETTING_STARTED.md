# Getting Started with PF2E Kingdom Manager

This quick start guide walks you through setting up and running your first kingdom turn.

## Prerequisites

- You're running a Pathfinder 2E Kingmaker campaign
- The GM has deployed the PF2E Kingdom Manager (or you're accessing it at `http://localhost:8000`)
- You have an account (check your email for login link from the GM)

## 5-Minute Setup

### Step 1: Log In

1. Navigate to the app and click **Sign In**
2. Enter your email
3. Check your email for the login link and click it
4. You're logged in!

### Step 2: Create Your Kingdom (GM Only)

1. Click **Create Kingdom**
2. Fill in basic details:
    - **Name**: Your kingdom's name
    - **Charter**: Select one (Conquest, Expansion, Exploration, Grant, or Open)
    - **Heartland**: Choose your starting terrain type
    - **Government**: Pick a government style
    - **Capital**: Name your first settlement
3. Click **Create**

### Step 3: Assign Leadership (GM Only)

1. On your kingdom page, click **Leadership**
2. Assign your party members (and NPCs) to the 8 roles:
    - Ruler, Counselor, General, Emissary, Magister, Treasurer, Viceroy, Warden
3. Click **Save**

### Step 4: Share with Players

1. On your kingdom page, copy the **Share Link**
2. Send it to your players
3. Players can now view your kingdom and log activities

## Your First Turn

### Step 1: Create a Turn

1. Go to your kingdom's **Dashboard**
2. Click **Create Turn**
3. Set the turn's starting values:
    - Unrest (usually 0 at game start)
    - Ruin counters (Corruption, Crime, Decay, Strife—start at 0)
    - Commodity stockpiles (Food, Lumber, Ore, Stone, Luxuries)
    - Resource Points rolled this turn
4. Click **Create Turn**

### Step 2: Log an Activity

1. On the turn page, click **Log Activity**
2. Describe what your kingdom did:
    - **Activity Type**: "Claim Hex" or "Build Structure" or "Diplomacy Check"
    - **Description**: Free-form notes
    - **Degree of Success**: Did you crit succeed, succeed, fail, or crit fail?
3. If resources were spent, update them:
    - RP spent
    - Commodities used
4. Click **Create Activity**

### Step 3: Complete the Turn

1. Once all activities are logged, go back to the turn page
2. Update final values:
    - Final Unrest (if changed)
    - Final Ruin (if changed)
    - Final commodity stockpiles
    - Kingdom XP earned (if any)
3. Click **Complete Turn**

That's it! You've logged one month of kingdom activity.

## Key Differences from the Rules

This tool is **not** a strict rules engine. Instead, it's a **free-form activity logger** that helps you track kingdom state.

- **No phase enforcement**: Log activities in any order; there's no Upkeep → Commerce → Activity → Event structure enforced by the system
- **No dice automation**: You roll dice at your table as normal; the tool just tracks results
- **Manual state management**: You manually adjust Unrest, Ruin, commodities, and RP—the system doesn't auto-calculate penalties

See the **User Guide** for more on how the system works.

## Common Workflows

### Leadership Check During Activity

1. At your table, roll `d20 + skill modifier`
2. Determine the degree of success
3. In the tool, log the activity with the result
4. Note the modifier breakdown in the activity description (e.g., "+2 Culture +1 Trained –1 Unrest = +2")

### Building a Structure

1. Spend RP and commodities (see turn state)
2. Log a "Build Structure" activity
3. Note what was built and whether it succeeded
4. Update commodity stockpiles at turn end

### Claiming a Hex

1. Log a "Claim Hex" activity
2. Record the hex location and terrain type
3. Update your territory map (not in tool yet—use separate maps for Phase 3)
4. Award kingdom XP if applicable

### Leveling Up

1. When you hit 1,000 XP, click **Level Up** on the Dashboard
2. Update your kingdom level
3. Assign new feats or skill increases
4. Continue playing

## Helpful Resources

- **Rules Reference**: Full breakdown of PF2E Kingmaker mechanics (`docs/RULES_REFERENCE.md`)
- **User Guide**: Deep dive into all features (`docs/USER_GUIDE.md`)
- **Official Rules**: [Pathfinder 2E Kingmaker](https://2e.aonprd.com/Rules.aspx?ID=1739)

## Troubleshooting

### **I can't log in**

- Check your email for the login link
- Make sure you're using the email you signed up with
- If you didn't receive a link, ask the GM to resend it

### **The kingdom isn't showing up**

- Refresh the page
- Make sure you created it (not someone else)
- Check that you're logged in with the right email

### **I want to fix a typo in an activity**

- Click the activity
- Click **Edit**
- Update the text
- Click **Save**

### **What if I messed up the turn state?**

- You can edit activities to correct RP or commodity spending
- You can edit the turn itself to adjust starting/ending values
- Only GMs can complete turns, so players can flag issues for review

## Next Steps

1. **Read the Rules Reference** to understand PF2E Kingmaker mechanics (`RULES_REFERENCE.md`)
2. **Explore the Dashboard** to get familiar with your kingdom's current state
3. **Check out the Leadership, Skills, and Members pages** for more kingdom management options
4. **Log a few turns** and iterate on the workflow with your group

Happy kingdom building! 👑

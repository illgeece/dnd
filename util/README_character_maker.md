# D&D 5E Character Maker

A comprehensive command-line tool for creating and managing D&D 5th edition characters. This tool provides all the functionality you need to create, edit, and track your D&D characters with persistent storage and an intuitive interface.

## Features

### ✨ Complete Character Creation
- **Step-by-step character creation wizard** with guided input
- **All D&D 5E character sheet fields** including:
  - Basic information (race, class, background, alignment, etc.)
  - Ability scores with automatic modifier calculation
  - Proficiencies (skills, saving throws, languages, tools)
  - Combat stats (AC, HP, initiative, speed)
  - Spellcasting setup for magic users

### 🎲 Combat Reference System
- **Quick combat reference** with essential stats at a glance
- **Hit point management** including damage, healing, and temporary HP
- **Spell slot tracking** with usage and recovery
- **Saving throw and skill quick reference**
- **Attack calculation helpers** for different weapon types
- **Conditions and notes tracker** for status effects

### 💾 Character Management
- **Multiple character support** - create and switch between characters
- **JSON file persistence** - all data saved automatically
- **Complete character editing** - modify any aspect of your character
- **Character sheet viewer** - formatted display of all character information
- **Import/Export friendly** JSON format for easy backup

### 🔮 Spellcasting System
- **Full spellcasting support** for any magic-using class
- **Spell save DC and attack bonus calculation**
- **Spell slot management** by level with expended tracking
- **Spellcasting ability configuration** (INT/WIS/CHA)
- **Custom spell and ability support**

## Installation & Usage

### Prerequisites
- Python 3.6 or higher
- No additional dependencies required (uses only standard library)

### Getting Started

1. **Clone or download** the `character_maker.py` file
2. **Run the program**:
   ```bash
   python3 character_maker.py
   ```
3. **Create your first character** using the guided creation wizard
4. **Enjoy!** Your characters will be automatically saved to `characters.json`

### Basic Workflow

1. **Create Character**: Choose option 1 from the main menu
2. **Follow the wizard**: Enter character details step by step
3. **Edit as needed**: Use option 5 to modify any character details
4. **Combat reference**: Use option 6 during game sessions for quick stats
5. **Auto-save**: All changes are automatically saved

## Menu System

### Main Menu
- **Create New Character** - Step-by-step character creation
- **Load Existing Character** - Switch between your characters
- **List All Characters** - View all your created characters
- **Delete Character** - Remove characters you no longer need
- **Edit Current Character** - Modify the currently loaded character
- **Combat Reference** - Quick access to combat-relevant stats

### Character Editing
- **Basic Information** - Name, race, class, background, etc.
- **Ability Scores** - Modify STR, DEX, CON, INT, WIS, CHA
- **Combat Stats** - AC, HP, speed, initiative
- **Proficiencies** - Skills, saving throws, languages, tools
- **Spellcasting** - Spell slots, save DC, attack bonus
- **Features & Traits** - Class/race features, custom abilities
- **View Character Sheet** - Formatted display of all character data

### Combat Reference
- **Manage Hit Points** - Damage, healing, temporary HP tracking
- **View Ability Modifiers** - Quick reference for all ability scores
- **View Saving Throws** - All saving throw bonuses at a glance
- **View Skills** - Skill bonuses organized by ability
- **Spellcasting Quick Ref** - Spell slots, DC, attack bonus, usage tracking
- **Attack Calculations** - Common attack bonuses for different weapons
- **Conditions & Notes** - Track status effects and combat notes

## Character Data Structure

Characters are stored with complete D&D 5E information:

```
Basic Info: Name, Player, Race, Class/Level, Background, Alignment, XP
Abilities: STR, DEX, CON, INT, WIS, CHA (with auto-calculated modifiers)
Combat: AC, Initiative, Speed, HP (current/max/temp), Hit Dice, Proficiency Bonus
Proficiencies: All 18 skills, 6 saving throws, languages, other proficiencies
Spellcasting: Class, ability, save DC, attack bonus, spell slots by level
Features: Race/class features, custom abilities, traits
Tracking: Conditions, combat notes, spell slot usage
```

## File Structure

- `character_maker.py` - Main program file
- `characters.json` - Character data storage (created automatically)
- `README_character_maker.md` - This documentation

## Tips & Best Practices

### Character Creation
- **Take your time** with the creation wizard - you can always edit later
- **Use default values** where appropriate by pressing Enter
- **Double-check ability scores** as they affect many other calculations
- **Set up spellcasting** properly if your character uses magic

### During Play
- **Use the combat reference** to quickly access important stats
- **Track HP changes** in real-time during combat
- **Monitor spell slot usage** to avoid surprises
- **Update conditions** and notes to track temporary effects

### Character Management
- **Regular backups** - copy your `characters.json` file occasionally
- **Descriptive names** - use clear character names to avoid confusion
- **Delete unused characters** to keep your list manageable

## Technical Details

### Calculations
- **Ability modifiers**: (Score - 10) ÷ 2 (rounded down)
- **Proficiency bonus**: 2 + (Level - 1) ÷ 4 (rounded down)
- **Skill modifiers**: Ability modifier + proficiency bonus (if proficient)
- **Spell save DC**: 8 + proficiency bonus + spellcasting ability modifier
- **Spell attack bonus**: Proficiency bonus + spellcasting ability modifier

### Data Storage
- Characters stored in JSON format for easy reading/editing
- Automatic save on program exit and after major changes
- Each character is a complete, self-contained data structure
- Cross-platform compatibility (works on Windows, macOS, Linux)

## Troubleshooting

### Common Issues
- **"No characters found"**: Create a new character first
- **"Invalid input"**: Check that you're entering numbers where expected
- **"Character already exists"**: Choose a different name or load the existing character
- **"File not found"**: The program will create a new `characters.json` automatically

### Data Recovery
- If `characters.json` becomes corrupted, rename it and start fresh
- Always keep backups of your character file for important campaigns
- Characters can be manually edited in the JSON file if needed

## Examples

### Sample Character Creation
```
Character name: Thorin Ironbeard
Player name: Alex
Race: Mountain Dwarf
Class and level: Fighter 3
Background: Soldier
Alignment: Lawful Good

Ability Scores:
Strength: 16 (+3)
Dexterity: 12 (+1)
Constitution: 16 (+3)
Intelligence: 10 (+0)
Wisdom: 13 (+1)
Charisma: 8 (-1)

Combat Stats:
AC: 18 (Chain Mail + Shield)
HP: 28/28
Initiative: +1
Speed: 25 ft (heavy armor)
Proficiency: +2

Proficiencies:
- Saving Throws: Strength, Constitution
- Skills: Athletics, Intimidation
- Languages: Common, Dwarvish
- Tools: Smith's Tools
```

### Combat Reference Display
```
COMBAT REFERENCE: Thorin Ironbeard
AC: 18 | Initiative: +1 | Speed: 25 ft
HP: 23/28
Proficiency: +2

Quick Actions:
- Longsword Attack: +5 to hit, 1d8+3 damage
- Athletics: +5
- Intimidation: +1
- Strength Save: +5
- Constitution Save: +5
```

## Contributing

This is a complete, standalone tool that meets the requirements outlined in the original specification. Feel free to extend it with additional features such as:

- Spell list management
- Equipment/inventory integration (note: intentionally excluded per requirements)
- Character sheet export (PDF/HTML)
- Online/shared character storage
- Integration with virtual tabletops

## License

This tool is provided as-is for personal use in D&D campaigns. Dungeons & Dragons and D&D are trademarks of Wizards of the Coast LLC.

---

**Happy adventuring!** 🎲✨ 
# D&D 5e Character Inventory Manager

An interactive command-line tool for managing player character inventories in Dungeons & Dragons 5th Edition.

## Features

- **Interactive CLI Interface**: Easy-to-use menu system
- **Persistent Storage**: Inventory saved in JSON format for session continuity
- **Required Fields**: Name (string), Weight (supports fractions), Rarity (string)
- **Additional Fields**: Quantity, Description, Value (GP), Item Type, Magical status, Attunement
- **Sorting & Searching**: Sort by any field, search by name/description/type
- **Item Stacking**: Automatically combines identical items
- **Weight Calculations**: Individual and total weight tracking
- **D&D 5e Integration**: Standard rarity levels, magical item support

## Usage

### Running the Program
```bash
python3 dnd_inventory.py
```

### First Time Setup
1. Enter your character name when prompted
2. Start adding items to your inventory

### Menu Options
1. **View Inventory** - Display all items in a formatted table
2. **Add Item** - Interactive item creation with all fields
3. **Remove Item** - Remove specific quantities of items
4. **Search Items** - Find items by name, description, or type
5. **Sort Inventory** - Sort by name, weight, rarity, quantity, value, type, or total weight
6. **Character Summary** - Overview of total items, weight, value, magical items
7. **Save & Exit** - Save inventory and quit
8. **Exit without Saving** - Quit without saving changes

### Item Entry Examples

**Weight Entry:**
- Whole numbers: `1`, `5`, `10`
- Fractions: `1/2`, `3/4`, `1/4`
- Decimals: `0.5`, `2.25`

**Rarity Options:**
- Common, Uncommon, Rare, Very Rare, Legendary, Artifact

**Sample Items:**
- Sword: Name="Longsword", Weight=3, Rarity="Common", Type="Weapon"
- Potion: Name="Potion of Healing", Weight=0.5, Rarity="Common", Type="Potion", Magical=Yes

## File Storage

The inventory is automatically saved to `character_inventory.json` in the same directory. This file contains:
- Character name
- Complete item database with all properties
- Human-readable JSON format for easy backup/sharing

## Technical Requirements

- Python 3.7+
- No external dependencies (uses only standard library)
- Cross-platform compatible (Windows, macOS, Linux)

## Notes

- The program ignores all other files in the project directory
- Inventory data persists between sessions
- Items with identical properties automatically stack
- Supports Unicode characters for item names and descriptions
- Graceful error handling for invalid input 
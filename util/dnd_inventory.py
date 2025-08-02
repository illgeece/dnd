#!/usr/bin/env python3
"""
D&D 5e Character Inventory Management System
Interactive command-line tool for managing player character inventories.
"""

import json
import os
from fractions import Fraction
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class Rarity(Enum):
    """Standard D&D 5e item rarities"""
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    VERY_RARE = "Very Rare"
    LEGENDARY = "Legendary"
    ARTIFACT = "Artifact"

@dataclass
class InventoryItem:
    """Represents a single inventory item"""
    name: str
    weight: float
    rarity: str
    quantity: int = 1
    description: str = ""
    value_gp: float = 0.0
    item_type: str = "Miscellaneous"
    magical: bool = False
    attuned: bool = False
    
    def __post_init__(self):
        """Validate item data after initialization"""
        if not self.name.strip():
            raise ValueError("Item name cannot be empty")
        if self.weight < 0:
            raise ValueError("Weight cannot be negative")
        if self.quantity < 1:
            raise ValueError("Quantity must be at least 1")
    
    @property
    def total_weight(self) -> float:
        """Calculate total weight for this item stack"""
        return self.weight * self.quantity
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert item to dictionary for JSON serialization"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InventoryItem':
        """Create item from dictionary"""
        return cls(**data)

class InventoryManager:
    """Manages the character's inventory"""
    
    def __init__(self, filename: str = "character_inventory.json"):
        self.filename = filename
        self.items: List[InventoryItem] = []
        self.character_name: str = "Unknown Adventurer"
        self.load_inventory()
    
    def load_inventory(self) -> None:
        """Load inventory from file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.character_name = data.get('character_name', 'Unknown Adventurer')
                    self.items = [InventoryItem.from_dict(item_data) 
                                for item_data in data.get('items', [])]
                print(f"✓ Loaded inventory for {self.character_name}")
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"⚠ Error loading inventory: {e}")
                print("Starting with empty inventory.")
                self.items = []
        else:
            print("No existing inventory file found. Starting fresh!")
    
    def save_inventory(self) -> None:
        """Save inventory to file"""
        try:
            data = {
                'character_name': self.character_name,
                'items': [item.to_dict() for item in self.items]
            }
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✓ Inventory saved for {self.character_name}")
        except Exception as e:
            print(f"✗ Error saving inventory: {e}")
    
    def add_item(self, item: InventoryItem) -> None:
        """Add an item to inventory, combining with existing if same name"""
        existing_item = self.find_item_by_name(item.name)
        if existing_item and self._items_can_stack(existing_item, item):
            existing_item.quantity += item.quantity
            print(f"✓ Added {item.quantity} {item.name}(s) to existing stack")
        else:
            self.items.append(item)
            print(f"✓ Added {item.name} to inventory")
    
    def _items_can_stack(self, item1: InventoryItem, item2: InventoryItem) -> bool:
        """Check if two items can be stacked together"""
        return (item1.name == item2.name and 
                item1.weight == item2.weight and
                item1.rarity == item2.rarity and
                item1.description == item2.description and
                item1.value_gp == item2.value_gp and
                item1.item_type == item2.item_type and
                item1.magical == item2.magical)
    
    def remove_item(self, name: str, quantity: int = 1) -> bool:
        """Remove specified quantity of an item"""
        item = self.find_item_by_name(name)
        if not item:
            print(f"✗ Item '{name}' not found in inventory")
            return False
        
        if quantity >= item.quantity:
            self.items.remove(item)
            print(f"✓ Removed all {item.name}(s) from inventory")
        else:
            item.quantity -= quantity
            print(f"✓ Removed {quantity} {item.name}(s) from inventory")
        return True
    
    def find_item_by_name(self, name: str) -> Optional[InventoryItem]:
        """Find an item by name (case-insensitive)"""
        name_lower = name.lower()
        for item in self.items:
            if item.name.lower() == name_lower:
                return item
        return None
    
    def get_total_weight(self) -> float:
        """Calculate total weight of all items"""
        return sum(item.total_weight for item in self.items)
    
    def get_total_value(self) -> float:
        """Calculate total value of all items"""
        return sum(item.value_gp * item.quantity for item in self.items)
    
    def sort_items(self, sort_by: str, reverse: bool = False) -> List[InventoryItem]:
        """Sort items by specified attribute"""
        valid_sorts = {
            'name': lambda x: x.name.lower(),
            'weight': lambda x: x.weight,
            'rarity': lambda x: x.rarity,
            'quantity': lambda x: x.quantity,
            'value': lambda x: x.value_gp,
            'type': lambda x: x.item_type.lower(),
            'total_weight': lambda x: x.total_weight
        }
        
        if sort_by not in valid_sorts:
            print(f"✗ Invalid sort option. Choose from: {', '.join(valid_sorts.keys())}")
            return self.items
        
        return sorted(self.items, key=valid_sorts[sort_by], reverse=reverse)
    
    def search_items(self, query: str) -> List[InventoryItem]:
        """Search for items by name or description"""
        query_lower = query.lower()
        return [item for item in self.items 
                if query_lower in item.name.lower() or 
                query_lower in item.description.lower() or
                query_lower in item.item_type.lower()]
    
    def display_inventory(self, items: Optional[List[InventoryItem]] = None, 
                         sort_by: str = 'name', reverse: bool = False) -> None:
        """Display inventory in a formatted table"""
        display_items = items if items is not None else self.sort_items(sort_by, reverse)
        
        if not display_items:
            print("\n📦 Inventory is empty!")
            return
        
        print(f"\n📦 {self.character_name}'s Inventory")
        print("=" * 80)
        print(f"{'Name':<25} {'Qty':<4} {'Weight':<8} {'Rarity':<12} {'Type':<15} {'Value':<8}")
        print("-" * 80)
        
        for item in display_items:
            magical_indicator = "✨" if item.magical else "  "
            attuned_indicator = "🔗" if item.attuned else "  "
            
            weight_str = f"{item.weight:g}"
            if item.quantity > 1:
                weight_str += f" ({item.total_weight:g})"
            
            value_str = f"{item.value_gp:g} gp" if item.value_gp > 0 else "-"
            
            print(f"{item.name:<25} {item.quantity:<4} {weight_str:<8} "
                  f"{item.rarity:<12} {item.item_type:<15} {value_str:<8} "
                  f"{magical_indicator}{attuned_indicator}")
        
        print("-" * 80)
        print(f"Total Items: {len(display_items)} | "
              f"Total Weight: {self.get_total_weight():g} lbs | "
              f"Total Value: {self.get_total_value():g} gp")
        print()

def parse_weight(weight_str: str) -> float:
    """Parse weight string, handling fractions"""
    try:
        return float(Fraction(weight_str))
    except (ValueError, ZeroDivisionError):
        raise ValueError(f"Invalid weight format: {weight_str}")

def get_user_input(prompt: str, input_type: type = str, required: bool = True, 
                  validation_func=None, default=None):
    """Get validated user input"""
    while True:
        try:
            user_input = input(prompt).strip()
            
            if not user_input and default is not None:
                return default
            elif not user_input and required:
                print("This field is required. Please enter a value.")
                continue
            elif not user_input:
                return None
            
            # Convert to appropriate type
            if input_type == bool:
                value = user_input.lower() in ('y', 'yes', 'true', '1')
            elif input_type == float:
                value = parse_weight(user_input)
            else:
                value = input_type(user_input)
            
            # Apply validation function if provided
            if validation_func and not validation_func(value):
                print("Invalid input. Please try again.")
                continue
            
            return value
            
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

def create_item_interactive() -> Optional[InventoryItem]:
    """Interactive item creation"""
    print("\n➕ Adding New Item")
    print("-" * 20)
    
    try:
        name = get_user_input("Item name: ", required=True)
        weight = get_user_input("Weight (lbs, can use fractions like 1/2): ", 
                               float, required=True,
                               validation_func=lambda x: x >= 0)
        
        print("\nRarity options:", ", ".join([r.value for r in Rarity]))
        rarity = get_user_input("Rarity: ", default="Common")
        
        quantity = get_user_input("Quantity: ", int, default=1,
                                 validation_func=lambda x: x >= 1)
        
        description = get_user_input("Description (optional): ", required=False) or ""
        value_gp = get_user_input("Value in gold pieces (optional): ", float, 
                                 required=False, default=0.0)
        item_type = get_user_input("Item type (optional): ", default="Miscellaneous")
        magical = get_user_input("Is magical? (y/n): ", bool, default=False)
        attuned = False
        if magical:
            attuned = get_user_input("Requires attunement? (y/n): ", bool, default=False)
        
        return InventoryItem(
            name=name,
            weight=weight,
            rarity=rarity,
            quantity=quantity,
            description=description,
            value_gp=value_gp,
            item_type=item_type,
            magical=magical,
            attuned=attuned
        )
    except KeyboardInterrupt:
        print("\n⚠ Item creation cancelled.")
        return None

def main():
    """Main program loop"""
    print("🎲 D&D 5e Character Inventory Manager ��")
    print("=======================================")
    
    # Initialize inventory manager
    inventory = InventoryManager()
    
    # Set character name if not already set
    if inventory.character_name == "Unknown Adventurer":
        name = get_user_input("\nCharacter name: ", required=False)
        if name:
            inventory.character_name = name
    
    while True:
        print("\n📋 MAIN MENU")
        print("1. View Inventory")
        print("2. Add Item")
        print("3. Remove Item")
        print("4. Search Items")
        print("5. Sort Inventory")
        print("6. Character Summary")
        print("7. Save & Exit")
        print("8. Exit without Saving")
        
        choice = get_user_input("\nChoose option (1-8): ", required=False)
        
        if choice == "1":
            inventory.display_inventory()
            
        elif choice == "2":
            item = create_item_interactive()
            if item:
                inventory.add_item(item)
                
        elif choice == "3":
            if not inventory.items:
                print("📦 Inventory is empty!")
                continue
            
            inventory.display_inventory()
            item_name = get_user_input("\nItem name to remove: ", required=False)
            if item_name:
                item = inventory.find_item_by_name(item_name)
                if item:
                    max_qty = item.quantity
                    qty = get_user_input(f"Quantity to remove (1-{max_qty}): ", 
                                       int, default=1,
                                       validation_func=lambda x: 1 <= x <= max_qty)
                    inventory.remove_item(item_name, qty)
                else:
                    print(f"✗ Item '{item_name}' not found.")
                    
        elif choice == "4":
            query = get_user_input("\nSearch for: ", required=False)
            if query:
                results = inventory.search_items(query)
                if results:
                    print(f"\n🔍 Search results for '{query}':")
                    inventory.display_inventory(results)
                else:
                    print(f"No items found matching '{query}'")
                    
        elif choice == "5":
            if not inventory.items:
                print("📦 Inventory is empty!")
                continue
                
            print("\nSort options: name, weight, rarity, quantity, value, type, total_weight")
            sort_by = get_user_input("Sort by: ", default="name")
            reverse = get_user_input("Reverse order? (y/n): ", bool, default=False)
            inventory.display_inventory(sort_by=sort_by, reverse=reverse)
            
        elif choice == "6":
            print(f"\n🎭 Character: {inventory.character_name}")
            print(f"📦 Total Items: {len(inventory.items)}")
            print(f"⚖️  Total Weight: {inventory.get_total_weight():g} lbs")
            print(f"💰 Total Value: {inventory.get_total_value():g} gp")
            
            magical_items = [item for item in inventory.items if item.magical]
            attuned_items = [item for item in inventory.items if item.attuned]
            print(f"✨ Magical Items: {len(magical_items)}")
            print(f"🔗 Attuned Items: {len(attuned_items)}")
            
        elif choice == "7":
            inventory.save_inventory()
            print("👋 Farewell, adventurer!")
            break
            
        elif choice == "8":
            confirm = get_user_input("Exit without saving? (y/n): ", bool, default=False)
            if confirm:
                print("👋 Farewell, adventurer!")
                break
                
        else:
            print("Invalid option. Please choose 1-8.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n💥 An unexpected error occurred: {e}")
        print("Your inventory should still be safely saved in the JSON file.")

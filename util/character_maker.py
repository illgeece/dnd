#!/usr/bin/env python3
"""
D&D 5E Character Maker
A command-line tool for creating and managing D&D 5th edition characters.
"""

import json
import os
import sys
import random
from typing import Dict, List, Optional, Any, Tuple

# D&D 5E Class Data
DND_CLASSES = {
    "Artificer": {
        "hit_die": 8,
        "primary_ability": ["Intelligence"],
        "saving_throws": ["Constitution", "Intelligence"],
        "subclasses": {
            "Alchemist": "Support through elixirs and healing",
            "Armorer": "Heavy armor and defensive capabilities",
            "Artillerist": "Ranged damage and battlefield control",
            "Battle Smith": "Combat pet and versatile fighting"
        }
    },
    "Barbarian": {
        "hit_die": 12,
        "primary_ability": ["Strength"],
        "saving_throws": ["Strength", "Constitution"],
        "subclasses": {
            "Path of the Berserker": "Frenzied rage and brutal attacks",
            "Path of the Totem Warrior": "Animal spirit guidance",
            "Path of the Ancestral Guardian": "Spiritual protection",
            "Path of the Storm Herald": "Elemental aura effects",
            "Path of the Zealot": "Divine rage and resurrection resistance"
        }
    },
    "Bard": {
        "hit_die": 8,
        "primary_ability": ["Charisma"],
        "saving_throws": ["Dexterity", "Charisma"],
        "subclasses": {
            "College of Lore": "Additional magical secrets and skills",
            "College of Valor": "Combat prowess and inspiration",
            "College of Glamour": "Fey magic and charm",
            "College of Whispers": "Secrets and psychological manipulation",
            "College of Swords": "Blade dancing and flourishes"
        }
    },
    "Cleric": {
        "hit_die": 8,
        "primary_ability": ["Wisdom"],
        "saving_throws": ["Wisdom", "Charisma"],
        "subclasses": {
            "Life Domain": "Healing and support magic",
            "Light Domain": "Radiant damage and illumination",
            "War Domain": "Combat blessing and weapon mastery",
            "Tempest Domain": "Lightning and thunder magic",
            "Nature Domain": "Plant and animal communion",
            "Trickery Domain": "Stealth and illusion magic",
            "Knowledge Domain": "Information and divination",
            "Death Domain": "Necromantic power"
        }
    },
    "Druid": {
        "hit_die": 8,
        "primary_ability": ["Wisdom"],
        "saving_throws": ["Intelligence", "Wisdom"],
        "subclasses": {
            "Circle of the Land": "Additional spells and spell recovery",
            "Circle of the Moon": "Enhanced wild shape abilities",
            "Circle of Dreams": "Healing and teleportation",
            "Circle of the Shepherd": "Beast summoning and support",
            "Circle of Spores": "Necromantic nature magic"
        }
    },
    "Fighter": {
        "hit_die": 10,
        "primary_ability": ["Strength", "Dexterity"],
        "saving_throws": ["Strength", "Constitution"],
        "subclasses": {
            "Champion": "Improved critical hits and survivability",
            "Battle Master": "Combat maneuvers and tactics",
            "Eldritch Knight": "Weapon and spell combination",
            "Arcane Archer": "Magical arrow effects",
            "Cavalier": "Mounted combat and protection",
            "Samurai": "Fighting spirit and social skills"
        }
    },
    "Monk": {
        "hit_die": 8,
        "primary_ability": ["Dexterity", "Wisdom"],
        "saving_throws": ["Strength", "Dexterity"],
        "subclasses": {
            "Way of the Open Hand": "Enhanced unarmed combat",
            "Way of Shadow": "Stealth and shadow magic",
            "Way of the Four Elements": "Elemental ki manipulation",
            "Way of the Long Death": "Life force manipulation",
            "Way of the Sun Soul": "Radiant energy projection",
            "Way of the Drunken Master": "Unpredictable fighting style"
        }
    },
    "Paladin": {
        "hit_die": 10,
        "primary_ability": ["Strength", "Charisma"],
        "saving_throws": ["Wisdom", "Charisma"],
        "subclasses": {
            "Oath of Devotion": "Classic holy warrior",
            "Oath of the Ancients": "Nature and fey protection",
            "Oath of Vengeance": "Relentless pursuit of justice",
            "Oath of Conquest": "Fear and domination",
            "Oath of Redemption": "Peace and rehabilitation",
            "Oathbreaker": "Fallen paladin with dark powers"
        }
    },
    "Ranger": {
        "hit_die": 10,
        "primary_ability": ["Dexterity", "Wisdom"],
        "saving_throws": ["Strength", "Dexterity"],
        "subclasses": {
            "Hunter": "Specialized monster hunting",
            "Beast Master": "Animal companion",
            "Gloom Stalker": "Darkvision and ambush tactics",
            "Horizon Walker": "Planar travel and detection",
            "Monster Slayer": "Anti-magic and creature knowledge",
            "Fey Wanderer": "Fey magic and charm resistance"
        }
    },
    "Rogue": {
        "hit_die": 8,
        "primary_ability": ["Dexterity"],
        "saving_throws": ["Dexterity", "Intelligence"],
        "subclasses": {
            "Thief": "Enhanced climbing and item use",
            "Assassin": "Disguise and poison expertise",
            "Arcane Trickster": "Magic and illusion",
            "Mastermind": "Social manipulation and help actions",
            "Swashbuckler": "Charismatic dueling",
            "Scout": "Mobility and survival skills",
            "Inquisitive": "Investigation and insight"
        }
    },
    "Sorcerer": {
        "hit_die": 6,
        "primary_ability": ["Charisma"],
        "saving_throws": ["Constitution", "Charisma"],
        "subclasses": {
            "Draconic Bloodline": "Dragon heritage and resilience",
            "Wild Magic": "Unpredictable magical surges",
            "Storm Sorcery": "Wind and lightning control",
            "Divine Soul": "Divine and arcane magic combination",
            "Shadow Magic": "Darkness and shadow manipulation",
            "Aberrant Mind": "Telepathic and alien magic"
        }
    },
    "Warlock": {
        "hit_die": 8,
        "primary_ability": ["Charisma"],
        "saving_throws": ["Wisdom", "Charisma"],
        "subclasses": {
            "The Fiend": "Infernal patron with fire resistance",
            "The Archfey": "Fey patron with charm abilities",
            "The Great Old One": "Cosmic horror patron with telepathy",
            "The Celestial": "Divine patron with healing abilities",
            "The Hexblade": "Sentient weapon patron",
            "The Genie": "Elemental patron with utility magic"
        }
    },
    "Wizard": {
        "hit_die": 6,
        "primary_ability": ["Intelligence"],
        "saving_throws": ["Intelligence", "Wisdom"],
        "subclasses": {
            "School of Abjuration": "Protective and dispelling magic",
            "School of Conjuration": "Summoning and teleportation",
            "School of Divination": "Future sight and information",
            "School of Enchantment": "Mind control and charm",
            "School of Evocation": "Damage and energy manipulation",
            "School of Illusion": "Deception and misdirection",
            "School of Necromancy": "Death and undeath magic",
            "School of Transmutation": "Change and transformation"
        }
    }
}

class Character:
    """Represents a D&D 5E character with all relevant stats and information."""
    
    def __init__(self, name: str = ""):
        self.name = name
        
        # Basic Character Info
        self.character_name = name
        self.character_class = ""
        self.subclass = ""
        self.level = 1
        self.background = ""
        self.player_name = ""
        self.race = ""
        self.alignment = ""
        self.experience_points = 0
        
        # Ability Scores
        self.strength = 10
        self.dexterity = 10
        self.constitution = 10
        self.intelligence = 10
        self.wisdom = 10
        self.charisma = 10
        
        # Proficiency and Combat Stats
        self.proficiency_bonus = 2
        self.armor_class = 10
        self.initiative = 0
        self.speed = 30
        self.hit_point_maximum = 8
        self.current_hit_points = 8
        self.temporary_hit_points = 0
        self.hit_dice = "1d8"
        
        # Saving Throws (proficiency)
        self.saving_throws = {
            "strength": False,
            "dexterity": False,
            "constitution": False,
            "intelligence": False,
            "wisdom": False,
            "charisma": False
        }
        
        # Skills (proficiency)
        self.skills = {
            "acrobatics": False, "animal_handling": False, "arcana": False,
            "athletics": False, "deception": False, "history": False,
            "insight": False, "intimidation": False, "investigation": False,
            "medicine": False, "nature": False, "perception": False,
            "performance": False, "persuasion": False, "religion": False,
            "sleight_of_hand": False, "stealth": False, "survival": False
        }
        
        # Spellcasting
        self.spellcasting_class = ""
        self.spellcasting_ability = ""
        self.spell_save_dc = 8
        self.spell_attack_bonus = 0
        self.spells_known = []
        self.spells_prepared = []
        self.spell_slots = {
            "1st": 0, "2nd": 0, "3rd": 0, "4th": 0, "5th": 0,
            "6th": 0, "7th": 0, "8th": 0, "9th": 0
        }
        self.spell_slots_expended = {
            "1st": 0, "2nd": 0, "3rd": 0, "4th": 0, "5th": 0,
            "6th": 0, "7th": 0, "8th": 0, "9th": 0
        }
        
        # Features and Traits
        self.features_and_traits = []
        self.custom_abilities = []
        
        # Other proficiencies
        self.languages = []
        self.other_proficiencies = []
    
    def get_ability_modifier(self, ability_score: int) -> int:
        """Calculate ability modifier from ability score."""
        return (ability_score - 10) // 2
    
    def get_skill_modifier(self, skill: str) -> int:
        """Calculate skill modifier including proficiency if applicable."""
        skill_ability_map = {
            "acrobatics": self.dexterity, "animal_handling": self.wisdom,
            "arcana": self.intelligence, "athletics": self.strength,
            "deception": self.charisma, "history": self.intelligence,
            "insight": self.wisdom, "intimidation": self.charisma,
            "investigation": self.intelligence, "medicine": self.wisdom,
            "nature": self.intelligence, "perception": self.wisdom,
            "performance": self.charisma, "persuasion": self.charisma,
            "religion": self.intelligence, "sleight_of_hand": self.dexterity,
            "stealth": self.dexterity, "survival": self.wisdom
        }
        
        ability_score = skill_ability_map.get(skill, 10)
        modifier = self.get_ability_modifier(ability_score)
        
        if self.skills.get(skill, False):
            modifier += self.proficiency_bonus
            
        return modifier
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert character to dictionary for JSON serialization."""
        return self.__dict__
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Character':
        """Create character from dictionary (JSON deserialization)."""
        character = cls()
        character.__dict__.update(data)
        return character


class CharacterManager:
    """Manages character data storage and retrieval."""
    
    def __init__(self, data_file: str = "characters.json"):
        self.data_file = data_file
        self.characters: Dict[str, Character] = {}
        self.load_characters()
    
    def load_characters(self):
        """Load characters from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    for name, char_data in data.items():
                        self.characters[name] = Character.from_dict(char_data)
                print(f"Loaded {len(self.characters)} characters.")
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Error loading characters: {e}")
                self.characters = {}
        else:
            print("No existing character file found. Starting fresh.")
    
    def save_characters(self):
        """Save characters to JSON file."""
        try:
            data = {name: char.to_dict() for name, char in self.characters.items()}
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            print("Characters saved successfully.")
        except Exception as e:
            print(f"Error saving characters: {e}")
    
    def add_character(self, character: Character):
        """Add a character to the manager."""
        self.characters[character.name] = character
    
    def get_character(self, name: str) -> Optional[Character]:
        """Get a character by name."""
        return self.characters.get(name)
    
    def list_characters(self) -> List[str]:
        """Get list of character names."""
        return list(self.characters.keys())
    
    def delete_character(self, name: str) -> bool:
        """Delete a character by name."""
        if name in self.characters:
            del self.characters[name]
            return True
        return False


class CharacterMakerCLI:
    """Command-line interface for the character maker."""
    
    def __init__(self):
        self.manager = CharacterManager()
        self.current_character: Optional[Character] = None
    
    def main_menu(self):
        """Display and handle the main menu."""
        while True:
            print("\n" + "="*50)
            print("D&D 5E CHARACTER MAKER")
            print("="*50)
            print("1. Create New Character")
            print("2. Load Existing Character")
            print("3. List All Characters")
            print("4. Delete Character")
            if self.current_character:
                print("5. Edit Current Character")
                print("6. Combat Reference")
                print(f"   Current: {self.current_character.name}")
            print("0. Save and Exit")
            
            try:
                choice = input("\nEnter your choice: ").strip()
                
                if choice == "1":
                    self.create_character()
                elif choice == "2":
                    self.load_character()
                elif choice == "3":
                    self.list_characters()
                elif choice == "4":
                    self.delete_character()
                elif choice == "5" and self.current_character:
                    self.edit_character_menu()
                elif choice == "6" and self.current_character:
                    self.combat_reference()
                elif choice == "0":
                    self.manager.save_characters()
                    print("Thank you for using D&D Character Maker!")
                    sys.exit(0)
                else:
                    print("Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n\nExiting...")
                self.manager.save_characters()
                sys.exit(0)
            except Exception as e:
                print(f"Error: {e}")
    
    def create_character(self):
        """Create a new character."""
        print("\n--- CREATE NEW CHARACTER ---")
        name = input("Character name: ").strip()
        
        if not name:
            print("Character name cannot be empty.")
            return
        
        if name in self.manager.characters:
            print(f"Character '{name}' already exists.")
            return
        
        character = Character(name)
        
        # Character creation wizard
        print(f"\nCreating character: {name}")
        print("Let's set up your character step by step...\n")
        
        # Basic information
        character.player_name = input("Player name (optional): ").strip()
        character.race = input("Race: ").strip()
        character.background = input("Background: ").strip()
        character.alignment = input("Alignment: ").strip()
        
        # Class and level selection
        self.select_class_and_subclass(character)
        self.select_level(character)
        
        # Set ability scores
        self.set_ability_scores(character)
        
        # Calculate level-based stats
        self.calculate_level_based_stats(character)
        
        # Set proficiencies
        self.set_proficiencies(character)
        
        # Set combat stats
        self.set_combat_stats(character)
        
        # Generate hit points
        self.generate_hit_points(character)
        
        # Apply class benefits
        self.apply_class_benefits(character)
        
        # Spellcasting setup (if applicable)
        if self.is_spellcaster_class(character.character_class):
            print(f"\n{character.character_class} is a spellcasting class. Setting up spellcasting...")
            self.setup_spellcasting(character)
        
        self.manager.add_character(character)
        self.current_character = character
        print(f"\nCharacter '{name}' created successfully!")
        print("You can now edit additional details using the Edit Character menu.")
    
    def load_character(self):
        """Load an existing character."""
        characters = self.manager.list_characters()
        
        if not characters:
            print("No characters available.")
            return
        
        print("\n--- LOAD CHARACTER ---")
        for i, name in enumerate(characters, 1):
            print(f"{i}. {name}")
        
        try:
            choice = int(input("Select character number: ")) - 1
            if 0 <= choice < len(characters):
                character_name = characters[choice]
                self.current_character = self.manager.get_character(character_name)
                print(f"Loaded character: {character_name}")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")
    
    def list_characters(self):
        """List all characters."""
        characters = self.manager.list_characters()
        
        if not characters:
            print("No characters found.")
            return
        
        print("\n--- ALL CHARACTERS ---")
        for name in characters:
            char = self.manager.get_character(name)
            class_info = f"{char.character_class} {char.level}" if hasattr(char, 'character_class') and hasattr(char, 'level') else getattr(char, 'class_level', 'Unknown')
            print(f"• {name} - {char.race} {class_info}")
    
    def delete_character(self):
        """Delete a character."""
        characters = self.manager.list_characters()
        
        if not characters:
            print("No characters to delete.")
            return
        
        print("\n--- DELETE CHARACTER ---")
        for i, name in enumerate(characters, 1):
            print(f"{i}. {name}")
        
        try:
            choice = int(input("Select character number to delete: ")) - 1
            if 0 <= choice < len(characters):
                character_name = characters[choice]
                confirm = input(f"Delete '{character_name}'? (y/N): ").strip().lower()
                if confirm == 'y':
                    self.manager.delete_character(character_name)
                    if self.current_character and self.current_character.name == character_name:
                        self.current_character = None
                    print(f"Character '{character_name}' deleted.")
                else:
                    print("Deletion cancelled.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")
    
    def edit_character_menu(self):
        """Character editing menu."""
        while True:
            char = self.current_character
            print(f"\n--- EDITING: {char.name} ---")
            print("1. Basic Information")
            print("2. Ability Scores")
            print("3. Combat Stats")
            print("4. Proficiencies")
            print("5. Spellcasting")
            print("6. Features & Traits")
            print("7. View Character Sheet")
            print("0. Return to Main Menu")
            
            choice = input("\nChoose section to edit: ").strip()
            
            if choice == "1":
                self.edit_basic_info()
            elif choice == "2":
                self.edit_ability_scores()
            elif choice == "3":
                self.edit_combat_stats()
            elif choice == "4":
                self.edit_proficiencies()
            elif choice == "5":
                self.edit_spellcasting()
            elif choice == "6":
                self.edit_features()
            elif choice == "7":
                self.view_character_sheet()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please try again.")
    
    def edit_basic_info(self):
        """Edit basic character information."""
        char = self.current_character
        print(f"\n--- BASIC INFORMATION ---")
        print(f"Current values (press Enter to keep current):")
        
        new_name = input(f"Character name [{char.character_name}]: ").strip()
        if new_name:
            old_name = char.name
            char.character_name = new_name
            char.name = new_name
            # Update in manager
            self.manager.characters[new_name] = char
            if old_name != new_name and old_name in self.manager.characters:
                del self.manager.characters[old_name]
        
        new_player = input(f"Player name [{char.player_name}]: ").strip()
        if new_player:
            char.player_name = new_player
        
        new_race = input(f"Race [{char.race}]: ").strip()
        if new_race:
            char.race = new_race
        
        # Handle both old and new character format
        current_class_info = f"{char.character_class} {char.level}" if hasattr(char, 'character_class') and hasattr(char, 'level') else getattr(char, 'class_level', '')
        
        print(f"Current class: {current_class_info}")
        if input("Change class? (y/n): ").lower().startswith('y'):
            self.select_class_and_subclass(char)
            self.select_level(char)
            self.recalculate_level_stats(char)
        
        new_background = input(f"Background [{char.background}]: ").strip()
        if new_background:
            char.background = new_background
        
        new_alignment = input(f"Alignment [{char.alignment}]: ").strip()
        if new_alignment:
            char.alignment = new_alignment
        
        new_xp = input(f"Experience points [{char.experience_points}]: ").strip()
        if new_xp:
            try:
                char.experience_points = int(new_xp)
            except ValueError:
                print("Invalid experience points value.")
        
        print("Basic information updated!")
    
    def edit_ability_scores(self):
        """Edit character ability scores."""
        char = self.current_character
        print(f"\n--- ABILITY SCORES ---")
        print("Current values (press Enter to keep current):")
        
        abilities = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
        
        for ability in abilities:
            current_score = getattr(char, ability)
            current_mod = char.get_ability_modifier(current_score)
            new_score = input(f"{ability.capitalize()} [{current_score} ({current_mod:+d})]: ").strip()
            if new_score:
                try:
                    score = int(new_score)
                    if 1 <= score <= 30:
                        setattr(char, ability, score)
                    else:
                        print(f"Score must be between 1 and 30.")
                except ValueError:
                    print(f"Invalid score for {ability}.")
        
        # Recalculate derived stats
        char.initiative = char.get_ability_modifier(char.dexterity)
        if char.spellcasting_ability:
            self.recalculate_spell_stats(char)
        
        print("Ability scores updated!")
    
    def edit_combat_stats(self):
        """Edit combat-related stats."""
        char = self.current_character
        print(f"\n--- COMBAT STATS ---")
        
        new_ac = input(f"Armor Class [{char.armor_class}]: ").strip()
        if new_ac:
            try:
                char.armor_class = int(new_ac)
            except ValueError:
                print("Invalid AC value.")
        
        print(f"Initiative [{char.initiative:+d}] (auto-calculated from DEX)")
        
        new_speed = input(f"Speed [{char.speed}]: ").strip()
        if new_speed:
            try:
                char.speed = int(new_speed)
            except ValueError:
                print("Invalid speed value.")
        
        new_max_hp = input(f"Max hit points [{char.hit_point_maximum}]: ").strip()
        if new_max_hp:
            try:
                char.hit_point_maximum = int(new_max_hp)
            except ValueError:
                print("Invalid max HP value.")
        
        new_current_hp = input(f"Current hit points [{char.current_hit_points}]: ").strip()
        if new_current_hp:
            try:
                char.current_hit_points = int(new_current_hp)
            except ValueError:
                print("Invalid current HP value.")
        
        new_temp_hp = input(f"Temporary hit points [{char.temporary_hit_points}]: ").strip()
        if new_temp_hp:
            try:
                char.temporary_hit_points = int(new_temp_hp)
            except ValueError:
                print("Invalid temp HP value.")
        
        new_hit_dice = input(f"Hit dice [{char.hit_dice}]: ").strip()
        if new_hit_dice:
            char.hit_dice = new_hit_dice
        
        print("Combat stats updated!")
    
    def edit_proficiencies(self):
        """Edit character proficiencies."""
        char = self.current_character
        print(f"\n--- PROFICIENCIES ---")
        print("1. Saving Throws")
        print("2. Skills")
        print("3. Languages")
        print("4. Other Proficiencies")
        print("0. Back")
        
        choice = input("Choose: ").strip()
        
        if choice == "1":
            print("\nSaving Throw Proficiencies:")
            for save in char.saving_throws:
                current = "Yes" if char.saving_throws[save] else "No"
                response = input(f"  {save.capitalize()} [{current}] (y/n): ").strip().lower()
                if response in ['y', 'n']:
                    char.saving_throws[save] = response == 'y'
        
        elif choice == "2":
            print("\nSkill Proficiencies:")
            for skill in char.skills:
                current = "Yes" if char.skills[skill] else "No"
                skill_display = skill.replace('_', ' ').title()
                response = input(f"  {skill_display} [{current}] (y/n): ").strip().lower()
                if response in ['y', 'n']:
                    char.skills[skill] = response == 'y'
        
        elif choice == "3":
            print(f"\nLanguages: {', '.join(char.languages) if char.languages else 'None'}")
            print("Enter languages separated by commas (or press Enter to keep current):")
            new_languages = input().strip()
            if new_languages:
                char.languages = [lang.strip() for lang in new_languages.split(',')]
        
        elif choice == "4":
            print(f"\nOther Proficiencies: {', '.join(char.other_proficiencies) if char.other_proficiencies else 'None'}")
            print("Enter proficiencies separated by commas (or press Enter to keep current):")
            new_profs = input().strip()
            if new_profs:
                char.other_proficiencies = [prof.strip() for prof in new_profs.split(',')]
    
    def edit_spellcasting(self):
        """Edit spellcasting information."""
        char = self.current_character
        print(f"\n--- SPELLCASTING ---")
        
        if not char.spellcasting_class:
            response = input("Enable spellcasting for this character? (y/n): ").strip().lower()
            if not response.startswith('y'):
                return
            
            char.spellcasting_class = input("Spellcasting class: ").strip()
            print("Spellcasting ability: 1. Intelligence  2. Wisdom  3. Charisma")
            while True:
                choice = input("Choose (1-3): ").strip()
                if choice == "1":
                    char.spellcasting_ability = "intelligence"
                    break
                elif choice == "2":
                    char.spellcasting_ability = "wisdom"
                    break
                elif choice == "3":
                    char.spellcasting_ability = "charisma"
                    break
                else:
                    print("Please choose 1, 2, or 3.")
        
        self.recalculate_spell_stats(char)
        
        print(f"Spellcasting class: {char.spellcasting_class}")
        print(f"Spellcasting ability: {char.spellcasting_ability}")
        print(f"Spell save DC: {char.spell_save_dc}")
        print(f"Spell attack bonus: +{char.spell_attack_bonus}")
        
        print("\nSpell Slots:")
        for level in ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th"]:
            current = char.spell_slots[level]
            if current > 0 or level == "1st":
                new_slots = input(f"  {level} level [{current}]: ").strip()
                if new_slots:
                    try:
                        char.spell_slots[level] = int(new_slots)
                        char.spell_slots_expended[level] = 0  # Reset expended
                    except ValueError:
                        print(f"Invalid value for {level} level slots.")
        
        print("Spellcasting updated!")
    
    def edit_features(self):
        """Edit features and traits."""
        char = self.current_character
        print(f"\n--- FEATURES & TRAITS ---")
        
        if char.features_and_traits:
            print("Current features:")
            for i, feature in enumerate(char.features_and_traits, 1):
                print(f"  {i}. {feature}")
        else:
            print("No features currently defined.")
        
        print("\n1. Add Feature")
        print("2. Remove Feature")
        print("3. Edit Feature")
        print("0. Back")
        
        choice = input("Choose: ").strip()
        
        if choice == "1":
            feature = input("Enter new feature: ").strip()
            if feature:
                char.features_and_traits.append(feature)
                print("Feature added!")
        
        elif choice == "2" and char.features_and_traits:
            try:
                index = int(input("Enter feature number to remove: ")) - 1
                if 0 <= index < len(char.features_and_traits):
                    removed = char.features_and_traits.pop(index)
                    print(f"Removed: {removed}")
                else:
                    print("Invalid feature number.")
            except ValueError:
                print("Please enter a valid number.")
        
        elif choice == "3" and char.features_and_traits:
            try:
                index = int(input("Enter feature number to edit: ")) - 1
                if 0 <= index < len(char.features_and_traits):
                    current = char.features_and_traits[index]
                    new_feature = input(f"Edit feature [{current}]: ").strip()
                    if new_feature:
                        char.features_and_traits[index] = new_feature
                        print("Feature updated!")
                else:
                    print("Invalid feature number.")
            except ValueError:
                print("Please enter a valid number.")
    
    def view_character_sheet(self):
        """Display a formatted character sheet."""
        char = self.current_character
        print(f"\n{'='*60}")
        print(f"CHARACTER SHEET: {char.name}")
        print(f"{'='*60}")
        print(f"Player: {char.player_name}")
        class_info = f"{char.character_class} {char.level}" if hasattr(char, 'character_class') and hasattr(char, 'level') else getattr(char, 'class_level', 'Unknown')
        subclass_info = f" ({char.subclass})" if hasattr(char, 'subclass') and char.subclass else ""
        print(f"Race: {char.race} | Class: {class_info}{subclass_info}")
        print(f"Background: {char.background} | Alignment: {char.alignment}")
        print(f"Experience: {char.experience_points}")
        
        print(f"\n--- ABILITY SCORES ---")
        abilities = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
        for ability in abilities:
            score = getattr(char, ability)
            mod = char.get_ability_modifier(score)
            print(f"{ability.capitalize()}: {score} ({mod:+d})")
        
        print(f"\n--- COMBAT STATS ---")
        print(f"Armor Class: {char.armor_class}")
        print(f"Initiative: {char.initiative:+d}")
        print(f"Speed: {char.speed} ft")
        print(f"Hit Points: {char.current_hit_points}/{char.hit_point_maximum}")
        if char.temporary_hit_points > 0:
            print(f"Temporary HP: {char.temporary_hit_points}")
        print(f"Hit Dice: {char.hit_dice}")
        print(f"Proficiency Bonus: +{char.proficiency_bonus}")
        
        # Saving throws
        print(f"\n--- SAVING THROWS ---")
        for save in char.saving_throws:
            if char.saving_throws[save]:
                ability_score = getattr(char, save)
                mod = char.get_ability_modifier(ability_score) + char.proficiency_bonus
                print(f"{save.capitalize()}: {mod:+d} (proficient)")
        
        # Skills
        print(f"\n--- SKILLS ---")
        for skill in char.skills:
            if char.skills[skill]:
                mod = char.get_skill_modifier(skill)
                skill_display = skill.replace('_', ' ').title()
                print(f"{skill_display}: {mod:+d}")
        
        # Spellcasting
        if char.spellcasting_class:
            print(f"\n--- SPELLCASTING ---")
            print(f"Class: {char.spellcasting_class}")
            print(f"Ability: {char.spellcasting_ability.capitalize()}")
            print(f"Spell Save DC: {char.spell_save_dc}")
            print(f"Spell Attack: {char.spell_attack_bonus:+d}")
            
            print("Spell Slots:")
            for level in ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th"]:
                total = char.spell_slots[level]
                used = char.spell_slots_expended[level]
                if total > 0:
                    print(f"  {level}: {total-used}/{total}")
        
        # Features
        if char.features_and_traits:
            print(f"\n--- FEATURES & TRAITS ---")
            for feature in char.features_and_traits:
                print(f"• {feature}")
        
        # Languages and proficiencies
        if char.languages:
            print(f"\n--- LANGUAGES ---")
            print(", ".join(char.languages))
        
        if char.other_proficiencies:
            print(f"\n--- OTHER PROFICIENCIES ---")
            print(", ".join(char.other_proficiencies))
        
        print(f"\n{'='*60}")
        input("Press Enter to continue...")
    
    def recalculate_level_stats(self, character: Character):
        """Recalculate level-dependent stats when level changes."""
        # Get level from new format or old format
        level = getattr(character, 'level', 1)
        if level == 1 and hasattr(character, 'class_level') and character.class_level:
            import re
            level_match = re.search(r'(\d+)', character.class_level)
            if level_match:
                level = int(level_match.group(1))
        
        character.proficiency_bonus = 2 + ((level - 1) // 4)
        character.initiative = character.get_ability_modifier(character.dexterity)
        
        if hasattr(character, 'spellcasting_ability') and character.spellcasting_ability:
            self.recalculate_spell_stats(character)
    
    def recalculate_spell_stats(self, character: Character):
        """Recalculate spellcasting stats when ability scores change."""
        if character.spellcasting_ability:
            ability_mod = character.get_ability_modifier(getattr(character, character.spellcasting_ability))
            character.spell_save_dc = 8 + character.proficiency_bonus + ability_mod
            character.spell_attack_bonus = character.proficiency_bonus + ability_mod
    
    def combat_reference(self):
        """Quick combat reference for easy access during gameplay."""
        while True:
            char = self.current_character
            print(f"\n{'='*50}")
            print(f"COMBAT REFERENCE: {char.name}")
            print(f"{'='*50}")
            
            # Core combat stats
            print(f"AC: {char.armor_class} | Initiative: {char.initiative:+d} | Speed: {char.speed} ft")
            print(f"HP: {char.current_hit_points}/{char.hit_point_maximum}", end="")
            if char.temporary_hit_points > 0:
                print(f" (+{char.temporary_hit_points} temp)")
            else:
                print()
            print(f"Proficiency: +{char.proficiency_bonus}")
            
            print(f"\n--- MENU ---")
            print("1. Manage Hit Points")
            print("2. View Ability Modifiers") 
            print("3. View Saving Throws")
            print("4. View Skills")
            print("5. Spellcasting Quick Ref")
            print("6. Attack Calculations")
            print("7. Conditions & Notes")
            print("0. Back to Main Menu")
            
            choice = input("\nSelect: ").strip()
            
            if choice == "1":
                self.manage_hit_points()
            elif choice == "2":
                self.view_ability_modifiers()
            elif choice == "3":
                self.view_saving_throws()
            elif choice == "4":
                self.view_skills()
            elif choice == "5":
                self.spellcasting_quick_ref()
            elif choice == "6":
                self.attack_calculations()
            elif choice == "7":
                self.conditions_notes()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
    
    def manage_hit_points(self):
        """Manage character hit points during combat."""
        char = self.current_character
        
        while True:
            print(f"\n--- HIT POINTS ---")
            print(f"Current: {char.current_hit_points}/{char.hit_point_maximum}")
            if char.temporary_hit_points > 0:
                print(f"Temporary: {char.temporary_hit_points}")
            
            print("\n1. Take Damage")
            print("2. Heal Damage")
            print("3. Add Temporary HP")
            print("4. Remove Temporary HP")
            print("5. Set Current HP")
            print("0. Back")
            
            choice = input("\nSelect: ").strip()
            
            if choice == "1":
                try:
                    damage = int(input("Damage taken: "))
                    # Apply to temp HP first
                    if char.temporary_hit_points > 0:
                        temp_lost = min(damage, char.temporary_hit_points)
                        char.temporary_hit_points -= temp_lost
                        damage -= temp_lost
                    
                    # Apply remaining damage to current HP
                    char.current_hit_points = max(0, char.current_hit_points - damage)
                    print(f"HP after damage: {char.current_hit_points}/{char.hit_point_maximum}")
                    
                    if char.current_hit_points == 0:
                        print("⚠️  CHARACTER IS UNCONSCIOUS!")
                        
                except ValueError:
                    print("Invalid damage value.")
            
            elif choice == "2":
                try:
                    healing = int(input("Healing received: "))
                    char.current_hit_points = min(char.hit_point_maximum, 
                                                 char.current_hit_points + healing)
                    print(f"HP after healing: {char.current_hit_points}/{char.hit_point_maximum}")
                except ValueError:
                    print("Invalid healing value.")
            
            elif choice == "3":
                try:
                    temp_hp = int(input("Temporary HP gained: "))
                    # Temp HP doesn't stack, take the higher value
                    char.temporary_hit_points = max(char.temporary_hit_points, temp_hp)
                    print(f"Temporary HP: {char.temporary_hit_points}")
                except ValueError:
                    print("Invalid temporary HP value.")
            
            elif choice == "4":
                char.temporary_hit_points = 0
                print("Temporary HP removed.")
            
            elif choice == "5":
                try:
                    new_hp = int(input(f"Set current HP (0-{char.hit_point_maximum}): "))
                    if 0 <= new_hp <= char.hit_point_maximum:
                        char.current_hit_points = new_hp
                        print(f"HP set to: {char.current_hit_points}/{char.hit_point_maximum}")
                    else:
                        print(f"HP must be between 0 and {char.hit_point_maximum}")
                except ValueError:
                    print("Invalid HP value.")
            
            elif choice == "0":
                break
    
    def view_ability_modifiers(self):
        """Quick view of ability scores and modifiers."""
        char = self.current_character
        print(f"\n--- ABILITY MODIFIERS ---")
        
        abilities = [
            ("STR", char.strength),
            ("DEX", char.dexterity), 
            ("CON", char.constitution),
            ("INT", char.intelligence),
            ("WIS", char.wisdom),
            ("CHA", char.charisma)
        ]
        
        for name, score in abilities:
            mod = char.get_ability_modifier(score)
            print(f"{name}: {score} ({mod:+d})")
        
        input("\nPress Enter to continue...")
    
    def view_saving_throws(self):
        """View saving throw bonuses."""
        char = self.current_character
        print(f"\n--- SAVING THROWS ---")
        
        saves = [
            ("Strength", char.strength, char.saving_throws["strength"]),
            ("Dexterity", char.dexterity, char.saving_throws["dexterity"]),
            ("Constitution", char.constitution, char.saving_throws["constitution"]),
            ("Intelligence", char.intelligence, char.saving_throws["intelligence"]),
            ("Wisdom", char.wisdom, char.saving_throws["wisdom"]),
            ("Charisma", char.charisma, char.saving_throws["charisma"])
        ]
        
        for name, score, proficient in saves:
            mod = char.get_ability_modifier(score)
            if proficient:
                mod += char.proficiency_bonus
                print(f"{name}: {mod:+d} (proficient)")
            else:
                print(f"{name}: {mod:+d}")
        
        input("\nPress Enter to continue...")
    
    def view_skills(self):
        """View skill bonuses."""
        char = self.current_character
        print(f"\n--- SKILLS ---")
        
        # Group skills by ability
        skill_groups = {
            "Strength": ["athletics"],
            "Dexterity": ["acrobatics", "sleight_of_hand", "stealth"],
            "Intelligence": ["arcana", "history", "investigation", "nature", "religion"],
            "Wisdom": ["animal_handling", "insight", "medicine", "perception", "survival"],
            "Charisma": ["deception", "intimidation", "performance", "persuasion"]
        }
        
        for ability, skills in skill_groups.items():
            print(f"\n{ability}:")
            for skill in skills:
                if char.skills.get(skill, False):
                    mod = char.get_skill_modifier(skill)
                    skill_display = skill.replace('_', ' ').title()
                    print(f"  {skill_display}: {mod:+d} (proficient)")
        
        input("\nPress Enter to continue...")
    
    def spellcasting_quick_ref(self):
        """Quick spellcasting reference."""
        char = self.current_character
        
        if not char.spellcasting_class:
            print("\nThis character is not a spellcaster.")
            input("Press Enter to continue...")
            return
        
        while True:
            print(f"\n--- SPELLCASTING REFERENCE ---")
            print(f"Class: {char.spellcasting_class}")
            print(f"Ability: {char.spellcasting_ability.capitalize()}")
            print(f"Spell Save DC: {char.spell_save_dc}")
            print(f"Spell Attack Bonus: {char.spell_attack_bonus:+d}")
            
            print(f"\nSpell Slots:")
            for level in ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th"]:
                total = char.spell_slots[level]
                used = char.spell_slots_expended[level]
                if total > 0:
                    remaining = total - used
                    print(f"  {level}: {remaining}/{total} remaining")
            
            print(f"\n1. Use Spell Slot")
            print(f"2. Recover Spell Slot")
            print(f"3. Reset All Slots")
            print(f"0. Back")
            
            choice = input("\nSelect: ").strip()
            
            if choice == "1":
                level = input("Spell level to use (1st, 2nd, etc.): ").strip()
                if level in char.spell_slots and char.spell_slots[level] > 0:
                    if char.spell_slots_expended[level] < char.spell_slots[level]:
                        char.spell_slots_expended[level] += 1
                        remaining = char.spell_slots[level] - char.spell_slots_expended[level]
                        print(f"{level} level slot used. {remaining} remaining.")
                    else:
                        print(f"No {level} level slots remaining!")
                else:
                    print("Invalid spell level or no slots of that level.")
            
            elif choice == "2":
                level = input("Spell level to recover (1st, 2nd, etc.): ").strip()
                if level in char.spell_slots and char.spell_slots_expended[level] > 0:
                    char.spell_slots_expended[level] -= 1
                    remaining = char.spell_slots[level] - char.spell_slots_expended[level]
                    print(f"{level} level slot recovered. {remaining} remaining.")
                else:
                    print("Invalid spell level or no expended slots of that level.")
            
            elif choice == "3":
                for level in char.spell_slots_expended:
                    char.spell_slots_expended[level] = 0
                print("All spell slots recovered!")
            
            elif choice == "0":
                break
    
    def attack_calculations(self):
        """Help calculate attack bonuses."""
        char = self.current_character
        print(f"\n--- ATTACK CALCULATIONS ---")
        
        print(f"Proficiency Bonus: +{char.proficiency_bonus}")
        print(f"Strength Modifier: {char.get_ability_modifier(char.strength):+d}")
        print(f"Dexterity Modifier: {char.get_ability_modifier(char.dexterity):+d}")
        
        print(f"\nCommon Attack Bonuses:")
        print(f"  Melee (STR): {char.proficiency_bonus + char.get_ability_modifier(char.strength):+d}")
        print(f"  Ranged (DEX): {char.proficiency_bonus + char.get_ability_modifier(char.dexterity):+d}")
        print(f"  Finesse (DEX): {char.proficiency_bonus + char.get_ability_modifier(char.dexterity):+d}")
        
        if char.spellcasting_class:
            print(f"  Spell Attack: {char.spell_attack_bonus:+d}")
        
        print(f"\nDamage Modifiers:")
        print(f"  Strength: {char.get_ability_modifier(char.strength):+d}")
        print(f"  Dexterity: {char.get_ability_modifier(char.dexterity):+d}")
        
        input("\nPress Enter to continue...")
    
    def conditions_notes(self):
        """Simple conditions and notes tracker."""
        char = self.current_character
        
        if not hasattr(char, 'conditions'):
            char.conditions = []
        if not hasattr(char, 'combat_notes'):
            char.combat_notes = []
        
        while True:
            print(f"\n--- CONDITIONS & NOTES ---")
            
            if char.conditions:
                print("Active Conditions:")
                for i, condition in enumerate(char.conditions, 1):
                    print(f"  {i}. {condition}")
            else:
                print("No active conditions.")
            
            if char.combat_notes:
                print("\nCombat Notes:")
                for i, note in enumerate(char.combat_notes, 1):
                    print(f"  {i}. {note}")
            else:
                print("\nNo combat notes.")
            
            print(f"\n1. Add Condition")
            print(f"2. Remove Condition")
            print(f"3. Add Note")
            print(f"4. Remove Note")
            print(f"5. Clear All")
            print(f"0. Back")
            
            choice = input("\nSelect: ").strip()
            
            if choice == "1":
                condition = input("Add condition: ").strip()
                if condition:
                    char.conditions.append(condition)
                    print(f"Added condition: {condition}")
            
            elif choice == "2" and char.conditions:
                try:
                    index = int(input("Remove condition number: ")) - 1
                    if 0 <= index < len(char.conditions):
                        removed = char.conditions.pop(index)
                        print(f"Removed: {removed}")
                    else:
                        print("Invalid condition number.")
                except ValueError:
                    print("Please enter a valid number.")
            
            elif choice == "3":
                note = input("Add note: ").strip()
                if note:
                    char.combat_notes.append(note)
                    print(f"Added note: {note}")
            
            elif choice == "4" and char.combat_notes:
                try:
                    index = int(input("Remove note number: ")) - 1
                    if 0 <= index < len(char.combat_notes):
                        removed = char.combat_notes.pop(index)
                        print(f"Removed: {removed}")
                    else:
                        print("Invalid note number.")
                except ValueError:
                    print("Please enter a valid number.")
            
            elif choice == "5":
                char.conditions = []
                char.combat_notes = []
                print("All conditions and notes cleared.")
            
            elif choice == "0":
                break
    
    def set_ability_scores(self, character: Character):
        """Set character ability scores."""
        print("\n--- ABILITY SCORES ---")
        print("Enter ability scores (8-20):")
        
        abilities = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
        
        for ability in abilities:
            while True:
                try:
                    score = input(f"{ability.capitalize()}: ").strip()
                    if score:
                        score = int(score)
                        if 1 <= score <= 30:  # Allow for magical enhancement
                            setattr(character, ability, score)
                            break
                        else:
                            print("Score must be between 1 and 30.")
                    else:
                        print("Using default score of 10.")
                        break
                except ValueError:
                    print("Please enter a valid number.")
    
    def calculate_level_based_stats(self, character: Character):
        """Calculate stats based on character level."""
        print("\n--- CALCULATING LEVEL-BASED STATS ---")
        
        # Get level (should already be set by select_level)
        level = getattr(character, 'level', 1)
        
        # Calculate proficiency bonus
        character.proficiency_bonus = 2 + ((level - 1) // 4)
        
        print(f"Proficiency bonus: +{character.proficiency_bonus}")
        
        # Hit dice will be set based on character class during HP generation
        if hasattr(character, 'character_class') and character.character_class in DND_CLASSES:
            hit_die = DND_CLASSES[character.character_class]["hit_die"]
            character.hit_dice = f"{level}d{hit_die}"
            print(f"Hit dice: {character.hit_dice}")
    
    def set_proficiencies(self, character: Character):
        """Set character proficiencies."""
        print("\n--- PROFICIENCIES ---")
        
        # Saving throws
        print("Saving throw proficiencies (press Enter to skip):")
        for save in character.saving_throws:
            response = input(f"  {save.capitalize()} saving throw? (y/n): ").strip().lower()
            character.saving_throws[save] = response.startswith('y')
        
        # Skills
        print("\nSkill proficiencies (press Enter to skip):")
        skill_groups = [
            ["acrobatics", "animal_handling", "arcana", "athletics"],
            ["deception", "history", "insight", "intimidation"],
            ["investigation", "medicine", "nature", "perception"],
            ["performance", "persuasion", "religion", "sleight_of_hand"],
            ["stealth", "survival"]
        ]
        
        for group in skill_groups:
            for skill in group:
                skill_display = skill.replace('_', ' ').title()
                response = input(f"  {skill_display}? (y/n): ").strip().lower()
                character.skills[skill] = response.startswith('y')
                if len([s for s in group if character.skills.get(s, False)]) >= 2:
                    break  # Limit to prevent too many skills
    
    def set_combat_stats(self, character: Character):
        """Set combat-related stats."""
        print("\n--- COMBAT STATS ---")
        
        # Armor Class
        while True:
            try:
                ac_input = input(f"Armor Class (default 10 + DEX mod = {10 + character.get_ability_modifier(character.dexterity)}): ").strip()
                if ac_input:
                    character.armor_class = int(ac_input)
                    break
                else:
                    character.armor_class = 10 + character.get_ability_modifier(character.dexterity)
                    break
            except ValueError:
                print("Please enter a valid number.")
        
        # Initiative
        character.initiative = character.get_ability_modifier(character.dexterity)
        
        # Speed
        while True:
            try:
                speed_input = input("Speed in feet (default 30): ").strip()
                if speed_input:
                    character.speed = int(speed_input)
                    break
                else:
                    character.speed = 30
                    break
            except ValueError:
                print("Please enter a valid number.")
        
        print(f"AC: {character.armor_class}")
        print(f"Initiative: +{character.initiative}")
        print(f"Speed: {character.speed} ft")
    
    def setup_spellcasting(self, character: Character):
        """Setup basic spellcasting information."""
        print("\n--- SPELLCASTING SETUP ---")
        
        character.spellcasting_class = input("Spellcasting class: ").strip()
        
        print("Spellcasting ability:")
        print("1. Intelligence  2. Wisdom  3. Charisma")
        while True:
            choice = input("Choose (1-3): ").strip()
            if choice == "1":
                character.spellcasting_ability = "intelligence"
                ability_mod = character.get_ability_modifier(character.intelligence)
                break
            elif choice == "2":
                character.spellcasting_ability = "wisdom"
                ability_mod = character.get_ability_modifier(character.wisdom)
                break
            elif choice == "3":
                character.spellcasting_ability = "charisma"
                ability_mod = character.get_ability_modifier(character.charisma)
                break
            else:
                print("Please choose 1, 2, or 3.")
        
        # Calculate spell save DC and attack bonus
        character.spell_save_dc = 8 + character.proficiency_bonus + ability_mod
        character.spell_attack_bonus = character.proficiency_bonus + ability_mod
        
        # Set spell slots (simplified - just ask for total)
        print("Enter number of spell slots per level (0 for none):")
        for level in ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th"]:
            try:
                slots = input(f"  {level} level slots: ").strip()
                if slots:
                    character.spell_slots[level] = int(slots)
                else:
                    break  # Stop at first empty entry
            except ValueError:
                print("Invalid number, skipping.")
        
        print(f"Spell save DC: {character.spell_save_dc}")
        print(f"Spell attack bonus: +{character.spell_attack_bonus}")
    
    def select_class_and_subclass(self, character: Character):
        """Select character class and subclass."""
        print("\n--- CLASS SELECTION ---")
        print("Choose your character class:")
        
        classes = list(DND_CLASSES.keys())
        for i, class_name in enumerate(classes, 1):
            class_data = DND_CLASSES[class_name]
            primary_abilities = "/".join(class_data["primary_ability"])
            print(f"{i:2d}. {class_name} (HD: d{class_data['hit_die']}, Primary: {primary_abilities})")
        
        while True:
            try:
                choice = int(input(f"\nSelect class (1-{len(classes)}): ")) - 1
                if 0 <= choice < len(classes):
                    selected_class = classes[choice]
                    character.character_class = selected_class
                    
                    # Show class details
                    class_data = DND_CLASSES[selected_class]
                    print(f"\n--- {selected_class.upper()} ---")
                    print(f"Hit Die: d{class_data['hit_die']}")
                    print(f"Primary Ability: {', '.join(class_data['primary_ability'])}")
                    print(f"Saving Throw Proficiencies: {', '.join(class_data['saving_throws'])}")
                    
                    # Apply saving throw proficiencies
                    for save in class_data["saving_throws"]:
                        character.saving_throws[save.lower()] = True
                    
                    break
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Subclass selection
        self.select_subclass(character)
    
    def select_subclass(self, character: Character):
        """Select character subclass."""
        class_data = DND_CLASSES[character.character_class]
        subclasses = list(class_data["subclasses"].items())
        
        print(f"\n--- {character.character_class.upper()} SUBCLASSES ---")
        for i, (subclass_name, description) in enumerate(subclasses, 1):
            print(f"{i:2d}. {subclass_name}")
            print(f"     {description}")
        
        while True:
            try:
                choice = int(input(f"\nSelect subclass (1-{len(subclasses)}): ")) - 1
                if 0 <= choice < len(subclasses):
                    character.subclass = subclasses[choice][0]
                    print(f"\nSelected: {character.subclass}")
                    break
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
    
    def select_level(self, character: Character):
        """Select character level."""
        print("\n--- LEVEL SELECTION ---")
        
        while True:
            try:
                level = int(input("Enter character level (1-20): "))
                if 1 <= level <= 20:
                    character.level = level
                    print(f"Level set to: {level}")
                    break
                else:
                    print("Level must be between 1 and 20.")
            except ValueError:
                print("Please enter a valid number.")
    
    def generate_hit_points(self, character: Character):
        """Generate hit points with option for random or manual entry."""
        print("\n--- HIT POINTS ---")
        class_data = DND_CLASSES[character.character_class]
        hit_die = class_data["hit_die"]
        con_mod = character.get_ability_modifier(character.constitution)
        
        # Calculate HP options
        max_hp = hit_die + con_mod + (character.level - 1) * (hit_die + con_mod)
        avg_hp = hit_die + con_mod + (character.level - 1) * (int(hit_die/2) + 1 + con_mod)
        
        print(f"Class: {character.character_class} (d{hit_die} hit die)")
        print(f"Constitution Modifier: {con_mod:+d}")
        print(f"Level: {character.level}")
        
        print(f"\nHP Calculation Options:")
        print(f"1. Maximum HP: {max_hp}")
        print(f"2. Average HP: {avg_hp}")
        print(f"3. Roll for HP (random)")
        print(f"4. Enter custom HP")
        
        while True:
            choice = input("\nSelect HP method (1-4): ").strip()
            
            if choice == "1":
                character.hit_point_maximum = max_hp
                character.current_hit_points = max_hp
                print(f"HP set to maximum: {max_hp}")
                break
            elif choice == "2":
                character.hit_point_maximum = avg_hp
                character.current_hit_points = avg_hp
                print(f"HP set to average: {avg_hp}")
                break
            elif choice == "3":
                rolled_hp = self.roll_hit_points(character, hit_die, con_mod)
                character.hit_point_maximum = rolled_hp
                character.current_hit_points = rolled_hp
                print(f"Rolled HP: {rolled_hp}")
                break
            elif choice == "4":
                while True:
                    try:
                        custom_hp = int(input("Enter custom HP: "))
                        if custom_hp > 0:
                            character.hit_point_maximum = custom_hp
                            character.current_hit_points = custom_hp
                            print(f"HP set to: {custom_hp}")
                            return
                        else:
                            print("HP must be positive.")
                    except ValueError:
                        print("Please enter a valid number.")
            else:
                print("Invalid choice. Please select 1-4.")
    
    def roll_hit_points(self, character: Character, hit_die: int, con_mod: int) -> int:
        """Roll hit points for each level."""
        total_hp = hit_die + con_mod  # Max HP at 1st level
        
        if character.level > 1:
            print(f"\nRolling HP for levels 2-{character.level}:")
            for level in range(2, character.level + 1):
                roll = random.randint(1, hit_die)
                level_hp = roll + con_mod
                total_hp += level_hp
                print(f"  Level {level}: d{hit_die} = {roll} + {con_mod} = {level_hp}")
        
        return total_hp
    
    def apply_class_benefits(self, character: Character):
        """Apply class-specific benefits and features."""
        class_name = character.character_class
        level = character.level
        
        # Add basic class features
        features = []
        
        # Universal features
        if class_name == "Barbarian":
            features.extend(["Rage", "Unarmored Defense"])
            if level >= 2:
                features.append("Reckless Attack")
                features.append("Danger Sense")
        elif class_name == "Bard":
            features.extend(["Bardic Inspiration", "Spellcasting"])
            if level >= 2:
                features.append("Jack of All Trades")
                features.append("Song of Rest")
        elif class_name == "Cleric":
            features.extend(["Spellcasting", "Divine Domain"])
            if level >= 2:
                features.append("Channel Divinity")
        elif class_name == "Druid":
            features.extend(["Druidcraft", "Spellcasting"])
            if level >= 2:
                features.append("Wild Shape")
                features.append("Druid Circle")
        elif class_name == "Fighter":
            features.extend(["Fighting Style", "Second Wind"])
            if level >= 2:
                features.append("Action Surge")
        elif class_name == "Monk":
            features.extend(["Unarmored Defense", "Martial Arts"])
            if level >= 2:
                features.append("Ki")
                features.append("Unarmored Movement")
        elif class_name == "Paladin":
            features.extend(["Divine Sense", "Lay on Hands"])
            if level >= 2:
                features.append("Fighting Style")
                features.append("Spellcasting")
                features.append("Divine Smite")
        elif class_name == "Ranger":
            features.extend(["Favored Enemy", "Natural Explorer"])
            if level >= 2:
                features.append("Fighting Style")
                features.append("Spellcasting")
        elif class_name == "Rogue":
            features.extend(["Expertise", "Sneak Attack", "Thieves' Cant"])
            if level >= 2:
                features.append("Cunning Action")
        elif class_name == "Sorcerer":
            features.extend(["Spellcasting", "Sorcerous Origin"])
            if level >= 2:
                features.append("Font of Magic")
        elif class_name == "Warlock":
            features.extend(["Otherworldly Patron", "Pact Magic"])
            if level >= 2:
                features.append("Eldritch Invocations")
        elif class_name == "Wizard":
            features.extend(["Spellcasting", "Arcane Recovery"])
            if level >= 2:
                features.append("Arcane Tradition")
        elif class_name == "Artificer":
            features.extend(["Magical Tinkering", "Spellcasting"])
            if level >= 2:
                features.append("Infuse Item")
        
        # Add subclass feature
        features.append(f"{character.subclass} features")
        
        # Add to character (avoid duplicates)
        for feature in features:
            if feature not in character.features_and_traits:
                character.features_and_traits.append(feature)
        
        print(f"\nApplied {class_name} features:")
        for feature in features:
            print(f"  • {feature}")
    
    def is_spellcaster_class(self, class_name: str) -> bool:
        """Check if a class is a spellcaster."""
        spellcaster_classes = [
            "Artificer", "Bard", "Cleric", "Druid", "Paladin", 
            "Ranger", "Sorcerer", "Warlock", "Wizard"
        ]
        return class_name in spellcaster_classes


def main():
    """Main entry point."""
    cli = CharacterMakerCLI()
    cli.main_menu()


if __name__ == "__main__":
    main() 
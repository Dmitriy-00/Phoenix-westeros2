# -*- coding: utf-8 -*-
"""
Core data models for the detective visual novel.
All game entities are represented as Python classes with JSON serialization support.
"""

init -10 python:
    import json
    from datetime import datetime

    class GameEntity:
        """Base class for all game entities with JSON serialization support."""

        def __init__(self, entity_id, name=""):
            self.id = entity_id
            self.name = name

        def to_dict(self):
            """Convert entity to dictionary for JSON serialization."""
            return self.__dict__.copy()

        @classmethod
        def from_dict(cls, data):
            """Create entity from dictionary (JSON deserialization)."""
            raise NotImplementedError("Subclasses must implement from_dict")


    class Character(GameEntity):
        """Represents a character in the game."""

        def __init__(self, char_id, name="", title="", faction_id=None,
                     description="", base_relationship=0, traits=None,
                     emotion_sprites=None):
            super(Character, self).__init__(char_id, name)
            self.title = title
            self.faction_id = faction_id
            self.description = description
            self.base_relationship = base_relationship
            self.current_relationship = base_relationship
            self.traits = traits or []
            self.emotion_sprites = emotion_sprites or {}
            self.is_alive = True
            self.location_id = None

        def modify_relationship(self, amount):
            """Modify relationship value, clamped between -100 and 100."""
            self.current_relationship = max(-100, min(100, self.current_relationship + amount))
            return self.current_relationship

        def get_sprite(self, emotion="neutral"):
            """Get character sprite for specific emotion."""
            return self.emotion_sprites.get(emotion, self.emotion_sprites.get("neutral", ""))

        @classmethod
        def from_dict(cls, data):
            char = cls(
                char_id=data.get("id", ""),
                name=data.get("name", ""),
                title=data.get("title", ""),
                faction_id=data.get("faction_id"),
                description=data.get("description", ""),
                base_relationship=data.get("base_relationship", 0),
                traits=data.get("traits", []),
                emotion_sprites=data.get("emotion_sprites", {})
            )
            char.current_relationship = data.get("current_relationship", char.base_relationship)
            char.is_alive = data.get("is_alive", True)
            char.location_id = data.get("location_id")
            return char


    class Faction(GameEntity):
        """Represents a faction (house, order, guild) in the game."""

        def __init__(self, faction_id, name="", faction_type="noble_house",
                     description="", base_reputation=0, relations=None):
            super(Faction, self).__init__(faction_id, name)
            self.type = faction_type
            self.description = description
            self.base_reputation = base_reputation
            self.current_reputation = base_reputation
            self.relations = relations or {}  # faction_id -> relationship value
            self.controlled_locations = []

        def modify_reputation(self, amount):
            """Modify reputation with this faction, clamped between -100 and 100."""
            self.current_reputation = max(-100, min(100, self.current_reputation + amount))
            return self.current_reputation

        def get_relation_with(self, other_faction_id):
            """Get relationship value with another faction."""
            return self.relations.get(other_faction_id, 0)

        @classmethod
        def from_dict(cls, data):
            faction = cls(
                faction_id=data.get("id", ""),
                name=data.get("name", ""),
                faction_type=data.get("type", "noble_house"),
                description=data.get("description", ""),
                base_reputation=data.get("base_reputation", 0),
                relations=data.get("relations", {})
            )
            faction.current_reputation = data.get("current_reputation", faction.base_reputation)
            faction.controlled_locations = data.get("controlled_locations", [])
            return faction


    class Location(GameEntity):
        """Represents a location in the game world."""

        def __init__(self, loc_id, name="", region="", loc_type="city",
                     description="", is_unlocked=False, map_position=None,
                     available_sublocations=None):
            super(Location, self).__init__(loc_id, name)
            self.region = region
            self.type = loc_type
            self.description = description
            self.is_unlocked = is_unlocked
            self.map_position = map_position or {"x": 0.5, "y": 0.5}
            self.available_sublocations = available_sublocations or []
            self.controlling_faction_id = None
            self.danger_level = 0
            self.time_of_day = "day"

        def unlock(self):
            """Unlock this location for travel."""
            self.is_unlocked = True

        def lock(self):
            """Lock this location."""
            self.is_unlocked = False

        @classmethod
        def from_dict(cls, data):
            location = cls(
                loc_id=data.get("id", ""),
                name=data.get("name", ""),
                region=data.get("region", ""),
                loc_type=data.get("type", "city"),
                description=data.get("description", ""),
                is_unlocked=data.get("is_unlocked", False),
                map_position=data.get("map_position", {"x": 0.5, "y": 0.5}),
                available_sublocations=data.get("available_sublocations", [])
            )
            location.controlling_faction_id = data.get("controlling_faction_id")
            location.danger_level = data.get("danger_level", 0)
            location.time_of_day = data.get("time_of_day", "day")
            return location


    class Clue(GameEntity):
        """Represents a piece of evidence/clue in an investigation."""

        def __init__(self, clue_id, name="", clue_type="item", description="",
                     reliability=100, related_characters=None, related_locations=None,
                     tags=None):
            super(Clue, self).__init__(clue_id, name)
            self.type = clue_type
            self.description = description
            self.reliability = reliability
            self.related_characters = related_characters or []
            self.related_locations = related_locations or []
            self.tags = tags or []
            self.discovered = False
            self.timestamp = None

        def discover(self):
            """Mark this clue as discovered."""
            self.discovered = True
            self.timestamp = datetime.now().isoformat()

        @classmethod
        def from_dict(cls, data):
            clue = cls(
                clue_id=data.get("id", ""),
                name=data.get("name", ""),
                clue_type=data.get("type", "item"),
                description=data.get("description", ""),
                reliability=data.get("reliability", 100),
                related_characters=data.get("related_characters", []),
                related_locations=data.get("related_locations", []),
                tags=data.get("tags", [])
            )
            clue.discovered = data.get("discovered", False)
            clue.timestamp = data.get("timestamp")
            return clue


    class DialogueNode(GameEntity):
        """Represents a node in a dialogue tree."""

        def __init__(self, node_id, speaker_id="", emotion="neutral", text="",
                     choices=None, conditions=None, effects=None):
            super(DialogueNode, self).__init__(node_id, "")
            self.speaker_id = speaker_id
            self.emotion = emotion
            self.text = text
            self.choices = choices or []  # List of choice dicts
            self.conditions = conditions or {}  # Conditions to show this node
            self.effects = effects or {}  # Effects when this node is shown

        def check_conditions(self, game_state):
            """Check if conditions are met to show this node."""
            # TODO: Implement condition checking logic
            return True

        def apply_effects(self, game_state):
            """Apply effects when this node is executed."""
            # TODO: Implement effects application
            pass

        @classmethod
        def from_dict(cls, data):
            return cls(
                node_id=data.get("id", ""),
                speaker_id=data.get("speaker_id", ""),
                emotion=data.get("emotion", "neutral"),
                text=data.get("text", ""),
                choices=data.get("choices", []),
                conditions=data.get("conditions", {}),
                effects=data.get("effects", {})
            )


    class InterrogationStatement:
        """Represents a single statement in an interrogation scene."""

        def __init__(self, stmt_id, text="", emotion="neutral",
                     correct_evidence=None, press_response="",
                     evidence_response=None):
            self.id = stmt_id
            self.text = text
            self.emotion = emotion
            self.correct_evidence = correct_evidence or []  # List of clue IDs
            self.press_response = press_response
            self.evidence_response = evidence_response or {}  # clue_id -> response text

        @classmethod
        def from_dict(cls, data):
            return cls(
                stmt_id=data.get("id", ""),
                text=data.get("text", ""),
                emotion=data.get("emotion", "neutral"),
                correct_evidence=data.get("correct_evidence", []),
                press_response=data.get("press_response", ""),
                evidence_response=data.get("evidence_response", {})
            )


    class InterrogationScene(GameEntity):
        """Represents an interrogation/trial scene (Phoenix Wright style)."""

        def __init__(self, scene_id, name="", character_id="", statements=None,
                     max_mistakes=3, success_effects=None, failure_effects=None):
            super(InterrogationScene, self).__init__(scene_id, name)
            self.character_id = character_id
            self.statements = statements or []  # List of InterrogationStatement objects
            self.max_mistakes = max_mistakes
            self.current_mistakes = 0
            self.success_effects = success_effects or {}
            self.failure_effects = failure_effects or {}
            self.completed = False

        def add_mistake(self):
            """Add a mistake to the counter."""
            self.current_mistakes += 1
            return self.current_mistakes >= self.max_mistakes

        def reset_mistakes(self):
            """Reset mistake counter."""
            self.current_mistakes = 0

        @classmethod
        def from_dict(cls, data):
            scene = cls(
                scene_id=data.get("id", ""),
                name=data.get("name", ""),
                character_id=data.get("character_id", ""),
                statements=[InterrogationStatement.from_dict(s) for s in data.get("statements", [])],
                max_mistakes=data.get("max_mistakes", 3),
                success_effects=data.get("success_effects", {}),
                failure_effects=data.get("failure_effects", {})
            )
            scene.current_mistakes = data.get("current_mistakes", 0)
            scene.completed = data.get("completed", False)
            return scene


    class CaseEnding:
        """Represents a possible ending for a case."""

        def __init__(self, ending_id, name="", conditions=None, description="",
                     effects=None):
            self.id = ending_id
            self.name = name
            self.conditions = conditions or {}
            self.description = description
            self.effects = effects or {}

        @classmethod
        def from_dict(cls, data):
            return cls(
                ending_id=data.get("id", ""),
                name=data.get("name", ""),
                conditions=data.get("conditions", {}),
                description=data.get("description", ""),
                effects=data.get("effects", {})
            )


    class Case(GameEntity):
        """Represents an investigation case/scenario."""

        def __init__(self, case_id, title="", short_description="", difficulty=1,
                     starting_location_id="", allowed_locations=None,
                     key_characters=None, required_clues_to_solve=None,
                     endings=None):
            super(Case, self).__init__(case_id, title)
            self.short_description = short_description
            self.difficulty = difficulty
            self.starting_location_id = starting_location_id
            self.allowed_locations = allowed_locations or []
            self.key_characters = key_characters or []
            self.required_clues_to_solve = required_clues_to_solve or []
            self.endings = endings or []  # List of CaseEnding objects
            self.current_stage = 0
            self.completed = False
            self.discovered_clues = []
            self.flags = {}

        def advance_stage(self):
            """Advance to next stage of the case."""
            self.current_stage += 1

        def add_discovered_clue(self, clue_id):
            """Add a clue to discovered clues list."""
            if clue_id not in self.discovered_clues:
                self.discovered_clues.append(clue_id)

        def check_solution_requirements(self):
            """Check if all required clues have been discovered."""
            return all(clue_id in self.discovered_clues for clue_id in self.required_clues_to_solve)

        def set_flag(self, flag_name, value):
            """Set a case flag."""
            self.flags[flag_name] = value

        def get_flag(self, flag_name, default=None):
            """Get a case flag value."""
            return self.flags.get(flag_name, default)

        @classmethod
        def from_dict(cls, data):
            case = cls(
                case_id=data.get("id", ""),
                title=data.get("title", ""),
                short_description=data.get("short_description", ""),
                difficulty=data.get("difficulty", 1),
                starting_location_id=data.get("starting_location_id", ""),
                allowed_locations=data.get("allowed_locations", []),
                key_characters=data.get("key_characters", []),
                required_clues_to_solve=data.get("required_clues_to_solve", []),
                endings=[CaseEnding.from_dict(e) for e in data.get("endings", [])]
            )
            case.current_stage = data.get("current_stage", 0)
            case.completed = data.get("completed", False)
            case.discovered_clues = data.get("discovered_clues", [])
            case.flags = data.get("flags", {})
            return case


    class WorldMap(GameEntity):
        """Represents the world map with regions and locations."""

        def __init__(self, map_id="world_map", name="World Map", regions=None):
            super(WorldMap, self).__init__(map_id, name)
            self.regions = regions or {}  # region_name -> {description, locations: [loc_ids]}
            self.current_location_id = None

        def get_locations_in_region(self, region_name):
            """Get all location IDs in a specific region."""
            return self.regions.get(region_name, {}).get("locations", [])

        def set_current_location(self, location_id):
            """Set the player's current location."""
            self.current_location_id = location_id

        @classmethod
        def from_dict(cls, data):
            world_map = cls(
                map_id=data.get("id", "world_map"),
                name=data.get("name", "World Map"),
                regions=data.get("regions", {})
            )
            world_map.current_location_id = data.get("current_location_id")
            return world_map


    class GameState:
        """Main game state container holding all game data."""

        def __init__(self):
            # Entity registries
            self.characters = {}  # char_id -> Character
            self.factions = {}    # faction_id -> Faction
            self.locations = {}   # loc_id -> Location
            self.clues = {}       # clue_id -> Clue
            self.cases = {}       # case_id -> Case
            self.world_map = None # WorldMap instance

            # Current game session data
            self.current_case_id = None
            self.current_location_id = None
            self.discovered_clues = []
            self.player_inventory = []

            # Dialogue and scene management
            self.dialogue_nodes = {}  # node_id -> DialogueNode
            self.interrogation_scenes = {}  # scene_id -> InterrogationScene

            # Flags and variables
            self.story_flags = {}
            self.temp_vars = {}

        def get_character(self, char_id):
            """Get character by ID."""
            return self.characters.get(char_id)

        def get_faction(self, faction_id):
            """Get faction by ID."""
            return self.factions.get(faction_id)

        def get_location(self, loc_id):
            """Get location by ID."""
            return self.locations.get(loc_id)

        def get_clue(self, clue_id):
            """Get clue by ID."""
            return self.clues.get(clue_id)

        def get_case(self, case_id):
            """Get case by ID."""
            return self.cases.get(case_id)

        def get_current_case(self):
            """Get the currently active case."""
            return self.cases.get(self.current_case_id) if self.current_case_id else None

        def discover_clue(self, clue_id):
            """Discover a new clue."""
            if clue_id not in self.discovered_clues:
                self.discovered_clues.append(clue_id)
                clue = self.get_clue(clue_id)
                if clue:
                    clue.discover()
                # Also add to current case if one is active
                current_case = self.get_current_case()
                if current_case:
                    current_case.add_discovered_clue(clue_id)

        def set_flag(self, flag_name, value):
            """Set a story flag."""
            self.story_flags[flag_name] = value

        def get_flag(self, flag_name, default=None):
            """Get a story flag value."""
            return self.story_flags.get(flag_name, default)

        def modify_character_relationship(self, char_id, amount):
            """Modify relationship with a character."""
            character = self.get_character(char_id)
            if character:
                return character.modify_relationship(amount)
            return 0

        def modify_faction_reputation(self, faction_id, amount):
            """Modify reputation with a faction."""
            faction = self.get_faction(faction_id)
            if faction:
                return faction.modify_reputation(amount)
            return 0

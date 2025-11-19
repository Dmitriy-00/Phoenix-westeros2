# -*- coding: utf-8 -*-
"""
Data loader system for loading and saving JSON data files.
Handles deserialization of JSON into game objects and serialization back to JSON.
"""

init -9 python:
    import json
    import os
    import codecs

    class DataLoader:
        """Handles loading and saving of all game data from/to JSON files."""

        def __init__(self, data_path="game/data"):
            self.data_path = data_path
            self.encoding = "utf-8"

        def _get_file_path(self, filename):
            """Get full path to a data file."""
            # In Ren'Py, we need to use renpy.config.gamedir
            if hasattr(renpy.config, 'gamedir'):
                base_path = renpy.config.gamedir
            else:
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            return os.path.join(base_path, "data", filename)

        def load_json_file(self, filename):
            """Load and parse a JSON file."""
            file_path = self._get_file_path(filename)
            try:
                # Try using Ren'Py's file loading first
                try:
                    with renpy.file(os.path.join("data", filename)) as f:
                        content = f.read().decode(self.encoding)
                        return json.loads(content)
                except:
                    # Fall back to regular file loading
                    with codecs.open(file_path, 'r', encoding=self.encoding) as f:
                        return json.load(f)
            except IOError as e:
                print("Warning: Could not load {}: {}".format(filename, str(e)))
                return None
            except json.JSONDecodeError as e:
                print("Error: Invalid JSON in {}: {}".format(filename, str(e)))
                return None

        def save_json_file(self, filename, data):
            """Save data to a JSON file."""
            file_path = self._get_file_path(filename)
            try:
                with codecs.open(file_path, 'w', encoding=self.encoding) as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                return True
            except IOError as e:
                print("Error: Could not save {}: {}".format(filename, str(e)))
                return False

        def load_characters(self, game_state):
            """Load all characters from characters.json."""
            data = self.load_json_file("characters.json")
            if data and "characters" in data:
                for char_data in data["characters"]:
                    character = Character.from_dict(char_data)
                    game_state.characters[character.id] = character
                print("Loaded {} characters".format(len(game_state.characters)))
            return game_state.characters

        def load_factions(self, game_state):
            """Load all factions from factions.json."""
            data = self.load_json_file("factions.json")
            if data and "factions" in data:
                for faction_data in data["factions"]:
                    faction = Faction.from_dict(faction_data)
                    game_state.factions[faction.id] = faction
                print("Loaded {} factions".format(len(game_state.factions)))
            return game_state.factions

        def load_locations(self, game_state):
            """Load all locations from locations.json."""
            data = self.load_json_file("locations.json")
            if data and "locations" in data:
                for loc_data in data["locations"]:
                    location = Location.from_dict(loc_data)
                    game_state.locations[location.id] = location
                print("Loaded {} locations".format(len(game_state.locations)))
            return game_state.locations

        def load_clues(self, game_state):
            """Load all clues from clues.json."""
            data = self.load_json_file("clues.json")
            if data and "clues" in data:
                for clue_data in data["clues"]:
                    clue = Clue.from_dict(clue_data)
                    game_state.clues[clue.id] = clue
                print("Loaded {} clues".format(len(game_state.clues)))
            return game_state.clues

        def load_cases(self, game_state):
            """Load all cases from cases.json."""
            data = self.load_json_file("cases.json")
            if data and "cases" in data:
                for case_data in data["cases"]:
                    case = Case.from_dict(case_data)
                    game_state.cases[case.id] = case
                print("Loaded {} cases".format(len(game_state.cases)))
            return game_state.cases

        def load_world_map(self, game_state):
            """Load world map from world_map.json."""
            data = self.load_json_file("world_map.json")
            if data:
                game_state.world_map = WorldMap.from_dict(data)
                print("Loaded world map: {}".format(game_state.world_map.name))
            return game_state.world_map

        def load_dialogue_nodes(self, filename):
            """Load dialogue nodes from a specific JSON file."""
            data = self.load_json_file(filename)
            nodes = {}
            if data and "nodes" in data:
                for node_data in data["nodes"]:
                    node = DialogueNode.from_dict(node_data)
                    nodes[node.id] = node
            return nodes

        def load_interrogation_scene(self, filename):
            """Load an interrogation scene from a specific JSON file."""
            data = self.load_json_file(filename)
            if data:
                return InterrogationScene.from_dict(data)
            return None

        def load_all_game_data(self, game_state):
            """Load all game data into the game state."""
            print("Loading game data...")
            self.load_characters(game_state)
            self.load_factions(game_state)
            self.load_locations(game_state)
            self.load_clues(game_state)
            self.load_cases(game_state)
            self.load_world_map(game_state)
            print("Game data loaded successfully!")
            return game_state

        def save_characters(self, game_state):
            """Save all characters to characters.json."""
            data = {
                "characters": [char.to_dict() for char in game_state.characters.values()]
            }
            return self.save_json_file("characters.json", data)

        def save_factions(self, game_state):
            """Save all factions to factions.json."""
            data = {
                "factions": [faction.to_dict() for faction in game_state.factions.values()]
            }
            return self.save_json_file("factions.json", data)

        def save_locations(self, game_state):
            """Save all locations to locations.json."""
            data = {
                "locations": [loc.to_dict() for loc in game_state.locations.values()]
            }
            return self.save_json_file("locations.json", data)

        def save_clues(self, game_state):
            """Save all clues to clues.json."""
            data = {
                "clues": [clue.to_dict() for clue in game_state.clues.values()]
            }
            return self.save_json_file("clues.json", data)

        def save_cases(self, game_state):
            """Save all cases to cases.json."""
            data = {
                "cases": [case.to_dict() for case in game_state.cases.values()]
            }
            return self.save_json_file("cases.json", data)

        def save_world_map(self, game_state):
            """Save world map to world_map.json."""
            if game_state.world_map:
                return self.save_json_file("world_map.json", game_state.world_map.to_dict())
            return False

        def save_all_game_data(self, game_state):
            """Save all game data from the game state."""
            print("Saving game data...")
            success = True
            success = success and self.save_characters(game_state)
            success = success and self.save_factions(game_state)
            success = success and self.save_locations(game_state)
            success = success and self.save_clues(game_state)
            success = success and self.save_cases(game_state)
            success = success and self.save_world_map(game_state)
            if success:
                print("Game data saved successfully!")
            else:
                print("Warning: Some data may not have been saved correctly.")
            return success

    # Create global data loader instance
    data_loader = DataLoader()

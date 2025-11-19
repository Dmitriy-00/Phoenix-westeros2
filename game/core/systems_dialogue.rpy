# -*- coding: utf-8 -*-
"""
Dialogue system for managing conversations from JSON data.
Supports branching choices, conditions, and effects.
"""

init -5 python:

    class DialogueManager:
        """Manages dialogue execution from JSON-based dialogue trees."""

        def __init__(self, game_state):
            self.game_state = game_state
            self.current_dialogue_id = None
            self.current_node_id = None
            self.dialogue_history = []

        def start_dialogue(self, dialogue_id, starting_node_id="start"):
            """Start a dialogue sequence."""
            self.current_dialogue_id = dialogue_id
            self.current_node_id = starting_node_id
            self.dialogue_history = []

        def get_current_node(self):
            """Get the current dialogue node."""
            if self.current_node_id:
                return self.game_state.dialogue_nodes.get(self.current_node_id)
            return None

        def go_to_node(self, node_id):
            """Navigate to a specific dialogue node."""
            if node_id in self.dialogue_history:
                print("Warning: Potential dialogue loop detected at node {}".format(node_id))
            self.dialogue_history.append(self.current_node_id)
            self.current_node_id = node_id

        def check_condition(self, condition):
            """
            Check if a condition is met.
            Condition format: {"type": "flag", "flag": "flag_name", "value": true}
                             {"type": "relationship", "character": "char_id", "min": 50}
                             {"type": "has_clue", "clue_id": "clue_id"}
            """
            if not condition:
                return True

            cond_type = condition.get("type")

            if cond_type == "flag":
                flag_name = condition.get("flag")
                required_value = condition.get("value")
                actual_value = self.game_state.get_flag(flag_name)
                return actual_value == required_value

            elif cond_type == "relationship":
                char_id = condition.get("character")
                min_rel = condition.get("min", -101)
                max_rel = condition.get("max", 101)
                character = self.game_state.get_character(char_id)
                if character:
                    rel = character.current_relationship
                    return min_rel <= rel <= max_rel
                return False

            elif cond_type == "has_clue":
                clue_id = condition.get("clue_id")
                return clue_id in self.game_state.discovered_clues

            elif cond_type == "faction_reputation":
                faction_id = condition.get("faction")
                min_rep = condition.get("min", -101)
                max_rep = condition.get("max", 101)
                faction = self.game_state.get_faction(faction_id)
                if faction:
                    rep = faction.current_reputation
                    return min_rep <= rep <= max_rep
                return False

            elif cond_type == "not":
                # Negation of another condition
                inner_condition = condition.get("condition")
                return not self.check_condition(inner_condition)

            elif cond_type == "and":
                # All conditions must be true
                conditions = condition.get("conditions", [])
                return all(self.check_condition(c) for c in conditions)

            elif cond_type == "or":
                # At least one condition must be true
                conditions = condition.get("conditions", [])
                return any(self.check_condition(c) for c in conditions)

            return True

        def apply_effect(self, effect):
            """
            Apply an effect from dialogue.
            Effect format: {"type": "set_flag", "flag": "flag_name", "value": true}
                          {"type": "modify_relationship", "character": "char_id", "amount": 10}
                          {"type": "discover_clue", "clue_id": "clue_id"}
                          {"type": "unlock_location", "location_id": "loc_id"}
            """
            if not effect:
                return

            effect_type = effect.get("type")

            if effect_type == "set_flag":
                flag_name = effect.get("flag")
                value = effect.get("value")
                self.game_state.set_flag(flag_name, value)
                print("Flag set: {} = {}".format(flag_name, value))

            elif effect_type == "modify_relationship":
                char_id = effect.get("character")
                amount = effect.get("amount", 0)
                new_rel = self.game_state.modify_character_relationship(char_id, amount)
                character = self.game_state.get_character(char_id)
                if character:
                    print("Relationship with {} changed by {}: now {}".format(
                        character.name, amount, new_rel))

            elif effect_type == "modify_reputation":
                faction_id = effect.get("faction")
                amount = effect.get("amount", 0)
                new_rep = self.game_state.modify_faction_reputation(faction_id, amount)
                faction = self.game_state.get_faction(faction_id)
                if faction:
                    print("Reputation with {} changed by {}: now {}".format(
                        faction.name, amount, new_rep))

            elif effect_type == "discover_clue":
                clue_id = effect.get("clue_id")
                self.game_state.discover_clue(clue_id)
                clue = self.game_state.get_clue(clue_id)
                if clue:
                    renpy.notify("Улика найдена: {}".format(clue.name))

            elif effect_type == "unlock_location":
                location_id = effect.get("location_id")
                location = self.game_state.get_location(location_id)
                if location:
                    location.unlock()
                    print("Location unlocked: {}".format(location.name))

            elif effect_type == "advance_case":
                current_case = self.game_state.get_current_case()
                if current_case:
                    current_case.advance_stage()
                    print("Case advanced to stage {}".format(current_case.current_stage))

            elif effect_type == "set_case_flag":
                flag_name = effect.get("flag")
                value = effect.get("value")
                current_case = self.game_state.get_current_case()
                if current_case:
                    current_case.set_flag(flag_name, value)

        def apply_effects(self, effects):
            """Apply multiple effects."""
            if isinstance(effects, dict):
                self.apply_effect(effects)
            elif isinstance(effects, list):
                for effect in effects:
                    self.apply_effect(effect)

        def get_available_choices(self, node):
            """Get all available choices from current node based on conditions."""
            if not node or not node.choices:
                return []

            available = []
            for choice in node.choices:
                # Check if choice conditions are met
                conditions = choice.get("conditions", [])
                if isinstance(conditions, dict):
                    conditions = [conditions]

                all_conditions_met = True
                for condition in conditions:
                    if not self.check_condition(condition):
                        all_conditions_met = False
                        break

                if all_conditions_met:
                    available.append(choice)

            return available

        def execute_choice(self, choice):
            """Execute a choice and apply its effects."""
            # Apply choice effects
            effects = choice.get("effects", [])
            self.apply_effects(effects)

            # Navigate to next node
            next_node = choice.get("next_node")
            if next_node:
                if next_node == "end":
                    self.end_dialogue()
                else:
                    self.go_to_node(next_node)
            else:
                self.end_dialogue()

        def end_dialogue(self):
            """End the current dialogue."""
            self.current_dialogue_id = None
            self.current_node_id = None

    # Helper function for use in Ren'Py scripts
    def show_dialogue_node(node, character_obj):
        """Display a dialogue node with character sprite and emotion."""
        if not node:
            return

        # Get character sprite
        emotion = node.emotion
        sprite = character_obj.get_sprite(emotion) if character_obj else ""

        # Show character with emotion
        if sprite:
            renpy.show(sprite)

        # Return the text to be displayed
        return node.text

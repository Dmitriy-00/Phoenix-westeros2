# -*- coding: utf-8 -*-
"""
Relationship and reputation system.
Manages relationships with characters and faction reputations.
"""

init -5 python:

    class RelationshipManager:
        """Manages relationships with characters and factions."""

        def __init__(self, game_state):
            self.game_state = game_state

        def get_relationship_level(self, relationship_value):
            """Convert numerical relationship to descriptive level."""
            if relationship_value >= 75:
                return "Excellent"
            elif relationship_value >= 50:
                return "Good"
            elif relationship_value >= 25:
                return "Friendly"
            elif relationship_value >= -25:
                return "Neutral"
            elif relationship_value >= -50:
                return "Unfriendly"
            elif relationship_value >= -75:
                return "Hostile"
            else:
                return "Enemy"

        def get_reputation_level(self, reputation_value):
            """Convert numerical reputation to descriptive level."""
            if reputation_value >= 75:
                return "Revered"
            elif reputation_value >= 50:
                return "Honored"
            elif reputation_value >= 25:
                return "Respected"
            elif reputation_value >= -25:
                return "Neutral"
            elif reputation_value >= -50:
                return "Distrusted"
            elif reputation_value >= -75:
                return "Despised"
            else:
                return "Hated"

        def modify_character_relationship(self, char_id, amount, reason=""):
            """
            Modify relationship with a character.
            Also affects their faction if applicable.
            """
            character = self.game_state.get_character(char_id)
            if not character:
                return 0

            old_value = character.current_relationship
            new_value = character.modify_relationship(amount)

            # Log the change
            if reason:
                print("Relationship with {} changed by {} ({}): {} -> {}".format(
                    character.name, amount, reason, old_value, new_value))

            # Also affect faction reputation (smaller amount)
            if character.faction_id:
                faction_amount = int(amount * 0.3)  # 30% of character relationship change
                if faction_amount != 0:
                    self.modify_faction_reputation(character.faction_id, faction_amount,
                                                   "through {}".format(character.name))

            return new_value

        def modify_faction_reputation(self, faction_id, amount, reason=""):
            """
            Modify reputation with a faction.
            May also affect relationships with key members.
            """
            faction = self.game_state.get_faction(faction_id)
            if not faction:
                return 0

            old_value = faction.current_reputation
            new_value = faction.modify_reputation(amount)

            # Log the change
            if reason:
                print("Reputation with {} changed by {} ({}): {} -> {}".format(
                    faction.name, amount, reason, old_value, new_value))

            return new_value

        def get_character_relationship_info(self, char_id):
            """Get detailed relationship information for a character."""
            character = self.game_state.get_character(char_id)
            if not character:
                return None

            return {
                "character": character,
                "value": character.current_relationship,
                "level": self.get_relationship_level(character.current_relationship),
                "change": character.current_relationship - character.base_relationship
            }

        def get_faction_reputation_info(self, faction_id):
            """Get detailed reputation information for a faction."""
            faction = self.game_state.get_faction(faction_id)
            if not faction:
                return None

            return {
                "faction": faction,
                "value": faction.current_reputation,
                "level": self.get_reputation_level(faction.current_reputation),
                "change": faction.current_reputation - faction.base_reputation
            }

        def get_all_relationships(self):
            """Get relationship info for all known characters."""
            relationships = []
            for char_id, character in self.game_state.characters.items():
                info = self.get_character_relationship_info(char_id)
                if info:
                    relationships.append(info)
            return relationships

        def get_all_reputations(self):
            """Get reputation info for all factions."""
            reputations = []
            for faction_id, faction in self.game_state.factions.items():
                info = self.get_faction_reputation_info(faction_id)
                if info:
                    reputations.append(info)
            return reputations

        def check_relationship_threshold(self, char_id, threshold):
            """Check if relationship with character meets or exceeds threshold."""
            character = self.game_state.get_character(char_id)
            if character:
                return character.current_relationship >= threshold
            return False

        def check_reputation_threshold(self, faction_id, threshold):
            """Check if reputation with faction meets or exceeds threshold."""
            faction = self.game_state.get_faction(faction_id)
            if faction:
                return faction.current_reputation >= threshold
            return False

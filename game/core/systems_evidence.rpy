# -*- coding: utf-8 -*-
"""
Evidence/Clue management system.
Handles discovery, organization, and presentation of evidence.
"""

init -5 python:

    class EvidenceManager:
        """Manages the evidence/clue system."""

        def __init__(self, game_state):
            self.game_state = game_state
            self.selected_clue_id = None

        def discover_clue(self, clue_id, notify=True):
            """Discover a new clue and add it to the investigation."""
            clue = self.game_state.get_clue(clue_id)
            if not clue:
                print("Warning: Clue {} not found".format(clue_id))
                return False

            if clue_id in self.game_state.discovered_clues:
                print("Clue {} already discovered".format(clue_id))
                return False

            # Mark as discovered
            self.game_state.discover_clue(clue_id)

            # Notify player
            if notify:
                renpy.notify("Улика найдена: {}".format(clue.name))
                print("Discovered clue: {} - {}".format(clue.name, clue.description))

            return True

        def get_discovered_clues(self):
            """Get all discovered clues."""
            clues = []
            for clue_id in self.game_state.discovered_clues:
                clue = self.game_state.get_clue(clue_id)
                if clue:
                    clues.append(clue)
            return clues

        def get_clues_by_type(self, clue_type):
            """Get discovered clues filtered by type."""
            return [clue for clue in self.get_discovered_clues()
                   if clue.type == clue_type]

        def get_clues_by_character(self, char_id):
            """Get discovered clues related to a specific character."""
            return [clue for clue in self.get_discovered_clues()
                   if char_id in clue.related_characters]

        def get_clues_by_location(self, loc_id):
            """Get discovered clues related to a specific location."""
            return [clue for clue in self.get_discovered_clues()
                   if loc_id in clue.related_locations]

        def get_clues_by_tag(self, tag):
            """Get discovered clues with a specific tag."""
            return [clue for clue in self.get_discovered_clues()
                   if tag in clue.tags]

        def select_clue(self, clue_id):
            """Select a clue for presentation."""
            if clue_id in self.game_state.discovered_clues:
                self.selected_clue_id = clue_id
                return True
            return False

        def get_selected_clue(self):
            """Get the currently selected clue."""
            if self.selected_clue_id:
                return self.game_state.get_clue(self.selected_clue_id)
            return None

        def clear_selection(self):
            """Clear clue selection."""
            self.selected_clue_id = None

        def check_clue_relevance(self, clue_id, statement_id, interrogation_scene):
            """
            Check if a clue is relevant to a specific statement in an interrogation.
            Returns: (is_correct, response_text)
            """
            for statement in interrogation_scene.statements:
                if statement.id == statement_id:
                    # Check if this clue is in the correct evidence list
                    if clue_id in statement.correct_evidence:
                        response = statement.evidence_response.get(clue_id, "Верно!")
                        return (True, response)
                    else:
                        return (False, "Эта улика не относится к данному утверждению.")

            return (False, "Утверждение не найдено.")

        def get_clue_count(self):
            """Get total number of discovered clues."""
            return len(self.game_state.discovered_clues)

        def get_clue_types(self):
            """Get list of all clue types present in discovered clues."""
            types = set()
            for clue in self.get_discovered_clues():
                types.add(clue.type)
            return sorted(list(types))

        def organize_clues_by_case(self):
            """Organize discovered clues by current case."""
            current_case = self.game_state.get_current_case()
            if not current_case:
                return self.get_discovered_clues()

            # Return only clues discovered in this case
            case_clues = []
            for clue_id in current_case.discovered_clues:
                clue = self.game_state.get_clue(clue_id)
                if clue:
                    case_clues.append(clue)
            return case_clues

        def check_case_solution(self):
            """Check if all required clues for current case have been found."""
            current_case = self.game_state.get_current_case()
            if not current_case:
                return False

            return current_case.check_solution_requirements()

        def get_reliability_color(self, reliability):
            """Get color code based on clue reliability."""
            if reliability >= 80:
                return "#00ff00"  # Green - highly reliable
            elif reliability >= 50:
                return "#ffff00"  # Yellow - moderately reliable
            elif reliability >= 20:
                return "#ff9900"  # Orange - questionable
            else:
                return "#ff0000"  # Red - unreliable

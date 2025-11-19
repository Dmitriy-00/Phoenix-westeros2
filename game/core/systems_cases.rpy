# -*- coding: utf-8 -*-
"""
Case management system.
Handles investigation scenarios, stages, and endings.
"""

init -5 python:

    class CaseManager:
        """Manages investigation cases and their progression."""

        def __init__(self, game_state):
            self.game_state = game_state

        def start_case(self, case_id):
            """Start a new case investigation."""
            case = self.game_state.get_case(case_id)
            if not case:
                print("Error: Case {} not found".format(case_id))
                return False

            # Set as current case
            self.game_state.current_case_id = case_id

            # Reset case state
            case.current_stage = 0
            case.completed = False
            case.discovered_clues = []
            case.flags = {}

            # Unlock starting location
            if case.starting_location_id:
                map_manager = MapManager(self.game_state)
                map_manager.unlock_location(case.starting_location_id, notify=False)
                map_manager.travel_to_location(case.starting_location_id)

            # Unlock all allowed locations for this case
            for loc_id in case.allowed_locations:
                map_manager.unlock_location(loc_id, notify=False)

            print("Started case: {}".format(case.name))
            return True

        def get_current_case(self):
            """Get the currently active case."""
            return self.game_state.get_current_case()

        def advance_case_stage(self):
            """Advance the current case to the next stage."""
            case = self.get_current_case()
            if case:
                case.advance_stage()
                print("Case '{}' advanced to stage {}".format(case.name, case.current_stage))
                return case.current_stage
            return 0

        def set_case_flag(self, flag_name, value):
            """Set a flag for the current case."""
            case = self.get_current_case()
            if case:
                case.set_flag(flag_name, value)
                print("Case flag set: {} = {}".format(flag_name, value))
                return True
            return False

        def get_case_flag(self, flag_name, default=None):
            """Get a flag value from the current case."""
            case = self.get_current_case()
            if case:
                return case.get_flag(flag_name, default)
            return default

        def check_solution_ready(self):
            """Check if the player has all required clues to solve the case."""
            case = self.get_current_case()
            if case:
                return case.check_solution_requirements()
            return False

        def get_available_endings(self):
            """
            Get available endings based on current case state.
            Returns list of endings whose conditions are met.
            """
            case = self.get_current_case()
            if not case:
                return []

            available = []
            dialogue_manager = DialogueManager(self.game_state)

            for ending in case.endings:
                # Check ending conditions
                conditions = ending.conditions

                # Simple condition checking
                if isinstance(conditions, dict):
                    all_met = True

                    # Check flags
                    for flag_name, required_value in conditions.items():
                        if flag_name == "correct_accusation":
                            # Special handling for correct accusation
                            if not self.get_case_flag("accused_character"):
                                all_met = False
                                break
                        elif flag_name == "faction_balance_ok":
                            # Check if faction reputations are balanced
                            # (implementation depends on specific requirements)
                            pass
                        else:
                            # Check case flag
                            actual_value = self.get_case_flag(flag_name)
                            if actual_value != required_value:
                                all_met = False
                                break

                    if all_met:
                        available.append(ending)

            return available

        def complete_case(self, ending_id=None):
            """Complete the current case with a specific ending."""
            case = self.get_current_case()
            if not case:
                return False

            case.completed = True

            # Find and apply ending effects
            if ending_id:
                for ending in case.endings:
                    if ending.id == ending_id:
                        print("Case '{}' completed with ending: {}".format(
                            case.name, ending.name))

                        # Apply ending effects
                        if ending.effects:
                            dialogue_manager = DialogueManager(self.game_state)
                            dialogue_manager.apply_effects(ending.effects)

                        return True

            print("Case '{}' completed".format(case.name))
            return True

        def get_case_progress(self):
            """Get progress information for the current case."""
            case = self.get_current_case()
            if not case:
                return None

            total_clues = len(case.required_clues_to_solve)
            found_clues = len([c for c in case.required_clues_to_solve
                             if c in case.discovered_clues])

            return {
                "case": case,
                "stage": case.current_stage,
                "clues_found": found_clues,
                "clues_total": total_clues,
                "progress_percent": (found_clues * 100 // total_clues) if total_clues > 0 else 0,
                "solution_ready": case.check_solution_requirements()
            }

        def get_all_cases(self):
            """Get all available cases."""
            return list(self.game_state.cases.values())

        def get_cases_by_difficulty(self, difficulty):
            """Get cases filtered by difficulty level."""
            return [case for case in self.game_state.cases.values()
                   if case.difficulty == difficulty]

        def reset_case(self, case_id=None):
            """Reset a case to its initial state."""
            if case_id is None:
                case = self.get_current_case()
            else:
                case = self.game_state.get_case(case_id)

            if case:
                case.current_stage = 0
                case.completed = False
                case.discovered_clues = []
                case.flags = {}
                print("Case '{}' reset".format(case.name))
                return True
            return False

        def get_key_characters(self):
            """Get key characters involved in the current case."""
            case = self.get_current_case()
            if not case:
                return []

            characters = []
            for char_id in case.key_characters:
                character = self.game_state.get_character(char_id)
                if character:
                    characters.append(character)
            return characters

        def is_location_allowed(self, loc_id):
            """Check if a location is allowed in the current case."""
            case = self.get_current_case()
            if not case:
                return True  # No case active, all locations allowed

            if not case.allowed_locations:
                return True  # No restrictions

            return loc_id in case.allowed_locations

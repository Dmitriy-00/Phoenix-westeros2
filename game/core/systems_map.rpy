# -*- coding: utf-8 -*-
"""
World map and location management system.
Handles navigation between locations and regions.
"""

init -5 python:

    class MapManager:
        """Manages the world map and location navigation."""

        def __init__(self, game_state):
            self.game_state = game_state

        def get_all_locations(self):
            """Get all locations."""
            return list(self.game_state.locations.values())

        def get_unlocked_locations(self):
            """Get all unlocked locations."""
            return [loc for loc in self.game_state.locations.values()
                   if loc.is_unlocked]

        def get_locations_in_region(self, region):
            """Get all locations in a specific region."""
            return [loc for loc in self.game_state.locations.values()
                   if loc.region == region]

        def get_unlocked_locations_in_region(self, region):
            """Get unlocked locations in a specific region."""
            return [loc for loc in self.get_locations_in_region(region)
                   if loc.is_unlocked]

        def unlock_location(self, loc_id, notify=True):
            """Unlock a location for travel."""
            location = self.game_state.get_location(loc_id)
            if not location:
                print("Warning: Location {} not found".format(loc_id))
                return False

            if location.is_unlocked:
                print("Location {} already unlocked".format(loc_id))
                return False

            location.unlock()

            if notify:
                renpy.notify("Новая локация: {}".format(location.name))
                print("Location unlocked: {}".format(location.name))

            return True

        def lock_location(self, loc_id):
            """Lock a location."""
            location = self.game_state.get_location(loc_id)
            if location:
                location.lock()
                return True
            return False

        def travel_to_location(self, loc_id):
            """Travel to a specific location."""
            location = self.game_state.get_location(loc_id)
            if not location:
                print("Error: Location {} not found".format(loc_id))
                return False

            if not location.is_unlocked:
                print("Error: Location {} is locked".format(loc_id))
                return False

            # Check if location is allowed in current case
            current_case = self.game_state.get_current_case()
            if current_case and current_case.allowed_locations:
                if loc_id not in current_case.allowed_locations:
                    print("Warning: Location {} not in allowed locations for current case".format(loc_id))
                    # Still allow travel, just warn

            # Set current location
            self.game_state.current_location_id = loc_id
            if self.game_state.world_map:
                self.game_state.world_map.set_current_location(loc_id)

            print("Traveled to: {}".format(location.name))
            return True

        def get_current_location(self):
            """Get the current location object."""
            if self.game_state.current_location_id:
                return self.game_state.get_location(self.game_state.current_location_id)
            return None

        def get_available_sublocations(self):
            """Get available sub-locations at current location."""
            current_loc = self.get_current_location()
            if current_loc:
                return current_loc.available_sublocations
            return []

        def get_regions(self):
            """Get all unique regions."""
            if self.game_state.world_map and self.game_state.world_map.regions:
                return list(self.game_state.world_map.regions.keys())
            else:
                # Fallback: extract regions from locations
                regions = set()
                for location in self.game_state.locations.values():
                    if location.region:
                        regions.add(location.region)
                return sorted(list(regions))

        def get_region_info(self, region):
            """Get information about a region."""
            if self.game_state.world_map and self.game_state.world_map.regions:
                return self.game_state.world_map.regions.get(region, {})
            return {}

        def get_location_distance(self, loc_id_1, loc_id_2):
            """Calculate distance between two locations (simple Euclidean)."""
            loc1 = self.game_state.get_location(loc_id_1)
            loc2 = self.game_state.get_location(loc_id_2)

            if not loc1 or not loc2:
                return 0

            x1, y1 = loc1.map_position.get("x", 0), loc1.map_position.get("y", 0)
            x2, y2 = loc2.map_position.get("x", 0), loc2.map_position.get("y", 0)

            import math
            return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        def get_nearby_locations(self, loc_id, max_distance=0.3):
            """Get locations within a certain distance."""
            current_loc = self.game_state.get_location(loc_id)
            if not current_loc:
                return []

            nearby = []
            for other_loc in self.game_state.locations.values():
                if other_loc.id != loc_id:
                    distance = self.get_location_distance(loc_id, other_loc.id)
                    if distance <= max_distance:
                        nearby.append({
                            "location": other_loc,
                            "distance": distance
                        })

            # Sort by distance
            nearby.sort(key=lambda x: x["distance"])
            return nearby

        def check_location_danger(self, loc_id):
            """Check danger level of a location."""
            location = self.game_state.get_location(loc_id)
            if location:
                return location.danger_level
            return 0

        def set_time_of_day(self, loc_id, time):
            """Set time of day for a location (day/night/dusk/dawn)."""
            location = self.game_state.get_location(loc_id)
            if location:
                location.time_of_day = time
                return True
            return False

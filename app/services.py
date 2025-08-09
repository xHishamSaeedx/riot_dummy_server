import random
from typing import List
from datetime import datetime, timedelta
from .models import PlayerStats, MatchResponse, PlayerMatchHistory


class MatchService:
    """Service class to handle match-related operations and dummy data generation."""
    
    # List of Valorant maps
    VALORANT_MAPS = [
        "Ascent",
        "Bind", 
        "Haven",
        "Split",
        "Icebox",
        "Breeze",
        "Fracture",
        "Pearl",
        "Lotus",
        "Sunset"
    ]
    
    @staticmethod
    def generate_dummy_players(match_id: str) -> MatchResponse:
        """
        Generate dummy player data for a given match ID.
        
        Args:
            match_id: The match identifier
            
        Returns:
            MatchResponse with 20 dummy players, match start time, and map
        """
        players = []
        
        # For test_match_123, use consistent data
        if match_id == "test_match_123":
            # Fixed match start time for test_match_123
            match_start_time = datetime(2024, 1, 15, 14, 30, 0)  # January 15, 2024 at 2:30 PM
            map_name = "Ascent"  # Fixed map for test_match_123
        else:
            # Generate random match start time (within last 30 days)
            days_ago = random.randint(0, 30)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            match_start_time = datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
            
            # Randomly select a Valorant map
            map_name = random.choice(MatchService.VALORANT_MAPS)
        
        # Generate 20 dummy players with correlated kills and ACS
        for i in range(20):
            player_id = f"player_{match_id}_{i+1}"
            kills = random.randint(0, 25)  # Random kills between 0-25
            
            # Base ACS calculation based on kills
            base_acs = 150 + (kills * 8)  # Base ACS increases with kills
            
            # Add some variation (±15% of base ACS)
            variation = random.uniform(-0.15, 0.15)
            average_combat_score = round(base_acs * (1 + variation), 2)
            
            # Ensure ACS stays within reasonable bounds (150-350)
            average_combat_score = max(150.0, min(350.0, average_combat_score))
            
            player_stats = PlayerStats(
                player_id=player_id,
                kills=kills,
                average_combat_score=average_combat_score
            )
            players.append(player_stats)
        
        return MatchResponse(
            match_id=match_id,
            match_start_time=match_start_time,
            map=map_name,
            players=players
        )
    
    @staticmethod
    def get_player_match_history(player_id: str) -> PlayerMatchHistory:
        """
        Get recent match history for a player.
        
        Args:
            player_id: The player identifier
            
        Returns:
            PlayerMatchHistory with 5 recent match IDs
        """
        # Extract player number from player_id (e.g., "player_test_match_123_3" -> "3")
        player_number = "1"  # Default
        if player_id.startswith("player_") and "_" in player_id:
            parts = player_id.split("_")
            if len(parts) >= 4:
                player_number = parts[-1]  # Get the last part as player number
        
        # Generate 5 different match IDs for this specific player
        recent_matches = []
        
        # First 4 matches are unique to this player
        for i in range(4):
            match_id = f"player_{player_number}_match_{i+1}"
            recent_matches.append(match_id)
        
        # 5th match is the common match that all players share
        recent_matches.append("test_match_123")
        
        return PlayerMatchHistory(
            player_id=player_id,
            recent_matches=recent_matches
        )

    @staticmethod
    def generate_special_test_match_data() -> MatchResponse:
        """
        Generate dummy player data specifically for test_match_123 with 10 players,
        where only the first 7 and last 3 players actually played the game.
        
        Returns:
            MatchResponse with 10 dummy players (players 1-7 and 18-20) who actually played
        """
        players = []
        
        # Fixed match start time for test_match_123
        match_start_time = datetime(2024, 1, 15, 14, 30, 0)  # January 15, 2024 at 2:30 PM
        map_name = "Ascent"  # Fixed map for test_match_123
        
        # Only include players who actually played: players 1-7 and 18-20
        # This gives us 10 total players (7 + 3 = 10)
        player_indices = list(range(7)) + list(range(17, 20))  # [0,1,2,3,4,5,6,17,18,19]
        
        for i in player_indices:
            player_id = f"player_test_match_123_{i+1}"
            
            kills = random.randint(0, 25)  # Random kills between 0-25
            
            # Base ACS calculation based on kills
            base_acs = 150 + (kills * 8)  # Base ACS increases with kills
            
            # Add some variation (±15% of base ACS)
            variation = random.uniform(-0.15, 0.15)
            average_combat_score = round(base_acs * (1 + variation), 2)
            
            # Ensure ACS stays within reasonable bounds (150-350)
            average_combat_score = max(150.0, min(350.0, average_combat_score))
            
            player_stats = PlayerStats(
                player_id=player_id,
                kills=kills,
                average_combat_score=average_combat_score
            )
            players.append(player_stats)
        
        return MatchResponse(
            match_id="test_match_123",
            match_start_time=match_start_time,
            map=map_name,
            players=players
        )

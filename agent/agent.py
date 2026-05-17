from typing import TypedDict, Optional

from models.schemas import MatchEvent

class PlayerStats(TypedDict):
    player_name: str
    goals: int
    assists: int
    yellow_cards: int
    red_cards: int
    matches: int
class AgentState(TypedDict):
    sequence: int
    comment: str
    event: Optional[MatchEvent]
    current_score: Optional[dict[str, int]]
    validation_passed: Optional[bool]
    error: Optional[str]
    player_stats: Optional[PlayerStats]
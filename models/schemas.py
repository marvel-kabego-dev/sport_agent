from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class TeamType(str, Enum):
    HOME = "home"
    AWAY = "away"


class ActionType(str, Enum):
    GOAL = "goal"
    ASSIST = "assist"
    RED_CARD = "red_card"
    YELLOW_CARD = "yellow_card"
    SUBSTITUTION = "substitution"
    SCORE_UPDATE = "score_update"


class MatchEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    sequence: int

    player: Optional[str] = None
    team: Optional[TeamType] = None

    action: ActionType

    minute: Optional[int] = None

    home_score: Optional[int] = None
    away_score: Optional[int] = None
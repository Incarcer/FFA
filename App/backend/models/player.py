from dataclasses import dataclass

@dataclass
class Player:
    player_id: str
    player_name: str
    position: str
    team_abbr: str
    projected_points: float
    adp: int
    bye_week: int
    tier: int
    vorp: float

    def to_dict(self):
        return self.__dict__

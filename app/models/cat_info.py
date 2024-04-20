from typing import Literal

from pydantic import BaseModel, Field


class CatInfo(BaseModel):
    """
    Summary
    -------
    the cat info
    """
    name: str
    health: int = Field(alias='hp')
    knockbacks: int = Field(alias='kb')
    speed: int
    damage: int
    damage_per_second: int = Field(alias='dps')
    range: int
    money: int
    att_type: Literal['0', '1']
    red: bool
    black: bool
    white: bool
    angel: bool
    alien: bool
    zombie: bool
    witch: bool
    aku: bool
    dojo_base: bool
    eva: bool
    relic: bool
    baron: bool
    beast: bool
    time_between_attacks: str = Field(alias='tba')
    special_attack_description: str = Field(alias='special_att_desc')
    flavour_text: str | None

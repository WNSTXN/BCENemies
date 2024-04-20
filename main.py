from re import search
from typing import TypedDict

from polars import DataFrame
from uvloop import run

from app.api import MyGamatoto
from app.models.enemy_info import EnemyInfo


class RestructuredEnemyInfo(TypedDict):
    """
    Summary
    -------
    the restructured enemy info
    """
    name: str
    health: int
    type: int
    knockbacks: int
    speed: int
    total_attack_power: int
    damage_per_second: int
    range: int
    min_range: int
    max_range: int
    money: int
    time_between_attacks: str


def get_type_flags(enemy_info: EnemyInfo) -> int:
    """
    Summary
    -------
    get the type flags
    """
    flag = 0

    if enemy_info.white:
        flag |= 0b0000000000000

    if enemy_info.red:
        flag |= 0b0000000000001

    if enemy_info.black:
        flag |= 0b0000000000010

    if enemy_info.angel:
        flag |= 0b0000000000100

    if enemy_info.alien:
        flag |= 0b0000000001000

    if enemy_info.zombie:
        flag |= 0b0000000010000

    if enemy_info.relic:
        flag |= 0b0000000100000

    if enemy_info.aku:
        flag |= 0b0000001000000

    if enemy_info.dojo_base:
        flag |= 0b0000010000000

    if enemy_info.baron:
        flag |= 0b0001000000000

    if enemy_info.beast:
        flag |= 0b0010000000000

    if enemy_info.witch:
        flag |= 0b0100000000000

    if enemy_info.eva:
        flag |= 0b1000000000000

    return flag


def get_long_distance_ranges(enemy_range: int, special_attack_description: str) -> tuple[int, int]:
    """
    Summary
    -------
    get the long distance ranges
    """
    range_numbers = search(r"Effective range (\d+)~(\d+)", special_attack_description)

    return (
        (int(range_numbers.group(1)), int(range_numbers.group(2)))
        if range_numbers else (0, enemy_range)
    )


def restructure_enemy_info(enemy_info: EnemyInfo) -> RestructuredEnemyInfo:
    """
    Summary
    -------
    restructure the enemy info
    """
    min_range, max_range = get_long_distance_ranges(enemy_info.range, enemy_info.special_attack_description)

    return RestructuredEnemyInfo(
        name = enemy_info.name,
        health = enemy_info.health,
        type = get_type_flags(enemy_info),
        knockbacks = enemy_info.knockbacks,
        speed = enemy_info.speed,
        total_attack_power = enemy_info.attack_power1 + enemy_info.attack_power2 + enemy_info.attack_power3,
        damage_per_second = enemy_info.damage_per_second,
        range = enemy_info.range,
        min_range = min_range,
        max_range = max_range,
        money = enemy_info.money,
        time_between_attacks = enemy_info.time_between_attacks
    )


async def build_data(client: MyGamatoto):
    """
    build the data
    """
    enemy_names = await client.get_enemy_names()
    enemy_infos = [await client.get_enemy_info(name) for name in enemy_names]
    restructured_enemy_info = [restructure_enemy_info(enemy_info) for enemy_info in enemy_infos]
    df = DataFrame(restructured_enemy_info)
    df.write_csv('enemy_infos.csv')


async def main():
    """
    Summary
    -------
    the main entrypoint
    """
    async with MyGamatoto('https://onestoppress.com/api') as client:
        await build_data(client)


if __name__ == "__main__":
    run(main())

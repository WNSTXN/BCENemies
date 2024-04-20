from json import dumps
from typing import Generator

from httpx import AsyncClient
from pydantic_core import ValidationError

from app.models import EnemyInfo


class MyGamatoto:
    """
    Summary
    -------
    the MyGamatoto API client
    """
    __slots__ = 'client', 'base_url'

    def __init__(self, base_url: str):

        self.client = AsyncClient()
        self.base_url = base_url


    async def __aenter__(self):

        return self


    async def __aexit__(self, *_):

        await self.client.aclose()


    async def get_cat_infos(self) -> dict[str, dict[str, str]]:
        """
        Summary
        -------
        get the cat infos
        """
        request = await self.client.get(f'{self.base_url}/allcats')
        return request.json()['sampledata']


    async def get_enemy_info(self, enemy_name: str) -> EnemyInfo:
        """
        Summary
        -------
        get the enemy info
        """
        while True:
            request = await self.client.post(
                f'{self.base_url}/singleenemy',
                json={ 'compare': enemy_name },
                headers={ 'Content-Type': 'application/json' }
            )

            if enemy_info := request.json().get('sampledata'):
                break

            print(f"Failed to retrieve {enemy_name}, retrying..")

        try:
            return EnemyInfo.model_validate(enemy_info, strict=True)

        except ValidationError as error:
            raise ValueError(
                f'Could not validate enemy info for {enemy_name}\n{dumps(request.json(), indent=2)}'
            ) from error


    async def get_enemy_names(self) -> Generator[str, None, None]:
        """
        Summary
        -------
        get all enemy names
        """
        request = await self.client.get(f'{self.base_url}/allenemies')

        return (
            enemy_name for enemy in request.json()['sampledata']
            if (enemy_name := enemy['enemy_name_en']) != ' '
        )

from dataclasses import dataclass

import jmespath

from src.core.config import settings
from src.dtos.api.spotify import (
    SearchResponseDTO,
    SpotifyArtistResponseDTO,
    SpotifyAlbumResponseDTO,
    SpotifyAlbumsResponseDTO,
    SpotifyTrackResponseDTO,
    SpotifyTracksResponseDTO
)
from src.enums.spotify import SpotifyType
from src.repositories.api.base import AiohttpRepositpry


@dataclass
class SpotifyRepository(AiohttpRepositpry):
    async def login(self, code: str) -> str:
        payload = {
            "code": code,
            "client_id": settings.spotify_client_id,
            "client_secret": settings.spotify_client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": "http://localhost:5173/profile",
        }

        async with await self.session.post(  # type: ignore[attr-defined]
            url="https://accounts.spotify.com/api/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=payload,
        ) as response:
            data = await response.json()

        return jmespath.search('access_token', data)

    async def get_me(self, access_token: str) -> dict:
        async with self.session.get(  # type: ignore[attr-defined]
            url="https://api.spotify.com/v1/me",
            headers={"Authorization": f"Bearer {access_token}"},
        ) as response:
            return await response.json()

    async def get_recommendations(self, offset: int = 0, limit: int = 10) -> SpotifyTracksResponseDTO:
        async with self.session.get(f'{self.base_url}/recommendations?offset={offset}&limit={limit}') as response:  # type: ignore[attr-defined]
            return SpotifyTracksResponseDTO(**await response.json())

    async def get_recommendations_count(self) -> int:
        async with self.session.get(f'{self.base_url}/recommendations') as response:  # type: ignore[attr-defined]
            data = await response.json()
            return jmespath.search('total', data)

    async def get_top_artist_tracks(self, artist_id: str) -> SpotifyTracksResponseDTO:
        async with self.session.get(f'{self.base_url}/artists/{artist_id}/top-tracks') as response:  # type: ignore[attr-defined]
            return SpotifyTracksResponseDTO(**await response.json())

    async def get_top_artist_tracks_count(self, artist_id: str) -> int:
        async with self.session.get(f'{self.base_url}/artists/{artist_id}/top-tracks') as response:  # type: ignore[attr-defined]
            data = await response.json()
            return jmespath.search('total', data)

    async def get_album_tracks(self, album_id: str, offset: int = 0, limit: int = 10) -> SpotifyTracksResponseDTO:
        async with self.session.get(f'{self.base_url}/albums/{album_id}/tracks?offset={offset}&limit={limit}') as response:  # type: ignore[attr-defined]
            return SpotifyTracksResponseDTO(**await response.json())

    async def get_album_tracks_count(self, album_id: str) -> int:
        async with self.session.get(f'{self.base_url}/albums/{album_id}/tracks') as response:  # type: ignore[attr-defined]
            data = await response.json()
            return jmespath.search('total', data)

    async def get_artist_albums(self, artist_id: str, offset: int = 0, limit: int = 10) -> SpotifyAlbumsResponseDTO:
        async with self.session.get(f'{self.base_url}/artists/{artist_id}/albums?offset={offset}&limit={limit}') as response:  # type: ignore[attr-defined]
            return SpotifyAlbumsResponseDTO(**await response.json())

    async def get_artist_albums_count(self, artist_id: str) -> int:
        async with self.session.get(f'{self.base_url}/artists/{artist_id}/albums') as response:  # type: ignore[attr-defined]
            data = await response.json()
            return jmespath.search('total', data)

    async def get_track(self, track_id: str) -> SpotifyTrackResponseDTO | None:
        async with self.session.get(f'{self.base_url}/tracks/{track_id}') as response:  # type: ignore[attr-defined]
            return SpotifyTrackResponseDTO(**await response.json()) if response.status != 404 else None

    async def get_album(self, album_id: str) -> SpotifyAlbumResponseDTO | None:
        async with self.session.get(f'{self.base_url}/albums/{album_id}') as response:  # type: ignore[attr-defined]
            return SpotifyAlbumResponseDTO(**await response.json()) if response.status != 404 else None

    async def get_artist(self, artist_id: str) -> SpotifyArtistResponseDTO | None:
        async with self.session.get(f'{self.base_url}/artists/{artist_id}') as response:  # type: ignore[attr-defined]
            return SpotifyArtistResponseDTO(**await response.json()) if response.status != 404 else None

    async def search(self, query: str, type_: SpotifyType, offset: int = 0, limit: int = 10) -> SearchResponseDTO:
        async with self.session.get(f'{self.base_url}/search?q={query}&type={type_}&offset={offset}&limit={limit}') as response:  # type: ignore[attr-defined]
            return SearchResponseDTO(**await response.json())

    async def search_count(self, query: str, type_: SpotifyType) -> int:
        async with self.session.get(f'{self.base_url}/search?q={query}&type={type_}') as response:  # type: ignore[attr-defined]
            data = await response.json()
            return jmespath.search('total', data)

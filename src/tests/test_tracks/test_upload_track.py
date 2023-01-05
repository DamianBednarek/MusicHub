from os.path import join
from pathlib import Path
from uuid import uuid4

import pytest
from httpx import AsyncClient

from src.tests.common import make_post_request, make_get_request
from src.tests.test_tracks.trackFactory import TrackFactory

TEST_DIR = Path(__file__).resolve().parent


async def upload_file_and_make_request(filename: str, client: AsyncClient, **kwargs):
    path = join(TEST_DIR, filename)
    with open(path, "rb") as track:
        await make_post_request(client, url="/upload-track", response_status=kwargs["response_status"],
                                files={"file": track}, data={"is_public": "True"})


@pytest.mark.track
class TestTrackUpload:
    @pytest.mark.parametrize("filename", ["test.mp3", "testwav.wav"])
    async def test_upload_track(self, client: AsyncClient, filename, get_auth_user):
        await upload_file_and_make_request(filename, client, response_status=200)

    async def test_bad_extension(self, client: AsyncClient, get_auth_user):
        await upload_file_and_make_request("test.ogg", client, response_status=422)

    async def test_bad_name(self, client: AsyncClient, get_auth_user):
        await upload_file_and_make_request("wrong-name!_test.mp3", client, response_status=422)

    async def test_get_track_by_uuid(self, client: AsyncClient, get_auth_user):
        track = TrackFactory(created_by=get_auth_user.email)
        await make_get_request(client, 200, url=f"/info/{track.id}")

    async def test_get_track_wrong_uuid(self, client: AsyncClient, get_auth_user):
        await make_get_request(client, 400, url=f"/info/{uuid4()}")

    async def test_get_all_tracks(self, client: AsyncClient, get_auth_user):
        TrackFactory.create_batch(10, created_by=get_auth_user.email)
        await make_get_request(client, 200, url="/tracks")

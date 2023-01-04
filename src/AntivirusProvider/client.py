import json
import time

import httpx
from fastapi import UploadFile
from httpx import Response

from .constants import ANTIVIRUS_BASE_URL, POST_HEADERS, GET_HEADERS, BAD_STATUSES, PROGRES_PERCENTAGE
from ..exceptions.handler import CustomException


def r_content_to_dict(response: Response) -> dict:
    return json.loads(response.content)


class AntivirusScan:

    def __init__(self, function, antivirus_url: str = ANTIVIRUS_BASE_URL,
                 post_headers: dict = POST_HEADERS, get_headers: dict = GET_HEADERS,
                 bad_statuses: tuple = BAD_STATUSES):
        self.function = function
        self.antivirus_url = antivirus_url
        self.post_headers = post_headers
        self.get_headers = get_headers
        self.bad_statuses = bad_statuses

    async def __call__(self, *args, **kwargs):
        result = self.function(*args, **kwargs)
        await self.scan_for_malicious_content(*args)
        return result

    async def scan_for_malicious_content(self, file_obj: UploadFile) -> None:
        async with httpx.AsyncClient() as client:
            r = r_content_to_dict(
                await client.post(url=self.antivirus_url, files={"file": file_obj.file}, headers=self.post_headers))

            result = await self.wait_for_scan(r.get("data_id"), client)

            if result.get("scan_results").get("scan_all_result_i") in self.bad_statuses:
                raise CustomException("File cannot be uploaded")

    async def wait_for_scan(self, file_id: str, client: httpx.AsyncClient, attempts: int = 10) -> dict:

        for i in range(attempts):
            r = r_content_to_dict(
                await client.get(url=f"{self.antivirus_url}/{file_id}", headers=self.get_headers))

            if r.get("scan_results").get("progress_percentage") == PROGRES_PERCENTAGE:
                return r
            time.sleep(1.0)
        raise CustomException("Timeout while trying to scan file")

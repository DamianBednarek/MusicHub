from enum import Enum

from src.core.config import settings

ANTIVIRUS_BASE_URL = "https://api.metadefender.com/v4/file/"
POST_HEADERS = {
    "Content-Type": "application/octet-stream",
    "apikey": settings.ANTIVIRUS_API_KEY
}
GET_HEADERS = {
    "apikey": settings.ANTIVIRUS_API_KEY,
    "x-file-metadata": "0"
}
PROGRES_PERCENTAGE = 100


class AntivirusStatuses(Enum):
    INFECTED = 1
    SUSPICIOUS = 2
    POTENTIALLY_VULNERABLE_FILE = 18
    FAILED_TO_SCAN = 3
    ABORTED = 11
    NOT_SCANNED = 10
    CANCELED = 19
    FILETYPE_NOT_SUPPORTED = 23


BAD_STATUSES = (x for x in AntivirusStatuses)

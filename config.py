import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    bot_token: str
    admin_id: int
    database_path: str
    google_sheets_enabled: bool
    google_sheet_id: str
    google_credentials_file: str


def load_config() -> Config:
    load_dotenv()

    bot_token = os.getenv("BOT_TOKEN")
    admin_id_raw = os.getenv("ADMIN_ID")
    database_path = os.getenv("DATABASE_PATH", "leads.db")

    google_sheets_enabled_raw = os.getenv("GOOGLE_SHEETS_ENABLED", "false")
    google_sheets_enabled = google_sheets_enabled_raw.strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )

    google_sheet_id = os.getenv("GOOGLE_SHEET_ID", "")
    google_credentials_file = os.getenv(
        "GOOGLE_CREDENTIALS_FILE",
        "credentials/google-service-account.json",
    )

    if not bot_token:
        raise RuntimeError("BOT_TOKEN is missing in .env")

    if not admin_id_raw:
        raise RuntimeError("ADMIN_ID is missing in .env")

    try:
        admin_id = int(admin_id_raw)
    except ValueError as exc:
        raise RuntimeError("ADMIN_ID must be a number") from exc

    if google_sheets_enabled and not google_sheet_id:
        raise RuntimeError("GOOGLE_SHEET_ID is missing in .env")

    if google_sheets_enabled and not google_credentials_file:
        raise RuntimeError("GOOGLE_CREDENTIALS_FILE is missing in .env")

    return Config(
        bot_token=bot_token,
        admin_id=admin_id,
        database_path=database_path,
        google_sheets_enabled=google_sheets_enabled,
        google_sheet_id=google_sheet_id,
        google_credentials_file=google_credentials_file,
    )
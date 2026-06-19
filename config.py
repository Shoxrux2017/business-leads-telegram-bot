import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Config:
    bot_token: str
    admin_id: int
    database_path: str


def load_config() -> Config:
    load_dotenv()

    bot_token = os.getenv("BOT_TOKEN")
    admin_id_raw = os.getenv("ADMIN_ID")
    database_path = os.getenv("DATABASE_PATH", "leads.db")

    if not bot_token:
        raise RuntimeError("BOT_TOKEN is missing in .env")

    if not admin_id_raw:
        raise RuntimeError("ADMIN_ID is missing in .env")

    try:
        admin_id = int(admin_id_raw)
    except ValueError as exc:
        raise RuntimeError("ADMIN_ID must be a number") from exc

    return Config(
        bot_token=bot_token,
        admin_id=admin_id,
        database_path=database_path,
    )
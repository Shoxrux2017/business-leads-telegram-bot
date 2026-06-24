import logging
from datetime import datetime

import gspread

from config import Config


logger = logging.getLogger(__name__)


SHEET_HEADERS = [
    "Created At",
    "Name",
    "Phone",
    "Service",
    "Comment",
    "Source",
    "Status",
]


def _ensure_headers(worksheet) -> None:
    existing_headers = worksheet.row_values(1)

    if existing_headers:
        return

    worksheet.append_row(SHEET_HEADERS, value_input_option="RAW")


def try_append_lead_to_google_sheets(
    config: Config,
    name: str,
    phone: str,
    service: str,
    comment: str,
) -> bool:
    if not config.google_sheets_enabled:
        return False

    try:
        client = gspread.service_account(filename=config.google_credentials_file)
        spreadsheet = client.open_by_key(config.google_sheet_id)
        worksheet = spreadsheet.sheet1

        _ensure_headers(worksheet)

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        worksheet.append_row(
            [
                created_at,
                name,
                phone,
                service,
                comment,
                "Telegram Bot",
                "New",
            ],
            value_input_option="RAW",
        )

        return True

    except Exception:
        logger.exception("Could not append lead to Google Sheets.")
        return False
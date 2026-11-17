import os
from pathlib import Path

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def authenticate():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    key_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not key_path:
        raise RuntimeError(
            "Set GOOGLE_APPLICATION_CREDENTIALS to your local service-account JSON key path. "
            "Never commit the key to GitHub."
        )
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        str(Path(key_path).expanduser()), scope
    )
    return gspread.authorize(creds)


def get_spreadsheet(sheet_name):
    return authenticate().open(sheet_name)


def share_spreadsheet(spreadsheet):
    """Optional helper; recipients must be explicitly configured by the operator."""
    user_emails = [
        email.strip()
        for email in os.environ.get("EDUCSYS_SHARE_EMAILS", "").split(",")
        if email.strip()
    ]
    try:
        for email in user_emails:
            spreadsheet.share(email, perm_type="user", role="writer")
            print(f"Spreadsheet shared with {email}")
    except Exception as exc:
        print(f"An error occurred while sharing the spreadsheet: {exc}")

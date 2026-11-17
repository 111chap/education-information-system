# Education Information System (EducSys)

Academic Python desktop application for adding, viewing, updating, and deleting student records stored in Google Sheets. Records contain Name, Email, Age, and Grade.

## Project structure

- `educsys_main.py`: styled Tkinter / CustomTkinter interface with a scrollable records table.
- `educsys_backend.py`: earlier plain Tkinter implementation; despite its filename, this is another complete GUI, not a separate server.
- `educsys_api.py`: Google Sheets authentication and access helpers.
- `requirements.txt`: third-party dependencies (unpinned; original environment versions were not recorded).

## Run locally

Requires Python with Tkinter, an internet connection, and your own Google Cloud service account. Enable the Google Sheets and Drive APIs for that account. Create a test spreadsheet named `EducSysDB`, with the first worksheet containing these exact column headers in row 1:

| Name | Email | Age | Grade |
| --- | --- | --- | --- |

Use fictional records for a demo. Share that test spreadsheet with the service-account email as Editor. Download its JSON key to a secure location outside this repository. No credential or actual student records are included here.

In PowerShell, from this folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:GOOGLE_APPLICATION_CREDENTIALS = 'C:\path\outside-repository\service-account.json'
.\.venv\Scripts\python.exe educsys_main.py
```

To run the earlier interface instead, launch `educsys_backend.py`.

The optional `share_spreadsheet()` helper is not called by either interface. It shares only with comma-separated recipients explicitly supplied through `EDUCSYS_SHARE_EMAILS`; leaving that variable unset shares with nobody.

## Archive notes and limitations

This is coursework, not a production student information system. The original GUI files are preserved in this upload. Authentication was adjusted to read a credential path from an environment variable, and personal sharing addresses and obsolete commented credential examples were removed from the API helper. Original local files were not edited.

- The original `tester.py` is byte-for-byte identical to `educsys_backend.py`; only the latter is included.
- Spreadsheet errors are not handled in the GUI, and API calls run on the UI thread.
- Update computes fallback values for empty inputs but sends the raw input values instead, so blank fields can overwrite existing values.
- Selection methods pass the selection tuple directly; multiple selections may cause Tcl errors. Row edits/deletions assume the spreadsheet row order has not changed externally.
- Validation covers required fields when adding, but not valid email, age, or grade formats.
- The styled interface uses fixed positioning and may clip on some display settings.
- There is no login, access-control layer, audit history, or production data protection workflow.

Verification: Python syntax compilation and isolated mocked authentication/configuration checks. No live Google account, real spreadsheet, or GUI interaction was used to validate CRUD behavior.

## Attribution

Preserved from BSIT coursework files held by Chris Daniel Apin (`111chap` / `ChapWVSU`). This archive does not establish sole authorship or individual contributions; confirm original group credits before presenting it as solo work. Third-party libraries retain their respective ownership and licenses. No new license is assigned to the coursework.

Suggested portfolio description: **Academic student-record CRUD desktop app built with Python, Tkinter/CustomTkinter, and the Google Sheets API.**

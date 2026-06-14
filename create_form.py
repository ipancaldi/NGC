#!/usr/bin/env python3
"""
Natural Gardeners Club — Brand Discovery Google Form Creator

Creates the Brand Discovery questionnaire via the Google Forms API.

Prerequisites:
  1. Enable Google Forms API and Google Drive API in Google Cloud Console.
  2. Create OAuth 2.0 credentials (Desktop app) and save as 'credentials.json'.
  3. pip install -r requirements.txt
  4. python create_form.py

On first run a browser window opens for OAuth authorisation.
Credentials are cached in token.pickle for subsequent runs.
"""

import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/drive",
]

CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.pickle"


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)
    return creds


# ---------------------------------------------------------------------------
# Drive helper — create folder for file-upload responses
# ---------------------------------------------------------------------------

def create_upload_folder(drive_service, form_title):
    metadata = {
        "name": f"{form_title} — Uploads",
        "mimeType": "application/vnd.google-apps.folder",
    }
    folder = drive_service.files().create(body=metadata, fields="id").execute()
    folder_id = folder["id"]
    # Make folder writable by anyone with the link (needed for file uploads)
    drive_service.permissions().create(
        fileId=folder_id,
        body={"type": "anyone", "role": "writer"},
    ).execute()
    return folder_id


# ---------------------------------------------------------------------------
# Question builders
# ---------------------------------------------------------------------------

def _short(title, description="", required=False):
    item = {
        "title": title,
        "questionItem": {
            "question": {
                "required": required,
                "textQuestion": {"paragraph": False},
            }
        },
    }
    if description:
        item["description"] = description
    return item


def _paragraph(title, description="", required=False):
    item = {
        "title": title,
        "questionItem": {
            "question": {
                "required": required,
                "textQuestion": {"paragraph": True},
            }
        },
    }
    if description:
        item["description"] = description
    return item


def _checkboxes(title, options, description="", required=False, other=False):
    opts = [{"value": o} for o in options]
    if other:
        opts.append({"isOther": True})
    item = {
        "title": title,
        "questionItem": {
            "question": {
                "required": required,
                "choiceQuestion": {
                    "type": "CHECKBOX",
                    "options": opts,
                },
            }
        },
    }
    if description:
        item["description"] = description
    return item


def _radio(title, options, description="", required=False, other=False):
    opts = [{"value": o} for o in options]
    if other:
        opts.append({"isOther": True})
    item = {
        "title": title,
        "questionItem": {
            "question": {
                "required": required,
                "choiceQuestion": {
                    "type": "RADIO",
                    "options": opts,
                },
            }
        },
    }
    if description:
        item["description"] = description
    return item


def _grid(title, rows, columns, description=""):
    """Multiple choice grid (one radio selection per row)."""
    item = {
        "title": title,
        "questionGroupItem": {
            "questions": [
                {"rowQuestion": {"title": row}} for row in rows
            ],
            "grid": {
                "columns": {
                    "type": "RADIO",
                    "options": [{"value": c} for c in columns],
                }
            },
        },
    }
    if description:
        item["description"] = description
    return item


def _file_upload(title, folder_id, description="", required=False):
    item = {
        "title": title,
        "questionItem": {
            "question": {
                "required": required,
                "fileUploadQuestion": {
                    "folderId": folder_id,
                    "maxFiles": 10,
                    "maxFileSize": 10485760,  # 10 MB
                },
            }
        },
    }
    if description:
        item["description"] = description
    return item


def _page_break(title, description=""):
    item = {"title": title, "pageBreakItem": {}}
    if description:
        item["description"] = description
    return item


# ---------------------------------------------------------------------------
# Questionnaire — ordered list of items
# ---------------------------------------------------------------------------

def build_questions(upload_folder_id):
    return [
        # ── SECTION 1 ──────────────────────────────────────────────────────
        _page_break("Section 1 — About the Club"),

        _short(
            "What is the name of your gardening club?",
            required=True,
        ),
        _paragraph(
            "How would you describe the club in one sentence?",
            description=(
                'e.g. "A welcoming community space where children and families '
                'learn to grow together."'
            ),
        ),
        _paragraph("Why was the club started?"),
        _paragraph("What makes your club special?"),
        _checkboxes(
            "What activities does the club currently offer?",
            [
                "Gardening workshops",
                "Seed planting",
                "Food growing",
                "Nature education",
                "Family activities",
                "School partnerships",
                "Seasonal events",
                "Community volunteering",
                "Wildlife & pollinator projects",
                "Arts & crafts",
                "Outdoor learning",
            ],
            other=True,
        ),

        # ── SECTION 2 ──────────────────────────────────────────────────────
        _page_break("Section 2 — Audience & Community"),

        _checkboxes(
            "Who is the club mainly for?",
            [
                "Young children (3–6)",
                "Children (7–12)",
                "Teenagers",
                "Parents & families",
                "Schools",
                "Local community",
                "Volunteers",
                "Older adults",
                "Beginner gardeners",
                "Experienced gardeners",
                "Everyone",
            ],
        ),
        _checkboxes(
            "What do you hope people feel when they interact with the club?",
            [
                "Welcome",
                "Calm",
                "Inspired",
                "Curious",
                "Connected",
                "Creative",
                "Happy",
                "Safe",
                "Empowered",
                "Included",
                "Excited to learn",
            ],
            other=True,
        ),
        _checkboxes(
            "What values are most important to the club?",
            [
                "Nature",
                "Community",
                "Learning",
                "Sustainability",
                "Accessibility",
                "Kindness",
                "Creativity",
                "Inclusion",
                "Wellbeing",
                "Fun",
                "Environmental awareness",
                "Seasonal living",
            ],
            other=True,
        ),

        # ── SECTION 3 ──────────────────────────────────────────────────────
        _page_break("Section 3 — Personality & Style"),

        _paragraph(
            "If the club were a person, how would you describe them?",
            description='e.g. "Friendly, creative, patient, knowledgeable, joyful, outdoorsy."',
        ),
        _checkboxes(
            "Which words best describe the style you want the club to have?",
            [
                "Natural",
                "Colourful",
                "Calm",
                "Playful",
                "Educational",
                "Modern",
                "Handmade",
                "Friendly",
                "Organic",
                "Creative",
                "Community-focused",
                "Rustic",
                "Bright",
                "Minimal",
                "Whimsical",
                "Premium",
            ],
            other=True,
        ),
        _grid(
            "Which visual styles do you naturally prefer?",
            rows=[
                "Botanical illustration",
                "Bright floral colours",
                "Minimal modern design",
                "Hand-drawn elements",
                "Nature photography",
                "Vintage gardening aesthetics",
                "Clean editorial layouts",
                "Child-friendly graphics",
                "Soft earthy colours",
                "Bold vibrant colours",
            ],
            columns=["Love it", "Like it", "Neutral", "Not for us"],
        ),

        # ── SECTION 4 ──────────────────────────────────────────────────────
        _page_break("Section 4 — Colours & Visual Identity"),

        _checkboxes(
            "Which colours feel right for the club?",
            [
                "Greens",
                "Bright flower colours",
                "Earthy browns",
                "Cream / off-white",
                "Warm yellows",
                "Pinks",
                "Orange / terracotta",
                "Lavender / purple",
                "Deep forest tones",
                "Soft pastel colours",
            ],
            other=True,
        ),
        _paragraph("Are there any colours or styles you definitely want to avoid?"),
        _radio(
            "What type of logo feels most appropriate?",
            [
                "Simple & modern",
                "Botanical & illustrated",
                "Friendly & playful",
                "Elegant & timeless",
                "Handcrafted",
                "Badge / emblem style",
                "Minimal symbol",
                "Unsure",
            ],
        ),

        # ── SECTION 5 ──────────────────────────────────────────────────────
        _page_break("Section 5 — Social Media & Communication"),

        _checkboxes(
            "Where will the brand mostly appear?",
            [
                "Instagram",
                "Facebook",
                "Posters & flyers",
                "Community boards",
                "Website",
                "Signage",
                "Aprons / uniforms",
                "Seed packets",
                "Workshops",
                "Tote bags & merch",
                "School materials",
                "Event banners",
            ],
            other=True,
        ),
        _checkboxes(
            "What type of social media content would you like to share?",
            [
                "Gardening tips",
                "Children's activities",
                "Seasonal updates",
                "Flower & plant photography",
                "Harvests",
                "Educational content",
                "Community stories",
                "Workshop promotion",
                "Wildlife & pollinators",
                "Recipes",
                "Before & after projects",
                "Volunteer moments",
            ],
            other=True,
        ),

        # ── SECTION 6 ──────────────────────────────────────────────────────
        _page_break("Section 6 — Inspiration"),

        _paragraph("Are there any brands, clubs, gardens or Instagram accounts you love?"),
        _paragraph("What do you like about them?"),
        _file_upload(
            "Upload any images, logos, colours or inspiration you'd like us to see.",
            folder_id=upload_folder_id,
            description="Accepted: images, PDFs, screenshots. Max 10 MB per file.",
        ),

        # ── SECTION 7 ──────────────────────────────────────────────────────
        _page_break("Section 7 — Future Vision"),

        _paragraph("Where would you love the club to be in 3 years?"),
        _paragraph("What would success look like for the club?"),
        _paragraph("Is there anything else you'd love the brand to communicate?"),
    ]


# ---------------------------------------------------------------------------
# Form creation
# ---------------------------------------------------------------------------

FORM_TITLE = "Natural Gardeners Club — Brand Discovery"
FORM_SUBTITLE = (
    "Help us shape the future look, feel and personality of the club."
)
CONFIRMATION_MESSAGE = (
    "Thank you for helping shape the future of Natural Gardeners Club.\n\n"
    "Your answers will help create a welcoming, joyful and community-driven "
    "identity that reflects the spirit of the club and the people who grow it together."
)


def create_form(forms_service):
    result = forms_service.forms().create(
        body={
            "info": {
                "title": FORM_TITLE,
                "documentTitle": FORM_TITLE,
            }
        }
    ).execute()
    form_id = result["formId"]

    # Set description and confirmation message
    forms_service.forms().batchUpdate(
        formId=form_id,
        body={
            "requests": [
                {
                    "updateFormInfo": {
                        "info": {
                            "description": FORM_SUBTITLE,
                        },
                        "updateMask": "description",
                    }
                },
                {
                    "updateSettings": {
                        "settings": {
                            "quizSettings": {"isQuiz": False},
                        },
                        "updateMask": "quizSettings.isQuiz",
                    }
                },
            ]
        },
    ).execute()

    return form_id


def add_questions(forms_service, form_id, questions):
    requests = [
        {"createItem": {"item": item, "location": {"index": idx}}}
        for idx, item in enumerate(questions)
    ]
    forms_service.forms().batchUpdate(
        formId=form_id, body={"requests": requests}
    ).execute()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    creds = get_credentials()
    forms_service = build("forms", "v1", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)

    print("Creating Drive folder for file-upload responses…")
    upload_folder_id = create_upload_folder(drive_service, FORM_TITLE)
    print(f"  Folder ID: {upload_folder_id}")

    print("Creating form…")
    form_id = create_form(forms_service)

    print("Adding questions…")
    questions = build_questions(upload_folder_id)
    add_questions(forms_service, form_id, questions)

    print("\n✅  Form created successfully!")
    print(f"   Form ID  : {form_id}")
    print(f"   Edit URL : https://docs.google.com/forms/d/{form_id}/edit")
    print(f"   Share URL: https://docs.google.com/forms/d/{form_id}/viewform")
    print(
        f"\n   Uploaded files will appear in your Drive folder:\n"
        f"   https://drive.google.com/drive/folders/{upload_folder_id}"
    )


if __name__ == "__main__":
    main()

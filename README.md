# NGC
Natural Gardeners Club

## Brand Discovery Questionnaire

`create_form.py` generates the **Natural Gardeners Club — Brand Discovery** Google Form
via the Google Forms API.

### Setup

**1. Enable APIs in Google Cloud Console**

- Go to [console.cloud.google.com](https://console.cloud.google.com/)
- Create or select a project
- Enable **Google Forms API** and **Google Drive API**
- Go to **APIs & Services → Credentials → Create Credentials → OAuth client ID**
- Application type: **Desktop app**
- Download the JSON and save it as `credentials.json` in this directory

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Run**

```bash
python create_form.py
```

A browser window opens for OAuth on first run; credentials are cached in `token.pickle`.
The script prints the edit URL and shareable respondent URL when done.

---

### Form structure

| Section | Questions |
|---------|-----------|
| 1 — About the Club | Club name, one-sentence description, origin, what makes it special, current activities |
| 2 — Audience & Community | Who the club is for, how people should feel, core values |
| 3 — Personality & Style | Club personality, style words, visual style preference grid |
| 4 — Colours & Visual Identity | Colour preferences, colours/styles to avoid, logo style |
| 5 — Social Media & Communication | Where brand appears, content types |
| 6 — Inspiration | Brands/accounts they love, what they like about them, file upload |
| 7 — Future Vision | 3-year vision, what success looks like, anything else to communicate |

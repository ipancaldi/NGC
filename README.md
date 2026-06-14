# NGC — Natural Gardeners Club

## Brand Discovery Questionnaire

A 7-section, 22-question brand discovery form hosted on GitHub Pages.
Responses are sent automatically to a Google Sheet you own.

---

## Live form

**`https://ipancaldi.github.io/NGC/`**

*(Enable GitHub Pages first — see step 5 below.)*

---

## How responses are collected

Every time someone submits the form their answers are:

1. **Sent to your Google Sheet** (one row per submission, timestamped)
2. **Saved as a local browser backup** — the thank-you screen has a *Download backup as CSV* button in case the Sheet is ever unreachable

You can open the Sheet at any time to see all responses, filter by column, or export to CSV / Excel.

---

## One-time setup (≈ 10 minutes)

### Step 1 — Create the Google Sheet

Go to [sheets.new](https://sheets.new) to create a blank spreadsheet.
Name it *NGC Brand Discovery Responses* (or whatever you like).

---

### Step 2 — Open Apps Script

Inside the Sheet: **Extensions → Apps Script**

A new tab opens with a code editor.

---

### Step 3 — Paste the script

Delete everything in the editor, then paste the entire contents of
[`apps-script/Code.gs`](apps-script/Code.gs) from this repo.

Press **Ctrl+S / Cmd+S** to save.

---

### Step 4 — Deploy as a web app

1. Click **Deploy → New deployment**
2. Click the gear icon ⚙ next to *Select type* and choose **Web app**
3. Fill in the settings:
   - **Description**: NGC Brand Discovery
   - **Execute as**: Me
   - **Who has access**: Anyone
4. Click **Deploy**
5. Click **Authorize access** and sign in when prompted
6. **Copy the Web app URL** — it looks like:
   `https://script.google.com/macros/s/AKfy.../exec`

---

### Step 5 — Connect the form to the Sheet

Open `index.html` in this repo and find this line near the top of the `<script>` block:

```js
var SCRIPT_URL = 'YOUR_APPS_SCRIPT_URL_HERE';
```

Replace `YOUR_APPS_SCRIPT_URL_HERE` with the URL you copied in Step 4, then commit and push to the `gh-pages` branch:

```bash
git add index.html
git commit -m "Connect form to Google Sheet"
git push origin gh-pages
```

---

### Step 6 — Enable GitHub Pages

1. Go to **github.com/ipancaldi/NGC → Settings → Pages**
2. Source: branch **`gh-pages`**, folder **`/ (root)`**
3. Click **Save**

Your form is live at `https://ipancaldi.github.io/NGC/` within ~1 minute.

---

## Re-deploying after code changes

If you ever update `Code.gs`, redeploy:

**Deploy → Manage deployments → Edit (pencil icon) → Version: New version → Deploy**

---

## Files

| File | Purpose |
|------|---------|
| `index.html` | The form (GitHub Pages) |
| `apps-script/Code.gs` | Google Apps Script — receives POST requests and writes to the Sheet |
| `create_form.py` | Alternative: creates a native Google Form via the Forms API |
| `requirements.txt` | Python dependencies for `create_form.py` |

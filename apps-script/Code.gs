// Natural Gardeners Club — Brand Discovery
// Google Apps Script web app: receives form submissions and writes to this Sheet.
//
// SETUP
//  1. Open the Google Sheet where you want responses saved.
//  2. Click Extensions → Apps Script.
//  3. Replace all code with this file, then save (Ctrl+S / Cmd+S).
//  4. Click Deploy → New deployment.
//     - Type          : Web app
//     - Execute as    : Me
//     - Who has access: Anyone
//  5. Click Deploy → copy the Web app URL.
//  6. Paste that URL into index.html where it says YOUR_APPS_SCRIPT_URL_HERE.
//  7. Commit & push index.html to the gh-pages branch.

var HEADERS = [
  'Timestamp',
  'Q1  Club name',
  'Q2  One-sentence description',
  'Q3  Why the club was started',
  'Q4  What makes it special',
  'Q5  Activities offered',
  'Q6  Who the club is for',
  'Q7  Feelings when interacting',
  'Q8  Club values',
  'Q9  Club personality',
  'Q10 Style words',
  'Q11 Botanical illustration',
  'Q11 Bright floral colours',
  'Q11 Minimal modern design',
  'Q11 Hand-drawn elements',
  'Q11 Nature photography',
  'Q11 Vintage gardening aesthetics',
  'Q11 Clean editorial layouts',
  'Q11 Child-friendly graphics',
  'Q11 Soft earthy colours',
  'Q11 Bold vibrant colours',
  'Q12 Colour preferences',
  'Q13 Colours / styles to avoid',
  'Q14 Logo style',
  'Q15 Where brand will appear',
  'Q16 Social media content types',
  'Q17 Brands / accounts loved',
  'Q18 What they like about them',
  'Q19 Inspiration links / ideas',
  'Q20 Vision in 3 years',
  'Q21 What success looks like',
  'Q22 Anything else to communicate'
];

// ── Receive a form submission ──────────────────────────
function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    // Write headers on first submission
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(HEADERS);
      sheet.setFrozenRows(1);

      // Style the header row
      var headerRange = sheet.getRange(1, 1, 1, HEADERS.length);
      headerRange.setBackground('#1b4332');
      headerRange.setFontColor('#ffffff');
      headerRange.setFontWeight('bold');

      // Auto-resize columns
      sheet.autoResizeColumns(1, HEADERS.length);
    }

    var row = JSON.parse(e.postData.contents);
    sheet.appendRow(row);

    return ContentService
      .createTextOutput(JSON.stringify({ status: 'ok', row: sheet.getLastRow() }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// ── Health check (visit the URL in a browser to confirm it's running) ──
function doGet(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var count = Math.max(0, sheet.getLastRow() - 1); // subtract header row
  return ContentService
    .createTextOutput('NGC Brand Discovery script is running. Responses collected: ' + count)
    .setMimeType(ContentService.MimeType.TEXT);
}

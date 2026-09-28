/**
 * Websa Worldwide enquiry log. Google Apps Script web app.
 *
 * What it does: receives every quotation request and contact enquiry from the website,
 * appends a row to a Google Sheet the directors can open on their phones, and emails
 * the directors a summary. No paid service, no server.
 *
 * Set-up (about ten minutes, done once by the owner of the Google account):
 *   1. Create a Google Sheet called "Websa enquiries". Copy its ID from the URL.
 *   2. Extensions > Apps Script. Replace the default code with this file.
 *   3. Set SHEET_ID and NOTIFY below.
 *   4. Deploy > New deployment > Web app. Execute as: Me. Who has access: Anyone. Deploy.
 *   5. Copy the web app URL into site.config.json as "form_endpoint" and run python build.py.
 *
 * The sheet gets these columns on first write: Received, Reference, Form, Status, Name, Company,
 * Country, City, Email, Phone, Type, Category, Description, Quantity, Unit, Budget, Link, Specs,
 * Delivery, Timeline, Brand, Heard via, Language, Page, Message. "Status" starts as "New" so the
 * directors can change it to "Quoted", "Won" or "Lost" and filter the sheet.
 */
var SHEET_ID = "PASTE_SHEET_ID_HERE";
var SHEET_NAME = "Enquiries";
var NOTIFY = ["info@websaworldwide.com"]; // add the directors' addresses, comma separated

var COLUMNS = ["received", "ref", "form", "status", "name", "company", "country", "city", "email", "phone", "type", "category_label", "description", "quantity", "unit", "budget", "link", "specs", "delivery", "timeline", "brand", "heard", "lang", "page", "message"];
var HEADERS = ["Received", "Reference", "Form", "Status", "Name", "Company", "Country", "City", "Email", "Phone", "Type", "Category", "Description", "Quantity", "Unit", "Budget", "Link", "Specs", "Delivery", "Timeline", "Brand", "Heard via", "Language", "Page", "Message"];

function doPost(e) {
  var data = {};
  try {
    data = JSON.parse(e.postData.contents);
  } catch (err) {
    data = e.parameter || {};
  }
  data.received = new Date();
  data.status = "New";
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADERS);
    sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight("bold");
    sheet.setFrozenRows(1);
  }
  sheet.appendRow(COLUMNS.map(function (k) { return data[k] === undefined ? "" : String(data[k]); }));

  var subject = "[Websa] " + (data.form === "quote" ? "Quotation request " : "Enquiry ") + (data.ref || "") + " from " + (data.name || "unknown") + (data.country ? " (" + data.country + ")" : "");
  var body = COLUMNS.map(function (k, i) { return data[k] ? HEADERS[i] + ": " + data[k] : null; }).filter(Boolean).join("\n") + "\n\nOpen the log: " + ss.getUrl();
  try { MailApp.sendEmail(NOTIFY.join(","), subject, body, { replyTo: data.email || "" }); } catch (err) {}

  return ContentService.createTextOutput(JSON.stringify({ ok: true, ref: data.ref || "" })).setMimeType(ContentService.MimeType.JSON);
}

function doGet() {
  return ContentService.createTextOutput(JSON.stringify({ ok: true, service: "Websa enquiry log" })).setMimeType(ContentService.MimeType.JSON);
}

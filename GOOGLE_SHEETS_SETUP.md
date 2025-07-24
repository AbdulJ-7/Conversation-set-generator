# Google Sheets Export Setup Guide

This guide will walk you through setting up Google Sheets export functionality for the Function Calling Conversation Generator.

## Prerequisites

- Google account with access to Google Cloud Platform
- Google Sheets API enabled
- Service account credentials

## Step-by-Step Setup

### 1. Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name: `conversation-generator` (or your preferred name)
4. Click "Create"

### 2. Enable Required APIs

1. In the Google Cloud Console, go to **APIs & Services** → **Library**
2. Search for and enable these APIs:
   - **Google Sheets API**
   - **Google Drive API** (needed for file access)

### 3. Create a Service Account

1. Go to **APIs & Services** → **Credentials**
2. Click **"+ CREATE CREDENTIALS"** → **"Service account"**
3. Fill in the details:
   - **Service account name:** `conversation-generator-service`
   - **Service account ID:** `conversation-generator-service` (auto-filled)
   - **Description:** `Service account for conversation generator exports`
4. Click **"Create and Continue"**
5. Skip the optional steps (roles and user access) by clicking **"Done"**

### 4. Generate and Download Credentials

1. In the **Credentials** page, find your newly created service account
2. Click on the service account email
3. Go to the **"Keys"** tab
4. Click **"Add Key"** → **"Create new key"**
5. Select **"JSON"** format
6. Click **"Create"**
7. The credentials file will download automatically

### 5. Setup Credentials in Your Project

1. Rename the downloaded file to `credentials.json`
2. Move it to your project root directory:
   ```
   prompt_generator/
   ├── credentials.json  ← Place it here
   ├── config.
   
   ├── conversation_generator.py
   └── ...
   ```

### 6. Configure Spreadsheet Access

**Option A: Share Existing Spreadsheet (Recommended)**
1. Open Google Sheets and create a new spreadsheet
2. Name it: `Function Calling Conversation Sets`
3. Click **"Share"** button
4. Add your service account email as an editor:
   - Email format: `conversation-generator-service@your-project-id.iam.gserviceaccount.com`
   - Role: **Editor**
5. Click **"Send"**

**Option B: Let the App Create Spreadsheet**
- The app will automatically create a spreadsheet
- You'll need to manually share it with yourself afterward using the service account email

### 7. Install Required Dependencies

```bash
# If using uv (recommended)
uv add gspread google-auth google-auth-oauthlib

# If using pip
pip install gspread google-auth google-auth-oauthlib
```

### 8. Configure the Application

1. Run the configuration manager:
   ```bash
   python config_manager.py
   ```

2. When prompted for Google Sheets export, choose **"y"**

3. Set your preferences:
   - **Spreadsheet title:** `Function Calling Conversation Sets` (or custom name)
   - **Credentials file:** `credentials.json` (default)

Alternatively, edit `config.yaml` directly:
```yaml
google_sheets:
  enabled: true
  spreadsheet_title: "Function Calling Conversation Sets"
  credentials_file: "credentials.json"
  export_summary: true
```

### 9. Test the Setup

1. Generate some conversation sets:
   ```bash
   python conversation_generator.py
   ```

2. Or test Google Sheets export directly:
   ```bash
   python google_sheets_exporter.py
   ```

3. Check your Google Sheets for the exported data

## Security Notes

### 🔒 Protect Your Credentials
- **Never commit `credentials.json` to version control**
- Add it to your `.gitignore` file:
  ```
  credentials.json
  *.json
  ```

### 🔑 Service Account Permissions
- The service account only has access to spreadsheets you explicitly share
- It cannot access your personal files or other Google services
- You can revoke access anytime by removing the service account from shared spreadsheets

## Troubleshooting

### Common Issues

**❌ "Credentials file not found"**
- Ensure `credentials.json` is in the project root directory
- Check the file path in `config.yaml`

**❌ "Permission denied" or "Spreadsheet not found"**
- Make sure you shared the spreadsheet with the service account email
- Check that the service account has "Editor" permissions

**❌ "API not enabled"**
- Enable Google Sheets API and Google Drive API in Google Cloud Console
- Wait a few minutes for APIs to activate

**❌ "Import error for gspread"**
- Install required packages: `pip install gspread google-auth google-auth-oauthlib`
- Or use uv: `uv add gspread google-auth google-auth-oauthlib`

### Getting Help

If you encounter issues:
1. Check the error messages in the terminal
2. Verify your Google Cloud project settings
3. Ensure all APIs are enabled
4. Confirm service account permissions

### Manual Export

If automatic export fails, you can manually export later:
```bash
python google_sheets_exporter.py
```

## What Gets Exported

The exporter creates two worksheets:

### 1. "Conversation Sets" Worksheet
- **ID:** Conversation set number
- **Title:** Conversation set title
- **User Motive:** User's goals and context
- **Domains & Subdomains:** Areas being explored
- **Turn 1-8:** Individual conversation turns
- **Tools 1-8:** Tools used in each turn
- **Generated On:** Creation timestamp
- **Provider/Model:** AI model information
- **File Path:** Source file location

### 2. "Generation Summary" Worksheet
- Generation statistics
- Provider and model information
- List of all generated files
- Timestamps and metadata

## Customization

You can customize the export by:
- Modifying spreadsheet title in config
- Editing column headers in `google_sheets_exporter.py`
- Adding custom formatting or formulas
- Creating additional worksheets

Enjoy automated Google Sheets export! 📊✨

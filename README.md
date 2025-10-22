# SFTP → SharePoint Uploader Setup Guide

This guide walks you through setting up your environment, Docker configuration, and the required `.env` file to run the **SFTP SharePoint Uploader**.

---

## 🐳 Docker Setup

### 1. Pull the `atmoz/sftp` image

Run the following command to pull the official **SFTP server** image:

```bash
docker pull atmoz/sftp
```

---

### 2. Create and run your SFTP container

You can quickly spin up an SFTP container using this command:

```bash
docker run -p 2222:22 -d atmoz/sftp username:password:::upload
```

**Explanation:**
- `username` → SFTP username  
- `password` → SFTP password  
- `upload` → Folder created automatically inside the container for file uploads  
- `-p 2222:22` → Exposes SFTP on port **2222** (change if needed)

You can verify that it’s running:
```bash
docker ps
```

And connect to it (for testing):
```bash
sftp -P 2222 username@localhost
```

---

## ⚙️ Environment Variables Setup

Create a `.env` file in your project directory with the following variables:

```bash
# === SFTP ===
SFTP_HOST=localhost
SFTP_PORT=2222
SFTP_USER=username
SFTP_PASS=password
REMOTE_DIR=upload
LOCAL_DIR="path to download folder"

# === SHAREPOINT ===
SHAREPOINT_SITE="https://aretexaus.sharepoint.com/sites/ANZ-D365FOIntegration"
DOC_LIBRARY="Shared Documents/ANZ Bank Statements"

# === COOKIES ===
FEDAUTH=""
RTFA=""
```

### 💡 Notes:
- `FEDAUTH` and `RTFA` cookies are from your logged-in SharePoint browser session.
- Never commit your `.env` file to GitHub — add it to `.gitignore`.

```bash
echo ".env" >> .gitignore
```

---

## ▶️ Running the Script

After setting everything up:
1. Make sure the SFTP container is running (`docker ps`).
2. Run your uploader (either locally or via Docker):
   ```bash
   python paramiks.py
   ```
3. The script will:
   - Connect to SFTP  
   - Download files to your local directory  
   - Upload them to SharePoint  

---

✅ **Done!**
You now have a fully functional **SFTP → SharePoint** uploader with Docker and environment variables.

import os
import paramiko
import requests
from dotenv import load_dotenv

load_dotenv()

SFTP_HOST = os.getenv("SFTP_HOST")
SFTP_PORT = int(os.getenv("SFTP_PORT", "22"))
SFTP_USER = os.getenv("SFTP_USER")
SFTP_PASS = os.getenv("SFTP_PASS")
REMOTE_DIR = os.getenv("REMOTE_DIR")
LOCAL_DIR = os.getenv("LOCAL_DIR")

SHAREPOINT_SITE = os.getenv("SHAREPOINT_SITE")
DOC_LIBRARY = os.getenv("DOC_LIBRARY")

FEDAUTH = os.getenv("FEDAUTH")
RTFA = os.getenv("RTFA")

os.makedirs(LOCAL_DIR, exist_ok=True)
print("Connecting to SFTP...")

transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
transport.connect(username=SFTP_USER, password=SFTP_PASS)
sftp = paramiko.SFTPClient.from_transport(transport)

for file in sftp.listdir(REMOTE_DIR):
    local_path = os.path.join(LOCAL_DIR, file)
    sftp.get(f"{REMOTE_DIR}/{file}", local_path)
    print(f"Downloaded: {file}")

sftp.close()
transport.close()

print("\nConnecting to SharePoint...")

session = requests.Session()
session.cookies.set("FedAuth", FEDAUTH, domain=".sharepoint.com")
session.cookies.set("rtFa", RTFA, domain=".sharepoint.com")
headers = {"Accept": "application/json;odata=verbose"}

digest_url = f"{SHAREPOINT_SITE}/_api/contextinfo"
resp = session.post(digest_url, headers=headers)
if not resp.ok:
    raise Exception(f"Failed to get digest token: {resp.status_code}\n{resp.text}")
digest = resp.json()["d"]["GetContextWebInformation"]["FormDigestValue"]

print("\nUploading files to SharePoint...")
upload_headers = {
    "Accept": "application/json;odata=verbose",
    "X-RequestDigest": digest,
}

for file_name in os.listdir(LOCAL_DIR):
    file_path = os.path.join(LOCAL_DIR, file_name)
    upload_url = (
        f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{DOC_LIBRARY}')/"
        f"Files/add(url='{file_name}',overwrite=true)"
    )

    with open(file_path, "rb") as file:
        resp = session.post(upload_url, headers=upload_headers, data=file)
        if resp.ok:
            print(f"Uploaded: {file_name}")
        else:
            print(f"Failed to upload {file_name} — {resp.status_code}")
            print(resp.text)

print("\nDone uploading statements")

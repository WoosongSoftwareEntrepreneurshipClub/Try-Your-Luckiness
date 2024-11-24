import os.path
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://mail.google.com/']

def sendMail(email, content, file_path):
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for future use
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        message = EmailMessage()

        message.set_content(content)
        message['To'] = email
        message["From"] = 'softwareentrepreneurshipclub@gmail.com'
        message['Subject'] = "Thank you for joining!"

        # Attach PDF file
        with open(file_path, "rb") as f:
            pdf_data = f.read()
            if not pdf_data:
                print("File has something wrong")
                return
            message.add_attachment(
                pdf_data,
                maintype="application",
                subtype="pdf",
                filename=os.path.basename(file_path),
            )
    
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}

        send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )
        print(f'Message Id: {send_message["id"]}')

    except HttpError as error:
        print(f"An error occurred: {error}")
        send_message = None

    return send_message


if __name__ == "__main__":
    # Replace with a valid email, content, and file path
    recipient_email = "scottjoon816@gmail.com"
    email_content = "Hello! This is your PDF attachment."
    file_path = "./result/ASDFADSF.pdf"  # Adjust to your file path
    sendMail(recipient_email, email_content, file_path)

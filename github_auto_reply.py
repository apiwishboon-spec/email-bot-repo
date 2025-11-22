import os
import imaplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Load from GitHub Secrets
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# HTML body with gradient, glow, autograph, phone, links, footer
HTML_BODY = """\
<!DOCTYPE html>
<html>
  <body style="margin:0; padding:0;
               background: linear-gradient(to bottom right, #ffc0cb, #add8e6);
               font-family:Inter, Arial, sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:80px;">
      <tr>
        <td align="center">

          <table width="90%" cellpadding="20" cellspacing="0"
                 style="max-width:500px;
                        background:rgba(255,255,255,0.97);
                        border-radius:15px;
                        box-shadow:
                           0 0 20px rgba(255, 192, 203, 0.6),
                           0 0 40px rgba(173, 216, 230, 0.5);">

            <tr>
              <td style="font-size:18px; color:#333;">

                Hi there! 👋<br><br>
                Thank you for reaching out. This is an automated confirmation
                to let you know your message has been safely received.<br><br>

                My response turnaround time is currently limited due to system operations.
                I’ll get back to you as soon as possible.<br><br>

                📞 Urgent? Contact: <strong>093-337-2907</strong><br><br>

                While waiting, feel free to explore my projects 🌟<br>
                <a href="https://notarickroll.page.gd/" target="_blank">Not a Rickroll</a><br>
                <a href="https://boon123.pythonanywhere.com/" target="_blank">PythonAnywhere Projects</a><br><br>

                Best regards,<br><br>

                <span style="
                  font-family:'Brush Script MT', cursive;
                  font-size:42px;
                  color:#333;">
                  A.Apiwish
                </span>

                <hr style="margin:25px 0; border:1px solid #ddd;">

                <p style="font-size:12px; color:gray; line-height:1.5;">
                  This is an automated system message from the administrator
                  (<a href='mailto:apiwish.boon@gmail.com'>apiwish.boon@gmail.com</a>).<br>
                  No further action is required unless you encounter issues.<br>
                  For any problems, please reach out directly.<br><br>
                  Thank you for your cooperation.
                </p>

              </td>
            </tr>
          </table>

          <p style="font-size:13px; color:#999; margin-top:40px;">
            © 2025 APIWISH ANUTARAVANICHKUL. All rights reserved.<br>
          </p>

        </td>
      </tr>
    </table>
  </body>
</html>
"""

def send_auto_reply(to_address):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Auto Reply"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_address

    html_part = MIMEText(HTML_BODY, "html")
    msg.attach(html_part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"[{datetime.now()}] ✅ Auto-reply sent to {to_address}")

    except Exception as e:
        print(f"[{datetime.now()}] ❌ Failed to send auto-reply: {e}")


def check_inbox():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select("inbox")

        status, data = mail.search(None, "UNSEEN")
        email_ids = data[0].split()

        if email_ids:
            print(f"[{datetime.now()}] ℹ️ Found {len(email_ids)} new email(s).")
        else:
            print(f"[{datetime.now()}] ℹ️ No new emails.")

        for eid in email_ids:
            _, msg_data = mail.fetch(eid, "(RFC822)")
            raw_msg = email.message_from_bytes(msg_data[0][1])
            sender = raw_msg["From"]
            send_auto_reply(sender)

        mail.close()
        mail.logout()

    except Exception as e:
        print(f"[{datetime.now()}] ❌ Inbox check error: {e}")


# One GitHub Actions run = one inbox scan
print(f"[{datetime.now()}] ⏳ GitHub Actions Run Started")
check_inbox()
print(f"[{datetime.now()}] ⏳ Run complete")

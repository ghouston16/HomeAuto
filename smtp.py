import smtplib, ssl
import time
port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "garyspi78@gmail.com"
receiver_email = "harrygouston@gmail.com"
password = "sensepig"
message = """\
Subject: Heating Status

Your Heating has been Switched On off by HomeAutonM8.
"""

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
  server.ehlo()  # Can be omitted
  server.starttls(context=context)
  server.ehlo()  # Can be omitted
  server.login(sender_email, password)
  server.sendmail(sender_email, receiver_email, message)

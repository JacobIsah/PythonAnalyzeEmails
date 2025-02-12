import imaplib
import email
from email.header import decode_header
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login("yours@gmail.com", "pssword")
mail.select("inbox")

status, messages = mail.search(None, "UNSEEN")
email_ids = messages[0].split()

status, msg_data = mail.fetch(email_ids[-1], "(RFC822)")
for response_part in msg_data:
    if isinstance(response_part, tuple):
        msg = email.message_from_bytes(response_part[1])

subject, encoding = decode_header(msg["Subject"])[0]
if isinstance(subject, bytes):
    subject = subject.decode(encoding or "utf-8")
print("Subject:", subject)

sender = msg.get("From")
print("From:", sender)

def extract_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                return part.get_payload(decode=True).decode("utf-8", errors="ignore")
    else:
        return msg.get_payload(decode=True).decode("utf-8", errors="ignore")

body = extract_email_body(msg)
print("Body:", body)


analysis = TextBlob(body)
print("Sentiment Score:", analysis.sentiment.polarity)

wordcloud = WordCloud(width=800, height=400, background_color="white").generate(body)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()





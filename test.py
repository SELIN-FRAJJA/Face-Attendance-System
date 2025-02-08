import smtplib
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    print("SMTP connection successful!")
    server.quit()
except Exception as e:
    print(f"SMTP connection failed: {e}")
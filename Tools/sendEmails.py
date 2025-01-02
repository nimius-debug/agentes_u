import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

# --- Hardcoded emails and their passwords ---
SENDER_CREDENTIALS = {
    "jgil@dtccompany.es": os.getenv("JGIL_DTC_PASS"),
    "jgil@dtccompany.net": os.getenv("JGIL_DTC_PASS"),
    "jgil@dtccompany.org": os.getenv("JGIL_DTC_PASS"),
    "ifraile@dtccompany.es": os.getenv("IVAN_DTC_PASS"),
    "ifraile@dtccompany.net": os.getenv("IVAN_DTC_PASS"),
    "ifraile@dtccompany.org": os.getenv("IVAN_DTC_PASS"),
}

def send_email(sender_email, password, recipient_email, subject, message):
    """
    Send an email using IONOS SMTP server with SSL/TLS.
    """
    smtp_server = "smtp.ionos.es"
    smtp_port = 465

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Error sending email to {recipient_email}: {e}")
        return False

def main():
    st.header("_:blue[(IONOS)] Mass Email Sender_", divider="gray", anchor=False)
    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.subheader("Upload Recipient Excel File")
        uploaded_file = st.file_uploader("Upload Excel (.xlsx)", type=["xlsx"])
        
        df = None
        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file)
                required_cols = ["Name", "Company", "Email"]
                if not all(col in df.columns for col in required_cols):
                    st.error(f"Excel must have columns {required_cols}.")
                    df = None
                else:
                    st.success("Excel file loaded successfully!")
                    st.dataframe(df)
            except Exception as e:
                st.error(f"Error reading Excel file: {e}")
    with col2:
        st.subheader("Email Configuration & Sending")

        # 1. Choose the sender email (dropdown)
        possible_senders = list(SENDER_CREDENTIALS.keys())
        sender_email = st.selectbox("Sender Email", possible_senders)

        # 2. Subject & Body (use placeholders {NAME} and {COMPANY})
        subject = st.text_input("Subject", value="Hello from Streamlit!")
        body_template = st.text_area(
            "Email Body (Use {NAME} or {COMPANY} placeholders)",
            value="Hello {NAME},\n\nWe have an amazing offer for {COMPANY}..."
        )

        # 3. Keep track of how many emails we’ve sent this session
        if "email_send_count" not in st.session_state:
            st.session_state["email_send_count"] = 0

        st.write(f"**Emails sent this session**: {st.session_state['email_send_count']} / 50")

        # 4. Send emails (only if df is loaded)
        if df is not None:
            total_rows = len(df)
            can_send = st.session_state["email_send_count"] < 50

            if st.button("Send Emails", disabled=not can_send):
                count_sent = 0
                password = SENDER_CREDENTIALS[sender_email]
                
                # Create a progress bar widget
                progress_bar = st.progress(0)
                
                for idx, row in df.iterrows():
                    # Limit to 50
                    if st.session_state["email_send_count"] >= 50:
                        st.warning("Limit of 50 emails reached.")
                        break

                    name = str(row["Name"])
                    company = str(row["Company"])
                    recipient_email = str(row["Email"])

                    # Personalize body
                    personalized_body = body_template.replace("{NAME}", name).replace("{COMPANY}", company)

                    # Send email
                    success = send_email(
                        sender_email=sender_email,
                        password=password,
                        recipient_email=recipient_email,
                        subject=subject,
                        message=personalized_body
                    )

                    if success:
                        count_sent += 1
                        st.session_state["email_send_count"] += 1

                    # Update progress bar (fraction from 0.0 to 1.0)
                    progress_fraction = (idx + 1) / total_rows
                    progress_bar.progress(progress_fraction)

                st.success(f"Finished sending {count_sent} emails.")
                # Optionally reset progress or leave it at 100%

main()
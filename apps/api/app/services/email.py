import os
from typing import Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


async def send_magic_link(email: str, magic_link: str) -> bool:
    """
    Send magic link email
    """
    provider = os.getenv("EMAIL_PROVIDER", "console")
    
    if provider == "console":
        return await _send_console_email(email, magic_link)
    elif provider == "sendgrid":
        return await _send_sendgrid_email(email, magic_link)
    elif provider == "postmark":
        return await _send_postmark_email(email, magic_link)
    else:
        raise ValueError(f"Unsupported email provider: {provider}")


async def _send_console_email(email: str, magic_link: str) -> bool:
    """
    Send email to console (for development)
    """
    print(f"\n{'='*50}")
    print(f"MAGIC LINK EMAIL TO: {email}")
    print(f"LINK: {magic_link}")
    print(f"{'='*50}\n")
    return True


async def _send_sendgrid_email(email: str, magic_link: str) -> bool:
    """
    Send email via SendGrid
    """
    # Implementation would use SendGrid API
    # For now, fall back to console
    return await _send_console_email(email, magic_link)


async def _send_postmark_email(email: str, magic_link: str) -> bool:
    """
    Send email via Postmark
    """
    # Implementation would use Postmark API
    # For now, fall back to console
    return await _send_console_email(email, magic_link)

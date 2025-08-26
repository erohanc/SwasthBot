import re

EMAIL = re.compile(r'([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)')
PHONE = re.compile(r'(\+?\d{1,3}[-\s]?)?(\d{3}[-\s]?\d{3}[-\s]?\d{4})')
MRN = re.compile(r'\b(MRN|PatientID|PID)[:\s\-]*([A-Za-z0-9\-]{4,})\b', re.IGNORECASE)

def redact(text: str) -> str:
    if not text:
        return text
    text = EMAIL.sub('[REDACTED_EMAIL]', text)
    text = PHONE.sub('[REDACTED_PHONE]', text)
    text = MRN.sub('[REDACTED_MRN]', text)
    return text

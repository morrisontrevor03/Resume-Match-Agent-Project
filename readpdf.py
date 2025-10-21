from pypdf import PdfReader
import re

path = "C:\\Users\\morri\\OneDrive\\Documents\\Resume 10-13-2025.pdf"

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    extracted_text = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text.append(text)
    return "\n".join(extracted_text)

text = extract_text_from_pdf(path)

EMAIL_RE = re.compile(r'''(?ix)\b[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}\b''')
PHONE_RE = re.compile(r'''(?x)(?:\+?\d{1,3}[\s.\-]?)?(?:\(?\d{3}\)?[\s.\-]?)\d{3}[\s.\-]?\d{4}(?:\s*(?:ext|x|x\.|extension)\s*\d{1,5})?''')
STREET_SUFFIXES = r'(?:Ave|Avenue|Blvd|Boulevard|St|Street|Rd|Road|Ln|Lane|Dr|Drive|Ct|Court|Way|Ter|Terrace|Pl|Place|Pkwy|Parkway|Hwy|Highway|Cir|Circle)'
STREET_LINE_RE = re.compile(rf'''\d{{1,6}}\s+[A-Za-z0-9.\'#\- ]+\s+{STREET_SUFFIXES}\b''', re.I)
POBOX_RE = re.compile(r'(?i)\bP\.?\s*O\.?\s*Box\s*\d+\b')
CITY_STATE_ZIP_RE = re.compile(r'''[A-Za-z.\- ]+,\s*(?:AL|AK|AZ|AR|CA|CO|CT|DC|DE|FL|GA|HI|IA|ID|IL|IN|KS|KY|LA|MA|MD|ME|MI|MN|MO|MS|MT|NC|ND|NE|NH|NJ|NM|NV|NY|OH|OK|OR|PA|PR|RI|SC|SD|TN|TX|UT|VA|VT|WA|WI|WV|WY)\s+\d{5}(?:-\d{4})?''', re.I)

def redact(text: str) -> str:
    text = EMAIL_RE.sub('[REDACTED EMAIL]', text)
    text = PHONE_RE.sub('[REDACTED PHONE]', text)
    text = POBOX_RE.sub('[REDACTED ADDRESS]', text)
    text = STREET_LINE_RE.sub('[REDACTED ADDRESS]', text)
    text = CITY_STATE_ZIP_RE.sub('[REDACTED ADDRESS]', text)
    return text

text_redacted = redact(text)
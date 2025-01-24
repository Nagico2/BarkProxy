import re


def extract_brackets(text):
    start_match = re.match(r'^【(.*?)】', text)
    end_match = re.search(r'【(.*?)】$', text)

    start = start_match.group(1) if start_match else None
    end = end_match.group(1) if end_match else None

    return start, end


def extract_name(text: str) -> str | None:
    start, end = extract_brackets(text)
    if end:
        return end
    if start:
        return start
    return None


def extract_verification_code(message: str) -> str | None:
    match = re.search(r'\b\d{4,6}\b', message)
    if match:
        return match.group(0)
    return None

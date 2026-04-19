import re

_FILLER = re.compile(
    r"\b(um|uh|er|ah|like|you know|I mean|kind of|sort of)\b",
    re.IGNORECASE
)
_LEADING = re.compile(r"^\s*(?:and|so|well|but)\s+", re.IGNORECASE)


def simplify_content(text):
    if not text or not text.strip():
        return text
    t = text.strip()
    t = _FILLER.sub(" ", t)
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"\s*[.!?]\s*", ". ", t)
    sentences = re.split(r"\s*\.\s+", t)
    points = []
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        s = _LEADING.sub("", s).strip()
        if not s or len(s) < 10:
            continue
        if len(s) > 100:
            parts = re.split(r",\s+|\s+and\s+", s, maxsplit=1)
            s = parts[0].strip()
            if not s.endswith("."):
                s = s + "."
            if len(s) < 10:
                continue
        points.append(s)
    return "\n".join(points) if points else text.strip()

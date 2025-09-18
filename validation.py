def sanitize_input_Green(text: str) -> str:
    if text is None:
        return ""
    s = text.replace("\r\n","\n").replace("\r","\n")

    parts = s.split("\n")
    parts = [p.strip(" \t") for p in parts]
    return "\n".join(parts)

def is_valid(text: str, MAX_LEN = 100):
    if not isinstance(text,str):
        return False
    t = text.replace("\r\n","\n").replace("\r","\n")
    if not t or t.isspace():
        return False
    if len(t) > MAX_LEN:
        return False
    return True

def sanitize_input_Red(text):
    pass

def sanitize_input_Refactor(text):
    if text is None:
        return ""

    s = text.replace("\r\n","\n").replace("\r","\n")

    parts = s.split("\n")
    if all( line == line.strip(" \t") for line in parts): 
        return s

    cleaned = (line.strip(" \t") for line in parts)
    return "\n".join(cleaned)

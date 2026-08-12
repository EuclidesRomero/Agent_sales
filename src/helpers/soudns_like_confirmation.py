def _sounds_like_confirmation(text: str) -> bool:
    """
    Reconoce frases cortas que suenan a que el cliente quiere el producto del
    que se habló hace un momento, sin nombrarlo de nuevo (ej: "dame una",
    "quiero uno", "sí, esa"). Es una lista simple a propósito -- prefiere
    fallar hacia "no reconocido" antes que asumir de más.
    """
    confirmation_words = {"dame", "quiero", "dime", "si", "sí", "esa", "ese", "eso", "una", "uno", "regalame", "regálame"}
    text_words = set(text.lower().split())
    return bool(text_words & confirmation_words)
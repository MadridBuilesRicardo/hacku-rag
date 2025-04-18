import re
from bs4 import BeautifulSoup

def clean_scraped_text(text: str) -> str:
    """
    Limpia y normaliza el texto scrap para que sea comprensible y útil para el modelo.
    Elimina menús, headers, duplicados, formularios, y textos residuales.
    """
    # 1. Eliminar etiquetas HTML si quedan
    text = BeautifulSoup(text, "html.parser").get_text(separator=" ")

    # 2. Unificar espacios y saltos de línea
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"\s{2,}", " ", text)

    # 3. Eliminar menús comunes o duplicaciones de navegación
    patrones_menus = [
        r"(?i)\bInicio\b",
        r"(?i)\bNosotros\b",
        r"(?i)\bServicios\b",
        r"(?i)\bContáctanos\b",
        r"(?i)\bContacto\b",
        r"(?i)\bBlog\b",
        r"(?i)\bFacebook[-f]?\b",
        r"(?i)\bInstagram\b",
        r"(?i)\bSíguenos en\b.*",
        r"(?i)\bGracias por contactarnos\b.*",
        r"(?i)\bSaltar al contenido\b",
        r"(?i)\bSlide\b",
        r"(?i)\bMenu\b",
        r"(?i)\bf\b",  # ícono de Facebook
    ]
    for pattern in patrones_menus:
        text = re.sub(pattern, "", text)

    # 4. Eliminar líneas de formularios
    campos_formulario = [
        r"(?i)\bNombre\b",
        r"(?i)\bCelular\b",
        r"(?i)\bTel[ée]fono\b",
        r"(?i)\bE[- ]?mail\b",
        r"(?i)\bMensaje\b",
        r"(?i)\bEnviar\b",
    ]
    for pattern in campos_formulario:
        text = re.sub(pattern, "", text)

    # 5. Eliminar información de contacto redundante
    text = re.sub(r"\(?\+?\d{2,4}[\s\-]?\d{3,}[\s\-]?\d{3,}", "", text)
    text = re.sub(r"\S+@\S+", "", text)
    text = re.sub(r"(?i)\bDirección\b.*", "", text)

    # 6. Eliminar duplicados simples (como “DISEÑO DISEÑO”)
    words = text.split()
    deduped_words = [words[0]] if words else []
    for i in range(1, len(words)):
        if words[i].lower() != words[i - 1].lower():
            deduped_words.append(words[i])
    text = " ".join(deduped_words)

    # 7. Recorte final
    return text.strip()

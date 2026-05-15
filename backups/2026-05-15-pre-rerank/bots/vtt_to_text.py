import re
from pathlib import Path

IN = Path("/openclaw/workspace/main/rag_store/approved/classified/youtube")

def clean_vtt(file):
    text = file.read_text(errors="ignore")

    # eliminar timestamps
    text = re.sub(r"\d{2}:\d{2}:\d{2}\.\d{3} --> .*", "", text)

    # eliminar cabecera VTT
    text = re.sub(r"WEBVTT.*?\n\n", "", text, flags=re.DOTALL)

    # eliminar etiquetas tipo <c> o <i>
    text = re.sub(r"<.*?>", "", text)

    # limpiar líneas vacías
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    # unir texto
    clean = " ".join(lines)

    return clean

def main():
    for f in IN.glob("*.vtt"):
        txt = clean_vtt(f)

        out = f.with_suffix(".txt")
        out.write_text(txt)

        print(f"Processed: {f.name}")

if __name__ == "__main__":
    main()

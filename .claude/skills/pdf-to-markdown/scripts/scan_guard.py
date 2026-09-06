"""
Guarda contra PDF digitalizado (scan) — o furo mais perigoso do conversor.

O extrator upstream (PyMuPDF / Docling) só lê a camada de texto do PDF.
Um PDF digitalizado (autos escaneados, contrato assinado fotografado, print
de fatura) não tem camada de texto: a conversão "sucede", grava um .md vazio
e o modelo conclui, com confiança, a partir de nada.

Este módulo:
  1. mede a densidade real de texto do markdown produzido;
  2. se for baixa demais, tenta OCR via PyMuPDF+Tesseract;
  3. se OCR não estiver disponível, escreve um AVISO EM BLOCO no topo do .md
     e devolve código de saída próprio, para que a falha seja barulhenta.

Nunca devolva um .md vazio em silêncio.
"""

import os
import re
import shutil
import sys

# Abaixo disto o documento é tratado como digitalizado.
MIN_CHARS_PER_PAGE = 40
MIN_CHARS_TOTAL = 200

SCAN_EXIT_CODE = 3

BANNER_NO_OCR = """<!-- PDF2MD:SCANNED_NO_OCR -->
> # ⚠️ NENHUM TEXTO EXTRAÍDO — NÃO USE ESTE ARQUIVO COMO FONTE
>
> Este PDF não possui camada de texto: é um documento **digitalizado
> (escaneado ou fotografado)**. A conversão não falhou por erro — não há
> o que converter sem OCR.
>
> **O conteúdo abaixo está vazio ou é resíduo. Não conclua nada a partir dele.**
>
> Para extrair o texto é necessário OCR. Instale o Tesseract com o pacote
> de português e rode de novo:
>
> - Debian/Ubuntu: `sudo apt-get install -y tesseract-ocr tesseract-ocr-por`
> - macOS (Homebrew): `brew install tesseract tesseract-lang`
>
> Alternativa, sem OCR: leia as páginas como imagem com a ferramenta Read,
> ou trate o documento pela via de análise de imagem.

---

"""

BANNER_OCR_USED = """<!-- PDF2MD:OCR_USED -->
> # ℹ️ TEXTO OBTIDO POR OCR — CONFERIR ANTES DE CITAR
>
> Este PDF é digitalizado e não tinha camada de texto. O conteúdo abaixo foi
> reconhecido por OCR (Tesseract), e **OCR erra**: números, datas, valores,
> nomes próprios e assinaturas são os campos mais frequentemente corrompidos.
>
> Não cite valor, data, número de processo ou cláusula deste arquivo sem
> conferir na imagem da página correspondente.

---

"""


def _prose_chars(markdown: str) -> int:
    """Conta caracteres de texto real, descontando ruído estrutural."""
    if not markdown:
        return 0
    text = markdown
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)  # front-matter
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)  # comentários/page breaks
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)  # imagens
    text = re.sub(r"\*\*\[Image:[^\]]*\]\*\*", " ", text)  # anotações de imagem
    text = re.sub(r"^\s*\|.*\|\s*$", " ", text, flags=re.MULTILINE)  # linhas de tabela
    text = re.sub(r"[#*`_>|\-\s]+", " ", text)  # sintaxe markdown + espaços
    return len(text.strip())


def native_text_chars(pdf_path: str) -> int:
    """Caracteres da camada de texto NATIVA do PDF, sem OCR.

    Sinal primário: é o único jeito honesto de saber se o documento é
    digitalizado. Inspecionar o markdown de saída não serve, porque o
    pymupdf4llm aplica OCR por conta própria quando o Tesseract está
    instalado — e entrega o resultado sem distinguir de texto nativo.
    """
    try:
        import pymupdf
    except ImportError:
        return -1
    try:
        total = 0
        with pymupdf.open(pdf_path) as doc:
            for page in doc:
                total += len((page.get_text() or "").strip())
        return total
    except Exception:
        return -1


def is_scanned_pdf(pdf_path: str, total_pages: int) -> bool:
    """True se o PDF não tiver camada de texto própria (documento digitalizado)."""
    chars = native_text_chars(pdf_path)
    if chars < 0:
        return False  # não deu para medir; não inventa diagnóstico
    if chars < MIN_CHARS_TOTAL:
        return True
    return (chars / max(total_pages or 1, 1)) < MIN_CHARS_PER_PAGE


def looks_scanned(markdown: str, total_pages: int) -> bool:
    """True se o markdown extraído for pobre demais para ser texto de verdade."""
    chars = _prose_chars(markdown)
    if chars < MIN_CHARS_TOTAL:
        return True
    pages = max(total_pages or 1, 1)
    return (chars / pages) < MIN_CHARS_PER_PAGE


def _tessdata_prefix() -> str | None:
    """Localiza o diretório tessdata exigido pelo PyMuPDF."""
    env = os.environ.get("TESSDATA_PREFIX")
    if env and os.path.isdir(env):
        return env
    candidates = [
        "/usr/share/tesseract-ocr/5/tessdata",
        "/usr/share/tesseract-ocr/4.00/tessdata",
        "/usr/share/tesseract-ocr/tessdata",
        "/usr/share/tessdata",
        "/usr/local/share/tessdata",
        "/opt/homebrew/share/tessdata",
    ]
    for path in candidates:
        if os.path.isdir(path):
            return path
    return None


def ocr_available() -> tuple[bool, str]:
    """(disponível, motivo). Motivo é vazio quando disponível."""
    if shutil.which("tesseract") is None:
        return False, "binário 'tesseract' não encontrado no PATH"
    if _tessdata_prefix() is None:
        return False, "diretório tessdata não localizado (defina TESSDATA_PREFIX)"
    return True, ""


def ocr_pdf(pdf_path: str, show_progress: bool = False) -> str:
    """Extrai texto por OCR, página a página, em markdown mínimo.

    Idioma via PDF2MD_OCR_LANG (padrão: por+eng). Levanta exceção em falha —
    quem chama decide o que fazer.
    """
    import pymupdf

    prefix = _tessdata_prefix()
    if prefix:
        os.environ["TESSDATA_PREFIX"] = prefix

    lang = os.environ.get("PDF2MD_OCR_LANG", "por+eng")
    dpi = int(os.environ.get("PDF2MD_OCR_DPI", "300"))

    parts: list[str] = []
    with pymupdf.open(pdf_path) as doc:
        total = doc.page_count
        for i, page in enumerate(doc, start=1):
            if show_progress:
                print(f"\r[pdf2md] OCR página {i}/{total}...", end="", file=sys.stderr)
            textpage = page.get_textpage_ocr(
                flags=0, language=lang, dpi=dpi, full=True
            )
            parts.append(page.get_text(textpage=textpage) or "")
    if show_progress:
        print("", file=sys.stderr)

    return "\n\n<!-- PAGE_BREAK -->\n\n".join(parts)

#!/usr/bin/env python3
"""
Hook UserPromptSubmit: converte automaticamente para .md todo PDF citado no prompt.

Contrato do hook: recebe JSON em stdin ({"prompt", "cwd", ...}) e devolve JSON
em stdout com hookSpecificOutput.additionalContext. Saida 0 sempre — um hook
que quebra o envio do prompt e' pior do que um hook que nao converte nada.
Qualquer erro vira silencio, nunca excecao vazando para o usuario.

Comportamento:
  - acha caminhos .pdf no texto do prompt (com ou sem aspas, com espacos);
  - pula o que ja tem .md atualizado (mtime do .md >= mtime do PDF);
  - converte no maximo MAX_PDFS por prompt e respeita timeout por arquivo;
  - repassa ao modelo o caminho do .md e o AVISO quando o PDF for digitalizado.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

MAX_PDFS = 5
MAX_BYTES = 200 * 1024 * 1024  # 200 MB
TIMEOUT_S = 240
SCAN_EXIT_CODE = 3


def find_wrapper() -> Path | None:
    """Localiza bin/pdf2md: primeiro no projeto, depois no ~/.claude global."""
    here = Path(__file__).resolve()
    candidates = [
        here.parent.parent / "skills" / "pdf-to-markdown" / "bin" / "pdf2md",
        Path.home() / ".claude" / "skills" / "pdf-to-markdown" / "bin" / "pdf2md",
    ]
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_dir:
        candidates.insert(
            0, Path(project_dir) / ".claude" / "skills" / "pdf-to-markdown" / "bin" / "pdf2md"
        )
    for c in candidates:
        if c.is_file() and os.access(c, os.X_OK):
            return c
    return None


def find_pdf_paths(prompt: str, cwd: str) -> list[Path]:
    """Extrai caminhos de PDF existentes do texto livre do prompt.

    Estrategia: para cada ocorrencia de '.pdf', anda para tras encurtando o
    prefixo ate encontrar um arquivo que exista. Assim funciona com caminho
    entre aspas, sem aspas, absoluto, relativo, com ~ e com espacos no nome.
    """
    found: list[Path] = []
    seen: set[str] = set()

    for m in re.finditer(r"\.pdf\b", prompt, flags=re.IGNORECASE):
        end = m.end()
        line_start = prompt.rfind("\n", 0, end) + 1
        segment = prompt[line_start:end]

        best: Path | None = None
        for start in range(len(segment)):
            candidate = segment[start:].strip().strip("\"'`<>()[],;")
            if not candidate:
                continue
            expanded = Path(os.path.expanduser(candidate))
            if not expanded.is_absolute():
                expanded = Path(cwd) / expanded
            try:
                if expanded.is_file():
                    best = expanded.resolve()
                    break  # o mais longo que existe vence
            except OSError:
                continue

        if best and str(best) not in seen:
            seen.add(str(best))
            found.append(best)
        if len(found) >= MAX_PDFS:
            break

    return found


def output_path_for(pdf: Path) -> Path:
    """.md ao lado do PDF; se o diretorio nao for gravavel, cai no cache."""
    if os.access(pdf.parent, os.W_OK):
        return pdf.with_suffix(".md")
    fallback = Path.home() / ".cache" / "pdf-to-markdown" / "converted"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback / (pdf.stem + ".md")


def up_to_date(pdf: Path, md: Path) -> bool:
    try:
        return md.is_file() and md.stat().st_mtime >= pdf.stat().st_mtime and md.stat().st_size > 0
    except OSError:
        return False


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    prompt = payload.get("prompt") or ""
    cwd = payload.get("cwd") or os.getcwd()
    if ".pdf" not in prompt.lower():
        return 0

    wrapper = find_wrapper()
    if wrapper is None:
        return 0

    try:
        pdfs = find_pdf_paths(prompt, cwd)
    except Exception:
        return 0
    if not pdfs:
        return 0

    lines: list[str] = []
    for pdf in pdfs:
        try:
            if pdf.stat().st_size > MAX_BYTES:
                lines.append(f"- `{pdf}`: nao convertido (maior que 200 MB). Converta manualmente.")
                continue
        except OSError:
            continue

        md = output_path_for(pdf)
        if up_to_date(pdf, md):
            lines.append(f"- `{pdf}` -> `{md}` (ja convertido e atualizado)")
            continue

        try:
            proc = subprocess.run(
                [str(wrapper), str(pdf), str(md)],
                capture_output=True,
                text=True,
                timeout=TIMEOUT_S,
            )
        except subprocess.TimeoutExpired:
            lines.append(f"- `{pdf}`: conversao excedeu {TIMEOUT_S}s e foi abortada.")
            continue
        except Exception as e:
            lines.append(f"- `{pdf}`: falha ao converter ({e}).")
            continue

        if proc.returncode == SCAN_EXIT_CODE:
            lines.append(
                f"- `{pdf}` -> `{md}` **PDF DIGITALIZADO SEM OCR: o .md nao tem "
                f"conteudo utilizavel.** Nao extraia fatos dele; leia as paginas "
                f"como imagem ou instale o Tesseract."
            )
        elif proc.returncode != 0:
            err = (proc.stderr or "").strip().splitlines()
            lines.append(f"- `{pdf}`: conversao falhou. {err[-1] if err else ''}")
        else:
            note = ""
            try:
                head = md.read_text(encoding="utf-8", errors="replace")[:200]
                if "PDF2MD:OCR_USED" in head:
                    note = " (texto obtido por OCR — conferir numeros, datas e valores)"
            except OSError:
                pass
            lines.append(f"- `{pdf}` -> `{md}`{note}")

    if not lines:
        return 0

    context = (
        "PDFs citados na mensagem foram convertidos para Markdown automaticamente "
        "(hook pdf_autoconvert). Leia o .md em vez do PDF:\n" + "\n".join(lines)
    )
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": context,
            }
        },
        sys.stdout,
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)

#!/usr/bin/env bash
# Instala esta skill em ~/.claude/skills/ para que fique disponível em TODAS as
# sessões, e não só dentro deste repositório.
#
# Sem argumento: copia (recomendado — a cópia não some se o repo for movido).
# Com --link:    cria symlink apontando para este diretório (edições refletem
#                nos dois lados; quebra se o repo for movido ou apagado).
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="$HOME/.claude/skills/pdf-to-markdown"
HOOK_SRC="$SRC/../../hooks/pdf_autoconvert.py"
HOOK_DEST="$HOME/.claude/hooks/pdf_autoconvert.py"

mkdir -p "$HOME/.claude/skills" "$HOME/.claude/hooks"

if [ -e "$DEST" ] || [ -L "$DEST" ]; then
  echo "Já existe: $DEST"
  read -r -p "Substituir? [s/N] " ans
  [ "$ans" = "s" ] || [ "$ans" = "S" ] || { echo "Abortado."; exit 1; }
  rm -rf "$DEST"
fi

if [ "${1:-}" = "--link" ]; then
  ln -s "$SRC" "$DEST"
  echo "Symlink criado: $DEST -> $SRC"
else
  mkdir -p "$DEST"
  cp -R "$SRC/SKILL.md" "$SRC/bin" "$SRC/scripts" "$SRC/.gitignore" "$DEST/"
  echo "Copiado para: $DEST"
fi

cp "$HOOK_SRC" "$HOOK_DEST"
chmod +x "$HOOK_DEST"
echo "Hook copiado para: $HOOK_DEST"

cat <<'MSG'

Falta um passo manual: registrar o hook em ~/.claude/settings.json.
O instalador NÃO edita esse arquivo — ele pode conter configuração sua que não
deve ser sobrescrita às cegas. Acrescente o bloco abaixo, mesclando com o que
já existir em "hooks":

{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$HOME/.claude/hooks/pdf_autoconvert.py",
            "timeout": 300
          }
        ]
      }
    ]
  }
}

Para OCR de documentos digitalizados (autos escaneados, contratos assinados):
  Debian/Ubuntu: sudo apt-get install -y tesseract-ocr tesseract-ocr-por
  macOS:         brew install tesseract tesseract-lang
MSG

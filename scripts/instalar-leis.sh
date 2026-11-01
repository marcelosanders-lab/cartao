#!/usr/bin/env bash
# Baixa só a base federal essencial do acervo ctresb/leis (~230 MB, ~29,5 mil arquivos).
# O acervo completo passa de 7 GB: não baixe tudo.
set -euo pipefail
DEST="${1:-leis}"
if [ ! -d "$DEST/.git" ]; then
  git clone --depth 1 --filter=blob:none --sparse https://github.com/ctresb/leis.git "$DEST"
fi
cd "$DEST"
git sparse-checkout set --no-cone \
  /constituicao.md \
  /federal/leis-ordinarias/ \
  /federal/leis-complementares/ \
  /federal/decretos-lei/ \
  /federal/emendas-constitucionais/ \
  /jurisprudencia/
git pull --depth 1 -q || true
echo "Arquivos federais: $(find federal -type f | wc -l)"

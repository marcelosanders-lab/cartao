# Origem e modificações

Base: https://github.com/aliceisjustplaying/claude-skill-pdf-to-markdown
(commit `9299034`, obtido em 2026-09-06 por clone raso).

O README upstream declara licença MIT, **mas o repositório não contém arquivo
`LICENSE`**. A declaração está sem instrumento. Antes de redistribuir este
código fora deste repositório, confirmar a licença com o autor.

## Arquivos mantidos como estão

- `scripts/extractor.py` — backends PyMuPDF e Docling, sem alteração.

## Arquivos modificados

- `scripts/pdf_to_md.py` — acrescentada a guarda de PDF digitalizado
  (campo `ocr` em `ExtractionConfig`, entrando na chave de cache; bloco de
  detecção antes da formatação da saída; banner no arquivo gravado; código de
  saída 3 quando não há texto). O restante é upstream.

## Arquivos novos

- `bin/pdf2md` — wrapper portátil. Resolve o diretório da skill a partir da
  própria localização e faz bootstrap do virtualenv. Substitui os caminhos
  hardcoded `~/.claude/skills/pdf-to-markdown/...` do SKILL.md upstream, que
  quebravam quando a skill era instalada dentro de um repositório.
- `scripts/scan_guard.py` — detecção de PDF sem camada de texto, OCR via
  PyMuPDF/Tesseract e os avisos gravados no `.md`.
- `install-global.sh` — instalação em `~/.claude/skills/`.
- `SKILL.md` — reescrito.

## Por que o SKILL.md foi reescrito

O upstream declarava-se *"the preferred method for PDF text extraction"*, o que
faz a skill disparar em qualquer menção a PDF e competir com as skills de
análise jurídica deste ambiente (`analisar-documentos`, `auditar-contrato`,
`analisar-jurisprudencia`, `analisar-caso-consumidor`,
`analisar-processo-assumindo-parte-contraria`, `construir-peticao`). Converter
quando o pedido era analisar entrega meio serviço. A descrição atual delimita a
skill como etapa de preparação de insumo e nomeia as skills que devem prevalecer.

Também foi limitada a instrução de abrir imagens automaticamente, que no
upstream não tinha teto: em autos com dezenas de páginas digitalizadas, isso
consumia o contexto inteiro.

## O furo corrigido

O upstream não faz OCR e não verifica se extraiu alguma coisa: um PDF
digitalizado produzia um `.md` vazio, com saída de sucesso e sem aviso. Aplicado
a autos escaneados, o resultado é o modelo concluindo a partir de nada. Agora a
ausência de camada de texto é medida direto no PDF, antes da conversão, e vira
OCR com ressalva ou aviso em bloco com código de saída 3.

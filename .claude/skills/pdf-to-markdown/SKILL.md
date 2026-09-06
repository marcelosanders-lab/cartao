---
name: pdf-to-markdown
description: Converte mecanicamente arquivos PDF em Markdown (.md), preservando cabeçalhos, tabelas, listas e imagens. É uma ETAPA DE PREPARAÇÃO DE INSUMO, não de análise. Use quando o pedido for de conversão ou extração de formato — "converte esse PDF", "transforma esse PDF em markdown", "extrai o texto desse PDF", "gera o .md desse arquivo", "esse PDF está ilegível, limpa" — ou quando outra skill precisar do conteúdo de um PDF como texto antes de trabalhar. NÃO use para analisar, resumir, criticar, opinar ou decidir sobre o conteúdo: análise de autos, provas, contratos, decisões, jurisprudência e casos pertence às skills analisar-documentos, auditar-contrato, analisar-jurisprudencia, analisar-caso-consumidor, analisar-processo-assumindo-parte-contraria e construir-peticao — essas skills invocam esta apenas para obter o texto e seguem com a análise. NÃO faz OCR por conta própria em todo caso: PDF digitalizado sem Tesseract instalado produz aviso em bloco, não conteúdo.
---

# PDF → Markdown (conversor)

Ferramenta de conversão. Entra um `.pdf`, sai um `.md` com o texto, as tabelas
e as imagens extraídas. Só isso.

## Fronteira desta skill

**Esta skill converte. Ela não analisa.**

| Pedido | Skill correta |
|---|---|
| "converte esse PDF", "extrai o texto", "gera o .md" | **esta skill** |
| "analisa esses documentos", "essas provas valem?" | `analisar-documentos` |
| "audita esse contrato", "acha falhas no contrato" | `auditar-contrato` |
| "esse precedente se aplica?", "analisa essa decisão" | `analisar-jurisprudencia` |
| "analisa esse caso", "vale a pena entrar com a ação?" | `analisar-caso-consumidor` |
| "monta a defesa", "escreve a petição" | `construir-peticao` |

Se o usuário entregar um PDF **e** pedir análise, o pedido é de análise: acione
a skill de análise cabível. Ela chama esta aqui para obter o texto. Nunca
substitua a análise pela conversão — entregar um `.md` quando pediram parecer
é entregar meio serviço.

## Conversão automática (hook)

O hook `UserPromptSubmit` em `.claude/hooks/pdf_autoconvert.py` já converte
sozinho todo PDF citado na mensagem do usuário, e informa o caminho do `.md`.
Na maioria dos casos **não é preciso rodar nada manualmente** — o `.md` já
existe quando você lê a mensagem. Confira o contexto antes de converter de novo.

Limites do hook: no máximo 5 PDFs por mensagem, 200 MB por arquivo, 240s de
timeout por conversão. Fora desses limites, converta manualmente.

## Uso manual

O wrapper resolve o próprio caminho, então funciona igual em
`~/.claude/skills/` ou em `.claude/skills/` de um repositório. Use sempre o
wrapper, nunca `python scripts/pdf_to_md.py` direto.

```bash
# a partir da raiz do projeto
.claude/skills/pdf-to-markdown/bin/pdf2md documento.pdf            # -> documento.md
.claude/skills/pdf-to-markdown/bin/pdf2md documento.pdf saida.md   # caminho customizado
.claude/skills/pdf-to-markdown/bin/pdf2md documento.pdf --docling  # tabelas complexas
```

Instalado globalmente, o caminho é `~/.claude/skills/pdf-to-markdown/bin/pdf2md`.

O wrapper cria o virtualenv e instala as dependências na primeira execução.
Não há passo de setup manual.

### Opções

| Opção | Efeito |
|---|---|
| `--docling` (= `--accurate`) | Tabelas via IBM TableFormer. ~1s/página; baixa ~500 MB de modelos na 1ª vez. |
| `--no-progress` | Sem indicador de progresso |
| `--clear-cache` | Limpa o cache deste PDF e reextrai |
| `--clear-all-cache` | Limpa o cache inteiro |
| `--cache-stats` | Estatísticas do cache |

Use `--docling` quando as tabelas saírem embaralhadas no modo padrão, ou quando
a exatidão da tabela for crítica (planilha de cálculo, extrato, laudo).

## PDF digitalizado — leia antes de usar o resultado

O conversor lê a **camada de texto** do PDF. Documento digitalizado (autos
escaneados, contrato assinado, foto de fatura, print) não tem camada de texto.

O script detecta isso sozinho, medindo a camada nativa antes de qualquer coisa,
e responde de três formas:

1. **Camada de texto presente** → conversão normal, sem aviso.
2. **Sem camada, Tesseract disponível** → aplica OCR e insere no topo do `.md`
   o marcador `<!-- PDF2MD:OCR_USED -->` com aviso de que números, datas,
   valores e nomes podem estar corrompidos. **Trate esse texto como leitura
   provável, não como transcrição fiel.** Não cite valor, data ou número de
   processo vindo de OCR sem conferir na imagem da página.
3. **Sem camada, sem Tesseract** → grava `<!-- PDF2MD:SCANNED_NO_OCR -->` com
   aviso em bloco e sai com código 3. **O arquivo não tem conteúdo utilizável.
   Não extraia fato nenhum dele.** Ou instale o Tesseract, ou leia as páginas
   como imagem.

Instalação do OCR:

```bash
sudo apt-get install -y tesseract-ocr tesseract-ocr-por   # Debian/Ubuntu
brew install tesseract tesseract-lang                     # macOS
```

Idioma do OCR: `PDF2MD_OCR_LANG` (padrão `por+eng`). Resolução: `PDF2MD_OCR_DPI`
(padrão 300).

## Imagens

Imagens são extraídas para `images/` ao lado do `.md`, referenciadas por caminho
relativo e listadas em tabela no fim do documento.

**Quando abrir uma imagem com a ferramenta Read:** só quando a pergunta depender
do conteúdo visual (gráfico, diagrama, organograma, assinatura, carimbo,
fotografia de dano) e o texto não responder. **Abra no máximo 3 imagens por
resposta**, escolhidas pela relevância. Um PDF de autos gera dezenas de imagens;
lê-las todas queima o contexto e não melhora a resposta. Se precisar de mais,
diga ao usuário quais e por quê, em vez de abrir em série.

## Cache

Cache em `~/.cache/pdf-to-markdown/`, com chave de conteúdo + modo de extração
(`fast`, `docling`, `ocr`). Invalidado quando o PDF muda, quando a versão do
extrator muda, ou por `--clear-cache`.

**Em sessão remota/efêmera o cache não sobrevive ao container.** A promessa de
"extrai uma vez, reusa sempre" vale na máquina local; em container, cada sessão
extrai de novo.

## Estrutura

```
.claude/skills/pdf-to-markdown/
├── SKILL.md
├── bin/pdf2md            # wrapper portátil: bootstrap do venv + execução
└── scripts/
    ├── pdf_to_md.py      # CLI (upstream + guarda de digitalização)
    ├── extractor.py      # backends PyMuPDF / Docling (upstream, intocado)
    └── scan_guard.py     # detecção de PDF digitalizado + OCR + avisos
```

## Diagnóstico

| Sintoma | Causa provável | Ação |
|---|---|---|
| `.md` só com aviso em bloco | PDF digitalizado, sem OCR | instalar Tesseract |
| Texto com erros em números/datas | veio de OCR | conferir na imagem da página |
| Tabelas embaralhadas | tabela sem borda / mesclada | `--docling` |
| `ModuleNotFoundError` | venv corrompido | `rm -rf .venv` e rodar o wrapper de novo |
| Nada acontece com PDF citado | hook não instalado neste projeto | rodar `bin/pdf2md` manualmente |

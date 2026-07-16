---
name: sanberg-brand
description: Applies the Sanberg Soluções Jurídicas visual identity (Marcelo Sanberg, advogado) to any document or page — colors, typography, spacing, logo, and printable legal-document layout. Use whenever creating or restyling a page, card, letterhead, or legal document (petição, procuração, contrato, parecer) for this law firm.
---

# Sanberg Soluções Jurídicas — Identidade Visual

Banca de advocacia de Porto Alegre/RS voltada a indivíduos e famílias de alto
patrimônio. Personalidade de marca: inovação + tecnologia, com a autoridade de
uma instituição sólida. Este skill traz os tokens de design e os templates
necessários para manter qualquer peça (site, cartão, papelaria, petição) fiel
à marca.

**Keywords**: Sanberg, advocacia, advogado, jurídico, petição, procuração,
brand, identidade visual, OAB, papelaria, letterhead.

## Design Tokens

Fonte canônica: `assets/manual-tokens.css` (bloco `:root`). Copie as variáveis
diretamente para o CSS do projeto em vez de redigitar os valores.

### Cores

| Token | Nome | HEX | Uso |
|---|---|---|---|
| `--navy` | Sanberg Navy | `#0E2A45` | Primária / institucional |
| `--navy-deep` | Midnight | `#081726` | Fundos escuros / capas |
| `--navy-700` | Navy 700 | `#15375A` | Hover / variação |
| `--gold` | Ouro Sanberg | `#C19A4B` | Acento principal |
| `--gold-bright` | Ouro claro | `#D4B26A` | Acento sobre navy |
| `--champagne` | Champanhe | `#E7D8B5` | Realce claro |
| `--steel` | Aço | `#3D5B79` | Secundária / dados |
| `--slate` | Ardósia | `#6E8497` | Secundária / legendas |
| `--paper` | Papel | `#F7F5EF` | Fundo base |
| `--cloud` | Nuvem | `#EAE7DE` | Fundo de cartão / mock |
| `--ink` | Tinta | `#14191E` | Texto corrente |
| `--grey` | Cinza | `#5C666D` | Texto secundário |
| `--hairline` | Fio | `#D9D5CB` | Bordas / divisores |

Proporção de uso: 60% Papel/branco · 28% Navy · 8% Ouro · 4% Aço.
Ouro sobre branco tem contraste reprovado (2.6:1) — use ouro só sobre navy ou
em elementos decorativos/grandes, nunca como texto sobre fundo claro.

### Tipografia

Três famílias (Google Fonts):
- **Spectral** (serifada) — títulos e display. Pesos 300–700 + itálico 400.
- **Space Grotesk** (grotesca) — corpo e interface. Pesos 300–700.
- **IBM Plex Mono** (monoespaçada) — dados, legendas técnicas, eyebrows
  (sempre UPPERCASE, letter-spacing amplo, ex. `.28em`).

```css
@import url('https://fonts.googleapis.com/css2?family=Spectral:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Space+Grotesk:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
```

| Estilo | Família | Peso | Uso |
|---|---|---|---|
| Display/H1 | Spectral | 600 | Capa, nome da marca, título de seção |
| H2/H3 | Spectral | 500 | Subtítulo / bloco |
| Subtítulo/Corpo | Space Grotesk | 400–500 | Texto corrente e interface |
| Técnico | IBM Plex Mono | 500 | Códigos, eyebrows, metadados |

### Espaçamento e forma

Escala 8pt: `8·16·24·32·48·64·96·128` px. Raio de cards 10–12px; pills 30px.
Borda padrão `1px solid var(--hairline)`. Acento de bloco: borda superior
`2px solid var(--gold)`. Sombra de mockup: `0 24px 60px -22px rgba(8,23,38,.45)`.

## Logo

O monograma é o "S" da Sanberg, com 3 conceitos (ver `assets/logos.jsx` para o
SVG de referência, portável para qualquer framework):

1. **Vértice** — três barras escalonadas + dois nós circulares formando um "S"
   ascendente. **Marca principal, use por padrão.**
2. **Pórtico** — "S" serifado emoldurado por cantoneira dupla. Peças formais.
3. **Égide** — "S" serifado branco sob escudo navy. Selos e assinaturas.

Lockup padrão: monograma + "Sanberg" (Spectral 600) + "Soluções Jurídicas"
(IBM Plex Mono, uppercase, letter-spacing `.34em`). Área de proteção = altura
do monograma em todos os lados. Tamanho mínimo: 24mm/120px (lockup), 10mm/32px
(símbolo isolado).

SVG mínimo do monograma Vértice (usar quando não puder importar o componente):

```html
<svg width="30" height="30" viewBox="0 0 64 64">
  <rect x="24" y="11" width="28" height="8" rx="4" fill="#0E2A45"/>
  <rect x="14" y="28" width="36" height="8" rx="4" fill="#C19A4B"/>
  <rect x="12" y="45" width="28" height="8" rx="4" fill="#0E2A45"/>
  <circle cx="50" cy="15" r="4" fill="#C19A4B"/>
  <circle cx="14" cy="49" r="4" fill="#C19A4B"/>
</svg>
```

## Gerando documentos jurídicos (petições, procurações, contratos, pareceres)

Use `assets/peticao-template.html` como ponto de partida — já traz cabeçalho
de marca, rodapé com dados de contato/OAB, e a estrutura padrão de uma peça
processual (endereçamento, qualificação das partes, seções numeradas
"Dos Fatos / Do Direito / Dos Pedidos", fechamento com local/data e
assinatura). Copie o arquivo, renomeie e:

1. Substitua todos os placeholders entre colchetes (`[NOME DO(A) AUTOR(A)]`,
   `[endereço completo]`, etc.) pelos dados reais do caso.
2. Ajuste o título da peça (ação de conhecimento, contestação, recurso etc.)
   e a numeração/títulos de seção conforme o tipo de peça.
3. Mantenha o cabeçalho de marca, o rodapé e a formatação tipográfica
   (Spectral para títulos, Space Grotesk para corpo, IBM Plex Mono para
   metadados) — são a identidade visual, não texto de exemplo.
4. O documento usa o web component `<doc-page>` (`assets/doc-page.js`) para
   paginação A4 imprimível — copie o script junto do HTML. Ver os comentários
   no topo de `doc-page.js` para atributos (`size`, `margin`, `orientation`,
   slots `header`/`footer`).
5. Dados reais de contato do escritório (telefone, endereço, e-mail, OAB)
   devem substituir os placeholders fictícios antes de qualquer uso real —
   nunca publique/imprima com os dados de exemplo do manual.

## Aplicando a marca em outras peças (site, cartão, papelaria)

Para uma página ou componente novo: importe os tokens de cor/tipografia de
`assets/manual-tokens.css`, use o monograma Vértice como ícone/avatar padrão,
e respeite a proporção de cor (predominância de papel/navy, ouro só como
acento). Para peças institucionais mais formais (certificados, assinaturas),
prefira os conceitos Pórtico ou Égide em vez do Vértice.

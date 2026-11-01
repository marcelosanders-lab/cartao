# Regras para citação e revisão de normas

Acervo de consulta: `leis/` (clone parcial de github.com/ctresb/leis).
Se a pasta não existir, rode `scripts/instalar-leis.sh` antes de qualquer revisão.

## O acervo NÃO é fonte oficial
Montado por conversão automática e OCR. Defeitos conhecidos (verificados em 01/11/2026):
- `versao_texto: "compilada (texto vigente)"` não garante que esteja atualizado. Exemplo:
  o Código Civil exibe os arts. 757 a 802 como vigentes, embora revogados pela Lei 15.040/2024.
- Cerca de 85% das leis federais estão na redação original.
- Algumas leis trazem só as partes vetadas (ex.: Lei 14.133/2021, LC 214/2025, Lei 14.365/2022).
- Alterações recentes podem faltar (ex.: CPC sem a Lei 15.484/2026; LGPD sem a Lei 15.352/2026).

## Regras obrigatórias
1. Nunca cite artigo de memória. Antes de citar, abra o arquivo em `leis/` e leia o dispositivo.
2. Em toda citação, informe o caminho do arquivo e o campo `versao_texto`.
3. Avise que pode estar desatualizado quando a versão for "original" ou
   "republicação/retificação", quando o artigo faltar ou quando houver lei posterior sobre o tema.
4. Se o dispositivo tiver "Vide", abra também a norma referida e verifique revogação ou alteração.
5. Em toda REVISÃO de peça: confira cada dispositivo citado contra o acervo e aponte
   divergência de redação, artigo revogado, dispositivo inexistente ou numeração errada.
6. Termine com a lista de tudo o que foi citado, para conferência no Planalto/DOU.

# Anexa velas novas reaproveitando as fechadas da leitura anterior.
#
#   . radar/velas.sh
#   v1 BTC_USDT "<linha 1d mais nova>" ["<seguinte>" ...]
#   v4 BTC_USDT "<linha 4h mais nova>" ["<seguinte>" ...]
#
# Linha: timestamp,open,high,low,close,volume_usd - da mais nova para a mais
# antiga, exatamente como a Crypto.com devolve.
#
# Passe TODAS as velas que mudaram desde a leitura anterior: a que estava em
# formacao (agora fechada, com numeros definitivos) mais as que fecharam depois
# mais a nova em formacao. O helper descarta a antiga vela em formacao, mantem
# 50 linhas e RECUSA o arquivo se sobrar buraco na serie.
#
# Sem radar/dados/<PAR>_<tf>.csv da leitura anterior (container novo), o
# reaproveitamento e impossivel: grave as 50 velas da resposta inteira.

_velas_anexar() {
  tf=$1; p=$2; shift 2
  base="radar/dados/${p}_${tf}.csv"
  out="radar/dados.novo/${p}_${tf}.csv"
  [ "$tf" = 1d ] && passo=86400 || passo=14400
  k=$#

  if [ ! -f "$base" ]; then
    echo "ERRO ${p}_${tf}: sem base em $base - colete as 50 velas inteiras" >&2
    return 1
  fi
  nb=$(wc -l < "$base")
  if [ "$nb" != 50 ]; then
    echo "ERRO ${p}_${tf}: base tem $nb linhas, esperado 50" >&2
    return 1
  fi
  if [ "$k" -lt 1 ] || [ "$k" -gt 49 ]; then
    echo "ERRO ${p}_${tf}: $k velas novas, esperado entre 1 e 49" >&2
    return 1
  fi

  # continuidade: a vela mais antiga do lote novo tem de encostar na primeira
  # vela reaproveitada. E isto que impede o buraco silencioso na serie.
  for r in "$@"; do mais_antiga=$r; done
  t_nova=$(printf '%s' "$mais_antiga" | cut -d, -f1)
  t_ret=$(sed -n 2p "$base" | cut -d, -f1)
  e_nova=$(date -u -d "$t_nova" +%s 2>/dev/null) || {
    echo "ERRO ${p}_${tf}: timestamp invalido $t_nova" >&2; return 1; }
  e_ret=$(date -u -d "$t_ret" +%s 2>/dev/null) || {
    echo "ERRO ${p}_${tf}: timestamp invalido na base $t_ret" >&2; return 1; }
  if [ "$((e_nova - e_ret))" -ne "$passo" ]; then
    echo "ERRO ${p}_${tf}: buraco na serie - mais antiga do lote $t_nova," \
         "primeira reaproveitada $t_ret (faltam velas no meio)" >&2
    return 1
  fi

  mkdir -p radar/dados.novo
  { for r in "$@"; do printf '%s\n' "$r"; done
    tail -n +2 "$base" | head -n "$((50 - k))"; } > "$out"

  n=$(wc -l < "$out")
  if [ "$n" != 50 ]; then
    echo "ERRO ${p}_${tf}: saiu com $n linhas" >&2; return 1
  fi
  d=$(cut -d, -f1 "$out" | sort | uniq -d | head -1)
  if [ -n "$d" ]; then
    echo "ERRO ${p}_${tf}: timestamp repetido $d" >&2; return 1
  fi
  return 0
}

v1() { _velas_anexar 1d "$@"; }
v4() { _velas_anexar 4h "$@"; }

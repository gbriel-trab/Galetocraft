#!/usr/bin/env bash
# Baixa SÓ os arquivos de alguns Pokémon do Cobblemon (modelo, animações, poser, resolver, texturas e ficha da
# espécie), com clone esparso e sem histórico. Não usa a API do GitLab (que limita requisições).
#
# Uso: baixar_cobblemon.sh PASTA_DESTINO POKEMON [POKEMON ...]
#   POKEMON: o nome (blaziken) ou a pasta com número (0257_blaziken).
#   TAG=1.8.4 baixar_cobblemon.sh ...  fixa a versão; sem TAG, usa a tag de versão mais recente.
#   CODIGO="BipedWalkAnimation.kt ClientMoLangFunctions.kt" acrescenta arquivos de código pelo nome.
#
# A pasta de destino deve ficar FORA do repositório do projeto: os modelos são CC BY-NC 3.0 e os Pokémon são da
# Nintendo. Depois, para ler outro arquivo do código sem baixar tudo: `git -C PASTA show HEAD:caminho/Arquivo.kt`
# (o clone é parcial: o arquivo vem sob demanda) e `git -C PASTA ls-tree -r --name-only HEAD | grep Nome` para achar.
set -euo pipefail
[ $# -ge 2 ] || { sed -n '2,13p' "$0"; exit 1; }
destino=$1; shift
REPO=https://gitlab.com/cable-mc/cobblemon.git
tag=${TAG:-$(git ls-remote --tags --refs "$REPO" | awk -F/ '{print $3}' | grep -E '^[0-9]+(\.[0-9]+){1,2}$' | sort -V | tail -1)}
echo "Cobblemon $tag -> $destino"
git clone -q --filter=blob:none --no-checkout --depth 1 --branch "$tag" "$REPO" "$destino"
cd "$destino"
MODELOS=common/src/main/resources/assets/cobblemon/bedrock/pokemon/models
padroes=("/LICENSE" "/README.md")
for p in "$@"; do
  if [[ ! $p =~ ^[0-9]{4}_ ]]; then
    achado=$(git ls-tree --name-only HEAD "$MODELOS/" | sed 's#.*/##' | grep -i -E "^[0-9]{4}_${p}$" | head -1 || true)
    [ -n "$achado" ] || { echo "não achei a pasta de '$p' em $MODELOS" >&2; exit 2; }
    p=$achado
  fi
  padroes+=("**/$p/**" "**/species/*/${p#*_}.json")
done
for c in ${CODIGO:-}; do padroes+=("**/$c"); done
git sparse-checkout set --no-cone "${padroes[@]}"
git checkout -q "$tag"
echo "commit $(git log -1 --format='%h %cd' --date=short)"
find . -path ./.git -prune -o -type f -print | sed 's#^\./##' | sort

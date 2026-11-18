# Galetocraft — instruções para o Claude

Projeto de mod de Minecraft com criaturas chamadas Cocorídeos/Galetos, batalhas por turnos (Rinhas), captura, reprodução e Mestres Elementais. Fale com o usuário em português do Brasil.

## Papel

- **Desde 18/11/2026 o Claude é o responsável por todo o projeto**, por decisão do criador: base de dados, regras, documentação, modelos e código do mod.
- **O ChatGPT serve apenas para gerar imagens.** Não existe mais base nem auditoria no ChatGPT.
- **O criador continua sendo quem aprova.** Nada vira oficial sem aprovação expressa dele. O Claude propõe, confere, registra e implementa.

## Fonte de verdade

- **Base vigente:** `base/vigente/*.json`, com artes em `base/artes/` e fontes em `base/fontes/`. Revisão atual: **7**. Manual em `base/LEIA_ME.md`.
- **Ferramenta:** `python ferramentas/base/galetobase.py` com os comandos `validar`, `ficha --especie N`, `atualizar --pacote`, `migrar --pacote` e `montar`.
- **Toda mudança na base** segue estes passos:
  1. Escrever um pacote em `docs/patches/` com `expected_revision`, `reason` e `evidence`.
  2. Aplicar com `atualizar`, para registros que já existem, ou `migrar`, para registros novos ou metadados.
  3. Rodar `validar`.
  4. Fazer o commit.

  Nunca edite os JSON à mão, nunca crie outra base ativa e não invente atributos, golpes, artes nem parâmetros.
- **Histórico:** o `Galetocraft.sqlite` da revisão 2 no Release `acervo-documental-2026-11-17` (pacote 00) e todo o acervo são históricos, preservados sem alteração. Use `montar` para gerar o SQLite completo (histórico + vigente). Os arquivos `*.sqlite` não são versionados.
- **"Homologado" não significa "implementado".** Tudo tem `runtime_validado = false`. Diga sempre se uma regra está só documentada ou se foi verificada no código.
- **Atributos-base são do nível 50.** O rótulo "nível 100" em fichas antigas é erro de rótulo. Para conferir fichas, use `docs/acervo_corrigido/` (ver `docs/ERRATA_NIVEL_50.md`).
- **Nomenclatura oficial** (regra `nomenclatura` na base; ver `docs/NOMENCLATURA_OFICIAL.md`):

  | Nome oficial | Nome antigo |
  |---|---|
  | Galetário | RoosterTeca |
  | Galolpédia | GalolpeTeca |
  | Herança de Bico | GalolpeTeca Hereditária |
  | Tonto | Tontura |
  | Ave Fênix | Tricrina Infernal |
  | Histórico da Rinha | Diário de Batalha |

  - Também são oficiais **Rinha** (o botão continua "Combate"), **Cocorídeos/Galeto** e **Galeria**.
  - Nomes antigos só aparecem em caminhos, arquivos, tabelas, chaves JSON, IDs em minúsculas e citações históricas.
- **Decisões do criador de 18/11/2026** (ver `docs/AUDITORIA_INCOERENCIAS.md`):
  - O mod é de todos os direitos reservados.
  - "Lendário Original" é uma classe própria, fora da escala; o Quetzacocó soma 700.
  - O par de gêmeos Cocórion+Cocórvolt fica inativo.
  - #007–#015 não têm golpe hereditário, por design.

## Imagens (ChatGPT)

O fluxo completo está em `base/LEIA_ME.md`. Em resumo:
1. Eu preparo o pedido com os dados da ficha vigente.
2. O criador gera a imagem no ChatGPT e me envia.
3. Eu confiro espécie, textos impressos, nomenclatura, originalidade (sem personagens de outras franquias) e SHA-256.
4. A imagem só entra em `current_art` ou em `modelos/referencias/` depois da aprovação expressa do criador, por migração.

## Acervo do Release

- Para extrair um arquivo de um ZIP sem baixar o pacote inteiro (cerca de 800 MB cada), use HTTP Range.
- Confira o SHA-256 contra `INVENTARIO_GALETOCRAFT.json`.
- Ferramentas em `ferramentas/acervo/`: correção do nível 50, aplicação da nomenclatura e gerador do pacote rev. 3.

## Código

- **Mod:** fica em `galetocraft/` e usa Fabric 1.21.11 com GeckoLib 5.4.5.
  - Para compilar: `JAVA_HOME=$(ls -d /usr/lib/jvm/java-25-openjdk-*) bash gradlew build`, com o JDK 25 instalado por `apt-get install -y openjdk-25-jdk-headless`.
  - Os testes rodam com `bash gradlew :nucleo:test`.
  - O build precisa do ambiente de nuvem "Galetocraft", que libera Fabric, Mojang e GeckoLib.
  - O `gradlew` não tem permissão de execução; use `bash gradlew`.
- **Núcleo de regras:** `galetocraft/nucleo`, em Java puro, embutido no jar.
  - Lê os dados de `nucleo/src/main/resources/galetocraft/dados/`, gerados por `python ferramentas/base/exportar_para_mod.py`. Rodar o exportador de novo depois de cada revisão da base.
  - O motor da Rinha fica em `br.galetocraft.nucleo.rinha`.
- **Implementado no mod:**
  - 12 entidades com IA neutra e LOD. Cada uma é um Galeto individual com nível, sexo e IVs salvos.
  - Comandos `/galetocraft base | ficha | rinha | duelo` (simulação), `desafiar | acao` (Rinha jogável contra Galeto selvagem, com menu clicável no chat), `equipe` (equipe do treinador) e `pena`.
  - Pena de Captura: captura no mundo (botão direito, 12 blocos, visão livre, espera após falha) e na Rinha (Itens → Pena de Captura). O capturado vai para a equipe principal (até 5) ou para as reservas, salvos com o jogador.
  - XP dos Cocorídeos por Rinha vencida (regra `experiencia`), com subida de nível.
  - Testes de cliente `RinhaTesteCliente` e `CapturaTesteCliente`. Para rodar sem placa de vídeo: `GALETO_TESTES=rinha,captura LIBGL_ALWAYS_SOFTWARE=1 xvfb-run -a bash gradlew runClientGameTest`.
- **Ainda falta:** golpes próprios do Galeto e aprendizado por nível, tela própria da Rinha, Galetário no jogo, passivas e efeitos de golpes, e reprodução. O roteiro está em `docs/ANALISE_DESENVOLVIMENTO.md` e o andamento em `docs/PROGRESSO_DESENVOLVIMENTO.md`.
- **Modelos:** rode `ferramentas/especies/<id>.py` e depois `ferramentas/exportar_especie.py <id>`, como descrito em `galetocraft/LEIAME.md`.
- **Git LFS:** os arquivos de `modelos/*/revisao/` e os PNGs do benchmark estão no LFS. Nesta cópia há só ponteiros.

## Conhecimento consolidado

O resumo completo (espécies, regras, sistemas, pendências e mapa do acervo) está em `docs/CONHECIMENTO_GALETOCRAFT.md`.

@docs/CONHECIMENTO_GALETOCRAFT.md

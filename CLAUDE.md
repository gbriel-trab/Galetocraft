# Galetocraft — instruções para o Claude

Projeto de mod de Minecraft com criaturas chamadas Cocorídeos/Galetos, batalhas por turnos (Rinhas), captura, reprodução e Mestres Elementais. Fale com o usuário em português do Brasil.

## Regras de trabalho

- **Fonte de verdade única:** `Galetocraft/Base_Atual/Galetocraft.sqlite`, que está em `Galetocraft_00_Base_Vigente.zip` no Release `acervo-documental-2026-11-17`.
  - Ler apenas `current_*` e `v_current_*`.
  - A tabela `species` e as demais tabelas são histórico.
  - A exportação `DADOS_VIGENTES_CONSULTA.json` do mesmo Release é derivada e serve para consulta rápida.
- **Nada é oficial sem aprovação expressa do criador.** Propostas, Betas, ramos R e estudos ficam separados e não são promovidos por inferência. Não inventar atributos, golpes, artes nem parâmetros ausentes.
- **"Homologado" não significa "implementado".** Tudo no banco tem `runtime_validado = false`. Diga sempre se uma regra está só documentada ou se foi verificada no código.
- **Para alterar a base:**
  - Usar `Atualizar_Galetocraft.py` com `expected_revision`, fonte e evidência.
  - Nunca criar outra base ativa, como uma "Beta 1.8".
  - Registro novo exige migração completa validada.
- **Atributos-base são do nível 50**, confirmado pelo criador.
  - O rótulo "nível 100" em fichas antigas é um erro de rótulo: os números são os mesmos.
  - Para conferir fichas, use `docs/acervo_corrigido/` e veja `docs/ERRATA_NIVEL_50.md`.
- **Nomenclatura oficial** (desde 18/11/2026; ver `docs/NOMENCLATURA_OFICIAL.md`):

  | Nome oficial | Nome antigo |
  |---|---|
  | Galetário | RoosterTeca |
  | Galolpédia | GalolpeTeca |
  | Herança de Bico | GalolpeTeca Hereditária |
  | Tonto | Tontura |
  | Ave Fênix | Tricrina Infernal |
  | Histórico da Rinha | Diário de Batalha |

  - Também são oficiais **Rinha** (a atividade; o botão continua "Combate"), **Cocorídeos/Galeto** e **Galeria**.
  - Use sempre o nome oficial em textos, interface e documentação.
  - Nomes antigos só ficam em caminhos, nomes de arquivo, tabelas, chaves JSON, IDs em minúsculas e citações históricas.
- **Decisões do criador de 18/11/2026** (auditoria completa em `docs/AUDITORIA_INCOERENCIAS.md`):
  - O mod é de **todos os direitos reservados**.
  - **Lendário Original** é uma classe própria, fora da escala; o Quetzacocó soma 700.
  - O par de gêmeos especiais Cocórion+Cocórvolt fica **inativo**.
  - #007–#015 **não têm golpe hereditário**, por design.
- **Pacote rev. 3 da base:** `docs/patches/rev3_coerencia_e_nomenclatura.json` reúne as correções de coerência e a nomenclatura. Foi testado, mas ainda não foi publicado na base principal. Até lá, a base do Release continua na revisão 2.
- **Arquivos grandes do Release:** use HTTP Range para extrair um arquivo de um ZIP sem baixar o pacote inteiro. Os pacotes 01–13 têm cerca de 800 MB cada. Confira o SHA-256 contra `INVENTARIO_GALETOCRAFT.json`.

## Código

- **Mod:** fica em `galetocraft/` e usa Fabric 1.21.11 com GeckoLib 5.4.5. Para compilar, rodar `gradlew build`; o Gradle precisa de JDK 25.
- **Implementado:** só 12 entidades exibidas com IA neutra e LOD.
- **Não implementado:** Rinha, captura, golpes, elementos e reprodução.
- **Modelos:** o fluxo atual é rodar `ferramentas/especies/<id>.py` e depois `ferramentas/exportar_especie.py <id>`. O `LEIAME.md` ainda descreve o fluxo antigo.
- **Git LFS:** os arquivos de `modelos/*/revisao/` e os PNGs do benchmark estão no LFS. Nesta cópia há só ponteiros.

## Conhecimento consolidado

O resumo completo (espécies, regras, sistemas, pendências e mapa do acervo) está em `docs/CONHECIMENTO_GALETOCRAFT.md`.

@docs/CONHECIMENTO_GALETOCRAFT.md

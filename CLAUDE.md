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
- **Arquivos grandes do Release:** use HTTP Range para extrair um arquivo de um ZIP sem baixar o pacote inteiro. Os pacotes 01–13 têm cerca de 800 MB cada. Confira o SHA-256 contra `INVENTARIO_GALETOCRAFT.json`.

## Conhecimento consolidado

O resumo completo (espécies, regras, sistemas, pendências e mapa do acervo) está em `docs/CONHECIMENTO_GALETOCRAFT.md`.

@docs/CONHECIMENTO_GALETOCRAFT.md

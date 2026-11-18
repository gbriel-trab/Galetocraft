# Galetocraft — Progresso do desenvolvimento

O roteiro e a comparação entre o design e o mod estão em `docs/ANALISE_DESENVOLVIMENTO.md`. Aqui fica o registro do que foi feito, sessão a sessão.

## 18/11/2026 — Fases 1 e 2 concluídas; começo da integração com o mod

### Ambiente de compilação
- **O mod compila e roda nesta nuvem:**
  - O ambiente "Galetocraft" libera Fabric, Mojang e GeckoLib.
  - O JDK 25 vem do apt (`openjdk-25-jdk-headless`).
  - Como o `gradlew` está sem permissão de execução, chamar com `bash gradlew`.
- **Validado num servidor dedicado de verdade** (`bash gradlew runServer --args=nogui`):
  - O mod carrega a base embutida ("Base vigente rev. 6 com 23 espécies").
  - Os comandos `/galetocraft` respondem.

### Base vigente
- **Revisão 5:** 10 regras oficiais que só existiam em tabelas históricas foram migradas para `current_rules`.
  - Regras: `matriz_elemental`, `dano_v5_6`, `combate_universal`, `estados_negativos`, `climas`, `santuarios`, `itens_segurados`, `captura`, `experiencia` e `treinador`.
  - O dano V5.6, homologado em 13/11, não estava na base. As regras superadas ficaram listadas como não vigentes.
- **Revisão 6:** 32 golpes próprios das espécies #001–#011 só tinham texto provisório ("consultar o JSON original protegido").
  - Foram completados com dados da ficha original protegida (tabela histórica `moves`): categoria, elemento, estado aplicado com chance e efeito estruturado.
  - Exemplos: Punho das Dunas aplica Tonto com 20% de chance, e Prisão das Areias é física.

### Núcleo de regras (`galetocraft/nucleo`)
É Java puro, sem Minecraft, embutido no jar do mod. Os dados vêm da base, gerados por `ferramentas/base/exportar_para_mod.py`. Há 21 testes, todos passando (`bash gradlew :nucleo:test`).

| Parte | Conteúdo |
|---|---|
| `dados` | Galetário com 23 espécies, 690 golpes e 33 regras; elementos, atributos, categorias, estados |
| `Eficacia` | Matriz 6×6, Tipagem Dupla V1 e Nexo V2.0 (tabela final do Quetzacocó conferida) |
| `Progressao` | Nível 50 → 100, com `A50×(L+50)/100`. A curva 1–49 dá erro, de propósito, por estar pendente |
| `DanoV56` | Fórmula oficial com os 6 exemplos e os 7 modificadores da especificação, todos conferidos |
| `Velocidade` | Esquiva universal e Golpe Duplo V2.2 |
| `MiraAnatomica` | Regiões (precisão), Guarda, Pressão, Exposição, Ruptura, decaimento |
| `Energia` e `PenaDeRitmo` | Energia, Concentração V2.3 e ciclo da Pena |
| `Estados` | Queimadura, Envenenamento progressivo, Tonto, Paralisia |
| `Ambiente` | 4 climas e 2 santuários, lidos da base |
| `Captura` | Fórmula, Pena de 5 níveis, Lendário só com Pena 5, cooldown, XP da Pena |
| `Experiencia` | Curva de XP, recompensa e fator de desafio |
| `rinha` | Motor de turnos (3v3, trocas, ordem por Velocidade, dano, 2º acerto, estados, Concentração/Pena, Mira, substituição), IA básica, simulador |

### No mod
- **Ao iniciar,** o mod carrega o Galetário e registra os comandos.
- **Comandos:**
  - `/galetocraft base`: revisão e contagens.
  - `/galetocraft ficha <espécie>`: número ou nome sem acento, ex.: `22` ou `sirenoco`.
  - `/galetocraft rinha <a> <b> [nível]`: Rinha 1×1 simulada, com o Histórico da Rinha.
  - `/galetocraft duelo <a> <b> [rinhas]`: só operadores; mostra a taxa de vitórias.

### Ainda não implementado no motor
- Passivas.
- Efeitos especiais dos golpes, além do estado aplicado.
- Suportes, exceto a Concentração.
- Golpes sequenciais.
- Precisão própria de cada golpe: a base não tem esse dado, então o motor usa 100%.
- Canto da Guarda e Leitura Perfeita.
- Itens.
- Sono.

O que ocorre de não implementado fica registrado no Histórico da Rinha.

### Achados para conferir com o criador
- **Ave Fênix:** a base vigente tem custo de Energia 100, mas a "GalolpeTeca Hereditária Atualizada", no acervo, diz 50. Precisa de verificação de fonte e data antes de mexer.
- **Velocidade das Rinhas:** com o dano V5.6 e o HP provisório, as Rinhas simuladas acabam em poucas rodadas (Cocórak × Taturico: 3,2 rodadas em média). Isso confirma o alerta da própria especificação V5.6 de que golpes fortes derrubam com um ou dois acertos. Avaliar quando a Vitalidade V5.6.1 e as passivas existirem.

### Próximos passos (fase 3 em diante)
1. Galeto individual na entidade: espécie, nível, sexo, IVs e golpes persistidos; atributos vindos do núcleo.
2. Rinha jogável contra um Galeto selvagem, com menu clicável no chat (Galetos / Combate / Itens / Fugir) e depois uma tela própria.
3. Item Pena e captura, equipe do treinador e Galetário dentro do jogo.
4. Passivas e efeitos dos golpes por família, a partir do texto oficial estruturado.

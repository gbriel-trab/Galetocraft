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

## 18/11/2026 — Fases 3 e 4: Galeto individual e Rinha jogável

### Fase 3 — Galeto individual (`GaloEntity`)
- **Cada criatura é um indivíduo** com nível, sexo e os 6 IVs, salvos com a entidade (`galeto_nivel`, `galeto_sexo`, `galeto_ivs`).
  - Sexo: sorteado pela distribuição da espécie no Galetário (Galeria). O Quetzacocó não tem sexo.
  - IVs: inteiros de 1 a 40, uniformes, como os IVs não herdados da reprodução.
  - Nível: 50 para todos, porque a curva 1–49 e as regras de aparecimento estão pendentes.
  - Entidades antigas, salvas antes desta versão, ganham os dados na primeira consulta.
- **O Pirococó** passou a herdar de `GaloEntity` e ganhou os mesmos dados.
- **Clicar com a mão vazia** mostra a ficha do indivíduo no chat. Exemplo: `#007 Taturico ♀ Nv50 · HP 85 · Comum · IVs [...]`.
- **Os IVs ainda não alteram os atributos:** a fórmula de IV, EV e peso com a norma do nível 50 está pendente (decisão 3 da análise).
- **Ainda falta:** golpes próprios do indivíduo, dono e sincronização com o cliente. Por enquanto, a Rinha usa os 5 golpes de origem.

### Fase 4 — Rinha jogável contra Galeto selvagem
- **Como jogar:**
  1. `/galetocraft equipe <a> [b] [c]` define a equipe de teste, de 1 a 3 espécies no nível 50. O padrão é Pirococó, Cocórrego e Esporocó. Sem argumentos, mostra a equipe.
  2. Perto de um Galeto (até 10 blocos), `/galetocraft desafiar` começa a Rinha contra o mais próximo.
  3. O menu aparece no chat, com botões clicáveis:

     | Linha | Botões |
     |---|---|
     | Estado | HP e Energia dos dois Galetos ativos, e o estado negativo |
     | Combate | Os 5 golpes, com o custo de Energia. Os golpes sem Energia ficam cinza. Passar o mouse mostra elemento, categoria, poder e efeito |
     | Galetos | Troca voluntária para outro Galeto da equipe |
     | Mira | Região mirada (precisão da região) |
     | Guarda | Neutra ou uma região |
     | Pena de Ritmo | Só aparece depois de uma Concentração. Usa o Canto Ofensivo num golpe de dano, o de Suporte nos outros golpes e o de Revezamento na troca |
     | Itens | Desativado: os itens da Rinha ainda são candidatos |
     | Fugir | Encerra a Rinha |

  4. Cada clique é uma ação. A IA básica escolhe a ação do selvagem, o motor do núcleo resolve a rodada e o Histórico da Rinha aparece no chat.
- **Regras da sessão:**
  - O Galeto selvagem fica parado, sem IA, durante a Rinha e volta ao normal no fim.
  - Um Galeto em Rinha não pode ser desafiado por outro jogador.
  - A Rinha termina com vitória, derrota, fuga, saída do jogador do servidor, desligamento do servidor ou distância maior que 32 blocos.
  - Se o mundo for salvo no meio de uma Rinha, o Galeto volta com a IA ligada.
  - A equipe de teste fica só na memória do servidor, até existirem captura e equipe do treinador.
- **Ajustes no núcleo:**
  - As regiões da Mira têm nome para o jogador: Cabeça/crina, Asas, Pernas/garras e Tronco.
  - O Canto de Suporte aparece no Histórico da Rinha, com o custo antes e depois.
- **Teste automático no cliente** (`RinhaTesteCliente`):
  - Joga uma Rinha inteira como um jogador: define a equipe, desafia um Taturico, muda Mira e Guarda, concentra, usa a Pena e clica nos golpes do menu até o fim.
  - Confere que o Taturico fica parado na Rinha e volta a ter IA depois.
  - Resultado em 18/11: vitória em 14 ações, com Canto de Suporte (custo 45 → 30) e Ruptura na Cabeça/crina.
  - Para rodar só este teste nesta nuvem, sem placa de vídeo: `GALETO_TESTES=rinha LIBGL_ALWAYS_SOFTWARE=1 xvfb-run -a bash gradlew runClientGameTest`. Os prints ficam em `build/run/clientGameTest/screenshots/`.
  - O filtro `GALETO_TESTES` (`pirococo`, `galeria`, `rinha`) vale para os três testes de cliente. Em renderização por software, a galeria em 1920×1080 passa do tempo limite de carregamento do mundo.

## 18/11/2026 — Fase 5: captura com a Pena e equipe do treinador

### Fonte das regras
- **Regra `captura` da base**, conferida com as 18 homologações da Pena no acervo, de 11 e 12/11 (pacote 11), e com a homologação final da Beta 1.2.59.
- **Revisão 7 da base** (`docs/patches/rev7_captura_coerencia.json`): a regra trazia dois campos da proposta já superada.
  - A fórmula `F = 1 + 0,15·(nível−1)` foi trocada pela tabela do reforço v1258: 1,00 / 1,30 / 1,65 / 2,05 / 2,50.
  - O indicador "retentativa sem espera" do mundo foi para 0, como a própria v1259 registra.

### Pena de Captura (item `galetocraft:pena_de_captura`)
- **O instrumento:** um por treinador, não consumível, sem arremesso.
- **Nível e XP ficam com o treinador,** não com o item. A Pena evolui pela XP acumulada: 1.000 / 4.000 / 11.000 / 26.000.
- **XP por captura:** `XP_base(raridade) + 2·nível`. Uma captura pode render várias evoluções e o excedente é reaproveitado. No nível 5 não entra XP nova.
- **Provisório, até o criador decidir:**
  - O jogador recebe a Pena com `/galetocraft pena` (ou no criativo, aba de ferramentas).
  - O desenho é o da pena vanilla, como marcador.

### Captura no mundo
- **Como funciona:**
  - Mira no Cocorídeo e usa o botão direito com a Pena na mão.
  - Alcance de 12 blocos, lido da base. Um bloco sólido no caminho impede a tentativa.
  - O resultado sai na hora: `P = 100·R·F/(R·F + D)`.
- **No sucesso:** aparece o Feixe do Rubi simplificado (uma linha de partículas cor de rubi) e o Cocorídeo sai do mundo.
- **Na falha:** o Cocorídeo segue normalmente e resiste por 20 s (60 s se Lendário). A espera vale para todos os jogadores.

### Captura na Rinha
- **Como se usa:** o botão Itens do menu passa a valer em Rinha contra selvagem quando o jogador tem a Pena. Itens → Pena de Captura faz a tentativa.
- **No motor do núcleo (`Decisao.Capturar`):**
  - A tentativa consome a ação do treinador e entra na ordem normal de Velocidade.
  - A força é `R·F·H·S`, com HP, Sono e Paralisia.
  - Na falha, a Rinha continua e o selvagem age se ainda tiver ação pendente.
  - No sucesso, a Rinha termina na hora, sem fim de rodada.
  - Sem espera adicional.
- **Captura não é vitória:** o motor registra `capturado()`, e `vencedor()` fica vazio.

### Treinador
- **Onde fica:** salvo com o jogador (Fabric Data Attachment), inclusive depois da morte.
- **Equipe principal:** até 5, número lido da regra `treinador`.
- **Reservas:** sem limite.
- **Destino do capturado:** a equipe, se houver vaga; senão, as reservas.
- **Na Rinha:** entram os 3 primeiros da equipe. Sem nenhum Galeto, entra a equipe de teste (`/galetocraft equipe teste <a> [b] [c]`).
- **`/galetocraft equipe`:** lista equipe, reservas e Pena, com botões provisórios (a regra não define o procedimento):
  - **guardar:** da equipe para as reservas.
  - **chamar:** das reservas para a equipe.
  - **primeiro:** põe o Galeto no topo da ordem.

### Decisões provisórias de implementação (sem regra homologada)
- **Alvo inelegível** (Lendário sem Pena 5, Lendário Original): a tentativa não começa e não consome a ação.
- **Galeto em Rinha:** não pode ser alvo da captura no mundo.
- **Posição da captura na rodada:** a regra só diz que o adversário age "na ordem regular". O motor põe a captura no lugar do Galeto do treinador, pela Velocidade.

### Testes
- **Núcleo:** 25 testes. Os novos cobrem captura na Rinha (fórmula com HP, sucesso encerra, falha continua, ordem por Velocidade, elegibilidade) e evolução e XP da Pena.
- **Cliente (`CapturaTesteCliente`):** joga com o botão direito de verdade.
  - Resultado em 18/11, no mundo: a 1ª tentativa falhou, a espera de 20 s foi conferida e a 2ª capturou o Taturico (+115 XP).
  - Na Rinha, com o Taturico: o Vagaló, mais rápido, agiu antes; a 1ª captura falhou e a 2ª capturou (+115 XP, total 230).
  - O botão "primeiro" reordenou a equipe.
- **`RinhaTesteCliente`** continua passando, agora com a equipe de teste.
- **Servidor dedicado** sobe com a base rev. 7.

### Próximos passos (fase 6 em diante)
1. Golpes próprios do Galeto individual (repertório aprendido) e sincronização com o cliente.
2. XP dos Cocorídeos por Rinha vencida (regra `experiencia`) e aprendizado de golpes (depende da tabela de níveis, ainda fora da camada vigente).
3. Passivas e efeitos dos golpes por família, a partir do texto oficial estruturado.
4. Tela própria da Rinha e do Galetário, no lugar do chat.
5. Rinha entre jogadores; soltar Galetos da equipe no mundo.

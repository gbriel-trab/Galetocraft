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

## 18/11/2026 — Fase 7 (parte 1): XP dos Cocorídeos por Rinha vencida

- **Regra `experiencia` (v1260)**, completa na base, implementada sem mudanças:
  - Só a Rinha vencida dá XP. Derrota, fuga e captura não dão.
  - Cada oponente derrotado conta uma vez: `floor((25 + 15·L) × M_raridade × C_desafio × M_modo)`, com `C_desafio = max(0,25; min(1,50; 1 + 0,03·(L − P)))`. P é o maior nível entre os Galetos do treinador que entraram em campo.
  - A soma é repartida entre os Galetos distintos que entraram em campo (mesmo sem golpear). O resto vai de 1 em 1, na ordem da primeira entrada. A reserva que não entrou não recebe.
  - O Cocorídeo capturado começa com `T(nível)` de XP, sem extra.
  - O nível sobe pela curva `T(N) = (N−1)³ + 10(N−1)²`. No nível 100 não entra XP nova.
- **No núcleo:**
  - A `Equipe` registra a ordem da primeira entrada em campo.
  - `Premiacao.liquidar` calcula a XP de cada participante.
  - `Experiencia.repartir` faz a divisão com o resto.
- **No mod:**
  - Cada Galeto guardado tem a sua XP.
  - No fim de uma Rinha vencida contra selvagem, os Galetos do treinador que entraram em campo ganham a XP e sobem de nível, se for o caso, com mensagem no chat.
  - A equipe de teste não ganha XP.
  - `/galetocraft equipe` mostra a XP e quanto falta para o próximo nível.
- **Testes:**
  - Núcleo: 27 testes. Os novos cobrem a divisão do resto e a XP só para quem entrou em campo.
  - Cliente: o `CapturaTesteCliente` vence uma Rinha com Vagaló e Taturico contra um Taturico selvagem e confere os 775 XP (388 + 387).
- **Observação de balanceamento:** escolhendo golpes ao acaso, a dupla Vagaló + Taturico perdeu 5 de 6 Rinhas contra um Taturico selvagem guiado pela IA. Ainda não há passivas nem efeitos de golpes, e o HP é o provisório.
- **Ainda falta:** golpes aprendidos por nível. A tabela de níveis não está na camada vigente da base, e a curva 1–49 continua pendente.

## 18/11/2026 — Pendências resolvidas com os dados mais recentes (base rev. 8)

Instrução do criador: "Resolve esses problemas todos com base nos dados mais recentes que temos disponíveis".

### Pesquisa
- **Corpus:** os 909 documentos de texto do acervo (pacotes 01 a 14) e as tabelas do `Galetocraft.sqlite` rev. 2.
- **O que cada achado registra:** data, status (homologado, candidato ou proposta), fonte e trecho literal.
- **Pacote:** `docs/patches/rev8_resolucoes.json`, gerado por `ferramentas/base/gerar_rev8_resolucoes.py`.

### Resolvido com dado

| Pendência | Dado mais recente adotado | Fonte |
|---|---|---|
| Energia da Ave Fênix | **E100**, sem mudança: o E50 é anterior à Energia V4 | Energia V4 homologada em 11/11; reafirmada de 12 a 15/11 |
| Curva dos níveis 1–49 | `A50 × (49 + 3(L−1))/196` | Norma R5.4 (14/11), reafirmada na R5.5 (15/11) |
| HP efetivo | HP nominal: 10 no nível 1, `ceil(1,5·HP50)` no 50 e `ceil(1,5·HP50·(L+50)/100)` até o 100 | R5.4; origem do 1,5× e do 10 na Combate v1.0 (08/11) |
| Vitalidade V5.6.1 | `Fvit = clamp((HP_ref/HPmax)^0,2; 0,8; 1,0)` no dano, com `HP_ref = floor(1,05 × HP_n(L; 80))` | Fórmula homologada em 13/11; HP_ref da R5.4 (tabela de 100 níveis conferida, sem divergência) |
| IV, EV e peso | nominal → `floor(A × (1 + (0,25·IV + 0,5·√EV)/100))` → peso V1.2 (half-up, mínimo 1) | IV/EV oficiais (08/11); Peso V1.2 (09/11); cadeia da R5.4 |
| Golpes por nível | regra `aprendizado`: 15 por nível e 15 por treinamento | Grades de #001–#012 (Beta 1.2.61, 12/11), #019, #020, #021 (12/11) e #022 (13/11) |
| Slots de golpes | 5 equipados, Concentração fixa, 4 slots livres depois dos 5 de origem, desequipados conservados, nada equipado sozinho, retrodesbloqueio na captura | Quatro Slots v2 (10/11); Beta 1.2.61 |
| Desempate de trocas com Velocidade igual | sorteio 50/50 | Extensão da regra oficial de desempate (09/11) |
| Espécie repetida no trio | permitida | Formato oficial dos Mestres (10/11): 3 Galetos de 2 espécies |
| Precisão própria dos golpes | 100% para todos | Nenhuma fonte tem precisão por golpe; a ideia "Ataques de Precisão" não foi aprovada |
| Posição da captura na rodada | na vez do treinador, pela Velocidade do Galeto ativo | Homologação v1252 ("depende de sua posição na ordem regular") |
| Alvo inelegível | a tentativa não começa e não gasta a ação | Proposta do auditor na Auditoria de Capturas 1.2.58 (12/11) |
| Alvo da captura | só Cocorídeo selvagem fora de Rinha | Homologações da Pena; Reprodução Etapa 01 (16/11) |

- **Conciliação das grades #001–#012:** as grades de 12/11 usam o repertório anterior à Reforma Integral.
  - Ficaram vazios 9 marcos, porque o golpe saiu do repertório vigente.
  - Os golpes vigentes sem marco passaram a ser aprendidos por treinamento.
  - O detalhe por espécie está em `aprendizado.conciliacao_001_012`.

### Sem nenhum dado no acervo (registrado em `current_issues`, U07–U12)
- **U07 — Spawn:** só existem habitats narrativos de #010 e #016–#018 e a regra "Divinos não aparecem naturalmente".
- **U08 — Pena de Captura:** obtenção, recuperação e arte. `nome_exato` e `design_exato` estão NULL na base.
- **U09 — Escalação da Rinha e gerenciamento da equipe.**
- **U10 — Galeto do treinador no mundo:** soltar e recolher.
- **U11 — Aprendizado de #013–#018.** O #023 continua em U03.
- **U12 — EV:** faixas de dificuldade no nível 50 e ganhos de EV em combate e treino.

No mod, esses pontos continuam com as soluções provisórias já descritas. Nada foi inventado.

**Propostas para o criador decidir** (18/11): `docs/propostas/PROPOSTAS_PENDENCIAS_2026-11-18.md`.
- Cobre U07–U12, U03, o Lendário Original, o balanceamento e a confirmação das cinco decisões por extensão.
- As tabelas de aprendizado propostas para #013–#018 e #023 foram geradas por `ferramentas/propostas/propor_aprendizado.py` e estão em `docs/propostas/proposta_aprendizado_013_018_023.json`.

### Implementação
- **Núcleo:**
  - `Progressao` (curva 1–49, HP nominal, IV/EV, peso, HP_ref, Vitalidade).
  - `Individuo` (IVs, EVs e peso do Galeto).
  - `Aprendizado` (tabelas, marcos, slots).
  - `DanoV56` com a Vitalidade.
- **Mod:**
  - Os Galetos do treinador lutam com seus IVs, EVs, peso e golpes equipados.
  - Os selvagens lutam com seus IVs e só com os golpes que já aprenderam no nível deles.
  - Ao subir de nível, o chat avisa os golpes aprendidos.
  - `/galetocraft golpes <n>` troca os slots fora da Rinha.
- **Testes:**
  - Núcleo: 30 testes, incluindo os 100 níveis de HP_ref conferidos contra a tabela da R5.4.
  - `CapturaTesteCliente`: vence um Taturico de nível 20 (81 XP, fator de desafio mínimo) e troca um golpe pelo botão do chat, que aparece no menu da Rinha seguinte.
- **Duração das Rinhas** (simulação de 200 Rinhas por confronto):
  - 1×1 com 10 pares: de 2,86 para 3,05 rodadas em média (+7%).
  - 3×3: de 11,95 para 12,61 rodadas (+5,5%).
  - As Rinhas continuam curtas. Faltam as passivas e os efeitos dos golpes.

## 18/11/2026 — Decisões do criador sobre as propostas (base rev. 9)

O criador aprovou as propostas de `docs/propostas/PROPOSTAS_PENDENCIAS_2026-11-18.md`:
- A, C, D, E, F, G e I como estavam.
- **B** com o nível dos selvagens sorteado de 1 a 70, sem depender do local.
- **H** como extremamente raro, com aviso global no chat. Nos esclarecimentos: selva ou montanha durante tempestade, depois dos 6 elementos, nível 70, Pena 5 e fator 0,14.

O pacote é `docs/patches/rev9_decisoes_criador.json`, e as pendências U03 e U07–U12 ficaram resolvidas (U08 aguarda só a arte da Pena).

### Implementado no mod

| Decisão | O que entrou |
|---|---|
| B: aparecimento | Regra `mundo_aparecimento` aplicada: aparecimento natural por bioma (tags de convenção e biomas vanilla), horário e tempestade; pesos 6/2/1; limite de 6 selvagens a até 64 blocos; selvagens naturais somem quando o jogador se afasta |
| B: nível | Todo Galeto novo sorteia de 1 a 70 |
| B: encontros raros | 1% por jogador na manhã ou no anoitecer, ou a cada minuto de tempestade, conforme a espécie; no máximo 1 ativo |
| H: Quetzacocó | 0,2% por minuto de tempestade por jogador elegível (selva ou montanha alta e Galetos dos 6 elementos); nível 70; mensagem global; foge no fim da tempestade; único por mundo (marca no mundo ao ser capturado). **Fica pronto para quando houver modelo**: a espécie ainda não tem entidade |
| C: kit de início | Pena nível 1 ao entrar e escolha única do inicial nível 5 pelos botões do chat |
| C: posse da Pena | Dono e versão gravados no item; só o dono usa; uma Pena nova invalida as anteriores; a Pena não fica no chão; volta ao entrar, renascer ou acordar; a dica mostra nível e treinador |
| D: escalação | Com mais de 3 Galetos, a escolha de 3 e de quem começa é feita no chat antes da Rinha; o selvagem fica reservado enquanto o treinador escolhe |
| E: companheiro | 1 Galeto segue o treinador; invulnerável; não é desafiado nem capturado; volta à equipe com a Pena, na Rinha ou quando o jogador sai |
| E: libertar | Confirmação dupla; o Galeto vira selvagem no lugar |
| F: aprendizado | Tabelas de #013–#018 e #023 na base; as 23 espécies aprendem por nível |
| G: EV | Faixas pelo total do nível 50 (`Ev` no núcleo); +0,1 EV por oponente derrotado, no atributo mais alto dele, para quem entrou em campo |

### Testes
- **Núcleo:** 31 testes. Os novos cobrem as faixas de EV e a cobertura das 23 tabelas de aprendizado.
- **`JornadaTesteCliente` (novo):**
  - kit e escolha única do inicial;
  - a Pena some do chão e volta na versão 2;
  - 8 selvagens com níveis entre 1 e 70 (ex.: 5 a 58);
  - Vagaló na lista de aparecimento das planícies;
  - companheiro invulnerável, não desafiável e recolhido;
  - escalação com Morcegalo começando;
  - libertar com confirmação dupla.
- **`RinhaTesteCliente` e `CapturaTesteCliente`:** continuam passando. Os selvagens do teste têm nível fixado por NBT, e a EV de combate aparece no chat.
- **Servidor dedicado:** sobe com a base rev. 9.

### Ainda não implementado (decidido, mas depende de outra parte)
- **Feixe do Rubi:** o encolhimento do Galeto e o som (falta animação no cliente).
- **Arte da Pena:** cores por nível (falta gerar a arte no ChatGPT).
- **Terreiro:** recebe Galetos direto da equipe (falta a reprodução).
- **Peso do companheiro:** a deriva de peso pelo movimento depende da alimentação, que ainda não existe.
- **Galetário:** aba Equipe e Reservas (falta a tela do Galetário).
- **Modelos:** aparecimento das 11 espécies sem entidade, incluindo o Quetzacocó.

## 18/11/2026 — Tempestade de areia no mundo (base rev. 10)

Pedido do criador, com as decisões: acontece **quando chove, no deserto**, e a **Rinha começa com o clima Tempestade de Areia**. O pacote é `docs/patches/rev10_tempestade_de_areia.json`, com a regra nova `tempestade_de_areia`.

- **Quando:** chove ou troveja no mundo, o lugar é deserto ou badlands e o céu está visível. Sob teto ou no subsolo não há tempestade.
- **Visual (cliente):**
  - **Poeira:** partícula própria `galetocraft:areia`, que usa as texturas vanilla de poeira tingidas de areia. Os grãos são soprados na direção do vento, que muda a cada dia de jogo, e a quantidade segue a opção de partículas.
  - **Névoa:** névoa amarelada pelo mixin `NevoaAtmosfericaMixin`, que encurta a névoa atmosférica e puxa a cor para a da areia.
  - **Vento:** som vanilla de vento do voo de élitro, mais grave.
  - Tudo com transição suave ao entrar e sair.
- **Jogo:**
  - Uma Rinha que começa dentro da tempestade já começa com o clima Tempestade de Areia (4 rodadas). O Histórico da Rinha mostra "Clima: Tempestade de Areia (4 rodadas)".
  - O encontro raro do Cocórak usa a tempestade real (2×).
  - A tempestade não causa dano nem lentidão.
- **Teste `TempestadeTesteCliente`:**
  - sem chuva, nada;
  - com chuva no deserto, intensidade 1,0 e detecção no servidor;
  - a Rinha começa com o clima;
  - fora do deserto, com a mesma chuva, intensidade 0;
  - prints antes e durante.
- **Os quatro testes de cliente** (rinha, captura, jornada e tempestade) passam juntos.

### Próximos passos (fase 6 em diante)
1. Mestres Elementais (golpes por treinamento) e sincronização com o cliente.
2. Alimentação (EV e peso) quando as faixas de EV estiverem recalibradas (U12).
3. Passivas e efeitos dos golpes por família, a partir do texto oficial estruturado.
4. Tela própria da Rinha e do Galetário, no lugar do chat.
5. Rinha entre jogadores; soltar Galetos da equipe no mundo.

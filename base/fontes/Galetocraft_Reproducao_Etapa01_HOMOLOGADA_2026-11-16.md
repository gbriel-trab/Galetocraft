# GALETOCRAFT — REPRODUÇÃO V2.0 — ETAPA 01
## Especificação final de design: Ninhos Especializados e Terreiro de Encontro

**Data de consolidação:** 16/11/2026  
**Status:** **OFICIAL — DESIGN HOMOLOGADO EXPRESSAMENTE PELO CRIADOR EM 16/11/2026**. Implementação e testes em Minecraft pendentes.  
**Escopo:** funcionamento da produção de ovos e seus ninhos; incubação ambiental detalhada permanece reservada à etapa 02 (pendente).  
**Prioridade das fontes:** regras oficiais do Galetocraft prevalecem sobre qualquer detalhe candidato deste documento.

### 1. Resumo decisório

- **Terreiro de Encontro:** bloco funcional 1×1, raio de seleção candidato de 8 blocos; seleciona dois galetos fisicamente presentes no mundo. Um casal válido tem macho e fêmea, duas entidades diferentes, ao menos uma ala da Galeria compartilhada, disponibilidade e autorização do responsável. Os tipos elementais não definem compatibilidade.
- **Tempo:** 10 minutos de **tempo ativo do jogo/servidor POR LEVA**; não 10 minutos por ovo. Sem cooldown adicional por galeto ou casal. A próxima leva inicia assim que a bandeja de três espaços for esvaziada e um casal válido for confirmado.
- **Ovos:** cada leva produz **1–3 ovos**; bandeja com 3 espaços. Bandeja não incuba. Os ovos podem ser guardados em inventários e baús. Sem resultado de nascimento criado duas vezes.
- **Ninhos:** exatamente oito variantes POR ALA, sem personalização por espécie; três ovos incubáveis simultaneamente por ninho. Um ninho de qualquer ala aceita qualquer ovo, mas a afinidade requer ala correspondente compartilhada por AMBOS os progenitores.
- **Benefícios de afinidade:** tempo-base de incubação ×0,70 (−30%), sem empilhar; 50% de chance única de Refinamento Garantido em um dos 3 IVs não herdados. Sem afinidade, nenhum bônus; antes da PRIMEIRA incubação sem afinidade, mostrar aviso e exigir confirmação.
- **Refinamento Garantido:** no primeiro começo de incubação elegível, uma única ativação probabilística de 50%; seleciona uniformemente um dos 3 IVs sorteados não herdados; realiza outro sorteio inteiro uniforme 1–40; mantém o maior; se não aumentou e o IV original é inferior a 40, aplica +1. IVs herdados intactos, teto 40. O resultado é persistente e irrepetível.
- **Eclosão:** exclusivamente MANUAL. Após completar incubação o ovo fica `PRONTO`; permanece ocupando seu espaço até interação. Consumir o ovo e criar 1–2 galetos deve ser atômico; sem lugar seguro para todos os filhotes, permanecer pronto sem consumo parcial.
- **Quebra do ninho:** recuperar o bloco vazio; devolver ovos como itens individuais para os espaços livres do inventário e soltar excedentes SEPARADAMENTE no chão com todos os dados preservados. Ovos no chão têm proteção proposta de 15 minutos de tempo carregado contra desaparecimento natural, mas permanecem expostos a danos ambientais. Inventário/baú/chão pausam incubação.
- **Status de implementação:** DESIGN OFICIAL; não significa que os novos blocos, migrações SQLite ou testes no mod já foram implementados.

### 2. Oito variantes e receitas OFICIAIS homologadas

Todos usam exatamente **1 Estrutura de Ninho + 2× material A + 2× material B**. Produção: 1 ninho, capacidade 3, mesma taxa de bônus. Insumos são todos recursos do Minecraft básico; as receitas evitam minérios ou itens raros obrigatórios. Pequenas diferenças reais de obtenção são aceitáveis e serão avaliadas em testes de progressão. Nenhum item é obtido exclusivamente de uma espécie de galeto.

**Estrutura de Ninho (1):** 4 tábuas de qualquer madeira + 4 gravetos, organizados em bancada 3×3 (tábuas nos quatro cantos; gravetos nos quatro lados; centro vazio).  
**Finalização:** Estrutura no centro; material A nos cantos superiores; material B nos cantos inferiores; outras casas vazias.

| Ala | Nome | Material A (2 unidades) | Material B (2 unidades) |
|---|---|---|---|
| Galiformes | Ninho de Palha | Trigo | Sementes de trigo |
| Alígeros | Ninho Suspenso | Penas | Linha |
| Colossais | Ninho Reforçado | Pedregulho | Andesito |
| Couraçados | Ninho de Pedra | Pedra lisa | Cascalho |
| Fitomorfos | Ninho de Raízes | Blocos de folhas (qualquer variedade) | Sementes de trigo |
| Hidromorfos | Ninho de Juncos | Alga | Cana-de-açúcar |
| Zoomorfos | Ninho Silvestre | Lã (qualquer cor) | Couro |
| Arcanos | Ninho Místico | Corante roxo | Corante azul |

Materiais são o único diferencial; não há tier, ninho evoluído, ninho por espécie ou probabilidade genética diferenciada por ala. Blocos ocupam 1×1 no chão; estilo visual e altura próprios não afetam colisões de galetos. Ninho Suspenso pode ter suportes puramente visuais.

### 3. Fluxo do Terreiro (máquina de estados)

`LIVRE` → (casal válido, bandeja vazia, confirmação do jogador) → `REPRODUZINDO` → (10 minutos transcorridos) → `LEVA_PRONTA` → (retirada de todos os ovos) → `LIVRE`.

- Um único casal ocupa cada Terreiro por vez; indivíduos ficam reservados e não podem ser usados simultaneamente noutros Terreiros ou Rinhas. O Terreiro valida autorização e elegibilidade no início da operação.
- As duas entidades devem estar presentes no raio de busca no ato da seleção. Caminhadas/animações são cosméticas; falha ocasional de pathfinding não provoca uma espera extra após confirmar o casal válido. Não há teleporte forçado.
- Ao confirmar, grava-se identificador de ciclo, progenitores, mundo, instante inicial e condição de saída; a bandeja deve estar vazia. Durante o processo, a interface exibe o tempo restante; não há produção intermediária por ovo.
- Após o término, o servidor resolve e grava uma única leva de 1–3 ovos, com IDs imutáveis, e libera a reserva dos progenitores. Não recalcular a leva por cliques, reaberturas, carregamentos ou quedas da conexão.
- O tempo mede progresso de jogo/servidor ativo; com mundo singleplayer pausado, a contagem fica pausada. Quando o mundo continua ativo mas o chunk descarrega, guardar a hora lógica e apurar o progresso no próximo carregamento, sem depender da renderização da interface. Nenhuma segunda espera é acrescentada.
- Se o Terreiro for destruído durante um ciclo ainda não concluído, cancela-se aquele ciclo e libera-se o casal, sem cooldown, com mensagem de confirmação/aviso quando o próprio jogador iniciar a quebra. Se já havia ovos prontos, protegê-los com as mesmas regras dos ovos devolvidos de ninhos.
- O Terreiro não concede bônus genéticos. A bandeja de 3 espaços é saída e armazenamento, sem incubar.

### 4. Formação e sorteio de ovos

**Regra oficial:** 1–3 ovos por reprodução. **Distribuição OFICIAL homologada**: 1 ovo = 25%, 2 ovos = 50%, 3 ovos = 25%. Média = 2 ovos/leva; expectativa de 12 ovos/h por Terreiro continuamente ocupado (se a bandeja for esvaziada imediatamente).

Os resultados genéticos e de nascimento ficam associados a cada ovo uma única vez, com a exceção futura e explicitamente registrada do refinamento em ninho compatível. Cada ovo normalmente contém um filhote; o evento gemelar mantém as probabilidades já aprovadas por ovo:
- Ovo elegível a gêmeo especial: 99,5% normal, 0,4% gêmeos da mesma espécie, 0,1% par especial (o 0,1% **integra** o total 0,5% de gêmeos).
- Ovo não elegível a gêmeo especial: 99,5% normal, 0,5% gêmeos da mesma espécie.
- Gêmeos têm os seis IVs IDÊNTICOS; reforços aplicados ao ovo serão idênticos para os dois indivíduos.
- Pares especiais aprovados incluem Pirococó/Renacocó e Cocórion/Cocórvolt; o protocolo exato de gatilhos e precedência desses pares especiais segue dependência **externa à Etapa 01**, não deve ser inventado nesta especificação.

**Regras genéticas oficiais:** três atributos sorteados uniformemente, sem repetição, herdam IVs com 70% origem materna/30% paterna de forma independente; os demais três IVs são sorteados uniformemente como inteiros 1–40. Nos nascimentos normais de progenitores de espécies diferentes, a espécie será da mãe (50%) ou do pai (50%), sem híbridos. Sexo por espécie com exceções já aprovadas; Herança de Bico conforme catálogo elegível, pai 100%, somente mãe 25%, Ave Fênix 100% se ao menos um dos pais possui. O refinamento proposto é uma **exceção nova e declarada à distribuição final uniforme** de um IV não herdado, jamais modifica os três herdados.

### 5. Estados de cada ovo no ninho

- `ARMAZENADO`: fora do ninho, sem progresso de incubação.
- `INCUBANDO`: em um dos três espaços; aplica progresso normal ou multiplicador 10/7 de velocidade conforme a afinidade atual.
- `PRONTO`: atingiu 100%; espera eclosão manual.
- `ECLODIDO`: consumo atômico do ovo, criação dos filhotes e registro da linhagem.
- A elegibilidade genética é avaliada só no primeiro evento de incubação. Com afinidade, realizar uma única rolagem 50% e persistir resultado; sem afinidade, mostrar aviso e exigir confirmação; ao confirmar, registrar irrevogavelmente `SEM_AFINIDADE_PRIMEIRA_INCUBACAO` e não oferecer refinamento futuro.
- Transferir entre ninhos: pausar e preservar progresso absoluto, não reabrir genética. Velocidade futura é determinada pela afinidade do ninho de destino.
- Ovos de diferentes casais podem ocupar os três espaços do mesmo ninho; afinidade e progresso são por ovo, não por ninho inteiro.
- Bloquear inserção automatizada por funis nesta primeira especificação, para que não contornem o aviso/consentimento da primeira incubação sem afinidade. Pode ser reavaliado depois com equivalência de validação.

### 6. Matemática verificada do Refinamento Garantido

- Ativação por ovo elegível: 50%.
- Melhoria efetiva: 48,75% por ovo elegível (só não melhora se a rolagem não ativar ou se o IV selecionado já for 40).
- Ganho esperado CONDICIONAL à ativação: **7,15 pontos** no IV selecionado.
- Ganho médio por ovo elegível: **+3,575 pontos na soma dos 6 IVs**.
- Probabilidade de ao menos um 40 entre os três IVs não herdados, antes do refinamento: 7,3140625%; após refinamento: aproximadamente 8,4726367%.
- Máximo um IV refinado, não acumulável, sem influir nos IVs herdados, na espécie, sexo, quantidade de ovos ou probabilidades de gêmeos.

**Observação técnica:** a redução de 30% no TEMPO exige multiplicar a VELOCIDADE de progresso por 10/7 (≈1,428571), e não somar 30% de progresso. O tempo-base e o conforto ambiental serão especificados apenas na Etapa 02.

### 7. Quebra, transporte, inventários e segurança

- Ninhos ocupados podem ser quebrados. O bloco cai como ninho vazio; cada ovo cai como item único não empilhável, conservando NBT/componentes com ID, progenitores, IVs, origem, estado do refinamento, resultado gemelar, progresso, prontidão e histórico necessário.
- Ao quebrar, tentar inserir no inventário do jogador os ovos que couberem; excedentes caem individualmente no chão, com proteção contra desaparecimento natural por 15 minutos de tempo carregado. Deixar claro que lava, explosões e outros riscos ambientais podem destruir itens, conforme regras aplicáveis do jogo.
- Ovos fora de ninhos não incubam; ovos `PRONTO` permanecem prontos mesmo fora do ninho, mas exigem inserção para eclosão manual.
- Nunca permitir que um mesmo identificador de ovo esteja válido simultaneamente no ninho e no mundo/inventário. O servidor deve controlar inserção, retirada, quebra, salvamento, carga e eclosão como transições idempotentes, protegidas contra duplo clique e ações simultâneas de dois jogadores.
- Ovos de um mesmo casal ou de casais diferentes não empilham se têm genética/IDs distintos. Ninhos ocupados não devem ser empurrados por pistões. Estados de eclosão só podem gerar filhotes uma vez.
- Nenhuma operação física ou genética sobre ovos de terceiros sem permissão do responsável.

### 8. Casos de aceitação para implementação (PLANEJADOS, NÃO EXECUTADOS NO MOD)

1. Macho e fêmea de mesma ala: Terreiro aceita; mesmo sexo: rejeita; alas disjuntas: rejeita.
2. Exceções oficiais de sexo respeitadas para Esporocó, Sirenocó, Cocórion e Cocórvolt.
3. Seleção inicial exige duas entidades distintas, dentro de 8 blocos e sem reservas conflitantes.
4. 10 minutos por LEVA, produção final de 1–3 ovos, sem cooldown de 30 min nem espera individual por ovo.
5. Bandeja precisa estar completamente vazia antes de iniciar próxima leva; nenhum clique duplica ovos.
6. Ninho da ala compartilhada reduz tempo a 70% do base; ala só de um progenitor não concede bônus.
7. Oito ninhos aceitam três ovos, inclusive ovos de casais diferentes; gêmeos ocupam um espaço.
8. Refinamento tem 50% de ativação, seleciona um IV não herdado, aumenta ao menos 1 se <40; nunca altera os 3 herdados.
9. Ovo selecionado com IV40 continua em 40; gêmeos mantêm os 6 IVs idênticos.
10. Primeira incubação sem afinidade mostra aviso; confirmação encerra chance genética; cancelamento preserva chance intacta.
11. Transferir ovo entre ninhos mantém o progresso absoluto; altera somente a velocidade futura, não há nova rolagem.
12. Ovo `PRONTO` não eclode sozinho; uma interação válida cria todos os filhotes ou nenhum.
13. Quebra com inventário cheio devolve ovos individualmente ao chão, com dados completos; sem duplicação.
14. Reinício de mundo/servidor preserva IDs, progenitores, genética, timer da leva, ovos, gêmeos e incubação.
15. Operações simultâneas multiplayer preservam unicidade de todos os ovos e filhotes.
16. Testes de frequências: 1–3 ovos com distribuição HOMOLOGADA de 25%/50%/25%; gêmeos 0,5%, parcela especial absoluta de 0,1% POR OVO ELEGÍVEL.
17. Não há alteração em espécies, alas, mapas de compatibilidade, elementos, raridades, golpes ou artes oficiais dos galetos.

### 9. Limites e pendências fora da etapa 01

- **Etapa 02 — Incubação Ambiental:** duração-base, regras de conforto/biomas, comportamento da incubação em diferentes condições; respeitar −30% dos ninhos compatíveis e não criar aceleração acumulativa explorável.
- **Etapa 03 — Aparência Juvenil:** visual e escala de filhotes, preservando anatomia oficial.
- **Etapa 05 — Nascimento Cinematográfico:** apresentação visual da eclosão, sem alterar resultado ou bloquear o jogo.
- **Etapa 07 — Comportamentos Naturais:** animações de deslocamento e comportamento no Terreiro.
- **Etapa 10 — Ovos com Identidade Visual:** padrões das cascas; sem revelar gêmeos especiais antes do nascimento.
- **Reprodução geral / integridade de dados:** gatilhos e precedência exatos dos pares de gêmeos especiais; catálogo de golpes elegíveis da Herança de Bico; ala do #023 ainda fora do mapa de 22 espécies. Essas dependências não autorizam invenção ou alteração de regras existentes.

### 10. Parecer, homologação e limites de implementação

**Parecer de design:** CONCLUÍDO E HOMOLOGADO EXPRESSAMENTE PELO CRIADOR EM 16/11/2026. Não há efeito novo sobre probabilidade de gêmeos, sexo, espécie ou IVs herdados; há uma exceção claramente delimitada na distribuição final de um dos IVs aleatórios.

**Auditoria matemática:** realizado cálculo analítico das probabilidades e expectativas acima.  
**Auditoria funcional no mod:** não executada; casos de teste listados como critérios de aceite.  
**Receitas e distribuição 25/50/25:** OFICIALMENTE HOMOLOGADAS pela decisão expressa do criador em 16/11/2026.

**Progresso:** **1/12 etapas HOMOLOGADAS; 11 restantes**, seguindo à Etapa 02 — Incubação Ambiental, ainda NÃO homologada.


### 11. Ata de homologação expressa — 16/11/2026

**Declaração do criador:** “Homologo oficialmente o design completo da Etapa 01 — Ninhos Especializados e Terreiro de Encontro — conforme a especificação final apresentada, incluindo as receitas e distribuição 25%/50%/25% de ovos. Registre a aprovação e vamos para a etapa 02.”

**Efeito:** todos os itens de DESIGN descritos nesta especificação passam a ser oficiais na Etapa 01, respeitando sempre as regras-base superiores do Galetocraft. A distribuição 25%/50%/25%, as oito receitas e o Refinamento Garantido são expressamente abrangidos.

**Não inferir:** implementação já feita no Minecraft, migração efetivada a banco SQLite, testes regressivos executados, duração-base/incubação ambiental homologada, gatilhos especiais de gêmeos ou catálogo completo de herança resolvidos.

**Sequência:** Etapa 01 encerrada; Etapa 02 — Incubação Ambiental — aberta em desenvolvimento, sem homologação automática. Restam 11 de 12 etapas.

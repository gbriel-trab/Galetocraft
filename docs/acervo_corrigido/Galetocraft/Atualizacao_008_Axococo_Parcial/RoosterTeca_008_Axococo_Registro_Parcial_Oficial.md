# Galetário #008 — Axococó | registro parcialmente homologado

**Data da aprovação:** 09/11/2026. **Raridade:** Comum. **Elemento:** Água. **Inspiração:** axolote. **Função:** regenerador tático / suporte aquático.

![Arte oficial aprovada do Axococó](Axococo_008_Arte_Oficial.png)

**Arte visual oficial:** Axococo_008_Arte_Oficial.png, SHA-256 `b3bb33f40be66f6c970dfb0f5d23a58be60581509493d3147cab44b0352503e2`. Conservar sem qualquer redesenho ou alteração. A arte é a prancha voxel com quatro vistas e detalhes. **Números de atributos, peso, passiva e golpes eventualmente impressos na própria prancha foram gerados como texto ilustrativo, e NÃO constituem valores oficiais.** Os valores oficiais de combate são os registrados abaixo.

## Estado de homologação

- **Arte:** OFICIAL.
- **Passiva:** OFICIAL.
- **Golpes:** OFICIAIS, compartilhados, não exclusivos e não hereditários.
- **Peso máximo natural:** **PENDENTE** (5,8 kg mostrado na ilustração/proposta anterior não homologado).
- **Seis atributos base no nível 100:** **PENDENTES** (total/base e distribuição ainda não aprovados).

> **Errata 18/11/2026:** os atributos-base do Galetocraft usam o nível 50 como referência (Norma de Progressão Nível 50 V1). Este registro não traz os números (registro parcial, superado pela ficha oficial completa); valores vigentes de #008 Axococó no nível 50: HP 95 / Ataque Físico 35 / Defesa Física 50 / Ataque Mágico 90 / Defesa Mágica 60 / Velocidade 40 (total 370).
- **Ficha completa do Galetário:** **PENDENTE**. Não avançar ao #009 até terminar #008.

## Passiva oficial — Memória das Brânquias

Quando sofre dano de ataques inimigos, reserva **25% do dano sofrido** como recuperação de HP para o início de sua próxima ação. Com clima Chuva, reserva **35%**. Recuperação máxima por ativação: **8% do HP máximo** normalmente, ou **10% do HP máximo** sob Chuva. Vários golpes podem alimentar a mesma reserva, mas não permitem ultrapassar o limite. Não cura sem dano prévio, não revive e não acumula reservas indefinidamente.

## Movimentos aprovados

| Slot | Nome | Categoria | Elemento | Poder | Energia |
|---:|---|---|---|---:|---:|
| 1 | Crina Poderosa | Mágico | Neutro | 40 | 0 |
| 2 | Concentração | Suporte | — | — | 0 |
| 3 | Estalo das Brânquias | Mágico | Água | 75 (95 condicionado) | 25 |
| 4 | Elo Regenerativo | Suporte/cura | — | — | 30 |
| 5 | Dilúvio Branquial | Mágico | Água | 85 | 45 |

1. **Crina Poderosa:** golpe básico preexistente, sem mudança.
2. **Concentração:** golpe preexistente, E0, 40% de chance de remover efeito negativo; respeitar Tonto.
3. **Estalo das Brânquias:** P75 E25. Se Axococó recuperou HP desde sua última ação, P95 em vez de P75. A cura pode vir da passiva ou de golpe de recuperação; bônus não acumula. Sem status adicional.
4. **Elo Regenerativo:** E30, suporte. Em si mesmo cura **25% do próprio HP máximo**. Se direcionado a um aliado ainda vivo na **reserva**, cura **20% do HP máximo do aliado** e **5% do HP máximo do Axococó**, sem troca e usando uma ação. Não revive, não remove condição negativa, não ultrapassa HP máximo.
5. **Dilúvio Branquial:** P85 mágico Água E45. Invoca **Chuva por quatro rodadas** ao executar o golpe validamente, mesmo que não acerte. Custo inclui 20 de invocação integrada. Chuva global: +25% dano de golpes Água, +10% dano de golpes Elétricos, −25% dano de golpes Fogo; aplicável a ambas as equipes, segundo regras oficiais.

**Hereditários:** ZERO. Todos os golpes são compartilhados, mas compatibilidade de outras espécies depende de aprovação individual.

## Regra universal de cura em reserva

Batalha padrão 3×3 continua com somente um Galeto ativo por equipe e dois reservas. Golpes de cura/suporte que recuperam HP podem escolher o usuário ativo ou um aliado vivo na reserva sem trocar Galetos; gastam ação normal e preservam seus percentuais e outros efeitos. **Pólen Revigorante** passa a poder escolher um aliado na reserva, mantendo 25% do HP máximo do alvo e E30. Passivas e habilidades que não sejam golpes de cura de HP não mudam automaticamente.

**Nota técnica:** banco de referência atualizado, não implementado no mod Minecraft. Sem simulador 3×3 específico desta revisão.

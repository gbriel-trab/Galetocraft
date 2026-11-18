# ROOSTERTECA OFICIAL — #008 AXOCOCÓ

**Estado: FICHA COMPLETA E HOMOLOGADA EM 09/11/2026.**

- **Espécie:** #008 Axococó — o galo axolote
- **Raridade:** Comum
- **Elemento:** Água
- **Função:** regenerador tático / suporte aquático
- **Peso máximo natural:** 5,8 kg (faixa técnica 80%–150%: 4,64–8,70 kg; ponto neutro 5,8 kg)

![Arte oficial — Axococó](Axococo_008_Arte_Oficial.png)

**Integridade da arte oficial:** SHA-256 `b3bb33f40be66f6c970dfb0f5d23a58be60581509493d3147cab44b0352503e2`. Manter as quatro vistas, brânquias, crista, cauda e demais detalhes inalterados. Os números eventualmente impressos na prancha foram gerados ilustrativamente e **não** são os parâmetros homologados; esta ficha e o banco governam status, peso e efeitos.

## Atributos base homologados — nível 50

| Atributo | Valor base |
|---|---:|
| HP | 95 |
| Ataque Físico | 35 |
| Defesa Física | 50 |
| Ataque Mágico | 90 |
| Defesa Mágica | 60 |
| Velocidade | 40 |
| **Soma** | **370** |

**HP no nível 100:** 143 pela fórmula oficial `ceil(1,5 × HP base)`, antes de IV/EV e modificadores de peso. Total de 370 dentro da raridade Comum (259–459); nenhuma faixa de raridade foi alterada.

## Passiva oficial — Memória das Brânquias

Após sofrer dano de ataques inimigos, acumula uma reserva regenerativa equivalente a **25% do dano sofrido** (ou **35% durante Chuva**) que recupera no início da sua próxima ação. A cura é limitada a **8% do HP máximo por ativação**, ou **10% sob Chuva**. Vários golpes recebidos podem alimentar a mesma reserva, mas não ultrapassam esse limite. A passiva não cura sem dano recebido, não revive o usuário e não acumula reservas indefinidamente.

## Golpes oficiais — cinco posições

| Slot | Golpe | Categoria | Elemento | Poder | Energia |
|---:|---|---|---|---:|---:|
| 1 | Crina Poderosa | Mágico | Neutro | 40 | 0 |
| 2 | Concentração | Suporte | — | — | 0 |
| 3 | Estalo das Brânquias | Mágico | Água | 75 / 95 condicional | 25 |
| 4 | Elo Regenerativo | Suporte / cura | — | — | 30 |
| 5 | Dilúvio Branquial | Mágico | Água | 85 | 45 |

1. **Crina Poderosa:** golpe básico já homologado, sem modificação.
2. **Concentração:** E0; 40% de chance de remover condição negativa persistente, respeitando os efeitos da Tontura.
3. **Estalo das Brânquias:** P75 e E25; poder sobe a 95 se o usuário recuperou HP desde a última ação (por passiva ou cura). Bônus não acumula; sem status adicional.
4. **Elo Regenerativo:** E30; ao mirar o próprio usuário recupera 25% do próprio HP máximo. Em um aliado vivo da reserva, recupera 20% do HP máximo desse aliado e 5% do HP máximo do usuário. Ação normal sem troca. Não revive, não remove condição negativa nem ultrapassa o HP máximo.
5. **Dilúvio Branquial:** mágico Água P85 E45; invoca Chuva por quatro rodadas após execução válida, mesmo sem acerto. Clima global: +25% dano de golpes Água; +10% dano de golpes Elétricos; −25% dano de golpes Fogo. E45 inclui a invocação integrada (25+20).

**Herança:** nenhum golpe é hereditário ou exclusivo. Todos são de catálogo geral, passíveis de compatibilidade com outras espécies somente após aprovação específica.

## Regra geral aprovada de cura para aliados na reserva

O combate padrão 3×3 mantém **um ativo e dois na reserva** de cada lado. Movimentos de cura/suporte que restauram HP podem escolher um aliado vivo da reserva e curá-lo sem trocá-lo para o campo. Os custos, condições e percentuais de cada golpe não mudam; respeitar HP máximo e vedação de reviver. **Pólen Revigorante** já pode escolher um aliado vivo da reserva, preservando 25% do HP máximo do alvo e E30. Esta regra não cria batalha 2×2.

## Estado técnico

Cadastro de referência em banco SQLite e JSON realizado; não significa implementação no Minecraft. Simulações competitivas 3×3 para esta configuração ainda não foram executadas.

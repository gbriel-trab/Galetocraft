# Galetocraft — Galetário #007 | Taturico (OFICIAL)

**Aprovação expressa do criador:** 09/11/2026. **Estado:** ficha do #007 completa e homologada no banco de referência; ainda não integrada ao mod Minecraft executável.

![Arte oficial inalterada do Taturico](Taturico_007_Arte_Oficial.png)

**Registro de imagem oficial:** `Taturico_007_Arte_Oficial.png`  
**SHA-256 da imagem aprovada:** `741fdabac8f1756419f9570c231f782e39aadba2d329647184d34c710e71827c`. O mesmo PNG é armazenado integralmente na tabela `species_visual_assets` do banco SQLite; não redesenhar ou substituir. A prancha é imagem de referência, não geometria 3D editável.

## Identidade

- **Número:** #007
- **Nome:** Taturico
- **Raridade:** Comum
- **Elemento:** Terra
- **Inspiração:** tatu / tatu-bola (galo-tatu)
- **Função:** defensor físico, proteção, contra-ataque, controle de clima
- **Visual:** estilo Minecraft voxel; carapaça segmentada e armadura da cabeça preservadas exatamente na arte oficial.
- **Peso natural máximo:** **7,5 kg** (100% da referência). Peso mínimo técnico 80%=6,0 kg e máximo técnico 150%=11,25 kg. Segue o sistema universal de alimentação e peso, que pode superar o máximo natural.

## Atributos base — nível 50

| Atributo | Base |
|---|---:|
| HP | **85** |
| Ataque Físico | **55** |
| Defesa Física | **105** |
| Ataque Mágico | **25** |
| Defesa Mágica | **60** |
| Velocidade | **40** |
| **SOMA** | **370** |

**HP máximo derivado no nível 100:** 128, antes de IV, EV e peso, pela regra `ceil(1,5 × 85)`. Os atributos listados são BASE; efeitos de passiva, peso, IV e EV não estão somados aos 370.

**Faixa oficial de Comum:** 259–459; 370 está dentro da faixa. As demais faixas permanecem Raro 460–624, Épico 625–774, Mítico 775–924 e Lendário 925–1300. Nenhum inicial foi alterado.

## Passiva oficial — Carapaça Reativa

- **Bônus permanente:** +10% Defesa Física.
- **Bloqueio:** 20% de chance de bloquear parcialmente um golpe físico; quando ativado, o dano desse golpe é reduzido em **30%**.
- **Tentativas:** no máximo uma por rodada; nenhum custo de energia.
- **Incompatibilidade:** o bloqueio da passiva **não se acumula com Guarda do Tatu**.

## Cinco golpes oficiais — catálogo geral / compartilhado

| Slot | Golpe | Categoria | Elemento | Poder | Energia |
|---:|---|---|---|---:|---:|
| 1 | Garra Afiada | Físico | Neutro | 40 | 0 |
| 2 | Concentração | Suporte | — | — | 0 |
| 3 | Impacto Blindado | Físico | Terra | 70 | 25 |
| 4 | Guarda do Tatu | Suporte / Contra-ataque | — | Variável | 30 |
| 5 | Coro das Dunas | Suporte / Clima | — | — | 20 |

### Funcionamento aprovado

1. **Garra Afiada:** efeito oficial existente, ataque físico neutro, P40/E0.
2. **Concentração:** efeito oficial existente, suporte E0, 40% de chance de remover o estado negativo ativo, respeitando regras de Tonto.
3. **Impacto Blindado:** P70/E25, dano físico Terra com **80% da Defesa Física atual no lugar do Ataque Físico** na fórmula normal de dano. Sem efeito secundário. Movimento novo e compartilhado.
4. **Guarda do Tatu:** E30. Protege o próprio usuário ou um aliado contra a próxima ação ofensiva até o próximo turno. Reduz 35% do dano físico e 20% do mágico recebido durante a proteção. Se Taturico sofrer dano físico, devolve 40% do dano efetivamente sofrido. Cobre até 2 golpes da mesma ação e permite no máximo 1 contra-ataque. Não acumula com o bloqueio da passiva. Movimento novo e compartilhado.
5. **Coro das Dunas:** movimento geral já existente, E20. Invoca **Tempestade de Areia** por quatro rodadas. Clima global: +25% de dano dos golpes Terra, +10% de Defesa Física para Galetos Terra e −25% de dano de golpes Ar, beneficiando/aplicando-se a ambos os lados conforme as regras existentes. É suporte dedicado, não golpe exclusivo.

## Herança, compatibilidade e combate

- **Golpes hereditários do Taturico:** nenhum (**zero**).
- Os cinco golpes estão na **Galolpédia**; apenas Impacto Blindado e Guarda do Tatu são novos; Coro das Dunas já existia e foi agora atribuído a #007.
- Outros Galetos só poderão aprender esses movimentos quando sua compatibilidade for aprovada.
- Limite universal: no máximo **2 golpes por ação**, incluindo segundo golpe adicional por Velocidade; um contra-ataque de Guarda do Tatu por ativação.
- A ficha não especifica novas mecânicas externas; preserva os sistemas de peso, status, clima e equipe 3×3 preexistentes.

**Situação da implementação:** banco/documentos e arte de referência atualizados; modelagem 3D executável e testes de batalha específicos ainda pendentes.

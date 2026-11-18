# Galetocraft — Galetário #009: Vagaló (OFICIAL)

**Revisão:** v1.10.1 | **Data de homologação:** 09/11/2026 | **Situação:** COMPLETO — expressamente aprovado pelo criador.

## Identidade

- **Número:** #009
- **Nome:** Vagaló
- **Elemento:** Elétrico
- **Raridade:** Comum
- **Função:** Sinalizador Tático — suporte de revezamento e controle de campo, não atacante mágico.
- **Inspiração visual:** vaga-lume; corpo voxel Minecraft, asas luminosas e iluminação bioluminescente.
- **Arte oficial exata:** `Vagalo_009_Arte_Oficial.png`, sem ajustes, SHA-256 `142adc7e68c4516bc0f2693630528cbd3f2f11eba1b3148f910a561bc701f847`.
- **Peso natural:** **3,1 kg**.

## Atributos base, nível 50 (total 370 pontos)

| Atributo | Valor aprovado |
|---|---:|
| HP | 60 |
| Ataque Físico | 25 |
| Defesa Física | 40 |
| Ataque Mágico | 15 |
| Defesa Mágica | 50 |
| Velocidade | **180** |
| **Total** | **370** |

No esquema técnico vigente, `hp_at_level_100` é **90** (derivado da regra pré-existente de referência HP × 1,5, sem alterar HP base 60). O teto natural de peso aprovado é 3,1 kg; os limites técnicos de peso continuam em 80% a 150% do natural, sem mudar as regras vigentes.

## Passiva oficial — Código Luminescente

- Cada **ação que executa validamente um golpe** concede **1 Pulso Luminoso**; máximo **2 pulsos armazenados**.
- Se uma ação produz dois golpes, gera somente **1 pulso**. Uma ação impedida não gera pulso.
- Em **troca voluntária válida**, inclusive troca incorporada a golpe de revezamento, os pulsos são consumidos e transferem benefícios ao substituto:
  - **1 pulso:** +10% de Velocidade pelas duas primeiras ações do Galeto que entrar.
  - **2 pulsos:** +20% de Velocidade pelas duas primeiras ações de quem entrar, além de reduzir em **20%** o dano do primeiro golpe recebido.
- A troca voluntária convencional continua custando uma ação e não consome energia. Os movimentos especiais têm custo próprio.
- Se não houver pulso, não há bônus. Substituição obrigatória após derrota não ativa a passiva. Troca impedida não transfere pulsos; efeitos não se acumulam consigo mesmos e desaparecem se o aliado sair de campo.

## Golpes oficiais (cinco slots; todos compartilhados e não hereditários)

| Slot | Golpe | Categoria | Elemento | Poder | Energia | Efeito oficial |
|---:|---|---|---|---:|---:|---|
| 1 | Garra Afiada | Físico | Neutro | 40 | 0 | Ataque básico, sem efeito extra |
| 2 | Concentração | Suporte | — | — | 0 | 40% de chance de remover o estado negativo ao executar validamente |
| 3 | Relé Luminoso | Físico | Elétrico | 50 | 30 | Ataca e, após execução válida, troca pelo aliado selecionado, ativando Código Luminescente |
| 4 | Cortina Cintilante | Suporte | Elétrico | — | 30 | Troca após execução; concede Véu Cintilante de redução de 35% do próximo golpe recebido ao aliado entrante |
| 5 | Choque Estático | Físico | Elétrico | 20 | 30 | 80% de chance de Paralisia (uma checagem por ação quando houver pelo menos um acerto com dano) |

### Limites de Relé Luminoso

- Exige substituto apto e troca permitida, escolhidos previamente. Executa sem prioridade da troca convencional; se Vagaló for impedido de agir, não ataca nem troca.
- Pode trocar mesmo se o dano falhar por esquiva, desde que a ação tenha sido validamente executada.
- Respeita teto universal de **dois golpes por ação**, com custo de energia único. A troca ocorre após os golpes permitidos; aliado entrante não recebe ação extra.

### Limites de Cortina Cintilante

- O Véu reduz **35%** do dano de **um único golpe físico ou mágico**. Expira após absorver o primeiro golpe, ou ao final da próxima rodada, o que vier primeiro.
- Sem efeito ofensivo; exige aliado disponível e troca permitida; sem prioridade especial, sem ação extra.
- Se a passiva de dois pulsos oferecer proteção de 20%, somente a maior redução de 35% se aplica; ambas são consumidas no primeiro golpe. Não acumula proteção.

### Limites de Choque Estático

- O golpe é **básico, compartilhado e não hereditário**; não realiza troca.
- Para tentar Paralisia, o ataque precisa **acertar e causar dano**.
- A chance de 80% é verificada **uma única vez por ação**, mesmo que haja dois acertos.
- Paralisia mantém efeitos oficiais: −25% de Velocidade e 20% de chance de perder a ação. Um alvo já com estado negativo persistente não pode receber outro, renovar ou substituir o atual.

## Família aprovada de golpes de status (Catálogo geral, sem atribuir a Vagaló)

Além de Choque Estático, quatro técnicas compartilhadas aprovadas para futuros Galetos: **Faísca Ardente** (Fogo/Queimadura), **Espinho Venenoso** (Planta/Envenenamento), **Jato Sufocante** (Água/Afogamento) e **Baque de Terra** (Terra/Tonto). Todas Físicas, poder 20, energia 30, 80% de aplicação e uma verificação por ação. **Não atribuir automaticamente a nenhuma espécie anterior.**

## Integridade e limites do registro

- Ficha homologada: arte, identidade, raridade, elemento, função, seis atributos, peso, passiva e cinco golpes.
- Nenhum golpe exclusivo/hereditário foi criado ou alterado. Golpes de status, regras de equipe 3×3 e artes anteriores foram preservados.
- A arte oficial é um PNG de referência, **não** modelo 3D jogável. Números impressos na arte podem ser ilustrativos; os valores oficiais são os deste registro e do banco.
- **Integração no Minecraft e validação competitiva desta revisão ainda não executadas.**

# GALETOCRAFT — GALETÁRIO #011 | ESPINHOCÓ

**Estado:** HOMOLOGAÇÃO CONCEITUAL INTEGRAL — APROVADO PELO CRIADOR  
**Data de consolidação:** 10/11/2026  
**Revisão da ficha individual:** 1.0-oficial (não altera a numeração global do banco)  
**Espécie:** #011 Espinhocó  
**Raridade:** Comum  
**Elemento:** Planta  
**Função:** Guardião Territorial — especialista em armadilhas de terreno e retaliação física  
**Design aprovado:** galo-porco-espinho vegetal, estilo voxel/Minecraft

> Esta homologação INTEGRAL, autorizada pelo criador após a apresentação dos atributos e peso, prevalece sobre menções históricas a 'ainda não aprovado' contidas nas fichas parciais de #011. Não muda qualquer ficha #001–#010.

## 1. Imagem oficial — verificação de integridade

- Arte canônica: `Espinhoco_011_Arte_Oficial.png`.
- SHA-256 exato: `a5874bac70a52e15beacb774692fd09d77349247b1d1c7e96587282ce7425de3`.
- Arquivo PNG, resolução 1536 × 1024, imagem idêntica à versão expressamente aprovada; foi conferida por comparação binária com a imagem arquivada na Biblioteca.
- Visual imutável sem autorização explícita: corpo arredondado e compacto, espinhos dorsais e cauda bege/marfim com base marrom, crista de folhas verde-oliva, asas foliares verdes, peito creme, bico amarelo, barbelas vermelhas e patas robustas de garras escuras.
- A prancha contém frente, lateral direita, traseira e lateral esquerda, expressões, detalhes e paleta.
- **Limite técnico:** arte de referência homologada, não arquivo 3D editável/jogável ou prova de integração no Minecraft; o texto 'Modelo Oficial 3D' impresso é decorativo.

## 2. Atributos-base — nível 50 (OFICIAIS)

| Atributo | Pontos |
|---|---:|
| HP | 75 |
| Ataque Físico | 95 |
| Defesa Física | 85 |
| Ataque Mágico | 20 |
| Defesa Mágica | 55 |
| Velocidade | 40 |
| **Total base** | **370** |

**Peso natural máximo de referência:** 6,2 kg, equivalente a 100% do peso natural no sistema vigente.  
**Intervalo técnico derivado de 80%–150% da referência:** 4,96 kg a 9,30 kg. São resultados da regra geral de peso, não atributos-base adicionais. Alterações por alimentação seguem o sistema universal, sem mudar a imagem homologada.

## 3. Habilidade passiva — Espinheiro Territorial (OFICIAL)

A passiva possui dois efeitos complementares. Ao **receber cada golpe físico direto que efetivamente cause dano**, inclusive o segundo golpe de uma ação dupla:

1. **Retaliação individual:** devolve ao atacante dano igual a **5% do HP máximo do atacante**, para **cada golpe físico recebido**. Não existe limitação de uma retaliação por rodada. Dois golpes físicos danosos produzem duas retaliações, de 5% cada.
2. **Espinhos territoriais acumulativos:** adiciona **uma carga** de armadilha ao lado do campo adversário para **cada golpe físico recebido**. Cada carga representa **6% do HP máximo do Galeto entrante** quando ocorre troca voluntária do adversário. Ex.: duas cargas = 12% do HP máximo do entrante, quatro cargas = 24%.

**Regras de armadilha expressamente definidas:** cargas se acumulam; funcionam com ataque duplo; não há teto de cargas nem duração em rodadas; as armadilhas permanecem no campo **até serem retiradas pelo oponente**, e não expiram automaticamente por passagem de tempo ou simples ativação. Trocas obrigatórias por derrota não ativam a armadilha territorial. Não ultrapassam o teto universal de 2 golpes por ação, pois retaliação e armadilha são efeitos e não golpes adicionais.

**Cuidados de implementação ainda não fixados em detalhe:** desempates de resolução simultânea, interações específicas de efeitos entre passivas de espécies futuras e procedimentos de interface. Não presumir regras novas nem contrariar as decisões de persistência/acúmulo.

## 4. Conjunto completo dos cinco movimentos (OFICIAL)

| Slot | Movimento | Categoria | Elemento | Poder | Energia | Efeito |
|---:|---|---|---|---:|---:|---|
| 1 | Garra Afiada | Físico | Neutro | 40 | 0 | Dano direto, sem adicional |
| 2 | Concentração | Suporte | Nenhum | — | 0 | 40% chance de remover um estado negativo persistente de si ao executar validamente |
| 3 | Espinho Venenoso | Físico | Planta | 20 | 30 | 80% chance de Envenenamento, se houver ao menos um acerto com dano; uma checagem por ação |
| 4 | Armadilha de Cipós | Suporte | Planta | — | 30 | Instala armadilha no lado adversário: em cada troca voluntária, Galeto entrante recebe −20% de Velocidade nas suas próximas 2 ações; não acumula redução no mesmo alvo; persiste até remoção |
| 5 | Rajada de Espinhos | Físico | Planta | 95 | 35 | Dano direto elevado, sem efeito adicional |

- **Todos são compartilhados, não exclusivos e não hereditários.** A atribuição ao Espinhocó é oficial; isso não altera espécies anteriores nem concede automaticamente técnicas às demais.
- **Garra Afiada e Concentração** preservam parâmetros universais já existentes.
- **Espinho Venenoso** preserva seu registro geral P20/E30/80%; não substitui nem acumula estados negativos persistentes, e faz no máximo uma verificação por ação inclusive com dois acertos.
- **Armadilha de Cipós** mantém-se instalada até a remoção adversária, sem duração máxima em rodadas. Sua lentidão individual, após acionamento, dura duas ações do entrante, sem acúmulo de lentidão sobre o mesmo alvo. Pode coexistir com as cargas criadas pela passiva Espinheiro Territorial.
- **Rajada de Espinhos** substituiu a proposta NÃO HOMOLOGADA de Solo Farpado e não adiciona veneno, armadilha ou bônus.

## 5. Sistema de terreno e remoção — limites da aprovação

- Armadilhas de terreno, incluindo as criadas pelo Espinhocó, **não expiram por rodadas**; permanecem até remoção pelo adversário.
- A regra geral de **limpeza completa de todas as armadilhas e cargas** pelo movimento de remoção é oficial.
- O criador definiu **apenas um movimento de suporte sem elemento** para a função de limpeza, mas **o nome 'Terreiro Purificado' e o custo 30** apresentados posteriormente continuam sem confirmação específica e não integram a lista dos cinco golpes deste Galeto.
- Climas e Santuários são categorias diferentes de armadilhas; seus movimentos de dissipação anteriores continuam inalterados.

## 6. Integridade, escopo e estado técnico

- **Ficha conceitual e lista de golpes: CONCLUÍDAS e HOMOLOGADAS.**
- **Arte: APROVADA, VERIFICADA e preservada byte a byte.**
- **Implementação Java/NeoForge, modelo tridimensional jogável, animações, validação técnica e partidas 3×3 específicas:** não comprovadas; não confundir esta conclusão conceitual com implementação.
- Nenhuma alteração a imagens, atributos, movimentos, passivas ou regras universais de espécies concluídas.
- Próxima espécie planejada no ciclo dos dez Comuns: **#012 Salambrasa**.

## 7. Arquivos relacionados

- Arte: `Espinhoco_011_Arte_Oficial.png` (mesmo SHA-256 acima).
- Golpes: `GalolpeTeca_011_Espinhoco_Oficial.md`.
- Dados estruturados: `Espinhoco_011_Dados_Oficiais.json`.
- Verificação: `Espinhoco_011_Verificacao_Arte.md`.

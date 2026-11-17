# Renacocó #019: especificação do dono (2026-11-14)

**Ficha:** "O Curandeiro da Ressurreição", fogo, mítico, suporte. A arte oficial é a autoridade máxima:
`019_renacoco_arte.png` (ilustração grande), `019_renacoco_ficha.png` (prancha), `_vistas.png`, `_expressoes.png` e
`_detalhes.png`. Alguns quadros da ficha citam personagens de outras franquias. **Não use esses nomes no código**,
só os elementos genéricos (cauda tripla de contas, aura de cura).

**Escala:** não está na tabela oficial. Provisório: **2,50 de altura × 1,60 de largura × 2,60 de comprimento**
(`ferramentas/dimensoes.py`). Fica abaixo do Cocórak (3,0) e bem acima de um galeto comum. Hitbox 0,96 × 2,5,
imune a fogo.

**Qualidade:** voxel orgânico de alto nível (no nível do Cobblemon, sem copiar nada): volumes bem definidos, cubos de
tamanhos variados, transições cuidadosas, pronto para jogo.

## Leitura visual obrigatória
- Ave mítica elegante, imponente, nobre e curandeira; postura ereta, corpo alto e esguio, pescoço longo e elegante.
- Cabeça afilada, bico amarelo alongado e reto, barbela vermelha embaixo do bico.
- Olhos azuis inteligentes, olhar confiante, sereno e determinado, com sobrancelha ou linha ocular marcante.
- **Crista:** grande, em chama ou plumas que sobem, amarela/dourada com base azul-clara, em várias camadas. Nada de bloco
  único ou coroa genérica.
- **Penas do rosto:** laterais azuis e amarelas formando uma moldura nobre.
- **Peito:** penas em camadas, azul-claro, azul e creme/amarelado. No centro, a cruz azul do renascimento, fiel e
  legível.
- **Manto roxo grande:**
  - bordas douradas, com espessura e caimento (não é placa reta);
  - fecho no alto com 2 medalhões dourados redondos;
  - emblema dourado da fênix nas costas;
  - padrões dourados nas pontas;
  - cobre parte das asas e do tronco, e o caimento lateral reforça a silhueta nobre.
- **Asas:** aparecem sob o manto como geometria real, penas em camadas azul, azul-claro e creme/amarelo.
- **Cauda tripla:** 3 extensões separadas, feitas de elos ou contas douradas com centro azul-claro, terminando em penas
  longas amarelas e azuis. Não pode virar cauda única nem fita sem volume.
- **Pernas:** longas, retas, amarelas/douradas.
- **Patas:** grandes e estáveis, dedos bem definidos e garras escuras.
- **Personalidade:** sabedoria, serenidade, autoridade, compaixão, poder espiritual.

## Proibido
- Reduzir a um passarinho pequeno ou fofo.
- Cabeça caricata ou pescoço curto.
- Engrossar ou achatar o corpo.
- Manto como chapa sem espessura.
- Cauda simplificada.
- Penas com poucos blocos.
- Pernas frágeis demais.
- Patas genéricas ou minúsculas.
- Mudar as cores.

## Paleta
- roxo e magenta/roxo vivo (manto);
- azul intenso e azul-claro/ciano (corpo);
- creme claro;
- amarelo/dourado;
- vermelho (barbela);
- escuro (garras).

## Ossos (sugeridos, adaptar ao padrão do projeto)
- Corpo: corpo, pescoço, cabeça (crista, penas do rosto, bico, barbela).
- Peito: penas do peito e símbolo.
- Manto: frente esquerda e direita, costas, lados.
- Asas, pernas e patas.
- Cauda: raiz e cauda 1, 2 e 3.

Prepare pivôs para:
- parado, andar e corrida leve;
- cabeça, asas e balanço do manto;
- as 3 caudas;
- dano, cura e poder.

## Auditoria pedida pelo dono (5 olhares)
1. **Fidelidade:** silhueta, cabeça, crista, cauda tripla e manto.
2. **Anatomia:** pernas, pescoço, tronco e cabeça; o bicho parece nobre e ereto?
3. **Geometria:** é voxel jogável? Há blocos grandes demais ou soluções preguiçosas?
4. **Textura:** cores, símbolos legíveis e UVs.
5. **Implementação:** ossos, pivôs e GeckoLib.
